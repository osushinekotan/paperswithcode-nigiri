from fastapi import APIRouter

from app.schemas.summary import SummaryItem
from app.services.formatter import format_summary
from app.services.searcher import search_papers
from app.services.summarizer import make_summary

router = APIRouter()


@router.get("/summary/", response_model=list[dict])
async def get_summary(
    keyword: str,
    page: int = 1,
    items_per_page: int = 1,
    openai_model: str = "gpt-3.5-turbo",
):
    papers = search_papers(keyword, page=page, items_per_page=items_per_page)
    summaries = [make_summary(paper, model_name=openai_model) for paper in papers]
    return summaries


@router.post("/summary/")
async def post_summary(item: SummaryItem):
    papers = search_papers(
        item.keyword, page=item.page, items_per_page=item.items_per_page
    )
    formatted_summaries = [
        format_summary(make_summary(paper, model_name=item.openai_model))
        for paper in papers
    ]
    return formatted_summaries
