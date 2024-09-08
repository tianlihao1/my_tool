import pygame
from my_tool import Control
import os


DEFAULT_RES_PATH=os.path.join(os.path.dirname(os.path.realpath(__file__)),'res')

DEFAULT_FONT_PATH=os.path.join(DEFAULT_RES_PATH,'font','SourceHanSerifCN','Regular.otf')

class Button(Control):
	'''
	用途：
		在界面上创建一个按钮，点击会有点击反馈，当按钮弹起是返回False，否则返回True
		
		
	属性：
		window：	按钮显示在的Surface对象
		window_rect:按钮显示的是Surface对象的Rect对象
		rect：		   按钮的坐标和大小（按钮的rect对象）
		text：		   按钮上的文字,默认为'按钮'
		font_path:			 按钮文字字体文件路径
		bg_color:	   按钮当前颜色
		text_color:	   按钮字体的颜色
		font_size：	 按钮字体的大小，默认为None
		start:			 按钮的启用状态
		mouse_down：		按钮被鼠标是否按下
	'''
	def __init__(self,window,rect,text='按钮',font=DEFAULT_FONT_PATH,has_bg=True,bg_color=(0,0,0),  image=None,is_image_scale=True, text_color=(255,255,255), font_size=None,cover_surface_color=(255,255,255),cover_surface_alpha=100, association_key_event=None,common=None,move=None,callback_function=None,event_enable=True,visible=True,start=True):
		
		super().__init__(window,event_enable,visible,start)

		#按钮矩形空间
		self.rect=pygame.Rect(rect)

		#按钮颜色
		self.bg_color=bg_color
		
		#文本颜色
		self.text_color=text_color

		#字体
		self.font_path=font

		#字号
		if not font_size:
			self.font_size=int(8*self.rect.height/10)
		else:
			self.font_size=font_size

		#字体对象
		self.font=pygame.font.Font(self.font_path,self.font_size)

		#按钮文字
		self.text=text

		self.update_text()
		
		self.is_image_scale_sign=is_image_scale
		
		#image的Surface
		self.bg_surface=image
		#self.update_bg()
		
		if self.bg_surface:
			
			#判断image是否包含pixel alpha通道
			if self.image.get_alpha():
				self.image=pygame.image.load(image).convert()
			else:
				self.image=pygame.image.load(image).convert_alpha()

			if not self.is_image_scale_sign:
				self.rect.size=self.image.get_size()
			else:
				self.image=pygame.transform.scale(image,self.rect.size)
		
		self.has_bg=has_bg

		self.bg=pygame.surface.Surface(self.rect.size).convert_alpha()
		
		self.update_bg()
		
		self.cover_surface_color=cover_surface_color
		self.cover_surface_alpha=cover_surface_alpha
		self.cover_surface=pygame.surface.Surface(self.bg.get_size())
		self.cover_surface.fill(self.cover_surface_color)
		self.cover_surface.set_alpha(self.cover_surface_alpha)
		

		#是否被鼠标按下
		self.mouse_down=False
		self.mouse_pos=None

		#一次点击按钮鼠标左键第一次弹起是为True
		self.is_mouse_up_sign=False
		#一次点击按钮鼠标左键第一次按下是为True
		self.is_mouse_down_sign=False

		if association_key_event:
			self.key_press_dict=dict.fromkeys(association_key_event,False)
		else:
			self.key_press_dict={}


		

		self.mouse_click_sign=False
		self.key_click_sign=False

		self.pressdown_sign=False
		self.pressup_sign=False

		self.callback_function=callback_function

		#是否启用
		self.start=start
		self.layout_init(common,move)

		#self.update_image()

	def update_bg(self):
		if self.bg_surface:
			if self.is_image_scale_sign:
				self.bg_surface=pygame.transform.scale(self.bg_surface,self.rect.size)
			else:
				self.rect.size=self.bg_surface.get_size()
		elif self.has_bg:
			return
		
		else:
			self.bg_surface=pygame.surface.Surface(self.rect.size).convert()
			self.bg_surface.fill(self.bg_color)



	def update_text(self,text=None):
		if text:
			self.text=text
		self.text_surface=self.font.render(self.text,True,self.text_color)
		self.text_rect=self.text_surface.get_rect()
		self.text_rect.center=self.rect.center

		

	def blit(self):
		#判断是否启用
		if self.start and self.visible:
