#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# gnome-shell-zoom-control-window
# (c) May 2012, Timothy Hobbs <timothyhobbs@seznam.cz>
# (c) Sep 2011, Tobias Quinn <tobias@tobiasquinn.com>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
# GPLv3

import dbus, sys, os
import GnomeZoomSettings

import gtk

class controlWindow:
    def __init__(self):
        self._z = GnomeZoomSettings.Zoomer()
        filename = "/usr/share/zoomcontrolwindow/zoomcontrolwindow.glade"
        if not os.path.exists("/usr/share/zoomcontrolwindow/zoomcontrolwindow.glade") or "-l" in sys.argv:
            print "Using GTKBuilder file from local directory."
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
