import sys
import os
sys.path.append(os.path.split(os.getcwd())[0])
print(os.path.split(os.getcwd()))

import Page
import my_tool
import pygame

window=pygame.display.set_mode((700,700))
pa=Page.Page(window)

pa.add(my_tool.Text(window,'hh',(0,0)))
Pb=pa.as_model()
pb=Pb(window)
pb.run()






