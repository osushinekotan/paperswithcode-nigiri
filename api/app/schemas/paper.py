from pydantic import BaseModel


class PaperItem(BaseModel):
    keyword: str
    page: int = 1
    items_per_page: int = 1
