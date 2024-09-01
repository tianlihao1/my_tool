import time
import pygame
import os
import random
import math

pygame.init()
#print(os.path.split(os.getcwd()))

DEFAULT_RES_PATH=os.path.join(os.path.dirname(os.path.realpath(__file__)),'res')

DEFAULT_FONT_PATH=os.path.join(DEFAULT_RES_PATH,'font','SourceHanSerifCN','Regular.otf')

DEFAULT_PIC_PATH=os.path.join(DEFAULT_RES_PATH,'pic')

#print(DEFAULT_FONT_PATH)

def round(value,precision):
	value=value/precision
	int_value=int(value)
	mid_values=int_value+0.5
	if value>=mid_values:
		value=(int_value+1)*precision
	else:
		value=(int_value)*precision
	return value


def floor(value,precision):
	value /=precision
	value=int(value)
	return value*precision





class Control():
	
	def __init__(self,window=None,event_enable=True,visible=True,start=True):
		
		self.window_rect=window.get_rect()
		self.window=window
		self.event_enable=event_enable
		self.visible=visible
		self.start=start
	
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
			self.start=not self.start
		else:
			self.start=status
			
	def layout_init(self,common=None,move=None):
		if not common is None:
			self.set_common(*common)
		if not move is None:
			self.move(*move)
			
	def check(self,event):
		pass
	
	def blit(self):
		pass

class Button(Control):
	'''
	用途：
		在界面上创建一个按钮，点击会有点击反馈，当按钮弹起是返回False，否则返回True
		
		
	属性：
		window：	按钮显示在的Surface对象
		window_rect:按钮显示的是Surface对象的Rect对象
		rect：		   按钮的坐标和大小（按钮的rect对象）
		title：		   按钮上的文字,默认为'按钮'
		font:			 按钮文字字体文件路径
		bg_color:	   按钮当前颜色
		text_color:	   按钮字体的颜色
		font_size：	 按钮字体的大小，默认为None
		start:			 按钮的启用状态
		down：		按钮是否按下
	'''
	def __init__(self,window,rect,text='按钮',font=DEFAULT_FONT_PATH,bg_color=(0,0,0),image=None,text_color=(255,255,255),font_size=None,covering_color=(255,255,255),event_enable=True,visible=True,start=True):
		
		super().__init__(window,event_enable,visible,start)

		#按钮矩形空间
		self.rect=pygame.Rect(rect)

		#按钮文字
		self.text=text

		#按钮颜色
		self.bg_color=bg_color
		
		self.up_bgcolor=bg_color

		#按钮图片
		self.image=None
		if image:
			self.image=pygame.transform.scale(image,self.rect.size)


		#文本颜色
		self.text_color=text_color

		#字体
		self.font=font

		#字号
		if not font_size:
			self.font_size=int(self.rect.width/(1.45*len(self.text)))
		else:
			self.font_size=font_size

		#字体对象
		self.font_tool=pygame.font.Font(self.font,self.font_size)

		#是否被按下
		self.down=False

		#是否启用
		self.start=start
		
		#遮盖层
		self.covering_rect=pygame.Surface(self.rect.size)
		self.covering_rect.set_alpha(200)
		self.covering_rect.fill(covering_color)
		
		

	def blit(self):
		#判断是否启用
		if self.start and self.visible:
			#基本图形绘制
			if self.image:
				self.window.blit(self.image,self.rect)
			else:
				pygame.draw.rect(self.window,self.bg_color,self.rect)
			
			#点击时覆盖层绘制
			if self.down:
				self.window.blit(self.covering_rect,self.rect)
			
			#按钮文本绘制
			font=self.font_tool.render(self.text,True,self.text_color)
			font_rect=font.get_rect()
			font_rect.center=self.rect.center
		#	font_rect.centerx=self.rect.centerx
		#	font_rect.centery=self.rect.centery
			self.window.blit(font,font_rect)

	def check(self,event):

		#按钮事件
		sign=False

		#判断按钮是否禁用
		if self.start and self.event_enable and event.type in [pygame.MOUSEBUTTONUP , pygame.MOUSEBUTTONDOWN , pygame.MOUSEMOTION]:
			#检测鼠标回弹
			if self.down==True and event.type==pygame.MOUSEBUTTONUP:
				self.down=False
				sign=True
			#）检测鼠标按下按钮
			elif self.rect.collidepoint(event.pos):
				if event.type==pygame.MOUSEBUTTONDOWN:
					self.down=True
		if self.event_enable:
			return sign
	
	def ispress(self):
		if self.event_enable:
			return self.down
		return None
	



class Radio_Member(Control):
	def __init__(self,window,key,rect,text=None,font=DEFAULT_FONT_PATH,text_color=(0,0,0),bg_color=None,up=None,down=None,status=False,event_enable=True,visible=True,start=True):
		self.key=key
		
		super().__init__(window,event_enable,visible,start)
		

		self.rect=pygame.rect.Rect(rect)

		self.text=text

		self.font_size=int(self.rect.height/1.45)

		self.font=pygame.font.Font(font,self.font_size)

		self.text_color=text_color

		self.bg_color=bg_color

		self.focus=False

		if not down:
			down=self.font.render('●',True,(0,0,0))
			self.rect.width=down.get_size()[0]
		else:
			down=pygame.transform.scale(down,self.rect)
		#图片功能待完善
		if not up:
		
			up=self.font.render('○',True,(0,0,0))
			self.rect.width=up.get_size()[0]
		else:
			up=pygame.transform.scale(down,self.rect)

		self.image={True:down,False:up}

		self.all_rect=self.rect

		self.status=status

	def blit(self):
		if self.start and self.visible:
			self.window.blit(self.image[self.status],self.rect)
			text_image=self.font.render(self.text,True,self.text_color,self.bg_color)
			self.window.blit(text_image,(self.rect.right+10,self.rect.y))
			self.all_rect=self.rect.copy()
			self.all_rect.width=self.rect.width+text_image.get_width()+10
			if self.focus:
				pygame.draw.rect(self.window,(0,0,0),self.all_rect,1)
	


