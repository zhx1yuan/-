# Cap_pro_HealthKBQA
本文是本科毕业设计：“基于医疗知识图谱的中文问答机器人”的具体实现
# 配置环境
- python 3.9  
- NEO4J 5.3.0  
- 使用虚拟环境安装依赖`pip install -r requirements.txt`  
## 数据导入
安装配置好neo4j后，需要在以下位置更改知识图谱的账号密码  
```
1_datamodel\build_medical_graph.py
2_Rasav1\chat\actions\actions.py
2_Rasav1\B.py
```  
接着运行下面路径的文件，把除新冠以外的医疗数据导入知识图谱  
`1_datamodel\build_medical_graph.py`  
然后运行下面路径的文件，导入新冠的医疗数据  
`2_Rasav1\B.py`  
导入时按照节点、关系、属性的顺序分别导入，相关代码已注释  
## 训练Rasa模型
下面用到的命令需要在命令行中进入 `2_Rasav1\chat` 路径下使用  
首先需要下载mitie的模型文件，放在 `\2_Rasav1\MitieNLP\total_word_feature_extractor_zh.dat`  
下载好后，使用 `rasa train` 命令（也可不用训练，文件中包含已经训练好的模型）  
## 测试
下面用到的命令需要在命令行中进入 `2_Rasav1\chat` 路径下使用  
### shell方式 命令行测试
新终端运行 `neo4j.bat console`  
新终端运行 `rasa run actions` 启动Action Server  
新终端运行 `rasa shell -vv` 进行测试，-vv用于观察后端，可去掉  
### run方式 UI界面测试
新终端运行 `rasa run` 启动服务  
打开 `3_mychatui\ui\public\index.html`，进入对话网页  
# 参考
> Rasa部分：彭友老师：https://github.com/pengyou200902/Doctor-Friende  
> 数据部分：刘焕勇老师：https://github.com/liuhuanyong/QASystemOnMedicalKG  
> 前端部分：阿里巴巴小蜜蜂：https://chatui.io/  
> Rasa 官方文档指引：https://rasa.com/docs/  
> mitie训练: https://github.com/crownpku/Rasa_NLU_Chi  
