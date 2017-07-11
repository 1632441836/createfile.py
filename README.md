cocos2dx-lua 项目， 开发新需求，使用sublime-text创建多个lua文件，基本需要的文件有Ctrl,Model,View,Util,DBUtil,Request等，再使用sublime-text的sinppet插件初始化lua文件，创建module 或 class 结构。
该脚本将上述内容一键创建。省去重复创建过程。


脚本语言：python
版本：python-2.7
脚本用法：
         （1）进入当前脚本目录，终端输入命令 python createfile.py  modulename (目标路径)
         如果参数传入了目标路径，会检测目标路径下有没有Resources/script/module结构，并在该结构下创建名为modulename的文件夹，文件夹内创建所需文件。
         （2）把脚本放在项目根目录下，运行命令不传目标路径参数。
          如果参数没传入目标路径，会检测当前 createfile.py的上级目录下，有没有Resources/script/module结构。有则使用该路径，没有则使用脚本配置的路径。
       
         

