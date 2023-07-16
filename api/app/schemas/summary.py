from pydantic import BaseModel


class SummaryItem(BaseModel):
    keyword: str
    page: int = 1
    items_per_page: int = 1
    openai_model: str = "gpt-3.5-turbo"
