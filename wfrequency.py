# -*- coding: utf-8 -*-

import pandas as pd
import re
import string
import sys,os

os.chdir(sys.path[0])  #ָ��Ŀ¼

#��ȡ�ֵ䣬��ȡword��translation������
df_dict = pd.read_csv("./stardict.csv")
df_dict = df_dict[["word","translation"]]

#��ȡ��ʶ�ĵ��ʣ�ȡword��
df_known = pd.read_excel("known.xlsx")
df_known = df_known[["word"]]

#��Ҫ���������
reader = open(sys.argv[1], 'r')
strs =reader.read()

#ʹ��������ʽ���ѵ�����ȡ�����������޸�ΪСд��ʽ
strs_q = re.findall("\w+",str.lower(strs))
#ȥ���б��е��ظ��������
word_list = sorted(list(set(strs_q)))

#ȥ���������ֺͷ��ţ��Լ�����С��2���ַ���
new_words = []
word_count = []
for i in word_list:
    m = re.search("\d+",i)
    n = re.search("\W+",i)
    if not m and  not n and len(i)>2:
        new_words.append(i)  #��ȡ����תΪlist�б�
        word_count.append(strs_q.count(i))  #��ȡ��Ƶ��תΪlist�б�
#��list�б�����Ϊdataframe����ʽ
df_words = pd.DataFrame({"word": new_words,"count":word_count})

#�Ա���������ȡ�ĵ��ʣ������ֵ��������˼ƥ��
df_merge = pd.merge(
    left = df_dict,
    right = df_words,
    left_on = "word",
    right_on = "word"
)

#��dataframe���ת��Ϊlist�б�
known_list=df_known["word"].tolist()

#����ȡ�ĵ����м�ȥ��ʶ�ĵ���
df_new=df_merge[~df_merge["word"].isin(known_list)]

#����������excle�ļ�
df_new.to_excel("./words.xlsx")