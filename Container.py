#from my_tool import Control
import inspect

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

#	def update(self,*args,**kargs):
#		for i in self.member.values():
#			i.update(*args,**kargs)

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
		
	

if __name__=='__main__':
	pass
	#a=ContainerControl()
	
	
#	a=Container()
#	print(id(a))
#	a.add(Container(),1)
#	b=MemberVisitor(a)
#	for i in b:
#		print(i)
#	print(dict(b))
#	b[1]=a
#	c=Container()
#	b[1]=c
#	print(id(c))
#	print(id(b.father.member[1]))
#	print(b.father.member_name_sort)
#	print(i for i in b)
#	if 1 in b:
#		print(1)


