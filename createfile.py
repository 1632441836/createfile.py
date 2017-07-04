#!coding=utf-8
# -*- coding:utf-8 -*-


# 用法 修改PROJECTPATH  SUBLIME_SNIPPET_PATH
# 创建需要的几个文件，读取sublime-snippet文件初始化文件

import os 
import sys
import shutil
import commands
from datetime import datetime

# 文件存储路径 手动修改
# PROJECTPATH=os.environ.get('ROOT')
PROJECTPATH="/Users/username/work/test/lua/"

# sublime-snippet问价路径 手动修改
SUBLIME_SNIPPET_PATH="/Users/username/Library/Application Support/Sublime Text 3/Packages/User/"
#要创建的文件
FILE_NAME_STR  = ["View","Ctrl","Model","Util","Request","Const","DBUtil"]
N_FILE_VIEW    = 0
N_FILE_CTRL    = 1
N_FILE_MODEL   = 2
N_FILE_UTIL    = 3
N_FILE_REQUEST = 4
N_FILE_CONST   = 5
N_FILE_DBUTIL  = 6
# sublime-snippet
FILE_SNIPPET    = ["lua_newclass_desc.sublime-snippet","lua_module_desc.sublime-snippet"]
N_SPFILE_CLASS  = 0
N_SPFILE_MODULE = 1 

# 要创建的模块名
modulename = ''


def judgeNext():
	value = raw_input('当前文件夹已经存在了,是否删除重新创建(y/n):')
	if (value=='y'):
		return True
	elif (value=='n'):
		return False
	else:
		return judgeNext()

# 获取当前登录系统的用户名
def getUserName():
	import getpass
	return getpass.getuser()

# 字符串首字母大写
def upperFirstWorld(srcStr):
	firstWorld = srcStr[0:1]
	lastWorld = srcStr[1:]
	newStr = firstWorld.upper() + lastWorld
	return newStr

# 获取文件名
def getFileName(idx):
	if idx > len(FILE_NAME_STR):
		print "not find file idx=%s" % idx
		return 
	return upperFirstWorld(modulename) + FILE_NAME_STR[idx] + ".lua"
		
#获取sublime-snippet文件路径 
def getSnippetPath(idx):
	if (idx > len(FILE_SNIPPET)):
		print "getSnippetPath error idx=%s" % idx
		return 
	return SUBLIME_SNIPPET_PATH + FILE_SNIPPET[idx]

# lua_newclass_desc.sublime-snippet文件内容复制到view文件
def copyClassToView(snippetFile,targetFile):
	if not os.path.exists(snippetFile):
		print "文件不存在 snippetFile = %s" % snippetFile
		return 
	if not os.path.exists(targetFile):
		print "文件不存在 targetFile = %s" % targetFile
		return 
	print "copy class snippet file to view.lua"
	sf = open(snippetFile)
	pf = open(targetFile,'w')
	for var in sf.readlines():
		if (var.find("<snippet>")!=-1 or var.find("<content><![CDATA[")!=-1):
			print "行首"
		elif (var.find("]]></content>")!=-1):
			print "内容读取完毕"
			break
		else: # ${1/\.lua//g} 替换成class名
			if (var.find("${1/\.lua//g}")!=-1):
				classname=os.path.basename(targetFile)
				classname=classname.split('.lua')[0]
				newstr=var.replace("${1/\.lua//g}",classname)
				pf.write(newstr)
			elif (var.find("-- FileName:")!=-1):
				newstr = "-- FileName: " + os.path.basename(targetFile) + "\n"
				pf.write(newstr)
			elif (var.find("-- Author:")!=-1):
				newstr = "-- Author: " + getUserName() + "\n"
				pf.write(newstr)
			elif (var.find("-- Date:")!=-1):
				nowtime = datetime.now()
				newstr = "-- Date: " + nowtime.strftime('%Y-%m-%d') + "\n"
				pf.write(newstr)
			else:
				pf.write(var)
	sf.close()
	pf.close()



