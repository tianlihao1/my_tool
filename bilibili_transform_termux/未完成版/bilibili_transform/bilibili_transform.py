#!/data/data/com.termux/files/usr/bin/python3
import os
import json
import functools
import argparse
from collections import namedtuple



with open(os.path.join(os.path.split(__file__)[0],'Setting.json'),'r') as file:
	setting_map=json.load(file)

Setting=namedtuple('Setting',setting_map.keys())

Setting=Setting(**setting_map)

#class Setting:
#	top_dir='/storage/emulated/0/Android/data/tv.danmaku.bili/download/'

#		#aim_audio_dir=
#		aim_video_dir='/storage/emulated/0/1work/bilibili_transform/video'

def set_parse():

	#视频还是音频
	parser=argparse.ArgumentParser()
	group=parser.add_mutually_exclusive_group()
	group.add_argument('-video','-v',action='store_true',help='输出为视频')
	group.add_argument('-audio','-a',action='store_true',help='输出为音频')
	group.add_argument('-mode','-m',help='选择模式： a：转为音频，v：转为视频',default='',choices=['a','v'])
	
	#列出缓存视频及其序号
	parser.add_argument('-list','-l',action='store_true',help='列出缓存视频及其序号')
	#选择要处理的缓存的序号
	parser.add_argument('-choose','-c',type=str,nargs='*',help='选择要处理的缓存的序号，只处理传入给该选项的缓存视频')
	
	parser.add_argument('-to',type=str,help='裁剪到传入给to的时间，格式：00:00:00	或直接填秒数')
	
	parser.add_argument('-ss',type=str,help='从传入给ss的时间开始裁剪，格式：00:00:00	或直接填秒数')
	
	parser.add_argument('-over',action='store_true',help='覆盖已转换过的视频')
	
	return parser


@functools.lru_cache
def get_all_res_path(top_dir):
	dir_list=[]
	for ch_dir in os.listdir(top_dir):
		#print(ch_dir)
		
		for i in get_res_path(os.path.join(top_dir,ch_dir)):
			path,path0=i
		#if audio:
			#path=os.path.join(path,'audio.m4s')
		#else:
			#path=os.path.join(path,'video.m4s')
			dir_list.append((path,path0))
	return dir_list
	


@functools.lru_cache
def get_res_path(subdirectory):
	'''
	:paser subdirectory:str download下第一层目录,sec_subdirectory为合集层
	:return list:包含subdirectory层下所有项(完整路径,entry.json的完整路径)
	'''
	#有合集
	second_subdirectories=os.listdir(subdirectory)
	result=[]
	#合集层
	#print(second_subdirectories)
	for sec_subdirectory in second_subdirectories:
		
		
		sec_subdirectory=os.path.join(subdirectory,sec_subdirectory)
		#
		res_path=get_res_path_in_sec_subdirectory(sec_subdirectory)
		result.append((res_path,os.path.join(sec_subdirectory,'entry.json')))
	return result
	


def get_res_path_in_sec_subdirectory(sec_subdirectory):
	for i in os.listdir(sec_subdirectory):
		path=os.path.join(sec_subdirectory,i)
		if os.path.isdir(path):
			res_path=path
	return res_path



def load_json(path):
	with open(path) as file:
		return json.load(file)

def is_aim_dir_exist():
	if not os.path.isdir(Setting.aim_audio_dir):
		os.mkdir(Setting.aim_audio_dir)
	if not os.path.isdir(Setting.aim_video_dir):
		os.mkdir(Setting.aim_video_dir)
	if not os.path.isdir(Setting.work_dir):
		os.mkdir(Setting.work_dir)
	


def transform(mode,res_path,title_json_path,command=''):
	#res_path,title_json_path=get_res_path(subdirectory)
	title= get_title_from_json(title_json_path)
	
	
	
	is_aim_dir_exist()
		
	audio_path=os.path.join(res_path,'audio.m4s')
	if mode=='v':
		video_path=os.path.join(res_path,'video.m4s')
		result_path=f'{os.path.join(Setting.work_dir,title)}.mp4'
		os.system(f'ffmpeg -i {audio_path} -i {video_path} -c copy {command} "{result_path}"')
		#print(f'ffmpeg -n -i {audio_path} -i {video_path} -c copy "{os.path.join(Setting.aim_video_dir,title)}.mp4"')
	else:
		result_path=f'{os.path.join(Setting.work_dir,title)}.mp3'
		os.system(f'ffmpeg -i {audio_path} {command} "{result_path}"')
	
	return result_path
		#print(f'ffmpeg -n -i {audio_path} "{os.path.join(Setting.aim_audio_dir,title)}.mp3"')

def combine(mode,*res_path):
	
	with open(os.path.join(Setting.work_dir,'content.txt'),'w') as file:
		for i in res_path:
			file.write(f"file '{i}'")


