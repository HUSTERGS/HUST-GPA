#-*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import json
import os
import sys
# 华科算法


def HUSTGPA(grade):
    if grade >= 85:
        return 4.0
    elif grade < 60:
        return 0
    else:
        return 1.5 + (grade - 60) * 0.1
# 标准算法


def StandardGPA(grade):
    if grade >= 90:
        return 4.0
    elif grade < 60:
        return 0
    elif grade >= 60 and grade < 70:
        return 1.0
    elif grade >= 70 and grade < 80:
        return 2.0
    elif grade >= 80 and grade < 90:
        return 3.0
# 北大算法
# def PKUGPA(grade):
#     if grade >= 95:
#         return 4.0
#     elif grade >= 90:
#         return 3.7
#     elif grade >= 85:
#         return 3.3
#     elif grade >= 80:
#         return 3.0
#     elif grade >= 77:
#         return 2.7
#     elif grade >= 73:
#         return 2.3
#     elif grade >= 70:
#         return 2.0
#     elif grade >= 67:
#         return 1.7
#     elif grade >= 63:
#         return 1.3
#     elif grade >= 60:
#         return 1.0
#     return 0


def PKUGPA(grade):
    if grade < 60:
        return 0
    return 4-3 * (100 - grade) ** 2 / 1600


all_info = {'course_info': [], 'GPA': ''}

result = {'HUST': 0, 'Standard': 0, 'PKU': 0}
credit_sum = 0


def calculate(df):
    global credit_sum

    for i in range(int(df.columns.size / 4)):
        course_name = df[df.columns[4 * i]]
        course_grade = df[df.columns[4 * i + 1]]
        course_credit = df[df.columns[4 * i + 2]]
        is_optional = df[df.columns[4 * i + 3]]
        for index, credit in enumerate(course_credit):
            # 如果是一门课程 并且不是选修 且学分不为0
            if not np.isnan(credit):
                # 是一门课程
                hust_result = ''
                standard_result = ''
                pku_result = ''
                # 处理缓考
                if course_grade[index] == "缓考/":
                    # 缓考的时候成绩和备注会调换位置
                    loc_grade = is_optional[index]
                else:
                    loc_grade = course_grade[index]
                # print(course_name[index], course_grade[index], course_credit[index], is_optional[index]);
                if type(is_optional[index]) != type('') or course_grade[index] == "缓考/":
                    # 不是公选，或者是缓考的课程
                    if str.isdigit(loc_grade):
                        # 不考虑成绩为良等的情况
                        hust_result = HUSTGPA(grade=int(loc_grade))
                        standard_result = StandardGPA(grade=int(loc_grade))
                        pku_result = PKUGPA(grade=int(loc_grade))

                        result['HUST'] += credit * hust_result
                        result['Standard'] += credit * standard_result
                        result['PKU'] += credit * pku_result
                        credit_sum += course_credit[index]
                all_info['course_info'].append({'course': course_name[index].strip(), 'grade': loc_grade, 'credit': course_credit[index], 'subGPA': {
                                               "HUST": hust_result, "Standard": standard_result, "PKU": pku_result},  'year': str(i + 1), 'is_optional': type(is_optional[index]) == type('') and is_optional[index] == "公选"})
    result['HUST'] /= credit_sum
    result['Standard'] /= credit_sum
    result['PKU'] /= credit_sum
    all_info['GPA'] = result

if __name__ == '__main__':
    if (len(sys.argv) == 2):
        if os.path.isfile(sys.argv[1]):
            try:
                calculate(pd.read_excel(sys.argv[1],  header=3))
                with open('result.json', 'w') as f:
                    f.write(json.dumps(all_info, ensure_ascii=False,
                            sort_keys=False, indent=4))
                print(result)
            except:
                print("Unknown Error")
            exit(0)
        else:
            print("Target not exist or is a dir")
            exit(0)
    else:
        print("Please enter with correct format")
    
