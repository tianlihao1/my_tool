import my_tool
import pygame
import Page


window=pygame.display.set_mode((800,800))
window.fill((255,255,255))
a=Page.Page(window)
a.add(my_tool.OutputBox(window))
#print(pygame.key.get_pressed()[pygame.K_a])
#breakpoint()
a.run()
