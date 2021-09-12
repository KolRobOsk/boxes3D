import os, sys
from functions_test import algorithm_check

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from mainalgo import *
import unittest
from functions_test import *
from random import randint
from cut_box import *

class algorithm_test(unittest.TestCase):
    def copy_box_list(self, list):
        copy_list = []
        for i in list:
            copy_list.append(i)
        return copy_list

    def test_funkcji_algorytm(self):
        table = []
        ile_pudelek = randint(199, 200)
        for j in range(ile_pudelek):
            table.append(box3D.random())
        table_copy = self.copy_box_list(table)
        stack = boxStack()
        stack.extend(table)
        drzewo = tree()
        algorithm().algorytm(stack, drzewo)
        self.assertEqual(True, algorithm_check().evaluate(table_copy, drzewo.ret_boxes(), 10000))

if __name__ == '__main__':
    unittest.main()

