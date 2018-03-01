# file: module_picker.py
# Copyright (C) 2018 Free Software Foundation
# This file is part of Dragon Hunt.

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

#This file holds the UI and logic for the module picking screen.
import os
import pygame
import g

import ui_manager

QUIT = "quit"
MODULE = "module"

class ModulePicker(object):
    def __init__(self, screen):
        self.screen = screen
        self.module_pos = 0
        self.array_mods = self.find_mods()
        self.mouse_xy = (0, 0)
        self.ui_manager = ui_manager.UIManager(screen)
        self.state = None

    def refresh_module_info(self):
        g.unclean_screen = True
        tmp = self.module_pos - (self.module_pos % 5)
        for i in range(5):
            if i == self.module_pos % 5:
                tmp_color = "dh_green"
            else:
                tmp_color = "light_gray"
            g.create_norm_box((g.tilesize * g.main.mapsizex / 4 + 2,
                               g.tilesize * g.main.mapsizey / 3 +
                               g.buttons["loadgame_down.png"].get_height() + 1 + i * 20),
                              (g.buttons["loadgame_down.png"].get_width() - 5, 17),
                              inner_color=tmp_color)

            if len(self.array_mods) <= tmp + i:
                savetext = ""
            else:
                savetext = self.array_mods[tmp + i]
            g.print_string(g.screen, savetext, g.font, (g.tilesize * g.main.mapsizex / 4 + 5,
                                                        g.tilesize * g.main.mapsizey / 3 +
                                                        g.buttons["loadgame_down.png"].get_height() + 3 + i * 20))

    def quit_game(self):
        self.state = QUIT

    def sel_list_mod(self):
        self.state = MODULE

    def key_handler(self, switch):
        if switch == g.bindings["cancel"]:
            self.quit_game()
        elif switch == g.bindings["up"]:
            self.module_pos -= 1
            if self.module_pos <= -1:
                self.module_pos = len(self.array_mods) - 1
            self.refresh_module_info()
        elif switch == g.bindings["down"]:
            self.module_pos += 1
            if self.module_pos >= len(self.array_mods):
                self.module_pos = 0
            self.refresh_module_info()
        elif switch == g.bindings["action"]:
            self.sel_list_mod()

    def mouse_handler_move(self):
        self.refresh_buttons()
        self.refresh_module_info()

    def refresh_buttons(self):
        self.ui_manager.draw_handler(*self.mouse_xy)
        g.unclean_screen = True

    def mouse_handler_down(self):
        tag = self.ui_manager.click_handler(*self.mouse_xy)
        if tag == "up":
            tmp = self.module_pos - (self.module_pos % 5) - 5
            if tmp < 0:
                self.module_pos = len(self.array_mods) - (len(self.array_mods) % 5) + (self.module_pos % 5)
                if self.module_pos >= len(self.array_mods):
                    self.module_pos = len(self.array_mods) - 1
            else:
                self.module_pos -= 5
            self.refresh_module_info()

        if tag == "down":
            tmp = self.module_pos - (self.module_pos % 5) + 5
            if tmp >= len(self.array_mods):
                self.module_pos = (self.module_pos % 5)
            else:
                self.module_pos += 5
                if self.module_pos >= len(self.array_mods):
                    self.module_pos = len(self.array_mods) - 1
            self.refresh_module_info()

        if tag == "load":
            self.sel_list_mod()

        if tag == "quit":
            self.quit_game()

        #save "listbox"
        if self.mouse_over(self.mouse_xy,
                           g.tilesize * g.main.mapsizex / 4,
                           g.tilesize * g.main.mapsizey / 3 + g.buttons["loadgame_up.png"].get_height(),
                           g.tilesize * g.main.mapsizex / 4 + g.buttons["loadgame_up.png"].get_width(),
                           g.tilesize * g.main.mapsizey / 3 + 140 - g.buttons["loadgame_down.png"].get_height()):

            base_y = (self.mouse_xy[1] -
                      g.tilesize * g.main.mapsizey / 3 + g.buttons["loadgame_up.png"].get_height())
            base_y -= 40
            if base_y % 20 < 2 or base_y % 20 > 18:
                return
            tmp = self.module_pos - (self.module_pos % 5) + (base_y / 20)
            if tmp >= len(self.array_mods):
                return
            else:
                self.module_pos = tmp
            self.refresh_module_info()

    @staticmethod
    def mouse_over(xy, x1, y1, x2, y2):
        if x1 <= xy[0] <= x2 and y1 <= xy[1] <= y2:
            return 1
        return 0

    @staticmethod
    def find_mods():
        module_dir = os.path.join(g.base_location, "modules")
        array_mods = os.listdir(module_dir)
        bad_names = {"CVS", "default"}
        return [module for module in array_mods
                if os.path.isdir(os.path.join(module_dir, module)) and module not in bad_names]

    def init_window(self):
        """
        Actually start the module picker screen.
        :return: The module to run, or None if the player decided to quit.
        """

        #if there is only one module, run it.
        if len(self.array_mods) == 1:
            return self.array_mods[0]

        pygame.display.set_caption("Select module")
        g.mod_directory = os.path.join(g.base_location, "modules", "default")

        self.ui_manager = ui_manager.UIManager(g.screen)

        background = ui_manager.UIBox(0, 0, g.screen.get_width(), g.screen.get_height(), outline_color="purple")
        black_bar = ui_manager.UIBox(0, g.tilesize * g.main.mapsizey / 2, g.tilesize * g.main.mapsizex, 30, "black")
        pick_one = ui_manager.UIText(g.tilesize * g.main.mapsizex / 2 + 10, g.tilesize * g.main.mapsizey / 2 + 15,
                                     "You have multiple modules installed. Pick one to play.", color="white")
        listbox_container = ui_manager.UIBox(g.tilesize * g.main.mapsizex / 4 - 2, g.tilesize * g.main.mapsizey / 3 - 2,
                                             g.buttons["loadgame_up.png"].get_width() + 4,
                                             140 + g.buttons["load.png"].get_height() + 4,
                                             outline_color="black", inner_color="light_gray")

        up_button = ui_manager.UIButton(g.tilesize * g.main.mapsizex / 4, g.tilesize * g.main.mapsizey / 3,
                                        "loadgame_up.png", tag="up")
        down_button = ui_manager.UIButton(g.tilesize * g.main.mapsizex / 4,
                                          g.tilesize * g.main.mapsizey / 3 + 140 - g.buttons["loadgame_down.png"].get_height(),
                                          "loadgame_down.png", tag="down")
        load_button = ui_manager.UIButton(g.tilesize * g.main.mapsizex / 4, g.tilesize * g.main.mapsizey / 3 + 140,
                                          "load.png", tag="load")
        quit_button = ui_manager.UIButton(g.tilesize * g.main.mapsizex / 4 + g.buttons["load.png"].get_width(),
                                          g.tilesize * g.main.mapsizey / 3 + 140, "quit.png", tag="quit")

        self.ui_manager.extend_elements([background, black_bar, pick_one, listbox_container, up_button, down_button,
                                         load_button, quit_button])

        self.refresh_buttons()
        self.refresh_module_info()
        self.main_loop()
        if self.state == QUIT:
            return None
        elif self.state == MODULE:
            return self.array_mods[self.module_pos]

    def main_loop(self):
        while 1:
            pygame.time.wait(30)
            g.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = QUIT
                    return
                elif event.type == pygame.KEYDOWN:
                    self.key_handler(event.key)
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_xy = event.pos
                    self.mouse_handler_move()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_xy = event.pos
                    self.mouse_handler_move()
                    self.mouse_handler_down()
            tmpjoy = g.run_joystick()
            if tmpjoy:
                self.key_handler(tmpjoy)

            if g.unclean_screen:
                g.unclean_screen = False
                pygame.display.flip()
            if self.state:
                return
