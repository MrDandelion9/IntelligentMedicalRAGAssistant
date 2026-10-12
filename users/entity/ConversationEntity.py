from pydantic import BaseModel,Field

class Conversation(BaseModel):
    question: str = Field(..., description="问题")
    parent_id: int = Field(..., description="历史对话id")
    answer: str = Field(..., description="答案")