#/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Feng Guofu"
import re
import sys


# Regular expressions
# 数值（正数负数、整数小数）
regex_num = '\-?\d+(\.\d+)?'
# 匹配出公式中的负号数值，包含负号前的运算符或括号“（”
# regex_minus = '[(^\-)(\D\-)]?\d+(\.\d+)?'  【】这样用，匹配有问题中间的小括号并不是整体
regex_minus = '((^\-)|(\D\-))?\d+(\.\d+)?'


def add(x, y, c_type):
    '''
    加减法运算
    :param x: 第一个运算值
    :param y: 第二个运算值
    :param type: 运算类型
	:return num: 运算结果
    '''
    num = 0
    if c_type == '+':
        num = float(x) + float(y)
    elif c_type == '-':
        num = float(x) - float(y)
    return num


def multi(m, n, c_type):
    '''
    乘除法运算
    :param m: 第一个运算值
    :param n: 第二个运算值
    :param type: 运算类型
	:return num: 运算结果
    '''
    num = 0
    if c_type == '*':
        num = float(m) * float(n)
    elif c_type == '/':
        num = float(m) / float(n)
    return num


def counts(operation):
    '''
    判断公式中有几个数值
    :param operation: 运算式
	:return count: 数值个数
    '''
    # 判断公式中第一个值是不是负数
    result_tmp = re.match('\-',operation)
    if result_tmp is not None:
        # 去除公式中第一个值的负号
        result_tmp = re.sub('\-','',operation,1)
        count = re.compile('[\+\-\*\/]').split(result_tmp)
    else :
        count = re.compile('[\+\-\*\/]').split(operation)
    return count


def parentheses(operation):
    '''
    括号处理，取出最内部括号里的运算式
    :param operation: 运算式
	:return result: 公式运算结果
    '''
    # 公式中的“+-”更改为“-”，“--”更改为“+”
    operation = operation.replace('+-','-')
    operation = operation.replace('--','+')
    #  匹配括号内只有数字和小数点或‘+-*/’的部分
    print("\033[31m计算公式为：\n %s\033[0m" %operation)
    result_src = re.search('\([0-9\.\+\-\*\/]+\)',operation)
    if result_src is not None:
        print("当前处理的括号内result_src公式：",result_src.group())
        # 去除取出部分的括号
        result = re.sub('\(|\)', '', result_src.group())
        print("去除括号后的result公式：",result)
        count = counts(result)
        # 判断是否只是一个数字（包括负数和浮点数）
        if len(count) == 1:  # 是数字则替换掉原公式
            # 原公式替换
            operation = operation.replace(result_src.group(),result,1)
            print("此次数值内单括号处理完成\n",operation)

        else: # 是公式，交给calculate函数处理
            print("开始括号内公式处理：",result)
            # 调用calculate处理公式
            result = calculate(result)
            print(result)
            # 对于返回结果替换原公式
            operation = operation.replace(result_src.group(), str(result),1)
        # 递归调用
        return parentheses(operation)
    else:
        result = calculate(operation)
        print("公式结果为：",result)
        return result


def calculate(operation):
    '''
    乘除加减运算，计算出没有括号部分公式的结果。调用add、multi函数
    :param operation: 运算式
	:return operation: 运算式运算结果
    '''
    # 匹配出乘法和除法（包含有负数和负数没有括号的情况）
    mul_div = re.search(regex_minus+'[\*\/]'+regex_num,operation)
    # 匹配出加法和减法
    add_sub = re.search(regex_minus+'[\+\-]'+regex_num,operation)
    # 乘除法处理
    if mul_div is not None:
        # 取出运算类型
        print("当前计算公式：",mul_div.group())
        c_type = re.search('\*|\/', mul_div.group()).group()
        # 以运算类型作为分隔符
        p = re.compile('[\*\/]')
        # 获取到运算的两个值
        nums = p.split(mul_div.group())
        # 计算运算结果
        result = multi(nums[0], nums[1], c_type)
        # 把计算公式替换成计算结果
        operation = operation.replace(mul_div.group(),str(result),1)
        print("乘除法计算后运算结果：", operation)

    # 加减法处理
    # 八种判断类型：-1-2  -1+2  -1--2  -1+-2  1-2  1+2  1--2  1+-2
    elif add_sub is not None:
        result = add_sub.group()
        # 查看有无“--”算法(-1--2  1--2)
        minus_two = re.search('\-\-', result)
        if minus_two is not None:
            result = result.replace('--', '+',1)
        # 查看有无“+-”算法(-1+-2  1+-2)
        plus_minus = re.search('\+\-', result)
        if plus_minus is not None:
            result = result.replace('+-', '-',1)

        # 负数减正数的情况(-1-2)
        results = 0
        negative2 = re.match('\-\d+(\.\d+)?\-\d+(\.\d+)?',result)
        if negative2 is not None:
            nums = re.compile('\-').split(result)  # 列表三个元素
            results = add(0-float(nums[1]), 0-float(nums[2]), '+')
        # 负数加正数的情况(-1+2  1+2)
        negative1 = re.match('\-?\d+(\.\d+)?\+\d+(\.\d+)?',result)
        if negative1 is not None:
            nums = re.compile('\+').split(result)
            results = add(nums[0], nums[1], '+')
        # 正数减正数的情况(1-2)
        minus = re.match('\d+(\.\d+)?\-\d+(\.\d+)?', result)
        if minus is not None :
            nums = re.compile('\-').split(result)
            results = add(nums[0], nums[1], '-')

        print('此次加减法运算结果：',results)
        operation = operation.replace(add_sub.group(),str(results),1)
        print("加减法法计算后运算结果：", operation)

    # 获取公式数值个数
    count = counts(operation)
    print("次数",len(count))
    # 如果公式数值个数大于1，继续处理
    if len(count) > 1:
        return calculate(operation)
        # 注意：递归调用函数，必须！return 函数名。
        # 否则：错误：在最里层return，其它层没有return，最终返回None
    else:
        print("\033[31m 括号内运算部分完成\n %s \033[0m" %operation)
        return operation


if __name__ == "__main__":
    oper = input("请输入数学运算公式(注意：是英文括号)：\n")
    # 去除公式中的空格
    oper = oper.replace(' ','')
    # 调用parentheses()函数进行公式运算
    try:
        calc_result = parentheses(oper)
        print("\n\n以上信息为公式运算过程……\n\n\n\033[32m")
        print("="*60,"\n运算公式：\n",oper,'\n',"="*60)
        print("运算结果：\033[32;1m")
        print(str(calc_result).center(60,' '))
        print("\033[32m\n","="*60,'\033[0m')
    except:
        print("\n"*20,"="*60,"\033[31;5;1m\n 运算公式输入错误。退出\033[0m")
        # 采用sys模块回溯最后的异常
        info=sys.exc_info()
        print(info[0],":",info[1])
        sys.exit()
