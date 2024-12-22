from ContainerControl import ContainerControl

class Group(ContainerControl):
	def __init__(self,window,name=None,father=None,event_enable=True,visible=True,disable=True,move=None,common=None,every_frame_function=None):
		super().__init__(every_frame_function=every_frame_function,window=window,event_enable=event_enable,visible=visible,disable=disable)
		#self.father=father
		if father:
			if name:
				father.add(self,name)
			else:
				father.add(self)
		self.rect=None
		self.layout_init(move,common)

	def blit(self):
		if self.visible and self.disable:
			#print(self.member)
			#1/0
			super().blit()
			
	def check(self,event=None):
		if self.event_enable and self.disable:
			super().check(event)

	def stop_all(self):
		for i in self.keys():
			try:
				i.stop()
			except AttributeError:
				pass

	def start_all(self):
		for i in self.keys():
			try:
				i.do()
			except AttributeError:
				pass

	def add(self,member,name=None,auto_give_name=True):
		ob_rect=getattr(member,'rect',None)
		if not ob_rect is None:
			try:
				self.rect.union_ip(ob_rect)
			except AttributeError:
				#可能存在指向同一变量
				self.rect=ob_rect.copy()
		super().add(member,name,auto_give_name)
		
	def move(self,x=0,y=0):
		if x or y:
			for i in self.values():
				try:
					i.move(x,y)
				except AttributeError:
					pass
	
#	def set_common(self,*args,**kargs):
	def set_common(self,*args,aim_object=None,object=None):
		'''
		:top
		:bottom
		:center
		:centerx
		:centery
		:right
		:left
		
		'''
		#确定父rect
		if not object:
			object=self.window_rect
		#确定子rect
		if not aim_object:
			aim_object=self.rect
		
		center0=tuple(object.center)
		for i in args:
			setattr(aim_object,i,getattr(object,i))
		center1=tuple(object.center)
		offset=(center1[0]-center0[0],center1[1]-center0[1])
		
		self.move(*offset)
		
		self.update_rect()
		
			