class Radio():
	def __init__(self,window,group_id,choose_one=True,event_enable=True,visible=True,start=True):

		self.window=window

		self.group_id=group_id

		self.member={}

		self.member_status={}

		self.choose_one=choose_one
		
		self.event_enable=event_enable

		self.start=start
		
		self.visible=visible

	def __getitem__(self, index):  # 1).索引值的获取
		return self.member[index]

	def creat(self,*args,**kargs):
		'''
		参数：
			:key,
			:rect,
			:text=None,
			:font='./res/font/SourceHanSerifCN/Regular.otf',
			:text_color=(0,0,0),
			:bg_color=None,
			:up=None,
			:down=None,
			:start=True


		'''

		member=Radio_Member(self.window,*args,**kargs)
		self.member[member.key]=member
		self.member_status[member.key]=member.status

	def set_layout(self,rect,layout,y_interval=0,x_interval=30):
		'''
		:rect	表示第1个Radio_Member的rect
		:layout	布局接受一个列表，列表的项表示列，列表项的值，表示该列的函数。如：[2,3]表示，有两列，第1列有两行，第二列有三行
		:y_interval	行间
		:x_interval	列间
		'''
		#[2,3]
		self.layout=[(l,j) for l , h_num in enumerate(layout) for j in range(h_num)]
		self.rect=pygame.rect.Rect(rect)
		self.x_interval=x_interval
		self.y_interval=y_interval
		
		


	def layout_creat(self,*args,**kargs):
		
		x=self.rect.x+self.layout[0][0]*self.x_interval
		y=self.rect.y+self.layout[0][1]*self.y_interval+self.layout[0][1]*self.rect.height
		rect=pygame.rect.Rect(x,y,*self.rect.size)
		self.creat(rect=rect,key=self.layout[0],**kargs)
		
		del self.layout[0]

	def blit(self):
		if self.start and self.visible:
			for values in self.member.values():
				values.blit()

	def check(self,event):
		if self.start and event.type in [pygame.MOUSEBUTTONUP , pygame.MOUSEBUTTONDOWN , pygame.MOUSEMOTION] and self.event_enable:
			for values in self.member.values():
				if values.all_rect.collidepoint(event.pos) and values.start and values.event_enable:
					values.focus=True
					if event.type==pygame.MOUSEBUTTONUP:
						if self.choose_one:
							for i in self.member_status.keys():

								self.member_status[i]=False
								self.member[i].status=False
						values.status=not values.status
						self.member_status[values.key]=not self.member_status[values.key]
						
						return True

				else:
					values.focus=False
		return False



	def get_stuats(self):
		return self.member_status
	
	def get_choices(self):
		choices=[]
		for i in self.member_status.keys():
			if self.member_status[i]:
				choices.append(i)
		return choices

	def move(self,x=0,y=0):
		for i in self.member.values():
			i.move(x,y)

	def reset_status(self):
		for value in self.member.values():
			value.status=False
		self.member_status.update(dict.fromkeys(self.member_status.keys(),False))

	def remove(self,key):
		del self.member[key]
		del self.member_status[key]
		
class Text(Control):
	def __init__(self,window,text,site,font=DEFAULT_FONT_PATH,font_size=30,text_color=(0,0,0),bg_color=None,has_box=False,has_mouse_inside_box=False,box_color=None,common=None,move=None,start=True):
		super().__init__(window)
		self.window=window

		self.window_rect=self.window.get_rect()

		self.font_size=font_size

		self.text=text

		self.font=pygame.font.Font(font,self.font_size)

		self.text_color=text_color

		self.bg_color=bg_color
		
		self.has_box=has_box

		self.has_mouse_inside_box=has_mouse_inside_box

		if not box_color:
			box_color=self.text_color
		self.box_color = box_color

		self.start=start

		self.mouse_inside=False

		self.text_image=self.font.render(self.text,True,self.text_color,self.bg_color)
		self.rect=self.text_image.get_rect()
		self.rect.x,self.rect.y=site
		
		self.layout_init(common,move)
		
		
	def blit(self):
		if self.start:
			#text=self.font.render(self.text,True,self.text_color,self.bg_color)
			self.window.blit(self.text_image,self.rect)
			
			if (self.mouse_inside and self.has_mouse_inside_box) or self.has_box:
				pygame.draw.rect(self.window,self.box_color,self.rect,width=1)

	def check(self , event):
		if self.start and self.event_enable:
			
			if event.type==pygame.MOUSEMOTION and self.rect.collidepoint(event.pos):
				self.mouse_inside = True
				if event.type == pygame.MOUSEBUTTONDOWN:
					return True
			else:
				self.mouse_inside=False
			return False
			
	def update(self, **kargs):
		super().update(**kargs)
		self.text_image=self.font.render(self.text,True,self.text_color,self.bg_color)
		self.rect.size=self.text_image.get_size()
		
		
		
