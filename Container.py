import pygame
class Container():
	def __init__(self,every_frame_function=None):
		self.member_name_sort=[]
		self.member={}
		self.auto_name=0
		self.bind(every_frame_function)
		
	def __getitem__(self,key):
		return self.member[key]

	def __setitem__(self,key,value):
		auto_give_name=False
		if not key:
			auto_give_name=True
		self.add(value,auto_give_name,key)

	def add(self,object,name=None,auto_give_name=True):
#		if name!=None:
#			self.member_name_sort.append(name)
		
		if (name is None) and auto_give_name:
			name=self.auto_give_name()
		
		self.member_name_sort.append(name)
		self.member[name]=object
		object.father=self
		object.name=name

		return name

	def remove(self,name):
		del self.member[name]
		self.member_name_sort.remove(name)

	def auto_give_name(self):
		member_keys=self.member.keys()
		self.auto_name+=1
		while True:
			if not self.auto_name in member_keys:
				return self.auto_name
			self.auto_name+=1

	def change_start_status(self,status=True):
		for item in self.member:
			item.start=status

	def change_visible_status(self,status=True):
		for item in self.member:
			item.visible=status

	def change_event_enable_status(self,status=True):
		for item in self.member:
			item.event_enable=status

	def __iter__(self):
		return self.member.__iter__()

	def blit(self):
		for name in self.member_name_sort[::-1]:
			self.member[name].blit()

	def check(self,event):
		#print(event)
		for item in self.member.values():
			item.check(event)
			
	def frame_update(self):
		for item in self.member.values():
			item.frame_update()
		if self.every_frame_function:self.every_frame_function(self)

	def get_members_name(self):
		return self.member.keys()

	def get_members(self):
		return self.member

#	def update(self,*args,**kargs):
#		for i in self.member.values():
#			i.update(*args,**kargs)

	def bind(self,func=None):
		self.every_frame_function=func
