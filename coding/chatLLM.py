import requests
from article_cat import ArticleCat
# payload = {
#   "name": "qwen",
#   "messages": [
#     {
#       "content": "You are an expert in the field of biology, familiar with all definitions of knowledge within the subject area of biology, and are well versed in the classification of subfields within biology.",
#       "role": "system",
#       "url": ""
#     },
#     {
#         "content": 'I have defined 70 taxonomic labels in the field of biology, please read and understand the meaning of each one of them. After you have read them, I will provide information about a tool, and you will then choose the taxonomic label that suits it based on that information. The following wrapped in <label> are the 70 taxonomy labels, each separated by a semicolon ";" <label>Genes & Genomes; Enrichment analysis; Gene expression; Gene expression profiling; Gene prediction; Gene regulation; Genetic variation; Genetics; Genotype and phenotype; Genotyping; Population genetics; Nucleic acids; DNA; DNA polymorphism; Functional, regulatory and non-coding RNA; Nucleic acid sites, features and motifs; Read mapping; RNA; RNA secondary structure prediction; SNP detection; Transcription factors and regulatory sites; Proteins & Proteomes; Gene and protein families; Protein folding, stability and design; Protein folds and structural domains; Protein interactions; Protein modelling; Protein secondary structure prediction; Protein sequence analysis; Protein sites, features and motifs; Protein structural motifs and surfaces; Protein structure analysis; Protein structure prediction; Sequence analysis; Genome annotation; Mapping; PCR primer design; Phylogenetics; Protein feature detection; Sequence alignment; Sequence assembly; Sequence sites, features and motifs; Structural Biology; Molecular dynamics; Molecular modelling; Nucleic acid structure analysis; Small molecules; Structure analysis; Structure prediction; Systems Biology & Omics; Epigenomics; Genomics; Metabolomics; Metagenomics; Proteomics; Transcriptomics; Virology and vaccine design; Public health and epidemiology; Cell biology; Formatting; Image analysis; Machine learning; Molecular interactions, pathways and networks; Oncology; Pathology; Pathway or network prediction; Pathway or network visualisation; Phylogeny; Sequencing; Single cell transcriptome<label>',
#         "role": "user",
#         "url": ""
#     }
#   ],
#   "temperature": None,
#   "topP": None,
#   "n": None,
#   "maxTokens": None,
#   "stop": []
# }

def ask_llm(url, payload, headers):
  response = requests.post(url, json=payload, headers=headers)
  print(response.json())
  return response.json()


def create_payload(llm_name = "qwen", temperature = None, topP = None, n = None, maxTokens = None, stop = []):
  payload = {
    "name": llm_name,
    "messages": [],
    "temperature": None,
    "topP": None,
    "n": None,
    "maxTokens": None,
    "stop": []
  }
  return payload


def get_content_from_response(response,llm_name):
  print("原始的response.json():",response)
  if llm_name in ["qwen","gpt"]:
    return response['data']['content']


def add_system_message(payload, message):
  payload['messages'].append({
    "content": message,
    "role": "system",
    "url": ""
  })
  return payload


def add_user_message(payload, message):
  payload['messages'].append({
    "content": message,
    "role": "user",
    "url": ""
  })
  return payload


def add_assistant_message(payload, message):
  payload['messages'].append({
    "content": message,
    "role": "assistant",
    "url": ""
  })
  return payload


