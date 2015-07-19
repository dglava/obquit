# obquit
Utility script for logging out of a session, inspired by Oblogout.

##### Dependencies
* Python 3
* PyGObject
* Python-Cairo
* GTK 3

##### What works
- custom command assignment for the various actions (uses systemd's systemctl by default)
- supports real (when using a compositor) and fake (doesn't need a compositor) transparency

##### What needs improvement
- probably a lot of stuff

##### How to use

Copy the config file to either *~/.config/obquit/* or to */etc/obquit/* for a system wide configuration.
Start the script manually or bind it to a keyboard shortcut.


![](http://s15.postimg.org/ifenvwm4b/image.png)
