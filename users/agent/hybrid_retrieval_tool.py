from langchain_core.tools import tool
from pydantic import BaseModel,Field

from common.VectorStore import get_vector_store
from users.utils import BM25Utils, RRFUtils, Rerank


#将检索方法改为类方法
class HybridRetriever:
    #向量检索初始化
    def __init__(self):
        self.vectorstore = get_vector_store()
        self.vector_retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 20},
        )
    #bm25检索初始化
        self.bm25, self.documents = BM25Utils.build_bm25_model(self.vectorstore)
    #方法
    # 打印检索结果
    def print_retriever(self,source,docs):
        for doc in docs:
            print(source, doc.page_content)
            print("================================")
        return docs
    def search(self, question):
        vector_results = self.vector_retriever.invoke(question)
        print_vectors_results = self.print_retriever("向量检索：",vector_results)
        bm25_results = BM25Utils.bm25_retriever(self.bm25, self.documents, question, k=20)
        print_bm25_results = self.print_retriever("bm25检索：", bm25_results)
        rrf_results = RRFUtils.rrf_retriever(vector_results, bm25_results)
        print_rrf_results = self.print_retriever("rrf融合：",rrf_results)
        return rrf_results


#将重排序转化为类
class Reranker:
    def __init__(self):#属性，初始化时执行
        self.reranker = Rerank.get_FlagReranker()
    def rerank(self,data,k=8):#方法
        #获取问题与检索结果
        question = data["question"]
        results = data["context"]#document对象
        history = data["history"]
        docs=[]
        for result in results:
            docs.append((question,result.page_content))
        #获取得分
        rerank_scores = self.reranker.compute_score(docs)#list
        #和文档进行绑定
        rerank_results = []
        for doc,score in zip(results,rerank_scores):
            rerank_results.append({
                "docs":doc,
                "score":score
            })
        #再取top-k
        rerank_results = sorted(rerank_results, key=lambda x: x["score"], reverse=True)[:k]
        for result in rerank_results:
            print("重排序结果：",result["docs"].page_content)
            print("================================")
        return {
            "question":question,
            "context":[result["docs"] for result in rerank_results],
            "history": history
        }


hybrid_retriever = HybridRetriever()  # 混合检索初始化
reranker = Reranker()#重排序初始化
#混合检索tool
class HybridRetrievalTool(BaseModel):
    question: str = Field(..., description="用户输入的问题")

@tool(
    name_or_callable="hybrid_retrieval_tool",
    description="""
    这是医学知识库混合检索工具。

    适用于：
    - 疾病知识查询
    - 症状原因分析
    - 医学概念解释
    - 药物和治疗相关问题

    工具内部已经完成：
    1. 向量语义检索
    2. BM25关键词检索
    3. RRF融合排序
    4. Reranker重排序

    返回top相关医学文档。

    调用工具后，应基于返回内容生成最终回答。
    """,
    args_schema=HybridRetrievalTool,#参数校验
)
def hybrid_retrieval_tool(question: str) -> str:
    docs = hybrid_retriever.search(question)#检索结果
    docs = reranker.rerank({
        "question": question,
        "context": docs,
        "history":[]
    })#调用重排序

    return "\n\n".join(
        f"[参考文档{i}] {doc.page_content}"
        for i, doc in enumerate(docs["context"], start=1)
    )