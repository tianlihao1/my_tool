import CButton
import my_tool
import pygame
import Page
import Button

window=pygame.display.set_mode((500,500))
window.fill((255,255,255))
a=Page.Page(window)
a.add(Cutton.Button(window,(10,10,200,100),association_key_event=[pygame.K_1],callback_function=lambda :print(1)))
#print(pygame.key.get_pressed()[pygame.K_a])
#breakpoint()
a.run()



