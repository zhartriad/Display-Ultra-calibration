pkgname=cachy-display-tool
pkgver=1.0
pkgrel=1
pkgdesc="Ferramenta ultra de ajuste de cores, brilho e saturação para CachyOS"
arch=('any')
depends=('python' 'python-gobject' 'gtk3' 'libvibrant' 'xorg-xrandr')
source=("main.py" "apply_display.py" "background.jpg")
sha256sums=('SKIP' 'SKIP' 'SKIP')

package() {

  mkdir -p "$pkgdir/usr/bin"
  mkdir -p "$pkgdir/usr/share/cachy-display"
  mkdir -p "$pkgdir/usr/share/applications"
  mkdir -p "$pkgdir/etc/xdg/autostart"

  install -Dm755 "$srcdir/main.py" "$pkgdir/usr/bin/cachy-display-tool"
  install -Dm755 "$srcdir/apply_display.py" "$pkgdir/usr/bin/cachy-display-apply"

  install -Dm644 "$srcdir/background.jpg" "$pkgdir/usr/share/cachy-display/background.jpg"

  echo "[Desktop Entry]
Version=1.0
Type=Application
Name=Cachy Display Ultra
Comment=Ajuste de saturação e cores (ThinkPad)
Exec=/usr/bin/cachy-display-tool
Icon=video-display
Terminal=false
Categories=Settings;HardwareSettings;
Keywords=display;color;saturation;gamma;" > "$pkgdir/usr/share/applications/cachy-display.desktop"

  echo "[Desktop Entry]
Type=Application
Name=Cachy Display Autostart
Comment=Aplica as configurações de cor salvas
Exec=/usr/bin/cachy-display-apply
OnlyShowIn=XFCE;GNOME;KDE;
Terminal=false" > "$pkgdir/etc/xdg/autostart/cachy-display-apply.desktop"
}
