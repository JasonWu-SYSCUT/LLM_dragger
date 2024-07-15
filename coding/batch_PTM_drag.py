import pandas as pandas
from llm_chat import run_llm_chat
import json
import os


template_prompt_json_path = r"files\prompt\prompt_template\payload_Job_ptmDrag_abstract.json"
custom_data_dir_path = r"files\literature\palmitoylation_bib_json"
save_path = r"files\result\palmitoylation_bib_json_fulltext_labeled"
 
 

for custom_data_json_path in os.listdir(custom_data_dir_path):
    # 调试时重复运行加速，跳过在目标文件夹中已有的文件
    # if custom_data_json_path != "palmitoylation_article10.json":
    #     continue
    if custom_data_json_path in os.listdir(save_path):
        continue
    print('job',custom_data_json_path, "start")
    with open(os.path.join(custom_data_dir_path, custom_data_json_path), "r") as f:
        ptm_article_dict = json.load(f)
        
        doi = ptm_article_dict["doi"]
        abstract = ptm_article_dict["abstract"]
        response_dic = run_llm_chat(custom_data_json_path = os.path.join(custom_data_dir_path, custom_data_json_path), 
                                    template_prompt_json_path = template_prompt_json_path)
        if response_dic == "request_failed":
            print('job',custom_data_json_path, "failed")
            continue
        response0 = response_dic["response0"]

        # chatGPT检测到内容有毒品相关的东西时统一都会回复下面这个内容，这种情况跳过
        if "but I can't assist with that request" in response0:
            continue
        result = {}
        PTM_mentioned = response0.split("PTM information mentioned: ")[1].split(";")[0]
        result["PTM_mentioned"] = PTM_mentioned
        if PTM_mentioned in ["Yes","have sites","possibly have sites"]:
            PTM_type = response0.split("The name of PTM type: ")[1].split(";")[0]
            Protein_name = response0.split("The name of protein: ")[1].split(";")[0]
            PTM_site = response0.replace("sites","site").split("Modification site: ")[1].split(";")[0]
            Source_text = response0.replace("judgment","judgement").split("Source text of judgement: ")[1].split(";")[0]
            result["PTM_type"] = PTM_type
            result["Protein_name"] = Protein_name
            result["PTM_site"] = PTM_site
            result["Source_text"] = Source_text
        ptm_article_dict.update(result)
        with open(os.path.join(save_path, custom_data_json_path), "w+") as f:
            json.dump(ptm_article_dict, f, indent=4)



