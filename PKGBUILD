# Author: Timothy Hobbs <timothyhobbs@seznam.cz>
# Maintainer: Timothy Hobbs <timothyhobbs@seznam.cz>
pkgname=gnome-shell-zoom-control-window
url=http://brmlab.cz/user/timthelion
pkgver=0.O.1
pkgrel=1
pkgdesc="A floating window to control zoom levels in gnome3"
arch=('i686' 'x86_64')
url="https://github.com/timthelion/gnome-shell-zoom-control-window"
license=('GPL3')
depends=('python2' 'dbus-python' 'gnome-shell')
makedepends=('git')
conflicts=('gnome-shell-zoom-control-window-git')
provides=('gnome-shell-zoom-control-window-git')

_gitroot="git://github.com/timthelion/gnome-shell-zoom-control-window.git"
_gitname="gnome-shell-zoom-control-window"

build() {
  cd "$srcdir"
  msg "Connecting to GIT server..."

  if [ -d $_gitname ] ; then
    cd $_gitname && git pull origin
    msg "The local files are updated."
  else
    git clone $_gitroot $_gitname
  fi

  msg "GIT checkout done or server timeout"

  install -D -m755 ${srcdir}/$_gitname/zoomcontrolwindow.py "${pkgdir}/usr/bin/zoomcontrolwindow.py" || return 1
  install -D -m644 ${srcdir}/$_gitname/zoomcontrolwindow.py.desktop "${pkgdir}/usr/share/applications/zoomcontrolwindow.py.desktop" || return 1
  install -D -m644 ${srcdir}/$_gitname/zoomcontrolwindow.glade "${pkgdir}/usr/share/zoomcontrolwindow/zoomcontrolwindow.glade" || return 1
}

# vim:set ts=2 sw=2 et:
