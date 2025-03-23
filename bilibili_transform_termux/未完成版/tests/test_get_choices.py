import unittest
from bilibili_transform.bilibili_transform import solve_choose_add_mode as get_choices,solve_section_mode
from functools import namedtuple

class Test(unittest.TestCase):
	def test_func_get_choices(self):
		DigitalClass=namedtuple('c1','choose')
		command=['1','2+3','1(2:00,13:00)+2(,3:00)+3(2:00,)+6+7(3:00)']
		result_list=[[['1', '', '']], [['2', '', ''], ['3', '', '']], [['1', '2:00', '13:00'], ['2', '', '3:00'], ['3', '2:00', ''], ['6', '', ''], ['7', '3:00', '']]]
		self.assertEqual(get_choices(command),result_list)
		
		
		command=['1','2(1:00)','3','+']
		result_list=[['1', '', ''], ['2', '1:00', ''], ['3', '', '']]
		self.assertEqual(get_choices(command),result_list)
		
		
	def test_solve_section_mode(self):
		result=[[[1, '', ''], [2, '', ''], [3, '', ''], [4, '', ''], [5, '', ''], [6, '', '']], [[1, '1:00', ''], [2, '1:00', ''], [3, '1:00', ''], [4, '1:00', ''], [5, '1:00', ''], [6, '1:00', '']]]
		self.assertEqual(solve_section_mode([[['16','',''],['1-6','','']],[['1-6','1:00','']]])
,result)
		