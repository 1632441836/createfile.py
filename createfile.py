# -*- coding:utf-8 -*-

'''
用法：

python createfile.py  modulename 目标路径

第二个参数目标路径可以不传。
如果参数不传目标路径，会自动检测当前脚本上级目录下是否有Resources/script/module结构，有，则使用该目录，没有则使用配置路径PROJECTPATH
然后在目标路径下创建名为 modulename 的文件夹和默认的几个文件 View，Ctrl，Model，Util，Request，Const，DBUtil
上面几个文件会用sublime-snippet 文件初始化

'''


import os 
import sys
import shutil
import commands
# import subprocess
from datetime import datetime
import re
# 文件存储路径 手动修改
PROJECTPATH = "/Users/username/work/newSvn/CardPirate/trunk/cocos2d-x-2.2.3/projects/CardPirate/Resources/script/module/"


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
	return  os.path.dirname(os.path.realpath(__file__)) + os.path.sep + filename


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
		print "文件不存在 snippetFile = %s" % format(snippetFile)
		return
	if not os.path.exists(targetFile):
		print "文件不存在 targetFile = %s" % format(targetFile)
		return
	with open(snippetFile) as sf:
		with open(targetFile, 'w') as pf:
			for var in sf.readlines():
				if re.match(r'.*\<.*\>',var):                              #去掉包含< ... > 的行
					print "去掉<snippet>类的行 var=%s" % var
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
		print "文件不存在 : %s" % format(targetFile)
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
		print "文件不存在 : %s" % format(targetFile)
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



# 在当前路径的上一级目录找 "Resources/script/module/"结构，如果能找到，使用该目录
def getCurModelPath():
	curpath = os.path.dirname(os.getcwd())
	writepath = curpath + os.path.sep + "Resources/script/module/"
	return writepath


# 判断当前输入的第二个参数是不是合法目录,是返回完成目录，不是返回空
def judgeInputPath(pathStr):
	if not pathStr.endswith('/'):
		pathStr += os.path.sep
	if not pathStr.endswith('Resources/script/module/'):
		pathStr += 'Resources/script/module/'
	if os.path.isdir(pathStr):
		return pathStr
	return None



########################################################################################################


if __name__ == '__main__':

	print "参数个数＝%s" % len(sys.argv)



	# 判断有无输入参数
	if len(sys.argv) <= 1:
		print "输入要创建的模块名"
		exit()

	modulename = sys.argv[1]
	print "要创建的模块名:%s" % format(modulename)

	# 目标路径
	targetPath = None
	# 检测输入路径是否合法
	if len(sys.argv) >= 3:#输入参数制定了创建目录
		print "输入路径＝%s" % sys.argv[2]
		path = judgeInputPath(sys.argv[2])
		if path :
			targetPath = os.path.join(path, modulename)
			print "使用输入目录，创建文件的目录＝%s" % path
		else:
			print "输入目录错误,检测当前脚本目录上级路径 : %s" % sys.argv[2]

	#检测当前脚本的上级路径是否合法
	if not targetPath and os.path.isdir(getCurModelPath()):     # 如果脚本放在工程根目录运行，取当前目录创建文件
		targetPath = os.path.join(getCurModelPath(), modulename)
		print "当前脚本上级路径正确,目标路径：%s" % targetPath

	#使用默认的配置路径
	if not targetPath:
		targetPath = os.path.join(PROJECTPATH, modulename)
		print "当前脚本上级路径错误，使用配置路径： %s" % targetPath


	print "要创建的文件夹路径:%s" % format(targetPath)
	#文件夹已经存在是否删除
	if os.path.exists(targetPath):
		rlt = judgeNext()
		if rlt :
			shutil.rmtree(targetPath)
		else:
			print "创建失败 目标文件夹已经存在"
			sys.exit()

	# 创建文件夹
	print "make dir "
	os.mkdir(targetPath)

	print "开始创建文件"
	list_key = FILE_NAME_DIC.keys()
	for var in list_key:
		filepath = targetPath + os.path.sep + getFileNameNew(var)
		pf = open(filepath,'w')
		pf.close()

	# 修改文件内容
	for var in list_key:
		filename = getFileNameNew(var)
		filepath = targetPath + os.path.sep + filename
		snippetname = FILE_NAME_DIC.get(var)
		snippet_path = getSnippetPath(snippetname)
		print "filename=%s" % filename
		if var == "Ctrl":
			createCtrlFile(snippet_path,filepath)
		elif var == "Request":
			createRequestFile(snippet_path,filepath)
		else:
			copySnippetToFile(snippet_path,filepath)









	



