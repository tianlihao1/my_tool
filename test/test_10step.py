import itertools
class Setting():
	width=6
	height=6

class GameMap():
	def __init__(self,width,height):
		self.width,self.height=width,height
		self.circles_dict={(x,y):Circle(x,y) for x in range(self.width) for y in range(self.height)}
		self.rotated_angel=0
	
	def reset(self):
		for i in self.circles_dict.values():
			i.reset()
		self.rotated_angel=0

	def print_for_str(self):
		for x in range(self.width):
			for y in range(self.height):
				print(self[(x,y)],end='  ')
			print()
			
	def __getitem__(self,key):
		return self.circles_dict[key]
		
	def get_total_angel(self):
		return self.rotated_angel
	
	def action(self,x,y):
		while True:
			try:
				f_x,f_y=self[(x,y)].turn()
			except KeyError:return
			else:
				self.rotated_angel+=90
			x+=f_x
			y+=f_y
			if x<0 or y<0:
				return


class Circle():
	angel_to_forward={0:(0,1),90:(1,0),180:(0,-1),270:(-1,0)}
	def __init__(self,x,y):
		self.x,self.y=x,y
		self.reset()

		
	def reset(self):
		self._gen_angel=itertools.cycle([0,90,180,270])
		self.angel=next(self._gen_angel)
		
	def __str__(self):
		return str(self.angel)
		
	def turn(self):
		self.angel=next(self._gen_angel)
		return self.angel_to_forward[self.angel]
		
if __name__ =='__main__':
	game=GameMap(6,6)
	game.action(0,0)
	game.action(0,0)
	game.print_for_str()