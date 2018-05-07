#-*- coding: UTF-8 -*-
import os, sys, time,shutil,zipfile

#reload(sys)
#sys.setdefaultencoding('utf8')
print (sys.getdefaultencoding())
print (sys.getfilesystemencoding())

def copy_file(src,tg):  
    if os.path.exists(tg):  
        print ("path already exists!" ) 
    else:  
        os.system("cp %s %s"%(src,tg))  
        print ("file created"  )
# 同步目录
# src_dir 源目录
# dst_dir 目标目录
# is_recursion 是否递归
# ignores 忽略文件名列表
def sync_dir(src_dir, dst_dir, is_recursion=True, ignores=[]):
	files = os.listdir(src_dir)
	for f in files:

		# 忽略列表

		if f in ignores: continue
		#print (chardet.detect(f))
		#if chardet.detect(f)['encoding'] == 'ascii':
		src_path = os.path.join(src_dir, f)
		dst_path = os.path.join(dst_dir, f)
		#else:
		#	src_path = os.path.join(src_dir, f.decode("GB2312"))
		#	dst_path = os.path.join(dst_dir, f.decode("GB2312"))

		if os.path.isdir(src_path):

			# 是否递归
			if not is_recursion: continue

			# 创建目录
			try:
				if not os.path.exists(dst_path): 
					os.makedirs(dst_path) 
					print("mkdir"+ dst_path)

				#os.mkdir(dst_path)
				#print("mkdir"+ dst_path)
			except:
				pass

			sync_dir(src_path, dst_path, is_recursion, ignores)

		else:
			try:			
				if not os.path.exists(dst_path): 
				#print ("copy"+ src_path.decode('utf-8')+ dst_path.decode('utf-8'))
					print (src_path+" "+dst_path)
					shutil.copy(src_path, dst_path)

			except IOError:
        			print ("error:"+src_path)
				#new_src_path = "'"+src_path+"'"
				#new_dst_path = "'"+dst_path+"'"
				#copy_file(new_src_path,new_dst_path)

def sync_tree(src_dir, dst_dir, level=1, ignores=[]):
	files = os.listdir(src_dir)
	for f in files:
		if f in ignores: continue
		src_path = os.path.join(src_dir, f)
		dst_path = os.path.join(dst_dir, f)
		if os.path.isdir(src_path):
			if not os.path.exists(dst_path): 
				os.makedirs(dst_path) 
				print("mkdir: "+ dst_path)

			if level>0:
				sync_tree(src_path, dst_path, level-1, ignores)

# 压缩目录
def zip_dir(src_dir, output_file, is_recursion=True, ignores=[]):
	f = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED)
	_zip(src_dir, f, is_recursion, ignores, src_dir)
	f.close()

def _zip(src_dir, zip_file, is_recursion, ignores, root_path):
	files = os.listdir(src_dir)
	for f in files:

		# 忽略列表
		if f in ignores: continue

		src_path = os.path.join(src_dir, f)
		zip_path = src_path[len(root_path):]

		if os.path.isdir(src_path):

			# 是否递归
			if not is_recursion: continue

			# 创建目录
			try:
				zip_file.write(src_path, zip_path)
				print("mkdir "+ src_path + " " +zip_path)
			except:
				pass

			_zip(src_path, zip_file, is_recursion, ignores, root_path)

		else:
			print("zip "+ " " +src_path+ zip_path)
			zip_file.write(src_path, zip_path)

def main(src,dist,is_sub="True",ignores="svn,Thumbs.db",iszip="False",level=2):
	print( "run -------------------")

	ign_dir=[]
	for str in ignores.split(','):
		ign_dir.append(str)

	if is_sub=="T":
		sync_dir(src,dist,True,ign_dir)
	elif is_sub=="F":
		sync_dir(src,dist,False,ign_dir)
	elif is_sub=="tree":
		sync_tree(src,dist,int(level),ignores)


	#os.system("cp %s %s"%("./a/*.xlsx",dist))

	if iszip == "T":
		zip_dir(src,dist+".zip",is_sub,ign_dir)
	
	print ("over ------------------")

if __name__ == '__main__':
	argv_num=len(sys.argv)
	if argv_num == 3:
		main(sys.argv[1],sys.argv[2])
	elif argv_num == 4:
		main(sys.argv[1],sys.argv[2],sys.argv[3])
	elif argv_num == 5:
		main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
	else:
		print("Import parameter is error!")