# Obquit
# Copyright (C) 2015  Dino Duratović <dinomol@mail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import configparser
import os.path
import subprocess
import sys
import atexit
from collections import OrderedDict

try:
    from gi.repository import Gtk, Gdk
except ImportError:
    print("Python-GObject not found. You need to install it.")
    sys.exit()

try:
    import cairo
except ImportError:
    print("Python-cairo not found. You need to install it.")
    sys.exit()

def execute_command(command):
    subprocess.Popen(command.split())

class OBquit:
    def __init__(self):
        # parse config
        self.parse_config()

        # window attributes
        self.window = Gtk.Window()
        self.window.fullscreen()
        self.window.set_decorated(False)
        self.window.set_app_paintable(True)
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.connect("key-press-event", self.on_keypress)

        self.window_screen = self.window.get_screen()
        self.screen_width = self.window_screen.get_width()
        self.screen_height = self.window_screen.get_height()

        # widget holding all the buttons and their labels
        self.button_line = Gtk.Box(
            spacing=10,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            homogeneous=True
            )

        # adds a button/label Box() for each command
        for name, command in self.commands.items():
            self.add_button(self.button_line, name, command)
        # TODO: maybe remove this and add a cancel button to the config
        self.add_button(self.button_line, "cancel")

        # runs the composited version with actual transparency if a
        # compositor is available and not specified otherwise in the config
        if self.window_screen.is_composited() and not self.force_fake:
           self.run_composited()
        else:
            self.run_fake_transparency()

    def parse_config(self):
        # TODO: try to make this more elegant
        user = os.path.expanduser("~/.config/obquit/obquit.conf")
        system = "/etc/obquit/obquit.conf"

        # a local user config takes precedence
        if os.path.exists(user):
            config_file = user
        elif os.path.exists(system):
            config_file = system
        else:
            config_file = None

        config = configparser.ConfigParser()
        if config_file:
            config.read(config_file)

        # Commands section
        if not config.has_section("Commands"):
            self.commands = OrderedDict(
                (("shutdown", "systemctl poweroff"),
                ("suspend", "systemctl suspend"),
                ("logout", "openbox --exit"),
                ("hibernate", "systemctl hibernate"),
                ("reboot", "systemctl reboot"))
                )
        else:
            self.commands = OrderedDict()
            for name, command in config["Commands"].items():
                self.commands[name] = command

        # Shortcuts section
        if not config.has_section("Shortcuts"):
            self.shortcuts = {
                "shutdown": "s",
                "suspend": "u",
                "logout": "l",
                "hibernate": "h",
                "reboot": "r"
                }
        else:
            self.shortcuts = {}
            for command, shortcut in config["Shortcuts"].items():
                self.shortcuts[command] = shortcut

        # Options section
        if config.has_option("Options", "opacity"):
            self.opacity = config.getfloat("Options", "opacity")
        else:
            self.opacity = 0.7

        if config.has_option("Options", "force fake"):
            self.force_fake = config.getboolean("Options", "force fake")
        else:
            self.force_fake = False

    def run_composited(self):
        # TODO: will probably cause issues if it returns None
        visual = self.window_screen.get_rgba_visual()
        self.window.set_visual(visual)

        self.window.connect(
            "draw",
            self.on_draw_composited,
            self.opacity
            )
        self.window.add(self.button_line)

    def run_fake_transparency(self):
        self.get_background()
        self.window.connect("draw", self.on_draw_fake, self.opacity)
        self.window.add(self.button_line)

    def add_button(self, parent, name, command=None):
        # creates a Box() containing a Button() and Label() with
        # the specified name and command
        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)

        # TODO: probably add icons to buttons or image theme support
        button = Gtk.Button("")
        button.connect("clicked", self.on_click, command)
        label = Gtk.Label()
        label.set_markup(
            "<span fgcolor='white' size='large'>{}</span>".format(name)
            )

        box.pack_start(button, False, False, 0)
        box.pack_start(label, False, False, 0)
        parent.pack_start(box, False, True, 0)

    def on_click(self, widget, command):
        # registers the command to be run when the GUI's main loop closes
        # it's probably cleaner this way
        if command:
            atexit.register(execute_command, command)
        Gtk.main_quit()

    def on_keypress(self, widget, event):
        # gets keypresses and executes a command
        if Gdk.keyval_name(event.keyval) == "Escape":
            Gtk.main_quit()

        for command, key in self.shortcuts.items():
            # if pressed key was defined in the config and
            # if its associated command was found in the commands section
            if (Gdk.keyval_name(event.keyval) == key and
                    command in self.commands.keys()):
                command_to_exec = self.commands[command]
                atexit.register(execute_command, command_to_exec)
                Gtk.main_quit()

    def on_draw_fake(self, widget, cairo_context, opacity):
        # draws a pixbuf as the window's background;
        # the pixbuf is a screenshot of the desktop
        Gdk.cairo_set_source_pixbuf(
            cairo_context,
            self.background_pixbuf,
            0, 0
            )
        cairo_context.paint()

        # overlays a black shade with the chosen opacity
        cairo_context.set_source_rgba(0, 0, 0, opacity)
        cairo_context.rectangle(
            0, 0,
            self.screen_width, self.screen_height
            )
        cairo_context.fill()

    def on_draw_composited(self, widget, cairo_context, opacity):
        cairo_context.set_source_rgba(0, 0, 0, opacity)
        # copy/pasted; maybe figure out what it actually does
        cairo_context.set_operator(cairo.OPERATOR_SOURCE)
        cairo_context.paint()

    def get_background(self):
        # grabs the root window (screenshot)
        root_window = Gdk.get_default_root_window()
        self.background_pixbuf = Gdk.pixbuf_get_from_window(
            root_window,
            0, 0,
            self.screen_width, self.screen_height
            )