def transfer(res_path,mode):
	aim_path=Setting.aim_video_path if mode=='v' else Setting.aim_audio_path
	aim_path=os.path.join(aim_path,Setting.os.path.split(res_path)[1])
	os.rename(res_path,aim_path)

	
def get_title_from_json(title_json_path):
	title=load_json(title_json_path)['page_data']['part']
	title=''.join(title.split())
	return title



def print_info():
	for num,i in enumerate(get_all_res_path(Setting.top_dir)):
		#print(len(get_all_res_path(Setting.top_dir)))
		print(num,':',get_title_from_json(i[1]))

def handle_mode(args):
	if args.audio:
		sign='a'
	elif args.video:
		sign='v'
	else:
		sign=args.mode
	if sign:return sign
	else:raise ValueError('必须设置输出的类型（音频[-a]/视频[-v]）或用-m [a/v]来指定类型')

def handle_list_parse(args):
	if args.list:
		print_info()
		return True
		
		
def get_format_choices_tuple(string:str):
	'''
	:return list:(序号字符串,起始时间,截止时间)
	'''
	try:
		num,time=string[:-1].split('(')
		contents=time.split(',')
		if len(contents)<2:
			return [num,time,'']
		else:
			return [num,*contents]
	except ValueError:
		return [string,'','']


def solve_choose_add_mode( choose_args_list):
	'''
	:return list:每一项为一个列表，列表中的每一项为tuple(序号,起始时间=-1,截止时间=-1)，为-1则为至一端。若该项不为“+”模式，则为仅含一项的列表
	'''
	if '+' in choose_args_list:
		#将choose中的所有合并一起
		result= [get_format_choices_tuple(i) for i in choose_args_list if i !='+' ]
		
	else:
		#每一项是否存在+
		result=[]
		for i in choose_args_list:
			if '+' in i:
				result.append([get_format_choices_tuple(j) for j in i.split('+') if j])
			else:
				result.append([get_format_choices_tuple(i)])
	return result

def solve_section_mode(args_list):
	'''
	args:
		args_list(list):
			经过solve_add_mode处理的list
	'''
	for num,single_item in enumerate(args_list):
		result=[]
		for sub_item in single_item:
			i = sub_item[0]
			try:result=[int(i)]
			except ValueError:
				start,end=i.split('-')
				result=list(range(int(start),int(end)+1))
			#	print('r',result)
		args_list[num]=[[i,*sub_item[1:]] for i in result]
	return args_list
		


def handle_choose_parse(args):

		subdirectories= get_all_res_path(Setting.top_dir)
		choices=args.choose if args.choose else [[i] for i in range(len(subdirectories))]
		
		choices=solve_section_mode( solve_choose_add_mode(choices))
		
		
		for outer in choices:
			for inner in outer:
				inner[0]=subdirectories[inner[0]]
		return choices
		#return (() for single_item in choices for i in single_item)

				
		#return (subdirectories[i]  for i in choices if i <= len(subdirectories)-1)


def handle_over_parse(args):
	if args.over:return '-y'
	else: return '-n'


def handle_to_parse(args):
	if args.to :
		return f'-to {args.to}'
	else:
		return ''

def handle_ss_parse(args):
	if args.ss:
		return f'-ss {args.ss}'
	else:
		return ''



def handle_parses(parser):
	args=parser.parse_args()
	#print(args)
	
	if handle_list_parse(args):
		return 
	try:
		mode=handle_mode(args)
	except Exception as e:
		print(e.args[0])
		return
	
	choices=handle_choose_parse(args)
	
	
	for item in choices:
		if len(item)>
		for part in item:
			
	
	
	
	
	command=\
		handle_ss_parse(args)+' '\
		+handle_to_parse(args)+' '\
		+handle_over_parse(args)
	
	

	for i in choices:
		transform(mode,*i,command)
	
#print_info()

def main():
	handle_parses(set_parse())



if __name__=='__main__':
	#print(get_all_res_path('/storage/emulated/0/Android/data/tv.danmaku.bili/download/'))
	main()
	#for i in get_all_res_path('/storage/emulated/0/Android/data/tv.danmaku.bili/download/'):
		#print(i)
	#print_info()
	
	#pass
	#print(Setting)
#transform('a','/storage/emulated/0/Android/data/tv.danmaku.bili/download/113825491714363/')

	#command=namedtuple('c1','choose')(['1','2+3','1(2:00,13:00)+2(,3:00)+3(2:00,)+6+7(3:00)'])
	#command=namedtuple('c1','choose')(['1-3(1:00)','3','+'])
	#print(command)
	#print(solve_section_mode(solve_choose_add_mode(command)))
	#print(solve_section_mode([[('16','',''),('1-6','','')],[('1-6','1:00','')]]))