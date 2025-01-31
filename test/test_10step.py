import itertools
import random

class Setting():
	width=6
	height=6
	gene_group_length=2
	start_num=100
	chromosome_length=10
	aim=10000
	
	exchange_rate=0.7
	mutate_rate=0.1
	realign_rate=0.1
	remain_rate=0.8

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
		for y in range(self.height):
			for x in range(self.width):
				print(self[(x,y)],end='\t')
			print()
			
	def __getitem__(self,key):
		#print(key)
		return self.circles_dict[key]
		
	def get_total_angel(self):
		return self.rotated_angel
	
	def action(self,x,y):
		while True:
			try:
				#print(x,y)
				f_x,f_y=self[(x,y)].turn()
			except KeyError:return
			else:
				self.rotated_angel+=90
			x+=f_x
			y+=f_y
			if x<0 or y<0:
				return
	def action_from(self,it,show=False):
		#print(type(it[0]))
		#print('action',it)
		for i in it:
			#print('action_from',it)
			self.action(*i)
			if show:
				self.print_for_str()
				print()
	
	def once_game_test(self,it):
		self.reset()
		self.action_from(it)
		return self.get_total_angel()

class Circle():
	angel_to_forward={0:(0,-1),90:(1,0),180:(0,1),270:(-1,0)}
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
		
		
def split_part(it,step):
	result=[]
	num=0
	for i in it:
		num+=1
		result.append(i)
		if num==step:
			yield result
			result=[]
			num=0
	if result:
		yield result



class Evolution():
	def __init__(self,chromosomes,exchange_rate,mutate_rate,realign_rate,remain_rate):
		self.chromosomes=chromosomes
		self.exchange_rate=exchange_rate
		self.mutate_rate=mutate_rate
		self.realign_rate=realign_rate
		self.remain_rate=remain_rate

	def gene_exchange(self,c0,c1):
		newc0,newc1=[],[]
		#print('c',c0,'\t',c1)
		for g0,g1 in zip(c0,c1):
			if random.random()<=self.exchange_rate:
				newc0.extend(g1)
				newc1.extend(g0)
			else:
				newc0.extend(g0)
				newc1.extend(g1)
		c0.rebuild(newc0)
		c1.rebuild(newc1)
		#print('c',c0,'\t',c1)
		#print('new',newc0,'\t',newc1)
		return newc0,newc1
	
	def gene_mutate(self,c):
		result=[]
		for g in c:
			if random.random()<=self.mutate_rate:
				#print(g)
				site=random.randint(0,len(g)-1)
				g[site]=c.get_random_gene_func()
			result.extend(g)
		c.rebuild(result)
		return result
				
	
	def gene_realign(self,c):
		result=[]
		for g in c:
			if random.random()<=self.realign_rate:
				random.shuffle(g)
			result.extend(g)
		c.rebuild(result)
		return result
	
	def select(self,select_func):
		
		for c in self.chromosomes:
			self.gene_mutate(c)
			self.gene_realign(c)
			
		
		random.shuffle(self.chromosomes)
		chromosomes=self.chromosomes[:]
		while True:
			if len(chromosomes) <= 1:
				break
			c0=chromosomes.pop()
			c1=chromosomes.pop()
			self.gene_exchange(c0,c1)
		
		
		self.chromosomes.sort(key=select_func,reverse=True)
		num=int(self.remain_rate*len(self.chromosomes))
		result=self.chromosomes[:num]
		result.extend([i.build(i.gene_sequence) for i in self.chromosomes[:len(self.chromosomes)-num]])
		#print(result)
		self.chromosomes=result
		
		
	def start_evolution(self,aim,select_func):
		num=1
		constant_going=True
		while True:
			try:
				#print(self.chromosomes)
				self.select(select_func)
				#print(self.chromosomes)
				print(f'第{num}代，最高分数{select_func(self.chromosomes[0])}，其序列为{self.chromosomes[0]}')
				num+=1
				if select_func(self.chromosomes[0])>=aim and constant_going:
					raise ZeroDivisionError
			except (ZeroDivisionError,KeyboardInterrupt):
				#print(1,self.chromosomes[0].gene_sequence)
				print(f'第{num}代，最高分数{select_func(self.chromosomes[0])}，其序列为{self.chromosomes[0]}')
				sign=input('continue?(c/y/n)')
				if sign=='n':break
				elif sign=='c':
					constant_going=False
				
				
				
			
		


class Chromosome():
	def __init__(self,gene_sequence,gene_group_length,get_random_gene_func=None):
		self.gene_sequence=gene_sequence
		self.gene_group_length= gene_group_length
		self.get_random_gene_func= get_random_gene_func
	
	def rebuild(self,it):
		self.gene_sequence=list(it)
		
	def build(self,gene_sequence):
		return Chromosome(gene_sequence,self.gene_group_length,self.get_random_gene_func)
		
	
	def __iter__(self):
		return split_part(self.gene_sequence,self.gene_group_length)
	
	def __str__(self):
		string=''
		for gene_group in self:
			for gene_element in gene_group:
				string+=str(gene_element)
			string+=' '
		return string
	
	def __len__(self):
		return len(self.gene_sequence)
	
def get_random_gene():
	return (random.randint(0,Setting.width),random.randint(0,Setting.height))
	
def get_many_chromosomes(num,chromosome_length,get_random_gene_func):
	#result=[for for i in range(chromosome_length)]
	result=[]
	for i in range(num):
		result.append(Chromosome([get_random_gene_func() for j in range(chromosome_length)],Setting.gene_group_length,get_random_gene_func))
	return result
			

def select_func(func):
	def inner(it):
		return func(it.gene_sequence)
	return inner

def main():
	print('main')
	evolution= Evolution(get_many_chromosomes(Setting.start_num,Setting.chromosome_length,get_random_gene),Setting.exchange_rate,Setting.mutate_rate,Setting.realign_rate,Setting.remain_rate)
	game=GameMap(Setting.height,Setting.width)
	print('start')
	evolution.start_evolution(Setting.aim,select_func(game.once_game_test))
	#evolution.gene_exchange(*get_many_chromosomes(2,10,get_random_gene))
	#print(select_func(game.once_game_test)(get_many_chromosomes(1,10,get_random_gene)[0]))
#	a=get_many_chromosomes(3,10,get_random_gene)
#	
#	a.sort(key=select_func(game.once_game_test),reverse=True)
#	for i in a:
#		print(select_func(game.once_game_test)(i))



		
if __name__ =='__main__':
#	game=GameMap(6,6)
#	game.action(0,0)
#	game.action_from(((0,0),(0,0)),show=True)
#	game.print_for_str()
	#print(game.get_total_angel())
#	print(list(zip(split_part((1,2,3,4,5),2) ,split_part((5,4,3,2,1),2))))
	#e=Evolution()
#	c0=Chromosome((1,2,3,4,5),2)
#	game=GameMap(Setting.height,Setting.width)
#	print( select_func(game.once_game_test)(get_many_chromosomes(1,10,get_random_gene)[0]))
	main()
	
#	a=[(1, 1),(3, 1),(2, 2),(1, 4),(4, 4),(2, 3),(1, 2),(1, 2) ,(3, 2),(4, 0)]
#	print(a)
#	gamemap=GameMap(6,6)
	#gamemap.action_from(a,show=True)
	#print(gamemap.get_total_angel())

	
	#print([get_random_gene() for i in range(10)])
	pass
	