# lua_module_desc.sublime-snippet 复制
def copyModelToFile(snippetFile,targetFile):
	if not os.path.exists(snippetFile):
		print "文件不存在 snippetFile = %s" % snippetFile
		return 
	if not os.path.exists(targetFile):
		print "文件不存在 targetFile = %s" % targetFile
		return 
	print "copy class snippet file to view.lua"
	sf = open(snippetFile)
	pf = open(targetFile,'w')
	for var in sf.readlines():
		if (var.find("<snippet>")!=-1 or var.find("<content><![CDATA[")!=-1):
			print "行首"
		elif (var.find("]]></content>")!=-1):
			print "内容读取完毕"
			break
		else: # ${1/\.lua//g} 替换成class名
			if (var.find("${1/\.lua//g}")!=-1):
				classname=os.path.basename(targetFile)
				classname=classname.split('.lua')[0]
				newstr=var.replace("${1/\.lua//g}",classname)
				pf.write(newstr)
			elif (var.find("-- FileName:")!=-1):
				newstr = "-- FileName: " + os.path.basename(targetFile) + "\n"
				pf.write(newstr)
			elif (var.find("-- Author:")!=-1):
				newstr = "-- Author: " + getUserName() + "\n"
				pf.write(newstr)
			elif (var.find("-- Date:")!=-1):
				nowtime = datetime.now()
				newstr = "-- Date: " + nowtime.strftime('%Y-%m-%d') + "\n"
				pf.write(newstr)
			else:
				pf.write(var)
	sf.close()
	pf.close()


# 处理ctrl文件
def resetCtrlFile(targetFile):
	if not os.path.exists(targetFile):
		print "文件不存在 targetFile = %s" % targetFile
		return 
	strBuff=''
	pf = open(targetFile,'r')
	for var in pf.readlines():
		if (var.find("-- 模块局部变量 --")!=-1): # 添加m_instance变量
			strBuff += var
			str="local m_instance = nil\n"
			strBuff += str
		elif (var.find("function destroy")!=-1): # 处理destroy接口
			str="\tif (m_instance) then \n" +"\t\tm_instance:destroy()\n" +"\t\tm_instance = nil\n" + "\tend\n"
			strBuff += var
			strBuff += str
		elif (var.find("function create")!=-1):# 处理create接口
			strBuff += var
			classfile = getFileName(N_FILE_VIEW)
			classfile = classfile.split('.lua')[0]
			str="\tm_instance = " + classfile + ".new()\n"
			str += "\tlocal layView = m_instance:create()\n"
			str += "\tLayerManager.changeModule(layView, moduleName(), {1}, true,1)"
			strBuff += str
		else:
			strBuff += var
	pf.close()
	pf = open(targetFile,'w')
	pf.write(strBuff)

################################################################################


# 判断有无输入参数
if (len(sys.argv) <= 1):
	print "输入要创建的模块名"
	sys.exit()

modulename = sys.argv[1]
print "要创建的模块名:%s" % modulename

#要创建的文件夹路径
targetPath=os.path.join(PROJECTPATH,modulename)
print("要创建的文件夹路径:%s" % targetPath)

#文件夹已经存在是否删除
if os.path.exists(targetPath):	
	rlt = judgeNext()
	if rlt==True:
		shutil.rmtree(targetPath)
	else:
		print "创建失败 目标文件夹已经存在"
		sys.exit()

	
# 创建文件夹
print("make dir ")
os.mkdir(targetPath)


print "开始创建文件"
index = 0
for var in FILE_NAME_STR:
	filepath = targetPath + "/" + getFileName(index) 
	pf = open(filepath,'w')
	pf.close()
	index = index + 1


filename = getFileName(N_FILE_VIEW)
filepath = targetPath + "/" + filename
snippet_path = getSnippetPath(N_SPFILE_CLASS)
print "读取snippet 文件 snippet_path=%s" % snippet_path
print "写入目标文件 filepath=%s" % filepath
#写入内容到View文件
copyClassToView(snippet_path,filepath)


# ctrl文件
snippet_path = getSnippetPath(N_SPFILE_MODULE)
filename = getFileName(N_FILE_CTRL)
filepath = targetPath + "/" + filename
print "读取snippet 文件 snippet_path=%s" % snippet_path
print "写入目标文件 filepath=%s" % filepath
copyModelToFile(snippet_path,filepath)
resetCtrlFile(filepath)


# 创建model util request
snippet_path = getSnippetPath(N_SPFILE_MODULE)
filename = getFileName(N_FILE_MODEL)
filepath = targetPath + "/" + filename
copyModelToFile(snippet_path,filepath)

snippet_path = getSnippetPath(N_SPFILE_MODULE)
filename = getFileName(N_FILE_UTIL)
filepath = targetPath + "/" + filename
copyModelToFile(snippet_path,filepath)


snippet_path = getSnippetPath(N_SPFILE_MODULE)
filename = getFileName(N_FILE_REQUEST)
filepath = targetPath + "/" + filename
copyModelToFile(snippet_path,filepath)

snippet_path = getSnippetPath(N_SPFILE_MODULE)
filename = getFileName(N_FILE_CONST)
filepath = targetPath + "/" + filename
copyModelToFile(snippet_path,filepath)

snippet_path = getSnippetPath(N_SPFILE_MODULE)
filename = getFileName(N_FILE_DBUTIL)
filepath = targetPath + "/" + filename
copyModelToFile(snippet_path,filepath)






	



