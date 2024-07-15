# LLM_dragger
 
## 1.原始文献数据预处理（师兄师姐都是给endnote）
endnote要导出规范化条目文件，我是自定义一个样式文件，配置导出格式，导出得到txt（每行包含文献条目信息），再拆成一个个json方便作为输入文件

### 执行代码
运行`endnote_bib2json.py`


## 2.文献更多信息嵌入

**核心代码是`tools/grobid_tei_xml_parser.py`**
Endnote里的信息只有标题、doi和摘要，但我们执行任务还需要全文、或特定文本（PTM任务中考虑放入Introduction最后一段）
如何拿到全文文本和特定文本？要有文献的PDF -> PDF用grobid转为XML文件 -> XML提取信息后嵌入到刚刚分开的每个文献的json文件里

使用`xml2json.py`，使用前准备好: 1.放有XML的文件夹路径  2.放有json的文件夹路径（会把数据写进这些json）修改`xml2json.py`里的路径


## 3.调用LLM

**核心代码是`batch_PTM_drag.py`**

##### 准备内容: Prompt模板&自定义Prompt特定内容(即上述的文献信息)
1. 将`batch_PTM_drag.py`中的`template_prompt_json_path`对象改为Prompt模板文件路径，在这个文件中自定义prompt通用内容
2. 将`batch_PTM_drag.py`中的`custom_data_dir_path`对象改为存有要填入prompt的自定义内容的文件夹目录
3. 指定输出结果路径`save_path`

修改这三处对象后，运行`batch_PTM_drag.py`等待程序运行，查看结果

## 4.结果整理
第3步完成后的结果是一个文章存一个json，仍然是分开的，为了方便统计和浏览，将多个json的信息提取到一个csv表格里，运行`json2csvc.py`



