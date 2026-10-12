import jieba
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from common.VectorStore import get_vector_store

# 中文停用词表（常见停用词，避免无意义词干扰BM25排序）
STOP_WORDS = set([
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都",
    "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会",
    "着", "没有", "看", "好", "自己", "这", "那", "他", "她", "它", "们",
    "这个", "那个", "什么", "哪", "怎么", "吗", "呢", "吧", "啊", "哦",
    "还", "被", "把", "让", "从", "对", "与", "但", "而", "或", "所",
    "为", "以", "及", "可", "可以", "能", "能够", "应该", "需要", "已经",
    "虽然", "如果", "因为", "所以", "只是", "还是", "不过", "然后",
    "之", "其", "中", "等", "等等", "即", "使", "向", "将", "按", "当",
    "于", "由", "比", "除了", "关于", "以及", "并且", "此外", "另外",
    "过", "着", "来", "去", "做", "作", "像", "如", "如同", "由于",
])
#对文档进行分词
#创建分词函数
def tokenizer(text):
    documents = jieba.cut(text)
    return [token for token in documents if token not in STOP_WORDS and len(token.strip()) > 1]
# 链接向量库
    vectorstore = get_vector_store()
def build_bm25_model(vectorstore):
    # 取出数据
    data = vectorstore.get()
    ids = data["ids"]
    docs = data["documents"]

    # for i in ids:
    #     print(i)
    # print(type(data))

    # 构造数据结构
    documents = [Document(id=ids[i], page_content=docs[i], metadata={"source": "medical.json"}) for i in
                 range(len(ids))]

    # 切割文本
    texts = [tokenizer(doc) for doc in docs]
    # 构建bm25模型
    bm25 = BM25Okapi(texts)
    return bm25, documents

#计算得bm25得分
def  bm25_retriever(bm25,documents,question,k=20):
    bm25_scores = bm25.get_scores(tokenizer(question))
    #为拿到的分数排序
    bm25_sorted_sorted = sorted(range(len(bm25_scores)), key=lambda k: bm25_scores[k], reverse=True)[:k]
    #获取前top-k文档
    bm25_results = [documents[i] for i in bm25_sorted_sorted]
    return bm25_results

    
