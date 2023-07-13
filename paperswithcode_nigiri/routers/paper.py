import os

from fastapi import APIRouter

from paperswithcode_nigiri.services.notifier import notice_slack
from paperswithcode_nigiri.services.searcher import search_papers
from paperswithcode_nigiri.services.summarizer import make_summary

router = APIRouter()


@router.get("/paper/", response_model=list[str])
async def get_papers(
    keyword: str,
    page: int = 1,
    items_per_page: int = 1,
    notice: None | str = None,
):
    papers = search_papers(keyword, page=page, items_per_page=items_per_page)
    summaries = []
    for paper in papers:
        summary = make_summary(paper)

        if notice is not None:
            if notice == "slack":
                notice_slack(webhook_url=os.getenv("SLACK_WEBHOOK_URL"), message=summary)
        summaries.append(summary)
    return summaries
