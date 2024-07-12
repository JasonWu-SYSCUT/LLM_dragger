import pandas as pd
import os
import csv
import json
#引入tools文件夹下的grobid_tei_xml_parser.py代码中的函数
from tools import grobid_xml_parser



json_dir = r"D:\SYSU\RenLab\Lab\PTM\palmitoylation_literature\palmitoylation_bib_json_introduct_fulltext"

xml_dir = r"D:\SYSU\RenLab\Lab\PTM\palmitoylation_literature\pdf_xml_all"


for xml_file in os.listdir(xml_dir):
    print("job start",xml_file)
    #通过grobid_xml_parser函数把xml文件转成字典，加载要写入的来源文件(source)
    article_dict = grobid_xml_parser(os.path.join(xml_dir,xml_file))
    if "doi" in article_dict.keys():
        article_doi = article_dict["doi"]
    else:
        article_doi = "NoData"
    # print("解析得到doi",article_doi)

    find = False

    for json_file in os.listdir(json_dir):
        with open(os.path.join(json_dir,json_file),"r") as json_f:
            #加载要写入的已有数据文件(target)
            json_obj = json.load(json_f)
        if str(json_obj["doi"]).replace("\ufeff","") == article_doi:
            #写入Introduction
            json_obj["fragment"] = article_dict["introduction_last_paragraph"]
            #写入全文
            if "fullText" in article_dict.keys():
                json_obj["fullText"] = article_dict["fullText"]
            #写入查找词
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
        
        
        



