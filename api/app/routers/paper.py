from fastapi import APIRouter

from app.services.searcher import search_papers

router = APIRouter()


@router.get("/paper/", response_model=list[dict])
async def get_paper(
    keyword: str,
    page: int = 1,
    items_per_page: int = 1,
):
    papers = search_papers(keyword, page=page, items_per_page=items_per_page)
    return papers
