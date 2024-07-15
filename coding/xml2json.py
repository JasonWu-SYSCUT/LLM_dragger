import pandas as pd
import os
import csv
import json
#引入tools文件夹下的grobid_tei_xml_parser.py代码中的函数
from tools import grobid_xml_parser



json_dir = r"files\literature\palmitoylation_bib_json"

xml_dir = r"files\literature\pdf_xml"


for xml_file in os.listdir(xml_dir):
    print("job start",xml_file)
    # 在我们的服务器中（已经安装好了grobid）把PDF转成XML后，通过grobid_xml_parser函数把xml文件转成字典，加载要写入的来源文件(source)
    article_dict = grobid_xml_parser(os.path.join(xml_dir,xml_file))
    if "doi" in article_dict.keys():
        article_doi = article_dict["doi"]
    else:
        article_doi = "NoData"

    find = False

    # 确定好一个信息来源的XML文件后，要去寻找应该写入的JSON目标文件，遍历所有文件并通过doi匹配
    for json_file in os.listdir(json_dir):
        with open(os.path.join(json_dir,json_file),"r") as json_f:
            # 加载要写入的已有数据文件(target)
            json_obj = json.load(json_f)
        if str(json_obj["doi"]).replace("\ufeff","") == article_doi:
            # 写入Introduction
            json_obj["fragment"] = article_dict["introduction_last_paragraph"]
            # 写入全文
            if "fullText" in article_dict.keys():
                json_obj["fullText"] = article_dict["fullText"]
            # 写入查找词（如果解析代码中有添加这个字段项）
            for key in article_dict.keys():
                if "check_value" in key:
                    json_obj[key] = article_dict[key]
                if "check_sentence" in key:
                    json_obj[key] = article_dict[key]
            
            with open(os.path.join(json_dir,json_file),"w") as json_fw:
                json.dump(json_obj, json_fw, indent=4)
            # print("doi",article_doi,"找到fragment添加")
            find = True
            break
    if find != True:
        print("doi",article_doi,"这个xml没有找到对应json")
        
        
        



