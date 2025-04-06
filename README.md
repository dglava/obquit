# obquit
Utility script for logging out of a session, inspired by Oblogout.

![](https://raw.githubusercontent.com/dglava/obquit/master/screen.png)

##### Dependencies (Arch package names)
* python
* python-gobject
* python-cairo
* gtk3

##### What works
- Custom command assignment (uses systemd's systemctl by default)
- Supports real (when using a compositor) and fake (doesn't need a compositor) transparency
- Keyboard shortcuts

##### What needs improvement
- Works pretty much as intended

##### How to use
- Build and install the package
- Edit the config file in /etc/obquit.conf
- Run `obquit`

Arch Linux users can install it from the [AUR](https://aur.archlinux.org/packages/obquit-git/).