#这里要改
			
			#blit bg
			self.window.blit(self.bg,self.rect)
			
			#blit font
			self.window.blit(self.text_surface,self.text_rect)
			
			#blit cover_surface
			if self.isdown():
				self.window.blit(self.cover_surface,self.rect)
				
			
	def check(self,event=None):

		#按钮事件
		self.is_mouse_up_sign=False
		self.is_mouse_down_sign=False
		self.pressup_sign=False
		self.pressdown_sign=False

		#判断按钮是否禁用
		if self.start and self.event_enable:
			#检测键盘事件
			if self.key_press_dict:
				key_pressed=pygame.key.get_pressed()
				for k in self.key_press_dict.keys():
					if key_pressed[k] and not self.key_press_dict[k]:
						self.key_press_dict[k]=True
						self.pressdown_sign=True
						return self.pressdown_sign
					elif not key_pressed[k] and self.key_press_dict[k]:
						self.key_press_dict[k]=False
						self.pressup_sign=True
						self.callback_function()
						return self.pressup_sign

			#检测鼠标状态
			button_status=pygame.mouse.get_pressed()
			
			if button_status[0] and not self.mouse_pos:
				self.mouse_pos=pygame.mouse.get_pos()
			elif not button_status[0]:
				self.mouse_pos=None

			if self.mouse_down==True and not button_status[0]:
				self.mouse_down=False
				self.is_mouse_up_sign=True
				
			#检测鼠标按下按钮
			elif button_status[0] and self.mouse_down!=True and  self.rect.collidepoint(self.mouse_pos):
				self.is_mouse_down_sign=True
				self.mouse_down=True
				

			if self.mouse_click_sign:
				self.mouse_click_sign=False
				self.is_mouse_up_sign,self.is_mouse_down_sign=True,True

			if self.key_click_sign:
				self.key_click_sign=False
				self.pressdown_sign,self.pressup_sign=True,True

			if self.is_mouse_up_sign or self.pressup_sign:
				if self.callback_function:self.callback_function()
				return True
			return False

	
	def isdown(self):
		'''返回是否被按钮按下'''
		if self.event_enable:
			return self.mouse_down or any(self.key_press_dict.values())
		return None

	def is_key_click_up(self):
		''' 键盘一次点击弹起 '''
		return self.pressup_sign

	def is_key_click_up_cut(self):
		''' 键盘一次点击弹起,并截断事件，即后面无法得到该次点击事件 '''
		sign=self.pressup_sign
		self.pressup_sign=False
		return sign

	def is_key_click_down(self):
		''' 键盘一次点击 '''
		return self.pressdown_sign

	def is_key_click_down_cut(self):
		''' 键盘一次点击,并截断事件，即后面无法得到该次点击事件 '''
		sign=self.pressdown_sign
		self.pressdown_sign=False
		return sign
		
	def is_mouse_click_up(self):
		'''鼠标一次弹起'''
		return self.is_mouse_up_sign

	def is_mouse_click_up_cut(self):
		''' 鼠标一次点击弹起,并截断事件，即后面无法得到该次点击事件 '''
		sign=self.is_mouse_up_sign
		self.is_mouse_up_sign=False
		return sign

	def is_mouse_click_down(self):
		'''鼠标一次点击'''
		return self.is_mouse_down_sign

	def is_mouse_click_down_cut(self):
		''' 鼠标一次点击,并截断事件，即后面无法得到该次点击事件 '''
		sign=self.is_mouse_down_sign
		self.is_mouse_down_sign=False
		return sign

	def mouse_click(self):
		'''模拟一次鼠标点击'''
		self.mouse_click_sign=True

	def key_click(self):
		'''模拟一次关联键盘点击'''
		self.key_click_sign=True

	def is_click_up(self):
		'''返回按钮的一次弹起'''
		return self.is_mouse_click_up() or self.is_key_click_up()

	def is_click_up_cut(self):
		'''返回按钮的一次弹起,并截断事件，即后面无法得到该次点击事件'''
		return self.is_mouse_click_up_cut() or self.is_key_click_up_cut()

	def is_click_down(self):
		'''返回按钮的一次按下'''
		return self.is_mouse_click_down() or self.is_key_click_down()

	def is_click_down_cut(self):
		'''返回按钮的一次按下,并截断事件，即后面无法得到该次点击事件'''
		return self.is_mouse_click_down_cut() or self.is_key_click_down_cut()

	def status_reset(self):
		self.pressup_sign=self.pressdown_sign=self.is_mouse_up_sign= self.is_mouse_down_sign=self.mouse_click_sign=self.key_click_sign=False


	#@classmethod
	def check_once(self,func):
		def inner():
			func()
			self.status_reset()
		return inner

	def change_font(self,font_path=None,font_size=None,font=None):
		'''修改字体'''
		if font_path:
			self.font_path=font_path
		if font_size:
			self.font_size=font_size
		if not font:
			self.font=pygame.font.Font(self.font_path,self.font_size)
		else:
			self.font=font
		self.update_text()

	def change_bg(self,has_bg=True,bg_color=None,image=False, image_path=False):
		self.has_bg=has_bg
		if bg_color:
			self.bg_color=bg_color
			self.bg_surface=None
	#	if image_path:
			
		elif image_path:
			#判断image是否包含pixel alpha通道
			self.image=pygame.image.load(image_path)
			if self.image.get_alpha():
				self.image=self.image.convert()
			else:
				self.image= pygame.image.load(self.image.convert_alpha())
		elif image:
			self.image=image
		self.update_bg()
			

	def update(self,*args,**kargs):
		'''本方法只能能改
key_press_dict
start
visible
event_enable
'''
		
		super().update(*args,**kargs)
		#self.update_bg()
		