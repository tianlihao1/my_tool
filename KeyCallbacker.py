from BasicMixIn import BasicControlMixIn
import pygame


class KeyCallbacker(BasicControlMixIn):
	def __init__(self,it):
		self.key_bind_dict={}
		self.bind_from(it)
	
	def bind(self,key_value,func,up_trigger):
		self.key_bind_dict[(key_value,up_trigger)]=func
		
	def bind_from(self,it):
		for i in it:
			self.bind(*i)
	
	def cancel(self,key_value,up_trigger=None):
		if up_trigger is None:
			self.key_bind_dict.pop((key_value,True),None)
			self.key_bind_dict.pop((key_value,False),None)
			return
		self.key_bind_dict.pop((key_value,up_trigger),None)
		
	def clear(self):
		self.key_bind_dict.clear()
		
	def __getitem__(self,key):
		return self.key_bind_dict[key]
	
	def check(self,event):
		if event.type==pygame.KEYDOWN:
			try:self[(event.key,False)]()
			except KeyError:pass
		elif event.type==pygame.KEYUP:
			try:self[(event.key,True)]()
			except KeyError:pass
		
		
		




