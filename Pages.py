import pygame
#import Page
#from Page import Page
from BasicMixIn import Container


#需要修改member逻辑
class Pages(Container):
	def __init__(self,window):
		super().__init__()
		self.window=window
		self.now_page_index=0
		#self.now_page=self.member[self.member_name_sort [self.now_page_index]]
		self.now_page=None
		self.remain_previous_bg_sign=False
		self.previous_bg=None
		self.change_page_event_dict={}
		self.message={}

	def next(self,son_sign=False,remain_previous_bg=False):
		if son_sign:
			self.next_to(self.now_page.next,remain_previous_bg)
		else:
			self.now_page_index+=1
			self.next_to(self.member_name_sort[self.now_page_index], remain_previous_bg)


	def next_to(self,name,remain_previous_bg=False):
#这里需要修改
		#print(self.member)
		self.now_page.stop_page(self.members[name])
		#self.remain_previous_bg=remain_previous_bg
		if (not self.remain_previous_bg_sign) and remain_previous_bg:
			self.previous_bg= pygame.surface.Surface(self.window.get_size())
			self.previous_bg.blit(self.window,(0,0))
		elif not self.remain_previous_bg_sign:
			self.remain_previous_bg_sign=False
		self.now_page_index=self.member_name_sort.index(id)
		previous_page_name=self.now_page.name
		self.now_page=self.members[name]
		self.now_page.start_page(previous_page_name)

	def blit(self):
		if self.remain_previous_bg_sign:
			self.window.blit(self.previous_bg,(0,0))
		self.now_page.blit()

	def add(self,member,name=None,auto_give_name=True):
		if not self.now_page:
			self.now_page=member
		#object.father=self
		name=super().add(member,name,auto_give_name)
		#print(name)
		#1/0
		#object.name=name
		self.change_page_event_dict[name]=[]

	def add_change_page_event(self,page,func,next_page):
		#print(object.name,type(object.name))
		
		if self.change_page_event_dict.get(page.name,None) ==None:
			self.change_page_event_dict[page.name]=[]
		
		self.change_page_event_dict[page.name].append((func,next_page))


	def check(self,event):
		super().check(event)
		#print(self.change_page_event_dict)
		#print(self.now_page.name)
		#print(self.now_page.name,type(self.now_page.name))
		for func,next_page in self.change_page_event_dict[self.now_page.name]:
			if func():
				self.next_to(next_page)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					exit()
				else:
					self.check(event)
			self.frame_update()
			self.blit()
			pygame.display.update()