# obquit
Utility script for logging out of a session, inspired by Oblogout.

![](https://s31.postimg.org/mzvm9q3vv/2016_06_20_20_48_49.png)

##### Dependencies (Arch package names)
* python (Python 3)
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
- `$ python setup.py install`
- Edit the config file in /etc/obquit.conf
- Run `$ obquit`

Arch Linux users can install it from the [AUR](https://aur.archlinux.org/packages/obquit-git/).
