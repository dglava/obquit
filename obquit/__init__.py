# Obquit
# Copyright (C) 2015  Dino Duratović <dinomol at mail dot com>
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

import subprocess
import sys
import atexit

from gi.repository import Gtk, Gdk

def execute_command(command):
    try:
        subprocess.Popen(command.split())
    except FileNotFoundError:
        pass

class OBquit:
    def __init__(self, commands, shortcuts, opacity, force_fake):
        # config attributes
        self.commands = commands
        self.shortcuts = shortcuts
        self.opacity = opacity
        self.force_fake = force_fake

        # window attributes
        self.window = Gtk.Window()
        self.window.fullscreen()
        self.window.set_decorated(False)
        self.window.set_skip_taskbar_hint(True)
        self.window.set_skip_pager_hint(True)
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

        # runs the composited version with actual transparency if a
        # compositor is available and not specified otherwise in the config
        if self.window_screen.is_composited() and not self.force_fake:
            self.run_composited()
        else:
            self.run_fake_transparency()

        # adds the box holding the buttons to the window
        self.window.add(self.button_line)
        # displays everything
        self.window.show_all()

        # main loop
        Gtk.main()

    def run_composited(self):
        """Runs the composited version with real transparency

        Requires a compositor. If this is run on a non-composited
        desktop, the background will just be black.
        """
        # TODO: will probably cause issues if it returns None
        visual = self.window_screen.get_rgba_visual()
        self.window.set_visual(visual)

        self.window.connect(
            "draw",
            self.on_draw_composited,
            self.opacity
            )

    def run_fake_transparency(self):
        """Runs the fake-transparency version

        Doesn't require a compositor. It achieves a transparent look by
        taking a screenshot of the desktop and using it as the window's
        background. The buttons get displayed on top of that.
        """
        self.get_background()
        self.window.connect("draw", self.on_draw_fake, self.opacity)

    def add_button(self, parent, name, command):
        """Adds a Box() with a Button() and Label()"""
        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)

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
        """For mouse clicks: runs the command when the GUI exits"""
        if command:
            atexit.register(execute_command, command)
        Gtk.main_quit()

    def on_keypress(self, widget, event):
        """For keypresses: runs the command when the GUI exits"""
        if Gdk.keyval_name(event.keyval) == "Escape":
            Gtk.main_quit()

        for command, key in self.shortcuts.items():
            # if pressed key was defined in the config and
            # if its associated command was found in the commands section
            if (Gdk.keyval_name(event.keyval).lower() == key and
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
        """Grabs the root window (screenshot)"""
        root_window = Gdk.get_default_root_window()
        self.background_pixbuf = Gdk.pixbuf_get_from_window(
            root_window,
            0, 0,
            self.screen_width, self.screen_height
            )
