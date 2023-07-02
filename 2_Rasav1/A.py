# encoding:utf-8
with open('汇知医学知识图谱_新型冠状病毒肺炎_20210820.txt', encoding='utf-8') as f:
    name = f.readline().strip().split(',')  # 读取文件第一行转成list，作为字典的key
    covid_list = []
    for line in f:  # 用for循环遍历句柄f，优点是无论文件有多大，读取都不会撑爆内存。
        # 不要用read()或readlines()，万一处理的文件超大会导致撑爆内存。
        if len(line) < 3:  # 过滤空行及数据不完整的行。
            continue
        line = line.strip().split(',')  # 将文件内容按','分隔转成列表
        covid_dict = {}  # 声明一空字典，保存每一行的内容
        for i in range(len(name)):  # 通过下标遍历name列表
            covid_dict[name[i]] = line[i]
        covid_list.append(covid_dict)
    print(covid_list)