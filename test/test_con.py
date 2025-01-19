import time
from concurrent import futures
def func(a):
	print(a)
	time.sleep(a)
	print(f'({a})')
def main():
	print('st')
	exe=futures.ThreadPoolExecutor(max_workers=3)
	re=exe.map(func,[1,2,3])
	#time.sleep(10)
	for i in re:
		print(i)
	print('end')
main()