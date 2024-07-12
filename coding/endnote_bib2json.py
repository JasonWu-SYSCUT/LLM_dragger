import json
import os
output_path = r"D:\SYSU\RenLab\Lab\PTM\palmitoylation_literature\palmitoylation_bib_json"
with open(r"C:\Users\china-2\Downloads\palmitoylation2.txt",encoding='utf-8') as f:
    lines = f.readlines()
    i = 165
    for line in lines:
        i+=1
        doi = line.split("$$$")[0]
        abstract = line.split("$$$")[1]
        palmitoylation_literature_bib_dict = {}
        palmitoylation_literature_bib_dict["doi"] = doi.replace("\ufeff","")
        palmitoylation_literature_bib_dict["abstract"] = abstract
        with open(os.path.join(output_path,f"palmitoylation_article{i}.json"), "w+") as f:
            json.dump(palmitoylation_literature_bib_dict, f, indent=4)