class TimingBar(Control):
	''' 计时条 '''
	def __init__(self,window,rect,totime,barcolor=(0,0,0),has_box_sign=True,boxcolor=(200,200,200),boxwidth=0,backflow=True,visible=True,start=True):
		
		super().__init__(window=window,start=start,visible=visible)
		
		self.rect=pygame.rect.Rect(rect)
		
		#计时条流动完所需的时间
		self.totime=totime
		
		#用来刻画时间间隔
		self.startime=0
		self.endtime=0
		
		#执行状态，即是否正在计时
		self.__doing_sign=False
		#用来刻画该计时条是否已开始计时且己达到totime
		self.__over_sign=False
		
		#计时条的颜色
		self.barcolor=barcolor
		
		#计时条是否有底框
		self.has_box_sign=has_box_sign 
		#底框颜色
		self.boxcolor=boxcolor
		#底框宽度
		self.boxwidth=boxwidth
	
		#倒流,即计时条宽度随着时间的增加而减小
		self.backflow=backflow
	def blit(self):
		''' 绘制函数 '''
		if self.__doing_sign:
			self.endtime=time.time()
		
		#绘制底框
		if self.has_box_sign and self.visible:
			pygame.draw.rect(self.window,self.boxcolor,self.rect,self.boxwidth)
		
		#绘制计时条
		if self.totime >= (self.endtime - self.startime ):
			if self.visible:
				if self.backflow:
					pygame.draw.rect(self.window,self.barcolor,(self.rect.x,self.rect.y,self.rect.width*(self.totime-self.endtime+self.startime)/self.totime,self.rect.height))
				else:
					pygame.draw.rect(self.window,self.barcolor,(self.rect.x,self.rect.y,self.rect.width*(1-(self.totime-self.endtime+self.startime)/self.totime),self.rect.height))
					
				
		else:
			self.__over_sign=True
			self.__doing_sign=False
			if not self.backflow and self.visible:
				pygame.draw.rect(self.window,self.barcolor,self.rect)
		

	def do(self):
		'''使计时条开始计时'''
		if not self.isover():
			self.__doing_sign=True
			self.__over_sign=False
			self.startime=time.time()-self.endtime+self.startime
			if self.endtime<self.startime:
				self.endtime=self.startime
		
		
	def stop(self):
		''' 使计时条计时停止 '''
		self.__doing_sign=False
		
	def turn(self):
		''' 使计时条计时状态反转，即正在计时则变为停止计时，停止计时则变为正在计时 '''
		if self.__doing_sign:
			self.stop()
		else:
			self.do()
	
		
	def isover(self):
		'''返回是否计时且已完成'''
		return self.__over_sign
		
	def isdoing(self):
		'''返回是否正在计时'''
		return self.__doing_sign
	
		
	def reset(self):
		''' 使计时条恢复初始状态 '''
		self.startime=self.endtime=0
		self.__doing_sign=False
		self.__over_sign=False
		

	def reset_do(self):
		''' 使计时条重新计时 '''
		self.reset()
		self.do()

	def get_time(self):
		''' 返回开始计时后计时的时间 '''
		return self.endtime-self.startime
	
	def get_rest_time(self):
		'''返回开始计时后距离to time还剩的时间'''
		return self.totime-self.get_time()




	#使用pygame.time.Clock
class CTimingBar(Control):
#	num=0
	
	def __init__(self,window,rect,totime,barcolor=(0,0,0),has_box_sign=True,boxcolor=(200,200,200),boxwidth=0,backflow=True,visible=True,start=True):
 #	   super().__init__(window)
		self.clock=pygame.time.Clock()
#		self.totime=3*10**3
		self.nowtime=0
		
		super().__init__(window=window,start=start,visible=visible)
		
		self.rect=pygame.rect.Rect(rect)
		
		#计时条流动完所需的时间
		self.totime=totime
		
				#执行状态，即是否正在计时
		self.__doing_sign=False
		#用来刻画该计时条是否已开始计时且己达到totime
		self.__over_sign=False
		
		#计时条的颜色
		self.barcolor=barcolor
		
		#计时条是否有底框
		self.has_box_sign=has_box_sign 
		#底框颜色
		self.boxcolor=boxcolor
		#底框宽度
		self.boxwidth=boxwidth
	
		#倒流,即计时条宽度随着时间的增加而减小
		self.backflow=backflow
		
#		self.__doing_sign=False
#		self.__over_sign=False
#		self.t=0
		
#		self.rect=pygame.rect.Rect((30,300,200,10))
		
#		self.bgcolor=(200,200,200)
#		self.barcolor=(0,0,0)
		
