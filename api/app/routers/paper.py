from fastapi import APIRouter

from app.services.searcher import search_papers
from app.services.summarizer import make_summary

router = APIRouter()


@router.get("/paper/", response_model=list[str])
async def get_papers(
    keyword: str,
    page: int = 1,
    items_per_page: int = 1,
):
    papers = search_papers(keyword, page=page, items_per_page=items_per_page)
    summaries = [make_summary(paper) for paper in papers]
    return summaries
