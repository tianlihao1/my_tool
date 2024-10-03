import my_tool
from Page import Page
import pygame

window=pygame.display.set_mode((1000,500))
page=Page(window)
page.add(my_tool.Dice_Group(window,(0,0,100,200),[2]))
page.run()