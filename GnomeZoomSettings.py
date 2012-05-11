#!/usr/bin/env python2

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


from gi.repository.Gio import Settings

class Zoomer:
    def __init__(self):
        self.incr = 0.1
        self._refreshSettings()

    def _refreshSettings(self):
        self.a11yAppPrefs = Settings('org.gnome.desktop.a11y.applications')
        self.magPrefs = Settings('org.gnome.desktop.a11y.magnifier')

    def zoomIn(self):
      mag_factor = self.magPrefs.get_double('mag-factor')
      self.magPrefs.set_double('mag-factor', mag_factor + self.incr)
      self.zoomOn()

    def zoomOut(self):
      mag_factor = self.magPrefs.get_double('mag-factor')
      self.magPrefs.set_double('mag-factor', mag_factor - self.incr)
      self.zoomOn()

    def zoomOff(self):
        self.a11yAppPrefs.set_boolean('screen-magnifier-enabled', False)

    def zoomOn(self):
        self.a11yAppPrefs.set_boolean('screen-magnifier-enabled', True)

    def isActive(self):
        return self.a11yAppPrefs.get_boolean('screen-magnifier-enabled')
