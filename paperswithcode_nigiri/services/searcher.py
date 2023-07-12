import requests

from paperswithcode_nigiri.const import PWC_SEARCH_ENDPINT


def get_params(page: int, items_per_page: int) -> dict:
    params = {"page": str(page), items_per_page: "items_per_page"}
    return params


def search_papers(
    keyword: str,
    page: int = 1,
    items_per_page: int = 10,
) -> list[dict]:
    """
    与えられたキーワードを使用して「Papers With Code」で検索を行い、タイトル、抄録、関連するURLを含む論文情報のリストを返す関数

    Args:
        client (PapersWithCodeClient): Papers With Code APIとやり取りするためのクライアントインスタンス。
        keyword (str): 検索に使用するキーワード。
        page (int, optional): 取得するページ番号。デフォルトは1。
        items_per_page (int, optional): ページあたりに表示する項目の数。デフォルトは10。

    Returns:
        list[dict]: 各論文に関する情報を含む辞書のリスト。各辞書には'title'、'abstract'、
                    'url_abs'、'url_pdf'、'url_repo'、'stars'、'framework'などのキーが含まれてる
    """

    params = get_params(page, items_per_page=items_per_page)
    papers = requests.get(PWC_SEARCH_ENDPINT.format(keyword=keyword), params=params).json()
    paper_informations = []
    for result in papers.results:
        paper = result.paper
        repository = result.repository
        paper_info = dict(
            title=paper.title,
            abstract=paper.abstract,
            url_abs=paper.url_abs,
            url_pdf=paper.url_pdf,
            url_repo=repository.url,
            stars=repository.stars,
            framework=repository.framework,
        )
        paper_informations.append(paper_info)
    return paper_informations
