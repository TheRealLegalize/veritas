#!/usr/bin/env python3
"""ShareX-style Screenshot with Zoom & Pixel Mesh"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import cairo
import subprocess
from pathlib import Path
from datetime import datetime
import sys

class Screenshot(Gtk.Window):
    def __init__(self, output_dir="~/Pictures/Screenshots"):
        super().__init__(type=Gtk.WindowType.POPUP)
        self.dir = Path(output_dir).expanduser()
        self.dir.mkdir(parents=True, exist_ok=True)
        
        # Config
        self.zoom_size, self.zoom_factor = 180, 12
        
        # Get screen info
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor() or display.get_monitor(0)
        geometry = monitor.get_geometry()
        self.w, self.h = geometry.width, geometry.height
        
        # Capture screen
        root = Gdk.get_default_root_window()
        if not root:
            print("Error: Cannot get root window", file=sys.stderr)
            sys.exit(1)
        
        self.screenshot = Gdk.pixbuf_get_from_window(root, 0, 0, self.w, self.h)
        if not self.screenshot:
            print("Error: Failed to capture screen", file=sys.stderr)
            sys.exit(1)
        
        # Setup window
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)
        
        self.set_app_paintable(True)
        self.set_default_size(self.w, self.h)
        self.fullscreen()
        
        # State
        self.x1 = self.y1 = self.x2 = self.y2 = self.mx = self.my = 0
        self.selecting = False
        
        # Drawing area
        da = Gtk.DrawingArea()
        da.connect('draw', self.draw)
        self.add(da)
        
        # Events
        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK | 
            Gdk.EventMask.BUTTON_RELEASE_MASK | 
            Gdk.EventMask.POINTER_MOTION_MASK | 
            Gdk.EventMask.KEY_PRESS_MASK
        )
        
        self.connect('button-press-event', self.on_press)
        self.connect('button-release-event', self.on_release)
        self.connect('motion-notify-event', self.on_motion)
        self.connect('key-press-event', self.on_key)
        self.connect('realize', self.on_realize)
        
        # Refresh
        GLib.timeout_add(16, lambda: self.queue_draw() or True)
        
        self.show_all()
    
    def on_realize(self, widget):
        """Set cursor after window is realized"""
        window = self.get_window()
        if window:
            cursor = Gdk.Cursor.new_from_name(self.get_display(), "crosshair")
            window.set_cursor(cursor)
    
    def on_press(self, widget, event):
        self.x1, self.y1, self.selecting = event.x, event.y, True
    
    def on_motion(self, widget, event):
        self.mx, self.my = event.x, event.y
        if self.selecting:
            self.x2, self.y2 = event.x, event.y
    
    def on_release(self, widget, event):
        self.x2, self.y2, self.selecting = event.x, event.y, False
        x, y = min(self.x1, self.x2), min(self.y1, self.y2)
        w, h = abs(self.x2 - self.x1), abs(self.y2 - self.y1)
        
        if w > 5 and h > 5:
            try:
                filename = self.dir / f"screenshot_{datetime.now():%Y%m%d_%H%M%S}.png"
                crop = self.screenshot.new_subpixbuf(int(x), int(y), int(w), int(h))
                crop.savev(str(filename), "png", [], [])
                
                # Copy to clipboard
                try:
                    subprocess.run(['wl-copy'], input=crop.save_to_bufferv("png")[1], 
                                 timeout=2, check=False)
                except:
                    pass
                
                # Notification
                try:
                    subprocess.run(['notify-send', '📸 Screenshot', 
                                  f'Saved: {filename.name}', '-i', str(filename), 
                                  '-t', '3000'], timeout=2, check=False)
                except:
                    pass
                
                print(f"✓ Saved: {filename}")
            except Exception as e:
                print(f"✗ Error saving: {e}", file=sys.stderr)
        
        Gtk.main_quit()
    
    def on_key(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            print("Cancelled")
            Gtk.main_quit()
    
    def draw(self, widget, cr):
        # Background
        Gdk.cairo_set_source_pixbuf(cr, self.screenshot, 0, 0)
        cr.paint()
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.paint()
        
        # Selection area
        if self.x1 != self.x2 and self.y1 != self.y2:
            x, y = min(self.x1, self.x2), min(self.y1, self.y2)
            w, h = abs(self.x2 - self.x1), abs(self.y2 - self.y1)
            
            if w > 0 and h > 0:
                # Clear selection area
                cr.save()
                cr.rectangle(x, y, w, h)
                cr.clip()
                Gdk.cairo_set_source_pixbuf(cr, self.screenshot, 0, 0)
                cr.paint()
                cr.restore()
                
                # Border
                cr.set_source_rgba(0.3, 0.6, 1, 0.9)
                cr.set_line_width(2)
                cr.rectangle(x, y, w, h)
                cr.stroke()
                
                # Dimensions
                self.draw_dimensions(cr, x, y, w, h)
        
        # Crosshair
        cr.set_source_rgba(1, 0, 0, 0.8)
        cr.set_line_width(1)
        cr.move_to(self.mx, 0)
        cr.line_to(self.mx, self.h)
        cr.stroke()
        cr.move_to(0, self.my)
        cr.line_to(self.w, self.my)
        cr.stroke()
        
        # Zoom window
        self.draw_zoom(cr)
    
    def draw_dimensions(self, cr, x, y, w, h):
        """Draw selection dimensions"""
        cr.select_font_face("Sans", 0, 1)
        cr.set_font_size(14)
        text = f"{int(w)} × {int(h)}"
        ext = cr.text_extents(text)
        
        tx = x + w/2 - ext.width/2
        ty = y - 15 if y > 40 else y + h + 25
        
        # Background
        padding = 6
        cr.set_source_rgba(0, 0, 0, 0.85)
        cr.rectangle(tx - padding, ty - ext.height - padding, 
                    ext.width + padding * 2, ext.height + padding * 2)
        cr.fill()
        
        # Text
        cr.set_source_rgb(1, 1, 1)
        cr.move_to(tx, ty)
        cr.show_text(text)
    
    def draw_zoom(self, cr):
        """Draw zoom window with pixel mesh"""
        zs, zf = self.zoom_size, self.zoom_factor
        cs = zs // zf
        
        # Calculate position
        zx, zy = self.mx + 30, self.my + 30
        if zx + zs + 50 > self.w: 
            zx = self.mx - zs - 30
        if zy + zs + 50 > self.h: 
            zy = self.my - zs - 30
        zx = max(10, min(zx, self.w - zs - 10))
        zy = max(10, min(zy, self.h - zs - 60))
        
        # Get source coordinates
        sx = int(max(0, min(self.mx - cs/2, self.screenshot.get_width() - cs)))
        sy = int(max(0, min(self.my - cs/2, self.screenshot.get_height() - cs)))
        
        try:
            # Crop and zoom
            cropped = self.screenshot.new_subpixbuf(sx, sy, cs, cs)
            zoomed = cropped.scale_simple(zs, zs, GdkPixbuf.InterpType.NEAREST)
            
            # Border
            cr.set_source_rgba(0, 0, 0, 0.95)
            cr.rectangle(zx - 3, zy - 3, zs + 6, zs + 6)
            cr.fill()
            
            # Zoomed image
            Gdk.cairo_set_source_pixbuf(cr, zoomed, zx, zy)
            cr.rectangle(zx, zy, zs, zs)
            cr.fill()
            
            # Pixel mesh
            cr.set_source_rgba(1, 1, 1, 0.4)
            cr.set_line_width(1)
            ps = zs / cs
            
            for i in range(cs + 1):
                # Vertical lines
                x_pos = zx + i * ps
                cr.move_to(x_pos, zy)
                cr.line_to(x_pos, zy + zs)
                cr.stroke()
                
                # Horizontal lines
                y_pos = zy + i * ps
                cr.move_to(zx, y_pos)
                cr.line_to(zx + zs, y_pos)
                cr.stroke()
            
            # Center pixel highlight
            center = zs / 2
            cr.set_source_rgba(1, 0, 0, 0.9)
            cr.set_line_width(2)
            cr.rectangle(zx + center - ps/2, zy + center - ps/2, ps, ps)
            cr.stroke()
            
            # Info panel
            self.draw_info_panel(cr, zx, zy, zs)
            
        except Exception as e:
            print(f"Zoom error: {e}", file=sys.stderr)
    
    def draw_info_panel(self, cr, zx, zy, zs):
        """Draw pixel information panel"""
        mx, my = int(self.mx), int(self.my)
        
        if not (0 <= mx < self.screenshot.get_width() and 
                0 <= my < self.screenshot.get_height()):
            return
        
        try:
            pixels = self.screenshot.get_pixels()
            rs = self.screenshot.get_rowstride()
            nc = self.screenshot.get_n_channels()
            off = my * rs + mx * nc
            r, g, b = pixels[off], pixels[off + 1], pixels[off + 2]
            
            ih = 45
            
            # Background
            cr.set_source_rgba(0, 0, 0, 0.95)
            cr.rectangle(zx, zy + zs, zs, ih)
            cr.fill()
            
            # Text
            cr.select_font_face("Monospace", 0, 0)
            cr.set_font_size(11)
            cr.set_source_rgb(1, 1, 1)
            
            cr.move_to(zx + 8, zy + zs + 18)
            cr.show_text(f"X:{mx} Y:{my}")
            
            cr.move_to(zx + 8, zy + zs + 35)
            cr.show_text(f"RGB:({r},{g},{b})")
            
            # Color preview box
            box_size = 30
            box_x = zx + zs - box_size - 8
            box_y = zy + zs + 8
            
            cr.set_source_rgb(r/255, g/255, b/255)
            cr.rectangle(box_x, box_y, box_size, box_size)
            cr.fill()
            
            cr.set_source_rgb(1, 1, 1)
            cr.set_line_width(1)
            cr.rectangle(box_x, box_y, box_size, box_size)
            cr.stroke()
            
        except Exception as e:
            print(f"Info panel error: {e}", file=sys.stderr)


def main():
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "~/Pictures/Screenshots"
    Screenshot(output_dir)
    Gtk.main()


if __name__ == '__main__':
    main()
