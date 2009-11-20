#!/usr/bin/python2.5

import gtk
import gobject
from gtk import gdk
import cairo

class Lightbox(gtk.Widget):
    def __init__(self, size, message):
        super(Lightbox, self).__init__()
        self.width, self.height = size
    
    def do_realize(self):
        '''called when the widget should create its windowing resources'''
        
        #self.event_box = gtk.EventBox()
        #screen = self.event_box.get_screen()
        #rgba = screen.get_rgba_colormap()
        #self.event_box.set_colormap(rgba)
        
        # First set an internal flag telling that we're realized
        self.set_flags(self.flags() | gtk.REALIZED)
        
        # Create a new gdk.Window which we can draw on.
        # Also say that we want to receive exposure events
        # and button click and button press events
        self.window = gdk.Window(
            self.get_parent_window(),
            width=self.width,
            height=self.height,
            window_type=gdk.WINDOW_CHILD,
            wclass=gdk.INPUT_OUTPUT,
            event_mask=(self.get_events()
                        | gdk.EXPOSURE_MASK
                        | gdk.BUTTON1_MOTION_MASK
                        | gdk.BUTTON_PRESS_MASK
                        | gtk.gdk.POINTER_MOTION_MASK
                        | gtk.gdk.POINTER_MOTION_HINT_MASK))

        # Associate the gdk.Window with ourselves, Gtk+ needs a reference
        # between the widget and the gdk window
        self.window.set_user_data(self)
        
        # Attach the style to the gdk.Window, a style contains colors and
        # GC contextes used for drawing
        self.style.attach(self.window)

        # The default color of the background should be what
        # the style (theme engine) tells us.
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.window.move_resize(*self.allocation)
        
        # self.style is a gtk.Style object, self.style.fg_gc is
        # an array or graphic contexts used for drawing the forground
        # colours
        self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
        
        self.window.set_composited(True)

        self.connect("motion_notify_event", self.motion_notify_event)
    
    def do_unrealize(self):
        # The do_unrealized method is responsible for freeing the GDK resources
        # De-associate the window we created in do_realize with ourselves
        self.window.destroy()
    
    def do_expose_event(self, event):
        """This is where the widget must draw itself."""
        print 'look at me'
        
        
        cr = self.window.cairo_create()
        
        cr.set_source_rgba(0.0, 0.0, 0.0, 0.0) # Transparent

        # Draw the background
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        #cr.set_operator(cairo.OPERATOR_OVER)
        #cr.paint_with_alpha(0.0)

        # draw rounded rect

        #/* a custom shape, that could be wrapped in a function */
        x0 = 0   #/*< parameters like cairo_rectangle */
        y0 = 0

        radius = max(50, self.width/2, self.height/2)  #/*< and an approximate curvature radius */

        x1 = x0 + width
        y1 = y0 + height

        cr.move_to  (x0, y0 + radius)
        cr.arc (x0 + radius, y0 + radius, radius, 3.14, 1.5 * 3.14)
        cr.line_to (x1 - radius, y0)
        cr.arc (x1 - radius, y0 + radius, radius, 1.5 * 3.14, 0.0)
        cr.line_to (x1 , y1 - radius)
        cr.arc (x1 - radius, y1 - radius, radius, 0.0, 0.5 * 3.14)
        cr.line_to (x0 + radius, y1)
        cr.arc (x0 + radius, y1 - radius, radius, 0.5 * 3.14, 3.14)

        cr.close_path ()

        cr.set_source_rgba (0.0, 0.0, 0.0, 0.5)
        cr.fill_preserve ()
        #cr.set_source_rgba(0.5, 0.5, 1.0, 0.8)
        #cr.stroke()
    
    def motion_notify_event(self, widget, event):
        # if this is a hint, then let's get all the necessary
        # information, if not it's all we need.
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state
        
        #print x,y
    
    def do_button_press_event(self, event):
        """The button press event virtual method"""

        print 'button', event.button
        return True

if __name__ == "__main__":
    # register the class as a Gtk widget
    gobject.type_register(Lightbox)

    win = gtk.Window()
    #win.resize(200,200)
    win.connect('delete-event', gtk.main_quit)
    
    pixbuf = gtk.gdk.pixbuf_new_from_file('ian2.png')
    pixmap, mask = pixbuf.render_pixmap_and_mask()
    width, height = pixmap.get_size()
    win.set_app_paintable(True)
    win.resize(width, height)
    win.realize()
    win.window.set_back_pixmap(pixmap, False)

    lb = Lightbox((200,100), 'hello world')

    win.add(lb)
    win.show_all()
    gtk.main()
