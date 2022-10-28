#!/usr/bin/python3
import os

# maOS10.15以上,自己编译的xlua.bundle会在第一次启动unity的时候提示损坏,移动到废纸篓 执行这个 sudo 执行
file = input("地址")
# current_address = os.path.dirname(os.path.abspath(__file__)) #当前目录下所有文件
current_address = os.path.dirname(os.path.abspath(file))
for parent, dirnames, filenames in os.walk(current_address):
    # Case1: traversal the directories
    # for dirname in dirnames:
    #     print("Parent folder:", parent)
    #     print("Dirname:", dirname)
    # Case2: traversal the files
    count = 0
    for filename in filenames:
        count += 1
        # print("Parent folder:", parent)
        print("正在执行:", filename)
        isok = os.system("sudo xattr -r -d com.apple.quarantine " + parent + "/" + filename)
        print("OK：{} 当前进度:{} 总进度:{}".format(isok, count, len(filenames)))