def get_standard_labels_in_response(response):
  judge_labels = []
  standard_labels = ["Genes & Genomes","Enrichment analysis","Gene expression","Gene expression profiling","Gene prediction","Gene regulation","Genetic variation","Genetics","Genotype and phenotype","Genotyping","Population genetics","Nucleic acids","DNA","DNA polymorphism","Functional, regulatory and non-coding RNA","Nucleic acid sites, features and motifs","Read mapping","RNA","RNA secondary structure prediction","SNP detection","Transcription factors and regulatory sites","Proteins & Proteomes","Gene and protein families","Protein folding, stability and design","Protein folds and structural domains","Protein interactions","Protein modelling","Protein secondary structure prediction","Protein sequence analysis","Protein sites, features and motifs","Protein structural motifs and surfaces","Protein structure analysis","Protein structure prediction","Sequence analysis","Genome annotation","Mapping","PCR primer design","Phylogenetics","Protein feature detection","Sequence alignment","Sequence assembly","Sequence sites, features and motifs","Structural Biology","Molecular dynamics","Molecular modelling","Nucleic acid structure analysis","Small molecules","Structure analysis","Structure prediction","Systems Biology & Omics","Epigenomics","Genomics","Metabolomics","Metagenomics","Proteomics","Transcriptomics","Virology and vaccine design","Public health and epidemiology","Cell biology","Formatting","Image analysis","Machine learning","Molecular interactions, pathways and networks","Oncology","Pathology","Pathway or network prediction","Pathway or network visualisation","Phylogeny","Sequencing","Single cell transcriptome" ]
  for label in standard_labels:
    if label in response:
      judge_labels.append(label)
  print(judge_labels)
  return judge_labels


