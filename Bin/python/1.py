#!/usr/bin/env python3
import os, sys, curses, shutil, subprocess, json, time

IMG_EXT = {'.png','.jpg','.jpeg','.webp','.gif','.bmp','.tiff','.tif'}
def is_img(p): return os.path.isfile(p) and os.path.splitext(p)[1].lower() in IMG_EXT

class Previewer:
    def __init__(self):
        self.mode = 'ueberzugpp' if shutil.which('ueberzugpp') else ('chafa' if shutil.which('chafa') else None)
        self.proc = None
        self.id = 'preview'
        self.last = (None, None)  # (path, area)
        if self.mode == 'ueberzugpp':
            self.proc = subprocess.Popen(['ueberzugpp','layer','--parser','json'],
                                         stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                         text=True)

    def _sync_on(self): sys.stdout.write("\x1b[?2026h")
    def _sync_off(self): sys.stdout.write("\x1b[?2026l"); sys.stdout.flush()

    def show(self, path, area):
        if not self.mode or not path or not os.path.exists(path): return
        x,y,w,h = area
        if w<=0 or h<=0: return
        if self.last == (path, area): return  # ничего не меняем — без мерцания

        if self.mode == 'ueberzugpp':
            try:
                d = {"action":"add","identifier":self.id,"path":path,"x":x,"y":y,"width":w,"height":h,"scaler":"contain"}
                self.proc.stdin.write(json.dumps(d)+"\n"); self.proc.stdin.flush()
            except Exception: pass
        elif self.mode == 'chafa':
            try:
                raw = subprocess.run(['chafa','--size',f'{w}x{h}', path],
                                     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8','ignore')
                lines = raw.rstrip('\n').split('\n')
                self._sync_on(); sys.stdout.write("\x1b[?25l\x1b[s")
                for i in range(h):
                    line = lines[i] if i < len(lines) else ""
                    sys.stdout.write(f"\x1b[{y+i+1};{x+1}H{line}\x1b[0K")
                sys.stdout.write("\x1b[u\x1b[?25h"); self._sync_off()
            except Exception: pass
        self.last = (path, area)

    def clear(self, area=None):
        if self.mode == 'ueberzugpp' and self.proc and self.proc.stdin and not self.proc.stdin.closed:
            try:
                self.proc.stdin.write(json.dumps({"action":"remove","identifier":self.id})+"\n"); self.proc.stdin.flush()
            except Exception: pass
        elif self.mode == 'chafa' and area:
            # мягкая очистка: без “протирки” всей области, только сброс хвостов строк
            x,y,w,h = area
            self._sync_on()
            for i in range(max(h,0)):
                sys.stdout.write(f"\x1b[{y+i+1};{x+1}H\x1b[0K")
            self._sync_off()
        self.last = (None, None)

    def close(self):
        try:
            self.clear(self.last[1])
            if self.mode == 'ueberzugpp' and self.proc:
                try:
                    if self.proc.stdin and not self.proc.stdin.closed: self.proc.stdin.close()
                except Exception: pass
                self.proc.terminate()
        except Exception: pass

class App:
    def __init__(self, stdscr, start_dir):
        self.s = stdscr
        self.cur = os.path.abspath(start_dir)
        self.items = []; self.sel = 0; self.top = 0
        self.prev = Previewer()
        self.side_layout = True
        self.last_hw = self.s.getmaxyx()
        curses.curs_set(0)
        curses.start_color(); curses.use_default_colors()
        use256 = curses.COLORS >= 256
        if use256:
            c = curses.init_pair
            c(1, 252, -1)   # text
            c(2, 16, 141)   # selected: black on mauve-ish
            c(3, 252, 60)   # header
            c(4, 179, -1)   # folder: peach
            c(5, 110, -1)   # image: sky
        else:
            curses.init_pair(1, curses.COLOR_WHITE, -1)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
            curses.init_pair(4, curses.COLOR_YELLOW, -1)
            curses.init_pair(5, curses.COLOR_CYAN, -1)
        self.s.timeout(120)  # обновляемся ~8 раз/с, ловим resize без клавиш
        self.load()

    def load(self):
        try: names = os.listdir(self.cur)
        except Exception: names = []
        ent = []
        for n in names:
            p = os.path.join(self.cur, n)
            ent.append((n, os.path.isdir(p), is_img(p)))
        ent.sort(key=lambda x: (not x[1], x[0].lower()))
        self.items = ent; self.sel = 0; self.top = 0

    def layout(self):
        h, w = self.s.getmaxyx()
        self.side_layout = (w >= 56)
        if self.side_layout:
            listw = max(20, int(w*0.5))
            list_rows = h-1
            prevx, prevy = listw + 1, 1
            prevw, prevh = max(0, w - prevx), h-1
        else:
            listw = w
            prevy = h//2
            list_rows = max(0, prevy - 1)
            prevx, prevw = 0, w
            prevh = h - prevy
        return (listw, list_rows, (prevx, prevy, prevw, prevh))

    def draw(self):
        s = self.s; s.erase()
        h, w = s.getmaxyx()
        s.attrset(curses.color_pair(3))
        try:
            s.addstr(0, 0, (" "*(w-1)))
            s.addstr(0, 1, self.cur[:max(0, w-3)])
        except curses.error: pass
        s.attrset(curses.color_pair(1))
        listw, list_rows, _ = self.layout()
        if self.sel < self.top: self.top = self.sel
        if self.sel >= self.top + list_rows: self.top = self.sel - list_rows + 1
        for i in range(list_rows):
            idx = self.top + i
            if idx >= len(self.items): break
            name, isdir, isimgf = self.items[idx]
            icon = "📁" if isdir else ("🖼️" if isimgf else "📄")
            text = f"{icon} {name}"[:max(0, listw-1)]
            pair = 4 if isdir else (5 if isimgf else 1)
            attr = curses.color_pair(pair if idx != self.sel else 2)
            try: s.addstr(1+i, 0, text.ljust(max(0, listw-1)), attr)
            except curses.error: pass
        try:
            s.addstr(h-1, 1, "↑↓ нав • Enter открыть/путь • ⌫ вверх • q выход"[:max(0, w-2)], curses.color_pair(1))
        except curses.error: pass
        s.refresh()

    def show_preview(self):
        _, _, area = self.layout()
        if not self.items:
            self.prev.clear(area); return
        name, isdir, isimgf = self.items[self.sel]
        path = os.path.join(self.cur, name)
        if isimgf: self.prev.show(path, area)
        else: self.prev.clear(area)

    def run(self):
        self.draw(); self.show_preview()
        while True:
            # если изменилась геометрия — мгновенно перерисуем (без ожидания клавиши)
            hw = self.s.getmaxyx()
            if hw != self.last_hw:
                self.last_hw = hw
                self.draw(); self.show_preview()

            k = self.s.getch()
            if k == -1:
                continue
            if k in (ord('q'), 27): self.prev.close(); return None
            elif k in (curses.KEY_UP, ord('k')):
                if self.sel > 0: self.sel -= 1
            elif k in (curses.KEY_DOWN, ord('j')):
                if self.sel < len(self.items)-1: self.sel += 1
            elif k in (curses.KEY_BACKSPACE, 127, 8):
                parent = os.path.dirname(self.cur.rstrip(os.sep)) or self.cur
                if parent and parent != self.cur:
                    self.cur = parent; self.load()
            elif k in (curses.KEY_ENTER, 10, 13):
                if not self.items: continue
                name, isdir, _ = self.items[self.sel]
                path = os.path.join(self.cur, name)
                if isdir:
                    self.cur = path; self.load()
                else:
                    self.prev.close(); return os.path.abspath(path)
            elif k == curses.KEY_RESIZE:
                # сразу перерисуем и обновим превью
                self.draw(); self.show_preview()
                continue
            # обычная перерисовка после любой навигации
            self.draw(); self.show_preview()

def main(stdscr):
    start = sys.argv[1] if len(sys.argv)>1 else os.getcwd()
    return App(stdscr, start).run()

if __name__ == "__main__":
    sel = curses.wrapper(main)
    if sel: print(sel)
