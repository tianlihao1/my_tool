import inspect
from my_tool import Control
from Container import Container

class ContainerControl(Container,Control):
	def __init__(self,window=None,event_enable=True,visible=True,disable=False,every_frame_function=None):
		Container.__init__(self,every_frame_function=every_frame_function)
		Control.__init__(self,window=window,event_enable=event_enable,visible=visible,disable=disable)
		

#print(ContainerControl.__mro__)


