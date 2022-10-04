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


def getStrQuestionMarkIndex(str):
    index = str.find("？")
    if index == -1:
        index = str.find("?")
        return index, "?"
    return index, "？"


def getStrQuestionAnswerIndex(str):
    index = str.find("答案为：")
    if index == -1:
        index = str.find("答案为:")
        return index, "答案为:"
    return index, "答案为："


def getGetQuestionAnswerMatch(str):
    match = re.match(r"问题\d+：", str)
    if match:
        return match
    match = re.match(r"问题\d+:", str)
    return match


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
        index, answer_str = getStrQuestionAnswerIndex(message)
        if index == -1:
            return
        # question = message[0:index]
        # question = question.strip()

        answer, question = GetQuestionAnswer(message)
        if answer and answer != "":  # 存在答案直接返回
            print("问题:\n{}\n已经存在忽略存储{}:".format(question, answer))
            return
        answer = message[index + len(answer_str): index + len(answer_str) + 1]
        QuestionAnswerDic[question] = answer
        # with open(fileName, "w") as dump_f:
        #     json.dump(QuestionAnswerDic, dump_f, ensure_ascii=False)
        #     print("存储问题:\n{} \n答案是：{}".format(question, answer))
    else:
        print("问题:{}\n没有公布答案 不需要保存".format(message))


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
    #     index = getStrQuestionMarkIndex(message)
    #     question = message[0:index]
    #     if question in QuestionAnswerDic and QuestionAnswerDic[question] != "":
    #         return QuestionAnswerDic[question]
    # print("问题:{}\n没有答案".format(message))
    # return ""
    index = message.find('\n')
    question = message[0:index]
    question.strip()
    for questionData in QuestionAnswerDic.keys():
        if question in questionData:
            return QuestionAnswerDic[questionData], question
    return None, question

initQuestionAnswerJson()
writeQuestionAnswerJson(str)
print(
    GetQuestionAnswer(str))
