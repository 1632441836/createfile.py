#!coding=utf-8
# -*- coding:utf-8 -*-
# 用法 修改PROJECTPATH  SUBLIME_SNIPPET_PATH
# 创建需要的几个文件，读取sublime-snippet文件初始化文件

import os 
import sys
import shutil
# import commands
# import subprocess
from datetime import datetime

# 文件存储路径 手动修改
PROJECTPATH = "User/username/test/lua"

# sublime-snippet文件路径 手动修改
SUBLIME_SNIPPET_PATH = "/Users/username/Library/Application Support/Sublime Text 3/Packages/User/"

# 要创建的文件以及对应的snippet文件
FILE_NAME_DIC = {"View"   : "lua_newclass_desc.sublime-snippet",
				 "Ctrl"   : "lua_module_desc.sublime-snippet",
				 "Model"  : "lua_module_desc.sublime-snippet",
				 "Util"   : "lua_module_desc.sublime-snippet",
				 "Request": "lua_module_desc.sublime-snippet",
				 "Const"  : "lua_module_desc.sublime-snippet",
				 "DBUtil" : "lua_module_desc.sublime-snippet",
				 }

# 要创建的模块名
modulename = ''


def judgeNext():
	value = raw_input("当前文件夹已经存在了,是否删除重新创建(y/n):")
	if value == 'y':
		return True
	elif value == 'n':
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
def getFileNameNew(filestr):
	return upperFirstWorld(modulename) + filestr + ".lua"
		

#获取sublime-snippet文件路径 
def getSnippetPath(filename): 
	return SUBLIME_SNIPPET_PATH + filename


# lua_newclass_desc.sublime-snippet文件内容复制到view文件
def copyClassToView(snippetFile,targetFile):
	if not os.path.exists(snippetFile):
		print("文件不存在 snippetFile = {}".format(snippetFile))
		return 
	if not os.path.exists(targetFile):
		print("文件不存在 targetFile = {}".format(targetFile))
		return 
	with open(snippetFile) as sf:
		with open(targetFile,'w') as pf:
			for var in sf.readlines():
				if var.find("<snippet>") != -1 or var.find("<content><![CDATA[") != -1:
					print("行首")
				elif var.find("]]></content>") != -1:
					print("内容读取完毕")
					break
				else: # ${1/\.lua//g} 替换成class名
					if var.find("${1/\.lua//g}") != -1:
						classname = os.path.basename(targetFile)
						classname = classname.split('.lua')[0]
						newstr = var.replace("${1/\.lua//g}",classname)
						pf.write(newstr)
					elif var.find("-- FileName:") != -1:
						newstr = "-- FileName: " + os.path.basename(targetFile) + "\n"
						pf.write(newstr)
					elif var.find("-- Author:") != -1:
						newstr = "-- Author: " + getUserName() + "\n"
						pf.write(newstr)
					elif var.find("-- Date:") != -1:
						nowtime = datetime.now()
						newstr = "-- Date: " + nowtime.strftime('%Y-%m-%d') + "\n"
						pf.write(newstr)
					else:
						pf.write(var)



# lua_module_desc.sublime-snippet 复制
def copyModelToFile(snippetFile,targetFile):
	if not os.path.exists(snippetFile):
		print("文件不存在 snippetFile = {}".format(snippetFile))
		return 
	if not os.path.exists(targetFile):
		print("文件不存在 targetFile = {}".format(targetFile))
		return 
	with open(snippetFile) as sf:
		with open(targetFile,'w') as pf:
			for var in sf.readlines():
				if var.find("<snippet>") != -1 or var.find("<content><![CDATA[") != -1:
					print("行首")
				elif var.find("]]></content>") != -1:
					print("内容读取完毕")
					break
				else: # ${1/\.lua//g} 替换成class名
					if var.find("${1/\.lua//g}") != -1:
						classname = os.path.basename(targetFile)
						classname = classname.split('.lua')[0]
						newstr = var.replace("${1/\.lua//g}",classname)
						pf.write(newstr)
					elif var.find("-- FileName:") != -1:
						newstr = "-- FileName: " + os.path.basename(targetFile) + "\n"
						pf.write(newstr)
					elif var.find("-- Author:") != -1:
						newstr = "-- Author: " + getUserName() + "\n"
						pf.write(newstr)
					elif var.find("-- Date:") != -1:
						nowtime = datetime.now()
						newstr = "-- Date: " + nowtime.strftime('%Y-%m-%d') + "\n"
						pf.write(newstr)
					else:
						pf.write(var)



# 处理ctrl文件
def createCtrlFile(snippetFile,targetFile):
	copyModelToFile(snippetFile,targetFile)

	if not os.path.exists(targetFile):
		print("文件不存在 : {}".format(targetFile))
		return

	strBuff = ''
	with open(targetFile,'r') as pf:
		for var in pf.readlines():
			if var.find("-- 模块局部变量 --") != -1: # 添加m_instance变量
				strBuff += var
				str = "local m_instance = nil\n"
				strBuff += str
			elif var.find("function destroy") != -1: # 处理destroy接口
				str = "\tif (m_instance) then \n" + "\t\tm_instance:destroy()\n" + "\t\tm_instance = nil\n" + "\tend\n"
				strBuff += var
				strBuff += str
			elif var.find("function create") != -1:# 处理create接口
				strBuff += var
				classfile = getFileNameNew("View")
				classfile = classfile.split('.lua')[0]
				str = "\tm_instance = " + classfile + ".new()\n"
				str += "\tlocal layView = m_instance:create()\n"
				str += "\tLayerManager.changeModule(layView, moduleName(), {1}, true,1)"
				strBuff += str
			else:
				strBuff += var

	with open(targetFile,'w') as pf:
		pf.write(strBuff)

########################################################################################################


# 判断有无输入参数
if len(sys.argv) <= 1:
	print("输入要创建的模块名")
	sys.exit()

modulename = sys.argv[1]
print("要创建的模块名:{}".format(modulename))

#要创建的文件夹路径
targetPath = os.path.join(PROJECTPATH,modulename)
print("要创建的文件夹路径:{}".format(targetPath))

#文件夹已经存在是否删除
if os.path.exists(targetPath):	
	rlt = judgeNext()
	if rlt :
		shutil.rmtree(targetPath)
	else:
		print("创建失败 目标文件夹已经存在")
		sys.exit()

	
# 创建文件夹
print("make dir ")
os.mkdir(targetPath)


print("开始创建文件")
list_key = FILE_NAME_DIC.keys()
for var in list_key:
	filepath = targetPath + "/" + getFileNameNew(var)
	pf = open(filepath,'w')
	pf.close()


for var in list_key:
	filename = getFileNameNew(var)
	filepath = targetPath + "/" + filename
	snippetname = FILE_NAME_DIC.get(var)
	snippet_path = getSnippetPath(snippetname)
	print("var=%s" % var)
	if var == "View":
		copyClassToView(snippet_path,filepath)
	elif var == "Ctrl":
		createCtrlFile(snippet_path,filepath)
	else:
		copyModelToFile(snippet_path,filepath)









	



