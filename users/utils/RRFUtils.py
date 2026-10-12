#rrf融合
def rrf_retriever(vector_results,bm25_results,rank=60):
    scores_list={}
    docs_list={}
    for index,item in enumerate(vector_results,start=1):
        scores_list[item.id] = scores_list.get(item.id,0) + 1/(rank + index)
        docs_list[item.id] = item
    for index,item in enumerate(bm25_results,start=1):
        scores_list[item.id] = scores_list.get(item.id,0) + 1/(rank + index)
        docs_list[item.id] = item
    # 排序
    sorted_ids = sorted(scores_list, key=lambda x: scores_list[x], reverse=True)
    #取出topk文档
    return [docs_list[i] for i in sorted_ids[:20]]