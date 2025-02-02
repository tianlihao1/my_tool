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

def transform(mode,res_path,title_json_path,command=''):
	#res_path,title_json_path=get_res_path(subdirectory)
	title= get_title_from_json(title_json_path)
	
	
	
	is_aim_dir_exist()
		
	audio_path=os.path.join(res_path,'audio.m4s')
	if mode=='v':
		video_path=os.path.join(res_path,'video.m4s')
		os.system(f'ffmpeg -n -i {audio_path} -i {video_path} -c copy {command} "{os.path.join(Setting.aim_video_dir,title)}.mp4"')
		#print(f'ffmpeg -n -i {audio_path} -i {video_path} -c copy "{os.path.join(Setting.aim_video_dir,title)}.mp4"')
	else:
		os.system(f'ffmpeg -n -i {audio_path} {command} "{os.path.join(Setting.aim_audio_dir,title)}.mp3"')
		#print(f'ffmpeg -n -i {audio_path} "{os.path.join(Setting.aim_audio_dir,title)}.mp3"')

	
def get_title_from_json(title_json_path):
	title=load_json(title_json_path)['page_data']['part']
	title=''.join(title.split())
	return title



def handle_mode(args):
	if args.audio:
		sign='a'
	elif args.video:
		sign='v'
	else:
		sign=args.mode
	return sign

def handle_list_parse(args):
	if args.list:
		print_info()
		return True

def handle_choose_parse(args):
	if args.choose:
		subdirectories=get_all_res_path(Setting.top_dir)
		choices=[]
		for i in args.choose:
			try:a=[int(i)]
			except ValueError:
				start,end=i.split('-')
				a=list(range(int(start),int(end)+1))
			choices.extend(a)
				
		return (subdirectories[i]  for i in choices if i <= len(subdirectories)-1)

def print_info():
	for num,i in enumerate(get_all_res_path(Setting.top_dir)):
		#print(len(get_all_res_path(Setting.top_dir)))
		print(num,':',get_title_from_json(i[1]))

		

def set_parse():
	#视频还是音频
	parser=argparse.ArgumentParser()
	group=parser.add_mutually_exclusive_group()
	group.add_argument('-video','-v',action='store_true',help='输出为视频')
	group.add_argument('-audio','-a',action='store_true',help='输出为音频')
	group.add_argument('-mode','-m',help='选择模式： a：转为音频，v：转为视频',default='a',choices=['a','v'])
	
	#列出缓存视频及其序号
	parser.add_argument('-list','-l',action='store_true',help='列出缓存视频及其序号')
	#选择要处理的缓存的序号
	parser.add_argument('-choose','-c',type=str,nargs='*',help='选择要处理的缓存的序号，只处理传入给该选项的缓存视频')
	
	parser.add_argument('-to',type=str,help='裁剪到传入给to的时间，格式：00:00:00	或直接填秒数')
	
	parser.add_argument('-ss',type=str,help='从传入给ss的时间开始裁剪，格式：00:00:00	或直接填秒数')
	
	return parser


def handle_to_parses(args):
	if args.to :
		return f'-to {args.to}'
	else:
		return ''

def handle_ss_parser(args):
	if args.ss:
		return f'-ss {args.ss}'
	else:
		return ''

def handle_parses(parser):
	args=parser.parse_args()
	#print(args)
	
	if handle_list_parse(args):
		return 
	
	mode=handle_mode(args)
	
	choices=handle_choose_parse(args)
	
	
	
	command=handle_ss_parser(args)+' '+handle_to_parses(args)
	
	
	#print(list(choices))
	if not choices:
		#print(1)
		choices=get_all_res_path(Setting.top_dir)
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