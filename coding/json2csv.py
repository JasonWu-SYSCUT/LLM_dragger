import pandas as pd
import os
import json
import sys
import csv

#json文件夹
json_dir_path = r"D:\SYSU\RenLab\Lab\PTM\palmitoylation_literature\palmitoylation_bib_json_fulltext_labeled_chatgpt_full"
# json_dir_path = r"D:\SYSU\RenLab\Lab\PTM\palmitoylation_literature\palmitoylation_bib_json_labeled_0627_abstractLockPal_chatgpt"

#输出csv文件路径
# record_csv = r"D:\SYSU\RenLab\Lab\LLM\scicat\coding\tools\record_0703_fulltext_kimi.csv"
record_csv = r"D:\SYSU\RenLab\Lab\LLM\scicat\coding\tools\record_0703_fulltext_chatgpt_with_checkValue.csv"


# record_csv = open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),"record.csv"), "w+", newline="",encoding="utf-8")


## csv写入，按顺序每行里每列写
""" csv_wt = csv.writer(record_csv)
csv_wt.writerow(["file_index","doi", "abstract", "PTM_mentioned", "PTM_type", "Protein_name", "PTM_site", "Source_text"])
for json_f in os.listdir(json_dir_path):
    with open(os.path.join(json_dir_path, json_f), encoding="utf-8", mode="r") as f:
        ptm_article_dict = json.load(f)
        wt_list = [json_f]
        for key in ptm_article_dict.keys():
            wt_list.append(ptm_article_dict[key])
        csv_wt.writerow(wt_list)
"""
# record_csv.close()


def json2csv(
    key_list = ["file_name","doi", "abstract", "PTM_mentioned", "PTM_type", "Protein_name", "PTM_site", "Source_text",
                "include_check_value_cys","include_check_value_cysteine"]
        ):
    wt_dict = {}

    for key in key_list:
        wt_dict.update({key:[]})

    for json_f in os.listdir(json_dir_path):
        with open(os.path.join(json_dir_path, json_f), encoding="utf-8", mode="r") as f:
            ptm_article_dict = json.load(f)
            for key in key_list:
                if key == "file_name":
                    wt_dict[key].append(json_f)
                elif key in ptm_article_dict.keys():
                    wt_dict[key].append(ptm_article_dict[key])
                else:
                    wt_dict[key].append("NoData")

    df = pd.DataFrame(wt_dict,index=None)
    print(df)

    df.to_csv(record_csv,index=False)


def combine_two_df(df1,df2,on_col):
    return pd.merge(df1,df2,on=on_col)


if __name__ == "__main__":
    json2csv()