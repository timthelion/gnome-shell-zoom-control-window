#!/usr/bin/env python2

# gnome-shell-zoom-control-window
# (c) Jan 2012, Timothy Hobbs <timothyhobbs@seznam.cz>
# (c) Sep 2011, Tobias Quinn <tobias@tobiasquinn.com>
# GPLv3

import dbus, sys, os
from dbus import DBusException
session_bus = dbus.SessionBus()

import gtk

incr = 0.1

class Zoomer:
    def __init__(self):
        self._refreshDBUS()
        self._active = self._mag.isActive()
        cz = self._zoom.getMagFactor()
        self._currentZoom = [cz[0], cz[1]]

    def _refreshDBUS(self):
        self._mag = session_bus.get_object(
                'org.gnome.Magnifier',
                '/org/gnome/Magnifier')
        self._mag.getZoomRegions()
        self._zoom = session_bus.get_object(
                'org.gnome.Magnifier',
                '/org/gnome/Magnifier/ZoomRegion/zoomer0')

    def zoomIn(self):
        if self._active:
            self._currentZoom[0] *= (1.0+incr)
            self._currentZoom[1] *= (1.0+incr)
            try:
                self._zoom.setMagFactor(self._currentZoom[0], self._currentZoom[1])
            except DBusException:
                self._refreshDBUS()
        else:
            try:
                self._zoom.setMagFactor(1 + incr, 1 + incr)
            except DBusException:
                self._refreshDBUS()
            self._currentZoom = [1 + incr, 1 + incr]
            self._mag.setActive(True)
            self._active = True

    def zoomOut(self):
        if self._active:
            self._currentZoom[0] *= (1.0-incr)
            self._currentZoom[1] *= (1.0-incr)
            if self._currentZoom[0] <= 1:
                self._mag.setActive(False)
                self._active = False
            else:
                try:
                    self._zoom.setMagFactor(self._currentZoom[0], self._currentZoom[1])
                except DBusException:
                    self._refreshDBUS()

    def zoomOff(self):
        self._mag.setActive(False)
        self._active = False

    def zoomOn(self):
        self._mag.setActive(True)
        self._active = True

    def isActive(self):
        return self._active


class controlWindow:
    def __init__(self):
        self._z = Zoomer()
        filename = "/usr/share/zoomcontrolwindow/zoomcontrolwindow.glade"
        if not os.path.exists("/usr/share/zoomcontrolwindow/zoomcontrolwindow.glade"):
            filename = "zoomcontrolwindow.glade"
        builder = gtk.Builder()
        builder.add_from_file(filename)
        builder.connect_signals(self)
        self._onoffbutton = builder.get_object("zoom_on_off_button")
        self._refresh_zoom_button_label()
        self._window = builder.get_object("zoomcontrolwindow")
        self.show_above()
        #make a status icon
        self.statusicon = gtk.status_icon_new_from_stock(gtk.STOCK_FIND)
        self.statusicon.connect('activate', self.status_clicked )
        self.statusicon.connect('popup-menu', self.make_menu )
        self.statusicon.set_tooltip("Zoom")

    def show_above(self):
        self._window.show()
        self._window.set_keep_above(True)

    def make_menu(event_button, event_time, data=None, a=None):
        menu = gtk.Menu()
        exit_item = gtk.MenuItem("Exit")
        menu.append(exit_item)
        exit_item.connect_object("activate", close_app, "Exit")
        exit_item.show()
        menu.popup(None, None, None, 0,0)


    def _refresh_zoom_button_label(self):
        if self._z.isActive():
            self._onoffbutton.set_label("Zoom Off")
        else:
            self._onoffbutton.set_label("Zoom On")
        

    def on_buttonZoomIn_clicked(self, widget):
        self._z.zoomIn()
        self._refresh_zoom_button_label()

    def on_buttonZoomOut_clicked(self, widget):
        self._z.zoomOut()
        self._refresh_zoom_button_label()
    
    def on_buttonZoomOnOff_clicked(self, widget):
        if self._z.isActive():        
            self._z.zoomOff()
            self._refresh_zoom_button_label()
        else:
            self._z.zoomOn()
            self._refresh_zoom_button_label()

    def on_window_delete(self, window, widget):
        #don't delete; hide instead
        self._window.hide_on_delete()
        return True

    def status_clicked(self,status):
        if self._window.get_visible():
            self._window.hide_on_delete()        
        else:
            #unhide the window
            self.show_above()

    def on_status_right_click(data, event_button, event_time):
        make_menu(event_button, event_time)

def close_app(data=None):
    gtk.main_quit()

app = controlWindow()
gtk.main()
