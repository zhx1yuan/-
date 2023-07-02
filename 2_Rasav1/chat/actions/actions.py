# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
# This is a simple example for a custom action which utters "Hello World!"

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
    # def run(self, dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import logging
import re
import sys
from typing import Any, Text, Dict, List

from markdownify import markdownify as md
from py2neo import Graph
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

logger = logging.getLogger(__name__)
try:
    graph = Graph("http://localhost:7474", auth=("neo4j", "mynewpass"), name="neo4j")
except Exception as e:
    logger.error('Neo4j connection error: {}, check your Neo4j'.format(e))
    sys.exit(-1)
else:
    logger.debug('Neo4j Database connected successfully.')

p = "D:/1UPC/upc_zxy/cappro/Rasav1/JiebaTokenizer/disease.txt"
disease_names = [i.strip() for i in open(p, 'r', encoding="GBK").readlines()]

def make_button(title, payload):
    return {'title': title, 'payload': payload}

def retrieve_disease_name(name):
    names = []
    name = '.*' + '.*'.join(list(name)) + '.*'
    pattern = re.compile(name)
    for i in disease_names:
        candidate = pattern.search(i)
        if candidate:
            names.append(candidate.group())
    return names

class ActionEcho(Action):
    def name(self) -> Text:
        return "action_echo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_say = "You said: " + tracker.latest_message['text']
        dispatcher.utter_message(user_say)
        return []

class ActionFirst(Action):
    def name(self) -> Text:
        return "action_first"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_first")
        dispatcher.utter_message(md("您可以这样向我提问: <br/>头痛怎么办<br/>\
                              什么人容易头痛<br/>\
                              头痛吃什么药<br/>\
                              头痛能治吗<br/>\
                              头痛属于什么科<br/>\
                              头孢地尼分散片用途<br/>\
                              如何防止头痛<br/>\
                              头痛要治多久<br/>\
                              糖尿病有什么并发症<br/>\
                              糖尿病有什么症状"))
        return []

class ActionDonKnow(Action):
    def name(self) -> Text:
        return "action_donknow"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_donknow")
        dispatcher.utter_message(md("您可以这样向我提问: <br/>头痛怎么办<br/>\
                                      什么人容易头痛<br/>\
                                      头痛吃什么药<br/>\
                                      头痛能治吗<br/>\
                                      头痛属于什么科<br/>\
                                      头孢地尼分散片用途<br/>\
                                      如何防止头痛<br/>\
                                      头痛要治多久<br/>\
                                      糖尿病有什么并发症<br/>\
                                      糖尿病有什么症状"))
        return []


class ActionSearchTreat(Action):
    def name(self) -> Text:
        return "action_search_treat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        disease = tracker.get_slot("disease")
        # pre_disease = tracker.get_slot("sure")
        possible_diseases = retrieve_disease_name(disease)
        # if len(possible_diseases) == 1:
        a = graph.run("match (a:Disease{name:" + f'\'{disease}\'' "}) return a").data()[0]['a']
        if "cause" in a:
            intro = a['cause']
            response = "{0}的病因如下：\n{1}"
            retmsg = response.format(disease, intro)
        else:
            retmsg = "非常抱歉，暂时找不到这个病的病因"
        dispatcher.utter_message(retmsg)
        if "cure_way" in a:
            treat = a['cure_way']
            response = "{0}的治疗方式有：\n{1}"
            retmsg = response.format(disease, "、".join(treat))
        else:
            retmsg = disease + "非常抱歉，暂时找不到这个病的常见治疗方式"
        dispatcher.utter_message(retmsg)

        if len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_treat{{"disease":"{0}"}}'.format(d)))
            dispatcher.utter_button_message("这种疾病的类别很多，请点击列表选择您想查询的类别，若没有想要的，请忽略此消息", buttons)
        # else:
        #     dispatcher.utter_message("知识库中暂无与 {0} 疾病相关的记录".format(disease))
        return []