#		self.backflow=backflow=True

	def do(self):
		if not self.__over_sign:
			self.clock.tick()
			self.__doing_sign=True
	
	def stop(self):
		self.__doing_sign=False

	def isover(self):
		return self.__over_sign
		
	def isdoing(self):
		return self.__doing_sign
		
	def reset(self):
		self.nowtime=0
		self.__doing_sign=False
		self.__over_sign=False
		
	def reset_do(self):
		self.reset()
		self.do()
		
	
	def turn(self):
		''' 使计时条计时状态反转，即正在计时则变为停止计时，停止计时则变为正在计时 '''
		if self.__doing_sign:
			self.stop()
		else:
			self.do()
		
	def get_time(self):
		return self.nowtime
		
	def get_rest_time(self):
		return self.totime-self.nowtime
		
	def blit(self):
		if self.__doing_sign:
		   
			self.nowtime+=self.clock.tick()
			if self.nowtime>=self.totime:
				self.stop()
				self.__over_sign=True
				
		if self.visible:
			#绘制底框
			if self.has_box_sign and self.visible:
				pygame.draw.rect(self.window,self.boxcolor,self.rect,self.boxwidth)
			#pygame.draw.rect(self.window,self.bgcolor,self.rect)
		 #   if self.nowtime>0:
			if not self.backflow:
				pygame.draw.rect(self.window,self.barcolor,(self.rect.x,self.rect.y,self.rect.width*self.nowtime/self.totime,self.rect.height))
			elif self.nowtime<=self.totime:
				pygame.draw.rect(self.window,self.barcolor,(self.rect.x,self.rect.y,self.rect.width*(1-self.nowtime/self.totime),self.rect.height))

class Timing():
	def __init__(self,aimtime,loops=1,callback_function=None):
		self.aimtime=aimtime
		self.loops=loops
		self.now_loop_num=1
		self.nowtime=0
		self.callback_function=callback_function
		self.clock=pygame.time.Clock()
		self.__doing_sign=False
		self.__over_sign=False
		
	def check(self,event=None):
		if self.__doing_sign and not self.__over_sign:
			self.nowtime+=self.clock.tick()
			
			if self.nowtime>self.aimtime:

				if self.now_loop_num<self.loops or self.loops==-1:
					self.nowtime=0
					self.now_loop_num+=1
					#return True
				else:
					self.__doing_sign=False
					self.__over_sign=True
				if self.callback_function:
					self.callback_function(self)
				return True
		return False
			
	def get_now_loop_num(self):
		return self.now_loop_num

	def get_rest_loop_num(self):
		return self.loops-self.get_now_loop_num()

	def do(self):
#		if not self.__over_sign:
		self.clock.tick()
		self.__doing_sign=True
	
	def stop(self):
		self.__doing_sign=False

	def isover(self):
		return self.__over_sign
		
	def isdoing(self):
		return self.__doing_sign
		
	def reset(self):
		self.nowtime=0
		self.now_loop_num=1
		self.__doing_sign=False
		self.__over_sign=False
		
	def reset_do(self):
		self.reset()
		self.do()

	def set_loops(self,loops):
		self.now_loop_num=1
		self.loops=loops
		
	def set_callback_function(self,function):
		self.callback_function=function

	def get_rest_time(self):
		return self.aimtime-self.nowtime

	def get_time(self):
		return self.nowtime

	def turn(self):
		''' 使计时条计时状态反转，即正在计时则变为停止计时，停止计时则变为正在计时 '''
		if self.__doing_sign:
			self.stop()
		else:
			self.do()

	def blit(self):
		pass

