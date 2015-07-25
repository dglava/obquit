# obquit
Utility script for logging out of a session, inspired by Oblogout.

##### Dependencies (Arch package names)
* python (Python 3)
* python-gobject
* python-cairo
* gtk3

##### What works
- custom command assignment (uses systemd's systemctl by default)
- supports real (when using a compositor) and fake (doesn't need a compositor) transparency
- keyboard shortcuts

##### What needs improvement
- probably a lot of stuff

##### How to use

Copy the config file to either *~/.config/obquit/* or to */etc/obquit/* for a system wide configuration.
Start the script manually or bind it to a keyboard shortcut.


![](http://s15.postimg.org/ifenvwm4b/image.png)
