# -*- coding:utf-8 -*-

'''
用法：
1 修改PROJECTPATH  SUBLIME_SNIPPET_PATH
2 运行时把第一个参数作为模块名
  如： Python3 creatfile.py Baqi ，
  模块名＝ Baqi, 在PROJECTPATH目录下创建Baqi文件夹，文件夹内
  创建文件BaqiCtrl.lua BaqiView.lua BaqiConst.lua BaqiUtil.lua BaqiDBUtil.lua BaqiRequest.lua BaqiModel.lua ，
  读取lua_newclass_desc.sublime-snippet/lua_module_desc.sublime-snippet文件初始化上述文件
'''


import os 
import sys
import shutil
# import commands
# import subprocess
from datetime import datetime
import re
# 文件存储路径 手动修改
PROJECTPATH = "/Users/username/test/lua/"

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
	value = input("当前文件夹已经存在了,是否删除重新创建(y/n):")
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



# Ctrl destroy接口中补充内容
def getDestroyContent():
	str = '''	if (m_instance) then 
		m_instance:destroy()
		m_instance = nil
	end\n'''
	return str



# Ctrl create 接口补充内容
def getCreateContent(classfile):
	str = '''	m_instance = ''' + classfile + '''.new()
	local layView = m_instance:create()
	LayerManager.changeModule(layView, moduleName(), {1}, true,1)'''
	return str


# Request文件补充内容
def getNewWorkContent():
	str = '''\n
--[[
-- /**
--  * 提升新空岛贝的改造属性等级
--  * @param int $hid
--  * $param int $shellType 空岛贝类型
--  * @param int $reformNo 改造属性编号（从1开始，1，2，3）
--  * return array{
-- 			"ret" : "ok"/"eff",
-- 			"shell_info": 同enforceShell返回的shell_info一样结构
-- }
--  */
function evolveShell( hid,shellType,reformNo,fnCallBack )
	Network.rpc(function ( cbFlag, dictData, bRet )
		if (bRet) then
			logger:debug({evolveShell = dictData.ret})
			if (dictData.ret.ret == "ok") then
				if (fnCallBack) then
					fnCallBack()
				end
			end
		end
	end, "hero.evolveShell", "hero.evolveShell", Network.argsHandlerOfTable({hid,shellType,reformNo}), true)
end
]]
\n\n'''
	return str


# sublime-snippet文件内容复制到目标文件
def copySnippetToFile(snippetFile,targetFile):
	if not os.path.exists(snippetFile):
		print("文件不存在 snippetFile = {}".format(snippetFile))
		return
	if not os.path.exists(targetFile):
		print("文件不存在 targetFile = {}".format(targetFile))
		return
	with open(snippetFile) as sf:
		with open(targetFile, 'w') as pf:
			for var in sf.readlines():
				if re.match(r'.*\<.*\>',var):                             #去掉包含< ... > 的行
					print("去掉<snippet>类的行 var=%s" % var)
				else:
					if var.find("${1/\.lua//g}") != -1:                    # ${1/\.lua//g} 替换成class名
						classname = os.path.basename(targetFile)
						classname = classname.split('.lua')[0]
						newstr = var.replace("${1/\.lua//g}", classname)
						pf.write(newstr)
					elif re.search(r'\$\{.*TM_FILENAME\}$', var):          # 替换文件名
						filenamestr = os.path.basename(targetFile)
						newstr = re.sub(r'\$\{.*TM_FILENAME\}$', filenamestr, var)
						pf.write(newstr)
					elif re.search(r'\$\{.*TM_FULLNAME\}$', var):          # 替换作者名
						newstr = re.sub(r'\$\{.*TM_FULLNAME\}$', getUserName(), var)
						pf.write(newstr)
					elif var.find("-- Date:") != -1:
						nowtime = datetime.now()
						newstr = "-- Date: " + nowtime.strftime('%Y-%m-%d') + "\n"
						pf.write(newstr)
					else:
						pf.write(var)



# 处理ctrl文件
def createCtrlFile(snippetFile,targetFile):
	copySnippetToFile(snippetFile,targetFile)

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
				strBuff += var
				strBuff += getDestroyContent()
			elif var.find("function create") != -1:# 处理create接口
				strBuff += var
				classfile = getFileNameNew("View")
				classfile = classfile.split('.lua')[0]
				strBuff += getCreateContent(classfile)
			else:
				strBuff += var

	with open(targetFile,'w') as pf:
		pf.write(strBuff)




def createRequestFile(snippetFile,targetFile):
	copySnippetToFile(snippetFile, targetFile)
	if not os.path.exists(targetFile):
		print("文件不存在 : {}".format(targetFile))
		return
	strBuff = ''
	with open(targetFile, 'r') as pf:
		for var in pf.readlines():
			if var.find("function destroy") != -1:  # 添加m_instance变量
				str = getNewWorkContent()
				strBuff += str
				strBuff += var
			else:
				strBuff += var

	with open(targetFile, 'w') as pf:
		pf.write(strBuff)



########################################################################################################


if __name__ == '__main__':
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

	# 修改文件内容
	for var in list_key:
		filename = getFileNameNew(var)
		filepath = targetPath + "/" + filename
		snippetname = FILE_NAME_DIC.get(var)
		snippet_path = getSnippetPath(snippetname)
		print("filename=%s" % filename)
		if var == "Ctrl":
			createCtrlFile(snippet_path,filepath)
		elif var == "Request":
			createRequestFile(snippet_path,filepath)
		else:
			copySnippetToFile(snippet_path,filepath)









	