class ScrollBar(Control):
	''' 滚动条 '''
	def __init__(self,window,rect,extend,precision=1,stick_color=(0,0,0),bg_stick_color=(200,200,200),button_color=(255,255,255),bg_button_color=(100,100,100),event_able=True,start=True):
		super().__init__(window,event_enable=event_able,start=start)
		
		#整个滚动条的rect
		self.rect=pygame.rect.Rect(rect)
		
		#value的范围
		self.extend=extend
		
		#value的精度
		self.precision=precision
		
		self.value=self.extend[0]
		
		
		#更新对应的布局rect
		self.update_layout_rect()
		
		#按钮颜色
		self.button_color=button_color
		#按钮背景颜色
		self.bg_button_color=bg_button_color
		#滑动条颜色
		self.stick_color=stick_color
		#滑动条背景颜色
		self.bg_stick_color=bg_stick_color
		
		#上按钮标记
		self.__up_sign=False
		#下按钮标记
		self.__down_sign=False
		#滚动标记
		self.__move_sign=False
		
		#覆盖层Surface
		self.covering=pygame.surface.Surface(self.up_button_rect.size)
		self.covering.fill((255,255,255))
		self.covering.set_alpha(200)
		
		#圆角
		self.border_radius=int(min(self.stick_rect.width,self.stick_rect.height)/4)
	
	
	
	def update_layout_rect(self):
		
		#上按钮背景
		self.up_button_rect=pygame.rect.Rect(self.rect.x,self.rect.y,self.rect.width,self.rect.width)
		
		#下按钮背景
		self.down_button_rect=pygame.rect.Rect(self.rect.x,self.rect.bottom-self.rect.width,self.rect.width,self.rect.width)
		
		#滚动条背景
		self.bg_stick_rect=pygame.rect.Rect(self.rect.x,self.rect.y+self.rect.width,self.rect.width,self.rect.height-2*self.rect.width)
		
		#滚动条
		self.stick_rect=pygame.rect.Rect(self.rect.x,self.rect.y+self.rect.width+self.value_turn_y()-self.bg_stick_rect.top,self.rect.width,self.get_stick_height())
		
		#上按钮箭头点列表
		self.up_button_point_list=[(self.rect.x+self.rect.width/2,self.rect.y),(self.rect.x,self.rect.y+math.sqrt(3)*self.rect.width/2),(self.rect.x+self.rect.width,self.rect.y+math.sqrt(3)*self.rect.width/2)]
		
		#下按钮箭头点列表
		self.down_button_point_list=[(self.rect.x+self.rect.width/2,self.rect.bottom),(self.rect.x,self.rect.bottom-math.sqrt(3)*self.rect.width/2),(self.rect.x+self.rect.width,self.rect.bottom-math.sqrt(3)*self.rect.width/2)]
		

	def value_turn_y(self):
		''' 获得value对应的滚动条的y值 '''
		return (self.value-self.extend[0])*(self.bg_stick_rect.height-self.get_stick_height())/(self.extend[1]-self.extend[0]+1)+self.bg_stick_rect.top
		
	
	def get_stick_height(self):
		''' 获得滚动条的高 '''
		return int(self.bg_stick_rect.height/(self.extend[1]-self.extend[0]+1))
	
	
	def get_exact_value(self):
		''' 将滚动条的y转化成对应的value '''
		value= (self.stick_rect.y-self.bg_stick_rect.top)/(self.bg_stick_rect.height-self.stick_rect.height)*(self.extend[1]-self.extend[0]+1)+self.extend[0]
		if value > self.extend[1]:
			value=self.extend[1]
		
		return value
		
	def get_value(self):
		return self.value
		
	
	def set_value(self,value):
		''' 设置value '''
		
		#使value在范围内并赋值给self.value
		self.value=min(self.extend[1],max(self.extend[0],value))

		self.stick_rect.y=self.value_turn_y()

		
		
	def up(self):
		''' value向上一个精度,即value减一个精度 '''
		self.value-=self.precision
		self.set_value(self.value)
		
		
	def down(self):
		''' value向下一个精度,即value加一个精度 '''
		self.value+=self.precision
		self.set_value(self.value)
		
	def get_percentage(self):
		''' 获得value占整个范围的百分比 '''
		return (self.value-self.extend[0])/(self.extend[1]-self.extend[0])
	

	def move(self,x=0,y=0):
		super().move(x,y)
		self.update_layout_rect()
		
		
	def set_common(self,*args,**kargs):
		super().set_common(*args,**kargs)
		self.update_layout_rect()
	
	def update(self,**kargs):
		for name,value in kargs.items():
			if name in \
			[
				'start',
				'event_able',
				'extend',
				'precision',
				'bg_stick_color',
				'button_color',
				'bg_button_color',
				'stick_color',
				'window',
				'rect'
			]:
				setattr(self,name,value)
				

				if name=='extend':
					self.value=min(self.extend[1],max(self.extend[0],self.value))
				if name in \
				 ['window','rect','extend']:
					self.update_layout_rect()
			
	
		
	def blit(self):
		if self.start:
			#绘制上按钮背景
			pygame.draw.rect(self.window,self.bg_button_color,self.up_button_rect)
			#位置下按钮背景
			pygame.draw.rect(self.window,self.bg_button_color,self.down_button_rect)
			#绘制滚动条背景
			pygame.draw.rect(self.window,self.bg_stick_color,self.bg_stick_rect)
			#绘制上按钮箭头
			pygame.draw.polygon(self.window,self.button_color,self.up_button_point_list)
			#绘制下按钮箭头
			pygame.draw.polygon(self.window,self.button_color,self.down_button_point_list)
			#绘制滚动条
			pygame.draw.rect(self.window,self.stick_color,self.stick_rect,border_radius=self.border_radius)
			
			#绘制覆盖层
			if self.__up_sign:
				self.window.blit(self.covering,self.up_button_rect)
			elif self.__down_sign:
				self.window.blit(self.covering,self.down_button_rect)
				
				
				
	def check(self,event):
		if self.event_enable and self.start:
				
			#鼠标按键点击事件
			if event.type==pygame.MOUSEBUTTONDOWN:
				
				#判断鼠标坐标是否在上按钮中
				if self.up_button_rect.collidepoint(event.pos):
					self.__up_sign =True
					self.up()
				
				#判断鼠标坐标是否在下按钮中
				elif self.down_button_rect.collidepoint(event.pos):
					self.__down_sign=True
					self.down()
				
				#判断鼠标坐标是否在滚动条背景中
				elif self.bg_stick_rect.collidepoint(event.pos):
					self.__move_sign=True
					
					#让赋值给self.stick_rect.y的值在对应的范围内
					self.stick_rect.y=min(self.bg_stick_rect.bottom-self.stick_rect.height,event.pos[1])
	
					self.value=floor(self.get_exact_value(),self.precision)
					
			#鼠标按键弹起事件
			elif event.type==pygame.MOUSEBUTTONUP:
				self.__up_sign=False
				self.__down_sign=False
				self.__move_sign=False
				
			#鼠标移动事件
			if event.type==pygame.MOUSEMOTION and self.__move_sign:
				
				#让赋值给self.stick_rect.y的值在对应的范围内
				self.stick_rect.y=min(self.bg_stick_rect.bottom-self.stick_rect.height,max(self.bg_stick_rect.top,event.pos[1]))
	
				self.value=floor(self.get_exact_value(),self.precision)
				


