#!/usr/bin/env python2

# gnome-shell-zoom-control-window
# (c) Jan 2012, Timothy Hobbs <timothyhobbs@seznam.cz>
# (c) Sep 2011, Tobias Quinn <tobias@tobiasquinn.com>
# GPLv3

import dbus, sys
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
        builder = gtk.Builder()
        builder.add_from_file(filename)
        builder.connect_signals(self)
        self._onoffbutton = builder.get_object("zoom_on_off_button")
        self._refresh_zoom_button_label()
        window = builder.get_object("zoomcontrolwindow")
        window.show()

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
    
    def on_window_destroy(self, widget):
        sys.exit()

    def on_buttonZoomOnOff_clicked(self, widget):
        if self._z.isActive():        
            self._z.zoomOff()
            self._refresh_zoom_button_label()
        else:
            self._z.zoomOn()
            self._refresh_zoom_button_label()

app = controlWindow()
gtk.main()
