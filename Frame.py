from BasicMixIn import ContainerControl
import pygame


class Frame(ContainerControl):
	def __init__(self,window,rect,bgcolor=(255,255,255), bg_image=None, is_image_scale=True,visible=True,disable=True,move=None,common=None,every_frame_function=None):
		
		super().__init__(window=window,visible=visible,every_frame_function=every_frame_function,disable=disable)
		#self.window=window
		#self.window_rect=self.window.get_rect()
		
#		if father:
#			if name:
#				father.add(self,name)
#			else:
#				father.add(self)
		self.rect=pygame.rect.Rect(rect)
		#self.has_bg_sign=has_bg
		self.bgcolor=bgcolor
		self.bg_surface=pygame.surface.Surface(self.rect.size)
		self.frame_surface=pygame.surface.Surface(self.rect.size)
		
		
		if bg_image:
			bg_image=pygame.image.load(bg_image).convert()
			if is_image_scale:
				bg_image=pygame.transform.scale(bg_image, self.rect.size)
			else:
				self.rect.size=bg_image.get_size()
				self.bg_surface=pygame.surface.Surface(self.rect.size)
				self.frame_surface=pygame.surface.Surface(self.rect.size)
			self.bg_surface.blit(bg_image,(0,0))
		else:
			self.bg_surface.fill(self.bgcolor)
			
		#self.visible=visible
		#self.start=start
		self.layout_init(move,common)

	def blit(self):
		if self.visible:
			self.frame_surface.blit(self.bg_surface,(0,0))
			for member in self.values():
				member.blit()
			self.window.blit(self.frame_surface,self.rect)
			
	

	def add(self,member,name=None,auto_give_name=True):
		member.window=self.frame_surface
		member.window_rect=self.rect
		