class Animations(Control):
	def __init__(self,window):
		self.window=window
		self.rect=pygame.rect.Rect((100,300,300,300))
		self.path='./骰子/'
		self.picture_path=os.listdir(self.path)
		self.picture_path.sort()
		
#		self.picture_list=[pygame.transform.scale(pygame.image.load(self.path+i),self.rect.size) for i in self.picture_path]
		self.picture_list=[]
		
		self.sign=0
		self.isdoing=False
		self.isloop=True
		self.frame_rate=1
		self.frame_rate_sign=0
		
		self.loading_sign=0
		
		
		
		
	def loadnext(self):
		
		if not len(self.picture_list)==len(self.picture_path):
			self.picture_list.append(pygame.transform.scale(pygame.image.load(self.path+self.picture_path[self.loading_sign]),self.rect.size))
			self.loading_sign+=1
	
	def blit(self):
		
		self.loadnext()
		
		
#		self.frame_rate_sign+=1
		self.window.blit(self.picture_list[self.sign],self.rect)
#		if self.frame_rate_sign==self.frame_rate:
		if self.isdoing and self.frame_rate_sign==self.frame_rate:
			if self.sign < len(self.picture_list)-1:
				self.sign+=1
			elif self.isloop:
				self.sign=0
			self.frame_rate_sign=0
		elif self.isdoing:
			self.frame_rate_sign+=1
			
#		self.frame_rate_sign+=1
		
	def do(self):
		self.isdoing=True
		
	def reset(self):
		self.sign=0
		self.isdoing=False

	def load_in_once(self):
		while len(self.picture_list)<len(self.picture_path):
			self.picture_list.append(pygame.transform.scale(pygame.image.load(self.path+self.picture_path[self.loading_sign]),self.rect.size))
			self.loading_sign+=1
			
	def turn(self):
		self.isdoing=not self.isdoing
		
	def get_sign(self):
		return self.sign
		
		
		
class Dice(Control):
	def __init__(self,window,rect,box_width=2,box_color=(0,0,0),time_break=1,pic_path=None,start=True):
		super().__init__(window,start=start)
		
		self.rect=pygame.rect.Rect(rect)
		
		self.box_width=box_width
		self.box_color=box_color
		
		self.dice_rect=self.rect.copy()
		self.dice_rect.size=(self.rect.size[0]-self.box_width,self.rect.size[1]-self.box_width)
		self.dice_rect.center=self.rect.center
		
		if pic_path:
			self.pic_path=pic_path
		else:
			self.pic_path=os.path.join(DEFAULT_PIC_PATH,'骰子')

		self.image_list=[pygame.transform.scale(pygame.image.load(os.path.join(self.pic_path,i)).convert(),self.dice_rect.size) for i in os.listdir(self.pic_path)]
		
		self.sign=0
		
		self.__do_sign=False
		
		self.throw_once_sign=False
		self.time0=0
		self.time_break=time_break
		
	def blit(self):
		if self.__do_sign:
			if self.throw_once_sign and (time.time()-self.time0)>=self.time_break:
				self.stop()
				
			self.sign=random.randint(0,len(self.image_list)-1)
		pygame.draw.rect(self.window,self.box_color,self.rect)
		self.window.blit(self.image_list[self.sign],self.dice_rect)
		
	def do(self):
		self.__do_sign=True
		
	def stop(self):
		self.__do_sign=False
		
	def turn(self):
		self.__do_sign=not self.__do_sign
		
	def throw_once(self):
		if not self.__do_sign:
			self.throw_once_sign=True
			self.time0=time.time()
			self.do()
			
	def move(self,x=0,y=0):
		super().move(x,y)
		self.dice_rect.center=self.rect.center
			
			
	def update(self,*args,**kargs):
		super().update(*args,**kargs)
		self.dice_rect.center=self.rect.center
		
		
	def set_common(self,*args,**kargs):
		super().set_common(*args,**kargs)
		self.dice_rect.center=self.rect.center
		
	def get_num(self):
		return self.sign+1
		
	def set_time_break(self,time):
		self.time_break=time
		
		
class Dice_Group():
	def __init__(self,window,rect,layout,box_width=2,box_color=(0,0,0),time_break=1,start=True):
		self.window=window
			
		self.member={}
			
		self.rect=pygame.rect.Rect(rect)
			
		for num,L in enumerate(layout):
			for H in range(L):
				self.member[(H,num)]=Dice(self.window,(self.rect.x+num*self.rect.width,self.rect.y+H*self.rect.height,*self.rect.size),box_width,box_color,time_break,start)
			
			
	def blit(self):
		for i in self.member.values():
			i.blit()
		
	#	0/0
				
	def do(self):
		for i in self.member.values():
			i.do()
	
	def stop(self):
		for i in self.member.values():
			i.stop()	
				
				
	def turn(self):
		for i in self.member.values():
			i.turn()
				
	def throw_once(self):
		for i in self.member.values():
			i.throw_once()
				
	def get_num(self):
		num_dict={}
		for k,v in self.member.items():
			num_dict[k]=v.get_num()
		return num_dict
		
		
	def move(self,x=0,y=0):
		for i in self.member.values():
			i.move(x,y)			
			
	def __getitem__(self, index):  # 1).索引值的获取
		return self.member[index]

