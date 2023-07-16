import json
import os

import openai

PROMPT = """
    あなたは世界有数の研究者です。以下の論文のタイトルとアブストラクトを日本語に翻訳してください。
    その後要約してください。またあなたが知っている類似論文のタイトルを教えてください。
    最終的なアウトプットは以下キーを持つ辞書形式でお願いします。
    アウトプットに対して python の json.loads(output) をするので、そこでエラーが出ないようにして下さい。

    "title": タイトルの日本語翻訳結果を記載,
    "abstract": アブストラクトの日本語翻訳結果を記載,
    "summary": 要約結果を箇条書き(リスト形式)で何点か記載する,

    Title : {title}
    Abstract : {abstract}
"""


def get_meta_info(paper: dict) -> dict:
    return {"meta": paper}


def make_summary(paper: dict, model_name: str= "gpt-3.5-turbo") -> dict:
    summary_by_llm = summarize(
        title=paper["title"],
        abstract=paper["abstract"],
        openai_api_key=str(os.getenv("OPENAI_API_KEY")),
        model_name=model_name,
        temperature=float(str(os.getenv("TEMPERATURE"))),
    )
    meta_info = get_meta_info(paper=paper)
    output_summary = {**summary_by_llm, **meta_info}
    return output_summary


def summarize(
    title: str,
    abstract: str,
    openai_api_key: str,
    model_name: str = "gpt-3.5-turbo",
    temperature: float = 0.5,
) -> dict:
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
    summary = response["choices"][0]["message"]["content"]
    summary = json.loads(summary)
    return summary
