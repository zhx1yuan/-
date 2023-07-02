import py2neo
from pandas import DataFrame, Series
from py2neo import Graph,NodeMatcher
print(py2neo.__version__)
graph = Graph("http://localhost:7474", auth=("neo4j", "mynewpass"), name="neo4j")
matcher = NodeMatcher(graph)
disease = "感冒"
abc = f'\'{disease}\''

# b=matcher.match("Disease", name__exact = "肺出血－肾炎综合征")
# a=list(matcher.match("Disease").where(f"_.name =~ {ab} "))
# food = dict()
# a = graph.run(matcher).data()
# b = graph.run("match (a:Disease{name:" +f'\'{disease}\'' "}) return a").data()
# m = [x['m.name'] for x in graph.run("match (a:Disease{name:" +f'\'{disease}\'' "})-[:do_eat]->(m:Food) return m.name").data()]
# a = [x['s.name'] for x in
#      graph.run("MATCH (p:Disease{name:" +f'\'{disease}\'' "})-[:has_symptom]->(s:Symptom) RETURN s.name").data()]
# a = [x['s.name'] for x in
#      graph.run("MATCH (p:Disease{name:" +f'\'{disease}\'' "})-[r:acompany_with]->(s:Disease) RETURN s.name").data()]
# food['not_eat'] = "、".join(m)
# retmsg = "在患 {0} 期间，可以食用：{1}，\n但不推荐食用：{1}". \
#                 format(disease, food['not_eat'], food['not_eat'])
m = graph.run("match (a:Disease{name:" +f'\'{disease}\'' "}) return a").data()
# for i in m :
#     m1=i['a']
# m2=m[0]['a']['desc']
# a = [x['a.desc'] for x in graph.run("match (a:Disease{name:" +f'\'{disease}\'' "}) return a.desc").data()]
print(m)
# print(m1)
# print(m2)
# print(a)
# x=[{'a': (1,2)},{'b':2}]
# print(x[0].keys())
# print(list(x[0].keys()))