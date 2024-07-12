from bs4 import BeautifulSoup
import os
import sys
import csv



def run_grobid_xml_parser(xml_path):
    # GROBID生成的TEI_XML文件有一些<tag>名很不合法，会有歧义，这里进行替换
    replace_tag_dict = {
        "body":"grobid_body",
        "div":"grobid_div",
        "head":"grobid_head",
        "sourceDesc":"grobid_sourceDesc"
    }


    # 打开并读取XML文件
    with open(xml_path, 'r',encoding='utf-8') as file:
        xml_content = file.read()
        for tag_pair in replace_tag_dict:
            xml_content = xml_content.replace(f"<{tag_pair}", f"<{replace_tag_dict[tag_pair]}").replace(f"</{tag_pair}>", f"</{replace_tag_dict[tag_pair]}>")
    # 使用BeautifulSoup解析XML内容
    soup = BeautifulSoup(xml_content, 'lxml')


    # 查找所有<text>标签下的<body>标签，body标签只会有一个
    body_element = soup.find('grobid_body')
    # 查找body标签下所有div标签
    div_elements = body_element.find_all('grobid_div')

    # 逐个div去分析，div里的结构一般都是一个<header></header>标签和若干个<p></p>标签,header标签里的内容为大标题或小标题，大标题是固定的几种可能性，其他的可能是中标题或小标题
    literature_header_all = [
        ["Introduction","Background"],
        ["Result","Results","Results and discussion","Construction and content"],
        ["Method","Method Details","Materials and methods","Methods","Material and methods","Material and method","Methods and Materials"],
        ["Discussion","Discussion and conclusions"],
        ["Conclusion","Conclusions","CONCLUSION AND OUTLOOK"],
        ["Acknowledgement","Acknowledgements"],
        ["Reference","References"],
        ["Availability"],
        ["Funding"],
        ["Supplementary Material","Supplementary Information","Supplementary data","SUPPLEMENTAL INFORMATION"],
        ["Author contributions","Author details","Authors’contributions","Author contributions statement"],
        ["Conflicts of interest","Conflict of interest statement","DECLARATION OF INTERESTS"],
        ["Availability of data and materials","Availability and Implementation","RESOURCE AVAILABILITY"]
        ]
    INTRODUCTION_TAG = literature_header_all[0][0]
    RESULTS_TAG = literature_header_all[1][0]
    METHOD_TAG = literature_header_all[2][0]
    DISCUSSION_TAG = literature_header_all[3][0]
    CONCLUSION_TAG = literature_header_all[4][0]
    ACKNOWLEDGEMENT_TAG = literature_header_all[5][0]
    REFERENCE_TAG = literature_header_all[6][0]
    AVAILABILITY_TAG = literature_header_all[7][0]
    FUNDING_TAG = literature_header_all[8][0]
    SUPPLEMENTARY_TAG = literature_header_all[9][0]
    AUTHOR_CONTRIBUTION_TAG = literature_header_all[10][0]
    CONFLICT_TAG = literature_header_all[11][0]
    DATA_AVAILABILITY_TAG = literature_header_all[12][0]
    ABSTRACT_TAG = "Abstract"

    # 尽量确定每个章节的div_index，例如Introduction是1,Result是5,Conclusion是9,说明Introduction是1-4的div，可以取text合并在一块
    literature_section_index_dict = {}
    for div_index in range(len(div_elements)):
        div_header = div_elements[div_index].find('grobid_head')
        if div_header:
            # print(div_header)
            div_header_text = div_header.text
            for literature_headers in literature_header_all: #literature_headers是某种title的可能性list，如["Introduction","Background"]
                if (div_header_text.title() in literature_headers) or (div_header_text.capitalize() in literature_headers) or (div_header_text.lower() in literature_headers) or (div_header_text.upper() in literature_headers): #全大写、大写首字母、全小写
                    # literature_headers[0]是某一类title的第一种名字，例如Result,Results,选第一个作为key名
                    literature_section_index_dict[literature_headers[0]] = div_index

    # 如果空缺内容太多，最好加上最基础的RESULTS_TAG
    if RESULTS_TAG not in literature_section_index_dict.keys() and len(list(literature_section_index_dict.keys())) < 4:
        literature_section_index_dict[RESULTS_TAG] = 1

    # 如果没有Introduction的章节角标，一般第一个都是Introduction，给加上
    if INTRODUCTION_TAG not in literature_section_index_dict.keys():
        literature_section_index_dict[INTRODUCTION_TAG] = 0

    # 对literature_section_index_dict根据value进行从小到大排序
    sorted_dic = {k: v for k, v in sorted(literature_section_index_dict.items(), key=lambda x: x[1])}
    literature_section_index_dict = sorted_dic
    # print(literature_section_index_dict)



    # 根据已确定的每个章节序号，提取出每个章节的内容放到格式化字典里，但注意index指的是起始index，一直取直到下一个index的前一个
    literature_section_dict = {}
    for section in literature_section_index_dict:
        section_start_index = literature_section_index_dict[section]
        if list(literature_section_index_dict.keys()).index(section) == len(literature_section_index_dict.keys()) - 1:
            section_end_index = len(div_elements)
        else:
            section_end_index = literature_section_index_dict[list(literature_section_index_dict.keys())[list(literature_section_index_dict.keys()).index(section)+1]]
        section_content = ""
        for i in range(section_start_index, section_end_index):
            div = div_elements[i]
            # 取<head>标签内的内容，用双星号包裹，如果有的话
            if div.find_all("grobid_head"):
                section_content += f"**{div.find('grobid_head').text}**\n"
            # 取<p>标签内的内容
            for p in div.find_all('p'):
                section_content += p.text + "\n"
            # section_content += div_elements[i].text


        literature_section_dict[section] = section_content
    # print(literature_section_dict.keys())


    # 抽提XML中的DOI号码
    sourceDescDiv = soup.find("grobid_sourcedesc")
    # print(sourceDescDiv)
    if not sourceDescDiv:
        print(xml_path,"can't find sourceDescDiv for DOI")
    doi_div = sourceDescDiv.find("idno",attrs={"type":"DOI"})
    if doi_div:
        literature_section_dict["doi"] = doi_div.text
    # print("doi",doi)

    # 添加摘要
    abstract_div = soup.find_all("abstract")
    if abstract_div and ABSTRACT_TAG not in literature_section_dict.keys():
        literature_section_dict[ABSTRACT_TAG] = abstract_div[0].text


    ########################
    # 在Introduction部分找出最后一段（目前只是PTM项目用）
    # 情况1，Introduction离下一章的index不是很远，在2以内，则取下一章的index的前一个index
    # 情况2，Introduction离下一章的index很远，在2以上，则取Introduction自己div的index
    literature_section_index_list = list(literature_section_index_dict.values())
    if (literature_section_index_list[1] - literature_section_index_list[0]) < 2:
        last_paragraph_div_index = literature_section_index_list[1] - 1
    else:
        last_paragraph_div_index = literature_section_index_list[0]

    #查找该div中的最后一个<p>标签
    while div_elements[last_paragraph_div_index].find_all("p") == []:
        last_paragraph_div_index += 1
    last_paragraph_div = div_elements[last_paragraph_div_index]
    last_p_element = last_paragraph_div.find_all("p")[-1].text
    # print(last_p_element)
    literature_section_dict["introduction_last_paragraph"] = last_p_element
    ########################


    # 获取正文的全文
    full_text = ""
    useful_tags = [ABSTRACT_TAG,INTRODUCTION_TAG,RESULTS_TAG,METHOD_TAG,DISCUSSION_TAG,CONCLUSION_TAG]
    useless_tags = [ACKNOWLEDGEMENT_TAG,REFERENCE_TAG,AVAILABILITY_TAG,FUNDING_TAG,SUPPLEMENTARY_TAG,AUTHOR_CONTRIBUTION_TAG,CONFLICT_TAG,DATA_AVAILABILITY_TAG]
    # 获取literature_section_dict中key不为useless_tags的内容，拼接到一起，作为full_text
    for section in literature_section_dict:
        if section  in useful_tags:
            full_text += literature_section_dict[section] + "\n"
    if len(full_text) == 0:
        useless_tag_index_min = 9999
        for tag in literature_section_index_dict.keys():
            if tag in useless_tags:
                if literature_section_index_dict[tag] < useless_tag_index_min:
                    useless_tag_index_min = literature_section_index_dict[tag]
        if useless_tag_index_min < 9999:
            div_index = 0
            while div_index < useless_tag_index_min:
                div_index += 1
                div = div_elements[div_index]
                for p in div.find_all("p"):
                    full_text += p.text + "\n"
    if len(full_text) != 0:
        literature_section_dict["fullText"] = full_text

    # 在全文内检索是否存在特定字段，check_value是需要检索的字段，在literature_section_dict中记录"include_check_value_{检索字段}":True/False
    check_value = ["cys","cysteine"]
    for value in check_value:
        if value in full_text:
            literature_section_dict[f"include_check_value_{value}"] = True
        else:
            literature_section_dict[f"include_check_value_{value}"] = False


    # 在全文里检索某个特定字段并抽提出这个特定字段的前后各30个字符，check_value_sentence是需要检索的字段，在literature_section_dict中记录"check_value_sentence_{检索字段}":{前30个字符}+{检索字段}+{后30个字符}
    check_sentence_value = ["cys","cysteine"]
    for include_value in check_sentence_value:
        if include_value in full_text:
            include_value_index = full_text.index(include_value)
            if include_value_index - 30 < 0:
                start_index = 0
            else:
                start_index = include_value_index - 30
            if include_value_index + 30 > len(full_text):
                end_index = len(full_text)
            else:
                end_index = include_value_index + 30
            literature_section_dict[f"check_sentence_include_value_{include_value}"] = full_text[start_index:end_index]
        else:
            literature_section_dict[f"check_sentence_include_value_{include_value}"] = "NoData"




    return literature_section_dict

if __name__ == "__main__":
    # run_grobid_xml_parser(os.path.join(os.path.dirname(sys.argv[0]),'j.csbj.2020.10.038.grobid.tei.xml'))
    run_grobid_xml_parser(r"D:\SYSU\RenLab\Lab\PTM\palmitoylation_literature\pdf_xml_all\37432890.grobid.tei.xml")