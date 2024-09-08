import Button
import my_tool
import pygame
import Page

window=pygame.display.set_mode((100,100))
window.fill((255,255,255))
a=Page.Page(window)
a.add(Button.Button(window,(10,10,200,100),association_key_event=[pygame.K_1],callback_function=lambda :1/0))

a.run()