class ActionSearchFood(Action):
    def name(self) -> Text:
        return "action_search_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        possible_diseases = retrieve_disease_name(disease)
        """ search_food db action here """
        food = dict()
        # if disease == pre_disease or len(possible_diseases) == 1:
        m = [x['m.name'] for x in
             graph.run("match (a:Disease{name:" + f'\'{disease}\'' "})-[:do_eat]->(m:Food) return m.name").data()]
        food['can_eat'] = "、".join(m) if m else "暂无记录"

        m = [x['m.name'] for x in
             graph.run("match (a:Disease{name:" + f'\'{disease}\'' "})-[:no_eat]->(m:Food) return m.name").data()]
        food['not_eat'] = "、".join(m) if m else "暂无记录"

        retmsg = "在患 {0} 期间，可以食用：{1}，\n但不推荐食用：{2}". \
            format(disease, food['can_eat'], food['not_eat'])

        dispatcher.utter_message(retmsg)
        if len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_food{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        return []


class ActionSearchSymptom(Action):
    def name(self) -> Text:
        return "action_search_symptom"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        # pre_disease = tracker.get_slot("sure")
        # print("pre_disease::::" + str(pre_disease))
        possible_diseases = retrieve_disease_name(disease)
        # if disease == pre_disease or len(possible_diseases) == 1:
        a = [x['s.name'] for x in
             graph.run("MATCH (p:Disease{name:" +f'\'{disease}\'' "})-[:has_symptom]->(s:Symptom) RETURN s.name").data()]
        response = "{0}的症状可能有：{1}"
        retmsg = response.format(disease, "、".join(a))
        dispatcher.utter_message(retmsg)
        if len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_symptom{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        # else:
        #     dispatcher.utter_message("知识库中暂无与 {0} 相关的症状记录".format(disease))
        return []


class ActionSearchCause(Action):
    def name(self) -> Text:
        return "action_search_cause"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        # pre_disease = tracker.get_slot("sure")
        # print("pre_disease::::" + str(pre_disease))

        possible_diseases = retrieve_disease_name(disease)
        # if disease == pre_disease or len(possible_diseases) == 1:
        a = graph.run("match (a:Disease{name:" + f'\'{disease}\'' "}) return a.cause").data()[0]['a']
        if "cure_way" in a:
            treat = a['cure_way']
            response = "{0}的治疗方式有：{1}"
            retmsg = response.format(disease, "、".join(treat))
        else:
            retmsg = disease + "暂无该疾病的病因的记录"
        dispatcher.utter_message(retmsg)
        if len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_cause{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        # else:
        #     dispatcher.utter_message("知识库中暂无与 {0} 相关的原因记录".format(disease))
        return []


class ActionSearchNeopathy(Action):
    def name(self) -> Text:
        return "action_search_neopathy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        # pre_disease = tracker.get_slot("sure")
        # print("pre_disease::::" + str(pre_disease))

        possible_diseases = retrieve_disease_name(disease)
        # if disease == pre_disease or len(possible_diseases) == 1:
        a = [x['s.name'] for x in
             graph.run("MATCH (p:Disease{name:" + f'\'{disease}\'' "})-[:acompany_with]->(s:Disease) RETURN s.name").data()]
        response = "{0}的并发症可能有：{1}"
        retmsg = response.format(disease, "、".join(a))
        dispatcher.utter_message(retmsg)
        if len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_neopathy{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        # else:
        #     dispatcher.utter_message("知识库中暂无与 {0} 相关的并发症记录".format(disease))
        return []


class ActionSearchDrug(Action):
    def name(self) -> Text:
        return "action_search_drug"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        # pre_disease = tracker.get_slot("sure")
        # print("pre_disease::::" + str(pre_disease))

        possible_diseases = retrieve_disease_name(disease)
        # if disease == pre_disease or len(possible_diseases) == 1:
        a = [x['s.name'] for x in
             graph.run("MATCH (p:Disease{name:" + f'\'{disease}\'' "})-[:common_drug]->(s:Drug) RETURN s.name").data()]
        if a:
            response = "在患 {0} 时，可能会用药：{1}"
            retmsg = response.format(disease, "、".join(a))
        else:
            retmsg = "无 %s 的可能用药记录" % disease
        dispatcher.utter_message(retmsg)
        if len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_drug{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        # else:
        #     dispatcher.utter_message("知识库中暂无与 {0} 相关的用药记录".format(disease))
        return []


class ActionSearchPrevention(Action):
    def name(self) -> Text:
        return "action_search_prevention"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        # pre_disease = tracker.get_slot("sure")
        # print("pre_disease::::" + str(pre_disease))

        possible_diseases = retrieve_disease_name(disease)
        # if disease == pre_disease or len(possible_diseases) == 1:
        a = graph.run("match (a:Disease{name:" + f'\'{disease}\'' "}) return a").data()[0]['a']
        if 'prevent' in a:
            prevent = a['prevent']
            response = "以下是有关预防 {0} 的知识：\n{1}"
            retmsg = response.format(disease, md(prevent.replace('\n', '<br/>')))
        else:
            retmsg = disease + "暂无常见预防方法"
        dispatcher.utter_message(retmsg)
        if len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_prevention{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        # else:
        #     dispatcher.utter_message("知识库中暂无与 {0} 相关的预防记录".format(disease))
        return []


class ActionSearchDrugFunc(Action):
    def name(self) -> Text:
        return "action_search_drug_func"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        drug = tracker.get_slot("drug")
        if drug:
            a = [x['n.name'] for x in
                 graph.run("MATCH (n:Disease)-[:common_drug]->(a:Drug{name:" + f'\'{drug}\'' "}) RETURN n.name").data()]
            response = "{0} 可用于治疗疾病：{1}"
            retmsg = response.format(drug, "、".join(a))
        else:
            retmsg = drug + " 在疾病库中暂无可治疗的疾病"
        dispatcher.utter_message(retmsg)
        return []


class ActionSearchDiseaseTreatTime(Action):
    def name(self) -> Text:
        return "action_search_disease_treat_time"  # treat_period

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        # pre_disease = tracker.get_slot("sure")
        # print("pre_disease::::" + str(pre_disease))

        possible_diseases = retrieve_disease_name(disease)
        # if disease == pre_disease or len(possible_diseases) == 1:
        a = graph.run("match (a:Disease{name:" + f'\'{disease}\'' "}) return a").data()[0]['a']
        if "cure_lasttime" in a:
            treat_period = a['cure_lasttime']
            response = "{0}需要的治疗周期大致为：{1}"
            retmsg = response.format(disease, treat_period)
        else:
            retmsg = disease + "暂无治疗时间的记录"
        dispatcher.utter_message(retmsg)
        if len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(
                    make_button(d, '/search_disease_treat_time{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        # else:
        #     dispatcher.utter_message("知识库中暂无与 {0} 相关的治疗时间记录".format(disease))
        return []


class ActionSearchEasyGet(Action):
    def name(self) -> Text:
        return "action_search_easy_get"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        # pre_disease = tracker.get_slot("sure")
        # print("pre_disease::::" + str(pre_disease))

        possible_diseases = retrieve_disease_name(disease)
        # if disease == pre_disease or len(possible_diseases) == 1:
        a = graph.run("match (a:Disease{name:" + f'\'{disease}\'' "}) return a").data()[0]['a']
        easy_get = a['easy_get']
        response = "{0}的易感人群包括：{1}"
        retmsg = response.format(disease, easy_get)
        dispatcher.utter_message(retmsg)
        if len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_easy_get{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        # else:
        #     dispatcher.utter_message("知识库中暂无与 {0} 相关的易感人群记录".format(disease))
        return []


class ActionSearchDiseaseDept(Action):
    def name(self) -> Text:
        return "action_search_disease_dept"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        # pre_disease = tracker.get_slot("sure")
        # print("pre_disease::::" + str(pre_disease))

        possible_diseases = retrieve_disease_name(disease)
        # if disease == pre_disease or len(possible_diseases) == 1:
        a = graph.run("match (a:Disease{name:" + f'\'{disease}\'' "})-[:belongs_to]->(s:Department) return s.name").data()[0]['s.name']
        response = "{0} 属于 {1}"
        retmsg = response.format(disease, a)
        dispatcher.utter_message(retmsg)
        if len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_disease_dept{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        # else:
        #     dispatcher.utter_message("知识库中暂无与 {0} 疾病相关的科室记录".format(disease))
        return []
