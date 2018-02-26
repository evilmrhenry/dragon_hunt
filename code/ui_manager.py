# file: ui_manager.py
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

#This file holds a generic ui manager. It handles displaying ui elements, and seeing if a button has been pressed.


import g


class UIElement(object):
    """Base class. Do not initialize directly."""
    def __init__(self, x, y, width, height, tag=None, image=None):
        self.tag = tag
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.clickable = False

    def over(self, x, y):
        """Returns True if the x/y given is over the element"""
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

    def draw(self, screen, x, y):
        if self.image:
            screen.blit(self.image, self.x, self.y)


class UIImage(UIElement):
    """Represents an image. Doesn't do anything."""
    def __init__(self, x, y, image, tag=None):
        width = image.get_width()
        height = image.get_height()
        super(UIImage, self).__init__(x, y, width, height, tag, image)


class UIBox(UIElement):
    """Represents a box. It can create an outlined box, or a single-color box."""
    def __init__(self, x, y, width, height, tag=None, outline_color="black", inner_color=None):
        super(UIBox, self).__init__(x, y, width, height, tag)
        self.outline_color = g.colors[outline_color]
        self.inner_color = g.colors[inner_color] if inner_color else None

    def draw(self, screen, x, y):
        screen.fill(self.outline_color, (self.x, self.y, self.width, self.height))
        if self.inner_color:
            screen.fill(self.inner_color, (self.x+1, self.y+1, self.width-2, self.height-2))


class UIButton(UIElement):
    """Represents a button. Be sure to use a tag on this, so you can do something on click."""
    def __init__(self, x, y, image_unselected, image_selected=None, tag=None):
        if image_selected is None:
            image_selected = g.get_selected_name(image_unselected)
        self.image_unselected = g.buttons[image_unselected]
        self.image_selected = g.buttons[image_selected]
        super(UIButton, self).__init__(x, y, self.image_selected.get_width(), self.image_selected.get_height(), tag)
        self.clickable = True

    def draw(self, screen, x, y):
        """x/y should be the mouse location"""
        if self.over(x, y):
            screen.blit(self.image_selected)
        else:
            screen.blit(self.image_unselected)


class UIText(UIElement):
    """Represents a text display."""
    def __init__(self, x, y, text, tag=None, font=None, color="black", align=0):
        self.color = g.colors[color]
        text = text.replace("\t", "     ")
        if not font:
            font = g.font
        image = font.render(text, 1, self.color)
        self.font = font
        width = image.get_width()
        height = image.get_height()
        self.align = align
        self.base_x = x
        if self.align == 1:
            x -= width / 2
        elif self.align == 2:
            x -= width
        super(UIText, self).__init__(x, y, width, height, tag, image)

    def change_text(self, new_text):
        new_text = new_text.replace("\t", "     ")
        self.image = self.font.render(new_text, 1, self.color)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        if self.align == 1:
            self.x = self.base_x - self.width / 2
        elif self.align == 2:
            self.x = self.base_x - self.width


class UIManager(object):
    """
    Overall manager for the UI system.
    Expected usage: init with g.screen, use extend_elements() or append_element() to fill the UI manager with
    UI elements. Fill items in z-order. Once a frame call the draw_handler(), and call click_handler() on click.
    """
    def __init__(self, screen):
        self.screen = screen
        self._element_list = []

    def extend_elements(self, element_list):
        """:param element_list: A list of UIElement classes."""
        self._element_list.extend(element_list)

    def append_element(self, element):
        """:param element: A UIElement class"""
        self._element_list.append(element)

    def insert_element(self, i, element):
        """
        :param i: the index to insert at
        :param element: A UIElement class
        """
        self._element_list.insert(i, element)

    def pop_element(self, tag):
        """Will remove all elements with the specified tag"""
        for i in range(len(self._element_list)-1, -1, -1):
            if self._element_list[i].tag == tag:
                self._element_list.pop(i)

    def click_handler(self, x, y):
        """Will return the tag of the element clicked on, or None if nothing interesting was clicked on."""
        for i in range(len(self._element_list)-1, -1, -1):
            element = self._element_list[i]
            if element.clickable and element.tag and element.over(x, y):
                return element.tag
        return None

    def draw_handler(self, x, y):
        """Will redraw the UI elements. Call once a frame."""
        for element in self._element_list:
            element.draw(self.screen, x, y)
