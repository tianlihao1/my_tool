from Container import *
import pygame

class Frame(Container):
	def __init__(self,window,has_bg=True,bgcolor=(255,255,255), bg_image=None, is_image_scale=True,name=None,father=None):
		super().__init__()
		self.window=window
		self.window_rect=self.window.get_rect()
		#self.father=father
		if father:
			if name:
				father.add(self,name)
			else:
				father.add(self)
		self.rect=None
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

	def blit(self):
		if self.has_bg_sign:
			self.window.blit(self.bg_surface,(0,0))
		super().blit()

	def update(self):
		pass

	def stop(self):
		for i in self.member.keys():
			try:
				i.stop()
			except AttributeError:
				pass

	def start(self):#要改
		for i in self.member.keys():
			try:
				i.do()
			except AttributeError:
				pass

	def add(self,object,name=None,auto_give_name=True):
		ob_rect=getattr(object,'rect',None)
		if not ob_rect is None:
			try:
				self.rect.union_ip(ob_rect)
			except AttributeError:
				self.rect=ob_rect.copy()
		self.add(object,name,auto_give_name)
		
	def move(self,x=0,y=0):
		if x or y:
			for i in self.member.values():
				i.move(x,y)
	
#	def set_common(self,*args,**kargs):
		