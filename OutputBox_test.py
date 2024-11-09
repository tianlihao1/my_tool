import my_tool
import pygame
import Page

def print_info(self):
    print(self[1].get_exact_value(),self[1].extent,self[1].value)
window=pygame.display.set_mode((800,800))
window.fill((255,255,255))
a=Page.Page(window,every_frame_function=print_info)
# a.add(my_tool.OutputBox(window))
a.add(my_tool.ScrollBar(window,(0,0,30,200),(0,10),0.1))
# a[1].add('ajsdassssssssssssssssssssssssssssssss')
# a[1].scrollbar.stick_height=1
# a[1].scrollbar.update_layout_rect()

#print(pygame.key.get_pressed()[pygame.K_a])
#breakpoint()
a.run()
