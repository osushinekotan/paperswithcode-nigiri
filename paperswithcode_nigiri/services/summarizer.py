import os

import openai

PROMPT = """
    あなたは世界有数の研究者です。以下の論文のタイトルとアブストラクトを日本語に翻訳してください。
    その後要約してください。またあなたが知っている類似論文のタイトルを教えてください。
    出力は以下のフォーマットに従ってください。
    - Title: セクションに日本語翻訳結果を記載
    - Abstract: セクションに日本語翻訳結果を記載。
    - Summary: セクションに要約結果を箇条書きで何点か記載
    - Reference: セクションに類似論文のタイトルを箇条書きで何点か記載

    Title : {title}
    
    Abstract : 
    {abstract}

    フォーマット : 
    ```
    Title
    Abstract
    Summary
    Reference
    ```
"""


def get_meta_info(paper: dict) -> str:
    keys = ["title", "url_abs", "url_pdf", "url_repo", "stars", "framework"]
    info = "\nMeta:\n"
    for k in keys:
        info += f"- {k}: {paper[k]}\n"
    return info


def make_summary(paper: dict) -> str:
    summary_by_llm = summarize(
        title=paper["title"],
        abstract=paper["abstract"],
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model_name=os.getenv("LLM_MODEL"),
        temperature=float(str(os.getenv("TEMPERATURE"))),
    )
    meta_info = get_meta_info(paper=paper)
    pre_line = "*" * 150
    formatted_summary = "\n" + pre_line + "\n" + summary_by_llm + "\n" + meta_info

    return formatted_summary


def summarize(
    title: str,
    abstract: str,
    openai_api_key: str,
    model_name: str = "gpt-3.5-turbo",
    temperature: float = 0.5,
) -> str:
    """
    OpenAIのLLMを使用して、論文のアブストを要約する。

    Args:
        title (str): タイトル
        abstract (str): 要約するアブストの本文
        openai_api_key (str): OpenAI API
        model_name (str): LLM name
        temperature (float): 温度パラメタ

    Returns:
        str: 要約結果
    """
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(  # type: ignore
        model=model_name,
        messages=[
            {"role": "user", "content": PROMPT.format(title=title, abstract=abstract)},
        ],
        temperature=temperature,
    )
    return response["choices"][0]["message"]["content"]
