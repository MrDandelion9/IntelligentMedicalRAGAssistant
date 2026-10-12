from FlagEmbedding import FlagReranker

def get_FlagReranker():
    return FlagReranker(
        model_name_or_path='/models/bge-reranker-base',
        use_fp16=False
    )