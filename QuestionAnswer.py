#!/usr/bin/python3
import json
import os
import re

QuestionAnswerDic = {}

fileName = "QuestionAnswerFileName.json"
str = """
问题19：《桔梗谣》是哪里的民歌？

A:菲律宾
B:阿富汗
C:日本
D:朝鲜

答案为：D

桔梗谣是朝鲜族民歌。 “道拉基”是朝鲜族人民喜爱吃的一种野菜，叫“桔梗”，所以这首民歌叫《桔梗谣》，又名《道拉基》。
"""


def getStrQuestionAnswerIndex(str):
    # index = str.find("答案为：")
    # if index == -1:
    #     index = str.find("答案为:")
    #     return index, "答案为:"
    # return index, "答案为："
    return re.compile(r"答案为(:|：)").search(str.strip())


def getGetQuestionAnswerMatch(str):
    return re.match(r"问题\d+(:|：)", str.strip())


# 初始化列表
def initQuestionAnswerJson():
    global QuestionAnswerDic
    try:
        with open(fileName, 'r') as load_f:
            QuestionAnswerDic = json.load(load_f)
    except FileNotFoundError:
        f = open(fileName, 'w')
        f.close()
    except PermissionError:
        print("You don't have permission to access this file.")
    print("初始化{}文件成功".format(fileName))


# 写入问题到列表中
def writeQuestionAnswerJson(message):
    global QuestionAnswerDic
    message = message.strip()
    match = getGetQuestionAnswerMatch(message)
    if match:
        message = message[match.regs[0][1]:len(message)]
        search_re = getStrQuestionAnswerIndex(message)
        if not search_re:
            print("问题:{}\n问题都没有答案 所以不保存".format(message))
            return

        answer, question = GetQuestionAnswer(message)
        if answer and answer != "":  # 存在答案直接返回
            print("问题:\n{}\n已经存在答案 忽略存储{}:".format(question, answer))
            return
        # 获取答案（A、B、C、D ）字符
        answer = message[search_re.regs[1][0] + 1:search_re.regs[1][1] + 1]
        # 获取答案结果的开始index位置
        answer_index_start = message.find(answer) + 2
        # 获取答案结果的结束index位置
        answer_index_end = message.find("\n", answer_index_start)
        # 获取答案
        answer = message[answer_index_start:answer_index_end]
        # 把答案存入在表中
        QuestionAnswerDic[question] = answer
        print("问题:{}\n保存答案{}成功".format(question, answer))
    else:
        print("问题:{}\n问题都没有不保存".format(message))


# 保存问题列表到文件中
def writeQuestionAnswerJsonToFile():
    with open(fileName, "w") as dump_f:
        json.dump(QuestionAnswerDic, dump_f, ensure_ascii=False)
    print("保存Json文件完成")


# 获取问题答案 return 答案,问题
def GetQuestionAnswer(message):
    message = message.strip()
    match = getGetQuestionAnswerMatch(message)
    if match:
        message = message[match.regs[0][1]:len(message)]
        return GetQuestionAnswer(message)
    index = message.find('\n')
    question = message[0:index]
    question.strip()
    for questionData in QuestionAnswerDic.keys():
        if question in questionData:
            answer = QuestionAnswerDic[questionData]
            messages = message.split("\n")
            for str in messages:
                if answer in str:
                    answer_str = str[0:1]
                    if answer_str.upper() == "A" or answer_str.upper() == "B" or answer_str.upper() == "C" or answer_str.upper() == "D":
                        answer = answer_str.upper()
                        return answer, question
    return None, question


initQuestionAnswerJson()
writeQuestionAnswerJson(str)
print(
    GetQuestionAnswer(str))