class OutputBox(Control):
	def __init__(self,window,event_enable=True,visible=True,start=True):
		super().__init__(window,event_enable=event_enable,visible=visible,start=start)

		self.rect=pygame.rect.Rect((200,600,300,300))

		self.scrollbar_width=30

		#self.ouput_rect=pygame.rect.Rect((*self.rect.topright,self.rect.width-self.scrollbar_width,self.rect.height))

		self.font_size=20
		self.text_color=(0,0,0)
		self.text_bgcolor=None
		
		self.box_line_color=(0,0,0)

		self.font=pygame.font.Font(DEFAULT_FONT_PATH,self.font_size)

		self.output_rect=pygame.rect.Rect((*self.rect.topleft,self.rect.width-self.scrollbar_width,self.rect.height))
		
		self.scrollbar_rect=pygame.rect.Rect((*self.output_rect.topright,self.scrollbar_width,self.rect.height))

		self.text=self.split('shusmsjkkidjsjfhhfddffddfhf的摄影师杜一第对齐')
		
		self.scrollbar=ScrollBar(window,self.scrollbar_rect,(0,len(self.text)))

		self.output_surface=pygame.surface.Surface(self.output_rect.size)
		self.output_surface.fill((0,255,0))
		
	def split(self,text):
		#这里的替换实现
		text=text.replace('\t','	')
		text=text.split('\n')
		line_list=[]
		line_width=0
		sign=0
		for line in text:
			for site,letter in enumerate(line):
				#print((sign,site),line)
				#breakpoint()
				width=self.font.render(letter,True,self.text_color,self.text_bgcolor).get_width()
				line_width += width
				if line_width >= self.output_rect.width:
					line_list.append(line[sign:site])
					sign=site
					line_width= width
			line_list.append(line[sign:])
			sign=0
			line_width=0
		return line_list
	
	
	def update_rect(self):
		self.output_rect=pygame.rect.Rect((*self.rect.topleft,self.rect.width-self.scrollbar_width,self.rect.height))

		self.scrollbar_rect=pygame.rect.Rect((*self.output_rect.topright,self.scrollbar_width,self.rect.height))
		
		self.scrollbar.update(rect=self.scrollbar_rect)
		
	
	def add(self,text):
		if self.text:
			text=self.text[-1]+text
		text=self.split(text)
		self.text[-1:]=text
		self.scrollbar.update(extend=(0,len(self.text)))
		
		
	def blit(self):
		self.output_surface.fill((0,255,0))
		line_height=0
		for i in self.text[self.scrollbar.value:]:
			self.output_surface.blit(self.font.render(i,True,(0,0,0)),(0,line_height))
			line_height+=self.font.get_height()
			if line_height>=self.output_rect.height+self.font.get_height():
				break
		self.window.blit(self.output_surface,self.output_rect)
		pygame.draw.rect(self.window,self.box_line_color,self.rect,1)
		#self.scrollbar.blit()
			  
	
	def check(self,event):
		self.scrollbar.check(event)
		
	def update_text(self,text):
		self.text=[]
		self.add(text)




class InputBox(Control):
	def __init__(self,window,rect,text='', font=None,font_color=(0,0,0),font_size=None,bg_font_color=None,focus=False,cursor_index=0,box_line_color=(0,0,0),box_line_width=1,bg_color=(255,255,255),x_pad=2,y_pad=2,cursor_width=1,flash_sign=0,flash_sign_max=100,event_enable=True,visible=True,start=True,enter_callback=None):
		self.window = window
		super().__init__(window,event_enable=event_enable,visible=visible,start=start)

		self.window_rect=window.get_rect()
		
		self.rect=pygame.rect.Rect(rect)
		

		self.box_line_color=box_line_color
		self.box_line_width=box_line_width
		self.bg_color=bg_color

		self.x_pad=x_pad+self.box_line_width
		self.y_pad=y_pad

		if font_size:
			self.font_size=font_size
		else:
			self.font_size=self.rect.height
		self.font=pygame.font.Font(font,self.font_size)
#		self.font_width,self.font_height=self.font.size()
		self.font_color=font_color

		self.bg_font_color=bg_font_color
		self.text=list(text)
		

		self.text_surface_update()
		#self.text_surface=self.font.render(''.join(self.text),True, self.font_color,self.bg_font_color)

		self.focus=focus
		self.cursor_index=cursor_index
		#self.cursor_position=[self.rect.x+self.x_pad+ self.font.render(self.text, True,(0,0,0)).get_width(),self.rect.y-self.y_pad]
		

		self.cursor_width=cursor_width
		self.flash_sign=flash_sign
		self.flash_sign_max=flash_sign_max
		
		self.update_rect()
		self.deal_enter_event=enter_callback
	#	self.a=0
 #	   self.text_show_rect.left=self.cursor_position[0]


	def update_rect(self):
		self.text_start_position=(self.rect.x+self.x_pad,self.rect.y+ self.y_pad)
	
		#这是相对于self.window的rect
		self.text_rect=self.rect.copy()
		self.text_rect.x+=self.x_pad
		self.text_rect.y+=self.y_pad
		self.text_rect.width-=2*self.x_pad
		self.text_rect.height-=2*self.y_pad
	
	#这是相对于self.text_surface的rect
		self.text_show_rect=pygame.rect.Rect((0,0,self.rect.width- 2*self.x_pad,self.rect.height-2/self.y_pad))
		self.cursor_height=self.rect.height-2*self.y_pad
	
	@property
	def cursor_position(self):
		text_width=self.font.size(''.join(self.text[:self.cursor_index]))[0]
		
		if text_width >= self.text_show_rect.width:
			return (self.rect.right-self.x_pad, self.rect.y)
		else:
			return (text_width+self.rect.x+self.x_pad,self.rect.y)

	def blit(self):
		if self.visible:
	  #	  pygame.draw.line(self.window,self.font_color, self.cursor_position,[self.cursor_position[0],self.cursor_position[1]+self.cursor_height], width=self.cursor_width)
