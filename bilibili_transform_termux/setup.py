import os
import sys
import shutil
import json


def setup():
	if os.system('ffmpeg -version')!=0:
		answer=input('是否已安装ffmpeg(y/n)')
		if answer=='n':
			print( '请先安装ffmpeg再运行此脚本')
			return
		
	bin_path=os.path.split(sys.executable)[0]
	setup_path=os.path.split(__file__)[0]
	file_name='bilibili_transform'
	file_path=os.path.join(setup_path,f'{file_name}.py')

	#创建脚本入口文件
	message='''#!/data/data/com.termux/files/usr/bin/python3
import os
import sys

if __name__=='__main__':
	args=' '.join(sys.argv[1:])
	os.system('python {} '+args)'''
	
	with open(file_name,'w') as f:
		f.write(message.format(file_path)) 
	
	#移入bin中
	try:
		os.remove(os.path.join(bin_path,file_name))
	except FileNotFoundError:
		pass
	shutil.move(os.path.join(setup_path,file_name),bin_path)
	
	#授权可执行
	os.system(f'chmod +x {os.path.join(bin_path,file_name)}')
	#print(f'chmod +x {os.path.join(bin_path,file_name)}')
	
	
	setting_dict={'top_dir':'/storage/emulated/0/Android/data/tv.danmaku.bili/download/',
	'aim_video_dir':f'{os.path.join(setup_path,"video")}',
	'aim_audio_dir':f'{os.path.join(setup_path,"audio")}'}
	with open(os.path.join(setup_path,'Setting.json'),'w') as f:
		json.dump(setting_dict,f)
	
	#print(setting_dict)
	print('finish setup')


setup()




