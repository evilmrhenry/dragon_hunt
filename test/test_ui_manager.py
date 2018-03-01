# file: test_ui_manager.py
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

#This file holds the tests for ui_manager.py

import mock
import unittest
import pygame

pygame.init()  # This is because g.py does some pygame stuff on import; remove it once that's refactored out.
pygame.font.init()

import ui_manager


class MockedUIElement(ui_manager.UIElement):
    def __init__(self, tag=None):
        self.called = 0
        self.is_over = False
        super(MockedUIElement, self).__init__(0, 0, 0, 0, tag)

    def draw(self, screen, x, y):
        self.called += 1

    def over(self, x, y):
        return self.is_over


class TestUIManager(unittest.TestCase):
    def setUp(self):
        self.ui_manager = ui_manager.UIManager(mock.Mock())

    def test_pop_element(self):
        """
        Should remove both mock2 elements without touching the other elements. Also tests the draw_handler.
        """
        elements = [MockedUIElement(tag="mock1"),
                    MockedUIElement(tag="mock2"),
                    MockedUIElement(tag="mock3"),
                    MockedUIElement(tag="mock2"),
                    MockedUIElement(tag="mock4")]
        self.ui_manager.extend_elements(elements)
        self.ui_manager.pop_element("mock2")
        self.ui_manager.draw_handler(0, 0)
        self.ui_manager.pop_element("mock3")
        self.ui_manager.draw_handler(0, 0)
        self.assertEqual([element.called for element in elements], [2, 0, 1, 0, 2])

    def test_click_handler(self):
        """
        Should see that mock2 was clicked on. mock3 was not under the mouse, and mock1 is under mock2, so should not
        have priority.
        """
        elements = [MockedUIElement(tag="mock1"),
                    MockedUIElement(tag="mock2"),
                    MockedUIElement(tag="mock3")]
        elements[0].clickable = True
        elements[1].clickable = True
        elements[2].clickable = True
        elements[0].is_over = True
        elements[1].is_over = True
        self.ui_manager.extend_elements(elements)
        self.assertEqual("mock2", self.ui_manager.click_handler(0, 0))