#背景框
			pygame.draw.rect(self.window,self.bg_color,self.rect)
#线框
			pygame.draw.rect(self.window,self.box_line_color,self.rect\
				,self.box_line_width)
#文本
#			self.blit(self.font.render(''.join(self.text), True, self.font_color, background=self.bg_font_color),self.text_start_position)

			text_width=self.font.size(''.join(self.text[:self.cursor_index]))[0]
			if text_width<self.text_show_rect.width:
				self.text_show_rect.left=0
			else:
				self.text_show_rect.right=text_width
			self.window.blit(self.text_surface,self.text_start_position, self.text_show_rect)

#光标闪烁
			if self.focus and self.flash_sign<self.flash_sign_max:
				pygame.draw.line(self.window,self.font_color, self.cursor_position,[self.cursor_position[0],self.cursor_position[1]+self.cursor_height], width=self.cursor_width)
				self.flash_sign+=1
				#self.flash_sign=0
			elif self.focus and self.flash_sign==self.flash_sign_max:
				self.flash_sign=0


	def deal_mouse_event(self,event):
		#基本实现
		
		if self.rect.collidepoint(event.pos):
			#处理已经获得焦点鼠标点击文本框内事件
			if self.focus and self.text_rect.collidepoint(event.pos):
				now=past=self.cursor_position[0]
				subtract_sign=add_sign=False
				while True:
					#处理点到文本框内文字外
					if event.pos[0]>self.text_rect.left+self.text_surface.get_width():
						self.cursor_index=len(self.text)
						break
						
					#处理鼠标点到文字内
					elif event.pos[0]<now:
						#print(self.cursor_index)
						self.cursor_index-=1
						subtract_sign=True
					elif event.pos[0]>now:
						self.cursor_index+=1
						add_sign=True
					else:
						break

					#终点判定即中点判定
					if subtract_sign and add_sign:
						if event.pos[0] < (now +past)/2 and self.cursor_position[0]>event.pos[0]:
							self.cursor_move_forward(1)
						elif event.pos[0] > (now +past)/2 and self.cursor_position[0]<event.pos[0]:
							self.cursor_move_back(1)

						break

					past=now
					try:
						now=self.cursor_position[0]
					except IndexError:
						self.cursor_index-=1
						break
			#处理未获得焦点鼠标点击文本框事件
			elif not self.focus:
				self.focus=True
		#处理已经获得焦点鼠标点击文本框外事件
		elif self.focus:
			self.focus=False
	
	def cursor_move_forward(self,num):
		if self.cursor_index>=1:
			self.cursor_index-=num
			
	def text_surface_update(self):
		self.text_surface=self.font.render(''.join(self.text),True, self.font_color,self.bg_font_color)
	
	 
	def cursor_move_back(self,num):
		if len(self.text)>self.cursor_index:
			self.cursor_index += num

	def deal_keyboard_event(self,event):
		if self.focus:
			if event.key==pygame.K_BACKSPACE :
				if self.cursor_index>0:
					del self.text[self.cursor_index-1]
					self.cursor_move_forward(1)
					self.text_surface_update()
				
			elif event.key==pygame.K_LEFT:
				self.cursor_move_forward(1)
				
			elif event.key==pygame.K_RIGHT:
				self.cursor_move_back(1)
			elif event.key==pygame.K_RETURN:
				if self.deal_enter_event:
					self.deal_enter_event(self)
				
			else:
				text=event.unicode
				if not event.unicode:
					try:
						text=chr(event.key)
					except ValueError:
						pass
				self.add_text(text)
#				self.text[self.cursor_index:self.cursor_index]= list(text)
#				self.cursor_index+=len(text)
#			self.text_surface=self.font.render(''.join(self.text),True, self.font_color,self.bg_font_color)

	#def deal_enter_event(self,n):
	#	pass

	def set_enter_event(self,func):
		self.deal_enter_event=func

	def clear_text(self):
		self.text=[]
		self.cursor_index=0
		self.text_surface_update()
	
	def get_text(self):
		return ''.join(self.text)

	def set_text(self,text):
		text=list(text)
		self.text=text
		self.cursor_index=len(self.text)
		self.text_surface_update()
		#self.text_surface=self.font.render(''.join(self.text),True, self.font_color,self.bg_font_color)
	
	def add_text(self,text):
		self.text[self.cursor_index:self.cursor_index]= list(text)
		self.cursor_index+=len(text)
		#self.text_surface=self.font.render(''.join(self.text),True, self.font_color,self.bg_font_color)
		self.text_surface_update()
		

	def check(self,event):
		if self.start and self.event_enable:
			if event.type==pygame.MOUSEBUTTONDOWN:
				self.deal_mouse_event(event)

			elif event.type ==pygame.KEYDOWN:
				self.deal_keyboard_event(event)

				

