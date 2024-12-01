from Container import *

import pygame

class Page(Container):
	def __init__(self,window,has_bg=True,bgcolor=(255,255,255), bg_image=None, is_image_scale=True,name=None,father=None,every_frame_function=None):
		super().__init__()
		self.window=window
		self.window_rect=self.window.get_rect()
		#self.father=father
		if father:
			if name:
				father.add(self,name)
			else:
				father.add(self)
		else:
			self.father=None
		self.has_bg_sign=has_bg
		self.bgcolor=bgcolor
		self.bg_surface=pygame.surface.Surface(self.window_rect.size)
		if bg_image:
			self.bg_image=pygame.image.load(bg_image).convert()
			if is_image_scale:
				self.bg_image=pygame.transform.scale(self.bg_image, self.window_rect.size)
			self.bg_surface.blit(self.bg_image,(0,0))
		else:
			self.bg_surface.fill(self.bgcolor)
		self.bind(every_frame_function)

	def blit(self):
		if self.has_bg_sign:
			self.window.blit(self.bg_surface,(0,0))
		super().blit()
	
	def bind(self,func=None):
		self.every_frame_function=func

	def update(self):
		pass

	def stop_page(self,page_name):
		pass

	def start_page(self,page_name):
		pass
		
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					exit()
				else:

					self.check(event)
			if self.every_frame_function:self.every_frame_function(self)
			#if pygame.key.get_pressed()[pygame.K_1]: print(10)
			self.blit()
			pygame.display.update()
