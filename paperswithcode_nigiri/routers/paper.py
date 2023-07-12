from typing import List

from fastapi import APIRouter

from paperswithcode_nigiri.services.notifier import notice_slack
from paperswithcode_nigiri.services.searcher import search_papers
from paperswithcode_nigiri.services.summarizer import summarize_abstract

router = APIRouter()


@router.get("/{keyword}", response_model=List[str])
async def get_papers(keyword: str):
    papers = search_papers(keyword)
    summaries = [summarize_abstract(paper["abstract"]) for paper in papers]
    notice_slack(summaries)
    return summaries
