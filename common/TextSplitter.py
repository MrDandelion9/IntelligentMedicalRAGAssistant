from langchain_text_splitters import RecursiveCharacterTextSplitter
#文本分割
def text_splitter():
    splitter=RecursiveCharacterTextSplitter(
    chunk_size=180,
    chunk_overlap=30,
    #分割
    separators=[
        "。", "，", "？", "、", "：", "；", "！", "“", "”", "（",
        "）", "《", "》", "……", "——", "‘", "’", "·", "【", "】",
    ],
    length_function=len,
)
    return splitter