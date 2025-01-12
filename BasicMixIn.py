import inspect


class BasicControlMixIn():
	def check(self,event):
		pass
	def blit(self):
		pass
	def frame_update(self):
		pass



class Control(BasicControlMixIn):
	
	def __init__(self,window=None,event_enable=True,visible=True,disable=False):
		
		self.window_rect=window.get_rect()
		self.window=window
		self.event_enable=event_enable
		self.visible=visible
		self.disable=disable
	
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
		
		if not object:
			object=self.window_rect
		if not aim_object:
			aim_object=self.rect
		for i in args:
			setattr(aim_object,i,getattr(object,i))
		self.update_rect()
	def update_rect(self):
		pass
	
	def update(self,**kargs):
		for name,value in kargs.items():
			setattr(self,name,value)
		self.update_rect()
    


	def move(self,x=0,y=0):
		'''
		将控件向左移动x，向右移动y
		正为顺方向，负为逆方向
		参数：
		:x
		:y
		
		'''
		
		self.rect.x+= x
		self.rect.y+=y
		self.update_rect()

	def change_status(self,status=None):
		'''这是改变开启状态的方法'''
		if status==None:
			self.disable=not self.disable
		else:
			self.disable=status
			
	def layout_init(self,common=None,move=None):
		if not common is None:
			self.set_common(*common)
		if not move is None:
			self.move(*move)
			




class Container():
	def __init__(self,every_frame_function=None):
		self.member_name_sort=[]
		self.members={}
		self.auto_name=0
		self.bind(every_frame_function)
		
	def __contains__(self,item):
		return item in self.members.keys()
		
	def keys(self):
		return self.member_name_sort
	
	def items(self):
		return (((name,self.members[name]) for name in self.keys()))
		
	def values(self):
		return (self.members[name] for name in self.keys() )
	
	
	def __getitem__(self,key):
		return self.members[key]

	def __setitem__(self,key,value):
		auto_give_name=False
		if not key:
			auto_give_name=True
		self.add(value,auto_give_name,key)

	def add(self,member,name=None,auto_give_name=True):
#		if name!=None:
#			self.member_name_sort.append(name)
		
		if (name is None) and auto_give_name:
			name=self.auto_give_name()
			
		if not name in self:
			member.father=self
			member.name=name
			self.member_name_sort.append(name)

		self.members[name]=member


		return name

	def remove(self,name):
		del self.members[name]
		self.member_name_sort.remove(name)

	def auto_give_name(self):
		member_keys=self.members.keys()
		self.auto_name+=1
		while True:
			if not self.auto_name in member_keys:
				return self.auto_name
			self.auto_name+=1

	def change_start_status(self,status=True):
		for item in self.members:
			item.start=status

	def change_visible_status(self,status=True):
		for item in self.members:
			item.visible=status

	def change_event_enable_status(self,status=True):
		for item in self.members:
			item.event_enable=status

	def __iter__(self):
		return ((name,member) for name,member in self.members.values())

	def blit(self):
		for name in reversed(self.member_name_sort):
			self.members[name].blit()

	def check(self,event):
		#print(event)
		for item in self.members.values():
			item.check(event)
			
	def frame_update(self):
		for item in self.members.values():
			item.frame_update()
		if self.every_frame_function:self.every_frame_function(self)

	def get_members_name(self):
		return self.members.keys()

	def get_members(self):
		return self.members

	def bind(self,func=None):
		self.every_frame_function=func
	
	def get_MemberVisitor(self):
		return MemberVisitor(self)


class MemberVisitor():
	def __init__(self,father:Container):
		self.father=father
	
	def __getitem__(self,key):
		return self.father[key]
	
	def __setitem__(self,key,value):
		self.father.add(value,key)
	
	def __delitem__(self,key):
		self.father.remove(key)
		
	def __len__(self):
		return len(self.father.members)
		
	def __iter__(self):
		return ((name,member) for name,member in self.father.members.items())
		
	def __contains__(self,item):
		return item in self.father
		
	
class ContainerControl(Container,Control):
	#def __init__(self,window=None,event_enable=True,visible=True,disable=False,every_frame_function=None):
	def __init__(self,**kargs):
		control_paras=inspect.signature(Control.__init__).parameters
		container_paras=inspect.signature(Container.__init__).parameters
		
		para_to_Control={name:value for name,value in kargs.items() if name in control_paras }
		para_to_Container={name:value for name,value in kargs.items() if name in container_paras }
		
		Control.__init__(self,**para_to_Control)
		Container.__init__(self,**para_to_Container)



if __name__=='__main__':
	ContainerControl()
