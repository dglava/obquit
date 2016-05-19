# obquit
Utility script for logging out of a session, inspired by Oblogout.

##### Dependencies (Arch package names)
* python (Python 3)
* python-gobject
* python-cairo
* gtk3
* python-xdg

##### What works
- Custom command assignment (uses systemd's systemctl by default)
- Supports real (when using a compositor) and fake (doesn't need a compositor) transparency
- Keyboard shortcuts

##### What needs improvement
- Works pretty much as intended

##### How to use
- `$ python setup.py install`
- Edit the config file in /etc/obquit/obquit.conf
- Run `$ obquit`

Arch Linux users can use the provided PKGBUILD.

![](http://s15.postimg.org/ifenvwm4b/image.png)
