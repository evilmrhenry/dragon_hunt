# file: rpg.py
#Copyright (C) 2005 Free Software Foundation
#This file is part of Dragon Hunt.

#Dragon Hunt is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#Dragon Hunt is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Dragon Hunt; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#This file is the first file accessed upon game start.
#It allows the player to select the module, or, if there is only one,
#automatically selects for the player.

#from Tkinter import *
import os
import pygame
import sys

try:
    import psyco

    psyco.full()
except ImportError:
    print "Psyco not found. Installing Psyco will increase performance."

pygame.init()
pygame.font.init()


import g
import module_picker
import new_game


pygame.display.set_caption("Loading")

#I can't use the standard image dictionary, as that requires the screen to
#be created.
tmp_icon = pygame.image.load(os.path.join(g.base_location, "modules/default/images/buttons/icon.png"))
pygame.display.set_icon(tmp_icon)

g.screen_size = (640, 480)

if g.fullscreen == 1:
    g.screen = pygame.display.set_mode(g.screen_size, pygame.FULLSCREEN)
else:
    g.screen = pygame.display.set_mode(g.screen_size)

tmpjoycount = pygame.joystick.get_count()
if pygame.joystick.get_init() == 0:
    pygame.joystick.init()

g.joystick = 0
if tmpjoycount > g.joy_num:
    g.joystick = pygame.joystick.Joystick(g.joy_num)
    g.joystick.init()
elif tmpjoycount > 0:
    print "Bad joystick_number detected. Did you unplug a joystick recently?"
    print "Switching to first joystick."
    g.joystick = pygame.joystick.Joystick(0)
    g.joystick.init()


#given a certain mod, run it.
def sel_mod(selected_mod):
    g.mod_directory = os.path.join(g.base_location, "modules", selected_mod)

    g.create_norm_box((g.screen_size[0] / 4,
                       g.screen_size[1] / 3), (g.screen_size[0] / 2,
                                               g.screen_size[1] / 3),
                      "black", "light_gray")

    g.print_string(g.screen, "Loading. Please wait", g.font,
                   (g.screen_size[0] / 2, g.screen_size[1] / 2), align=1)
    #	g.main.canvas_map.create_text(, text="Loading. Please wait")
    pygame.display.set_caption("Loading")
    pygame.display.flip()
    #	g.window_main.update_idletasks()
    g.init_data()
    new_game.init_window()


def init_window():
    g.load_buttons()
    selected_module = None
    picker = module_picker.ModulePicker(g.screen)
    if len(sys.argv) > 1:
        sys.argv.pop(0)
        for arg in sys.argv:
            if arg.strip().lower() == "-debug":
                g.debug = True
                print "Activating debug mode"
            elif arg.strip().lower() == "-faststart":
                g.faststart = True
                print "Activating faststart mode"
            else:
                try:
                    mod_loc = picker.array_mods.index(arg)
                except ValueError:
                    print "Unknown module: " + arg
                    return 0
                selected_module = picker.array_mods[mod_loc]

    if not selected_module:
        selected_module = picker.init_window()
    if selected_module:
        sel_mod(selected_module)
    else:
        return 0


init_window()
