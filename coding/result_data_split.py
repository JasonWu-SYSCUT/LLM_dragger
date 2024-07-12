import pandas as pandas
from llm_chat import run_llm_chat
import json
import os
save_path = r"D:\SYSU\RenLab\Lab\PTM\palmitoylation_literature\palmitoylation_bib_json_fulltext_labeled"
save_path2 = r"D:\SYSU\RenLab\Lab\PTM\palmitoylation_literature\palmitoylation_bib_json_fulltext_labeled_0703"

def drag_middle_value(target_str, former_str, latter_str,replace_list = []):
    if replace_list:
        for rep in replace_list:
            target_str = target_str.replace(rep[0],rep[1])
    try:
        return target_str.split(former_str)[1].split(latter_str)[0]
    except:
        return "NoData"



for custom_data_json_path in os.listdir(save_path):
    # 调试时重复运行加速，跳过在目标文件夹中已有的文件
    # if custom_data_json_path != "palmitoylation_article10.json":
    #     continue
    print('job',custom_data_json_path, "start")
    with open(os.path.join(save_path, custom_data_json_path), "r") as f:
        ptm_article_dict = json.load(f)
        PTM_mention_value = ptm_article_dict["PTM_mentioned"]
        result = {}
        if "The name of PTM type" in PTM_mention_value:
            result["PTM_mentioned"] = PTM_mention_value.split("The name of PTM type: ")[0]
            # result["PTM_type"] = PTM_mention_value.split("The name of PTM type: ")[1].split("The name of protein")[0]
            result["PTM_type"] = drag_middle_value(PTM_mention_value,"The name of PTM type: ","The name of protein")
            # result["Protein_name"] = PTM_mention_value.split("The name of protein: ")[1].replace("sites","site").split("Modification site")[0]
            result["Protein_name"] = drag_middle_value(PTM_mention_value,"The name of protein: ","Modification site",[["sites","site"]])
            # result["PTM_site"] = PTM_mention_value.replace("sites","site").split("Modification site: ")[1].replace("judgment","judgement").split("Source text of judgement")[0]
            result["Protein_name"] = drag_middle_value(PTM_mention_value,"Modification site: ","Source text of judgement",[["sites","site"],["judgment","judgement"]])
            # result["Source_text"] = PTM_mention_value.replace("judgment","judgement").split("Source text of judgement: ")[1]
            result["Source_text"] = drag_middle_value(PTM_mention_value,"Source text of judgement: ","")
            ptm_article_dict.update(result)
        with open(os.path.join(save_path2, custom_data_json_path), "w+") as f:
            json.dump(ptm_article_dict, f, indent=4)



