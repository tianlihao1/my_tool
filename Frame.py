from Container import *
import pygame
from Group import Group

class Frame(Group):
	def __init__(self,window,has_bg=True,bgcolor=(255,255,255), bg_image=None, is_image_scale=True,name=None,father=None,visible=True,start=True,move=None,common=None,every_frame_function=None):
		super().__init__(window=window,name=name,father=father,visible=visible,start=start,move=move,common=common,every_frame_function=every_frame_function)
		#self.window=window
		#self.window_rect=self.window.get_rect()
		
#		if father:
#			if name:
#				father.add(self,name)
#			else:
#				father.add(self)
#		self.rect=None
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
		#self.visible=visible
		#self.start=start
		#self.layout_init(move,common)

	def blit(self):
		if self.visible:
			#print(self.member)
			#1/0
			if self.has_bg_sign:
				self.window.blit(self.bg_surface,(0,0))
			super().blit()
			

#	def add(self,object,name=None,auto_give_name=True):
#		ob_rect=getattr(object,'rect',None)
#		if not ob_rect is None:
#			try:
#				self.rect.union_ip(ob_rect)
#			except AttributeError:
#				self.rect=ob_rect.copy()
#		super().add(object,name,auto_give_name)
#		
	#def move(self,x=0,y=0):
#		if x or y:
#			for i in self.member.values():
#				try:
#					i.move(x,y)
#				except AttributeError:
#					pass
#	
#	def set_common(self,*args,**kargs):
#	def set_common(self,*args,aim_object=None,object=None):
#		'''
#		:top
#		:bottom
#		:center
#		:centerx
#		:centery
#		:right
#		:left
#		
#		'''
#		#确定父rect
#		if not object:
#			object=self.window_rect
#		#确定子rect
#		if not aim_object:
#			aim_object=self.rect
#		
#		center0=tuple(object.center)
#		for i in args:
#			setattr(aim_object,i,getattr(object,i))
#		center1=tuple(object.center)
#		offset=(center1[0]-center0[0],center1[1]-center0[1])
#		
#		self.move(*offset)
#		
#		self.update_rect()
		
#	def update_rect(self):
#		pass


#	def layout_init(self,common=None,move=None):
#		if not common is None:
#			self.set_common(*common)
#		if not move is None:
#			self.move(*move)

	
#	def change_status(self,status=None):
#		'''这是改变开启状态的方法'''
#		if status==None:
#			self.start=not self.start
#		else:
#			self.start=status
#			