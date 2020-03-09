# -*- coding: utf-8 -*-
import unittest
from pythaiair import Air
class TestUM(unittest.TestCase):
    def test_get_data(self):
        self.assertIsNotNone(Air().get_data())
