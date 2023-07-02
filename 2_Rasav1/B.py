# encoding:utf-8
from py2neo import Graph, Node, Relationship
import csv

# fr = open("新型冠状病毒肺炎.csv", mode="r", encoding="utf-8")
# fr = open("属性.csv", mode="r", encoding="utf-8")
fr = open("关系.csv", mode="r", encoding="utf-8")
lst = []
node = []
# entityId 0 ,entity 1 ,entityTag 2 ,property 3 ,valueId 4 ,value 5 ,valueTag 6 ,group 7 ,source 8
for row in csv.reader(fr):
    lst_ = []
    lst_.append(row[0])
    lst_.append(row[1])
    lst_.append(row[2])
    lst_.append(row[3])
    lst_.append(row[4])
    lst_.append(row[5])
    lst_.append(row[6])
    lst.append(lst_)
    node.append(row[1] + ' ' + row[2])
# print(lst)
graph = Graph("http://localhost:7474", auth=("neo4j", "mynewpass"), name="neo4j")
node = set(node)  # 消除重复结点
print(node)
# entityId 0 ,entity 1 ,entityTag 2 ,property 3 ,valueId 4 ,value 5 ,valueTag 6 ,group 7 ,source 8

# 建立结点 ：
# for item in node:
#     shiti, label = item.split()
#     cypher_ = "CREATE (:" + label + " {name:'" + shiti + "'})     "
#     graph.run(cypher_)
# 建立关系 ：
# for item in lst:
#     cypher_ = "MATCH  (a:" + item[2] + "),(b:" + item[6] + ") WHERE a.name = '" + item[1] + "' AND b.name = '" + item[
#         5] + "' CREATE (a)-[r:" + item[3] + "]->(b)"
#     graph.run(cypher_)
# 建立属性 ：
# for item in lst:
#     cypher_ = "MATCH (a:" + item[2] + "{name:'" + item[1] + "'}) set a." + item[3] + " = '" + item[5] +"'"
#     graph.run(cypher_)