def main():
  llm_chat_rjurl = "http://cloud.rj-info.com/ai/chat/completion?_timeout=111111111"
  llm_name = "qwen" #修改使用的大模型，可以改成gpt
  headers = {"content-type": "application/json"}

  #输入文章的信息，让LLM进行读取和理解
  article_info = {
    "tool_name": "StackPR",
    "description": "StackPR is a new computational approach for large-scale identification of progesterone receptor antagonists using the stacking strategy.",
    "abstract": "Progesterone receptors (PRs) are implicated in various cancers since their presence/absence can determine clinical outcomes. The overstimulation of progesterone can facilitate oncogenesis and thus, its modulation through PR inhibition is urgently needed. To address this issue, a novel stacked ensemble learning approach (termed StackPR) is presented for fast, accurate, and large-scale identification of PR antagonists using only SMILES notation without the need for 3D structural information. We employed six popular machine learning (ML) algorithms (i.e., logistic regression, partial least squares, k-nearest neighbor, support vector machine, extremely randomized trees, and random forest) coupled with twelve conventional molecular descriptors to create 72 baseline models. Then, a genetic algorithm in conjunction with the self-assessment-report approach was utilized to determine m out of the 72 baseline models as means of developing the final meta-predictor using the stacking strategy and tenfold cross-validation test. Experimental results on the independent test dataset show that StackPR achieved impressive predictive performance with an accuracy of 0.966 and Matthew's coefficient correlation of 0.925. In addition, analysis based on the SHapley Additive exPlanation algorithm and molecular docking indicates that aliphatic hydrocarbons and nitrogen-containing substructures were the most important features for having PR antagonist activity. Finally, we implemented an online webserver using StackPR, which is freely accessible at http://pmlabstack.pythonanywhere.com/StackPR . StackPR is anticipated to be a powerful computational tool for the large-scale identification of unknown PR antagonist candidates for follow-up experimental validation.",
    "keywords": None,
  }
  #LLM初始化信息
  system_message = "You are an expert in the field of biology, familiar with all definitions of knowledge within the subject area of biology, and are well versed in the classification of subfields within biology."

  # 第一次对话
  # 提问信息
  # 应发起的问题（暂定）“接下来我会给你一篇文献的信息，以及第一组分类学的标签，请你根据文献信息选择合适的分类标签，然后如果你选择的分类标签有更深一层的分类标签，我会让你进一步选择深一层分类标签中恰当的标签，如果没有则不用继续往细分方向判断分类。”
  ask_message1 = 'I have defined 70 taxonomic labels in the field of biology, please read and understand the meaning of each one of them. After you have read them, I will provide information about a tool, and you will then choose several taxonomic labels that suits it based on that information. The following wrapped in <label> are the 70 taxonomy labels, each separated by a semicolon ";" <label>Genes & Genomes; Enrichment analysis; Gene expression; Gene expression profiling; Gene prediction; Gene regulation; Genetic variation; Genetics; Genotype and phenotype; Genotyping; Population genetics; Nucleic acids; DNA; DNA polymorphism; Functional, regulatory and non-coding RNA; Nucleic acid sites, features and motifs; Read mapping; RNA; RNA secondary structure prediction; SNP detection; Transcription factors and regulatory sites; Proteins & Proteomes; Gene and protein families; Protein folding, stability and design; Protein folds and structural domains; Protein interactions; Protein modelling; Protein secondary structure prediction; Protein sequence analysis; Protein sites, features and motifs; Protein structural motifs and surfaces; Protein structure analysis; Protein structure prediction; Sequence analysis; Genome annotation; Mapping; PCR primer design; Phylogenetics; Protein feature detection; Sequence alignment; Sequence assembly; Sequence sites, features and motifs; Structural Biology; Molecular dynamics; Molecular modelling; Nucleic acid structure analysis; Small molecules; Structure analysis; Structure prediction; Systems Biology & Omics; Epigenomics; Genomics; Metabolomics; Metagenomics; Proteomics; Transcriptomics; Virology and vaccine design; Public health and epidemiology; Cell biology; Formatting; Image analysis; Machine learning; Molecular interactions, pathways and networks; Oncology; Pathology; Pathway or network prediction; Pathway or network visualisation; Phylogeny; Sequencing; Single cell transcriptome<label>'

  payload = create_payload(llm_name=llm_name)
  payload = add_system_message(payload, system_message)
  payload = add_user_message(payload, ask_message1)

  # 向llm发起提问
  response = ask_llm(llm_chat_rjurl, payload, headers)
  # 将回答写入数据中，继续提问
  llm_assistant_message = get_content_from_response(response,llm_name)
  payload = add_assistant_message(payload, llm_assistant_message)


  # 第二次对话
  # 填入新问题
  # ask_message2 = "The information about the tool is enclosed in triple backticks below.'''Tool Name: {}; Description: {}; Abstract: {}; Keywords: {};'''Please note that the labels you select must come from the 70 taxonomic labels I have provided. You do not necessarily need to choose labels from closely related fields, labels from related fields are acceptable. If you find that the labels you have selected are not among the 70 labels I have provided, please re-select suitable classification labels from the provided labels. If you extract a feature from the sample information but cannot find a suitable label in the classification labels to describe it, you can disregard the description of that feature.".format(
  ask_message2 = "The information about the tool is enclosed in triple backticks below.'''Tool Name: {}; Description: {}; Abstract: {}; Keywords: {};'''Please, based on this information, especially what has been presented in this work or by the authors, choose between 1 and 10 of the 70 taxonomic labels I have provided as suitable, appropriate and necessary for describing the tool. Please note that the labels you select must come from the 70 taxonomic labels I have provided. If you extract a feature from the sample information but cannot find a suitable label in the classification labels to describe it, you can disregard the description of that feature. Only when you find it hard to choose relevant labels, you do not necessarily need to choose labels from closely related fields, labels from related fields are acceptable. If you find that the labels you have selected are not among the 70 labels I have provided, please re-select suitable classification labels from the provided labels.".format(
  # ask_message2 = "The information about the tool is enclosed in triple backticks below.'''Tool Name: {}; Description: {}; Abstract: {}; Keywords: {};'''You can think step by step by first reading the information about the tool, then analysing each of the 70 taxonomic tags individually to see if they are relevant to the tool, and finally displaying the labels you think are relevant separated by semicolons.".format(
    article_info["tool_name"],article_info["description"],article_info["abstract"],article_info["keywords"]
  )
  payload = add_user_message(payload, ask_message2)

  # 向llm发起提问
  response = ask_llm(llm_chat_rjurl, payload, headers)
  # 将回答写入数据中，继续提问
  llm_assistant_message = get_content_from_response(response,llm_name)
  standard_labels_by_llm = get_standard_labels_in_response(llm_assistant_message)
  print(standard_labels_by_llm)
  return standard_labels_by_llm

if __name__ == '__main__':
    main()
  