import openai

PROMPT = """
    あなたは世界有数の研究者です。以下の論文のアブストラクトを日本語に翻訳してください。
    その後要約してください。またあなたが知っている類似論文のタイトルを教えてください。
    出力は以下のフォーマットに従ってください。
    - Abstract セクションに日本語翻訳結果を記載
    - Summary セクションに要約結果を箇条書きで何点か記載
    - Reference セクションに類似論文のタイトルを箇条書きで何点か記載

    アブストラクト : 
    ```
    {}
    ```

    フォーマット : 
    ```
    Abstract
    Summary
    Reference
    ```
"""


def summarize_abstract(
    abstract: str,
    openai_api_key: str,
    model_name: str = "gpt-3.5-turbo",
    temperature: float = 0.5,
) -> str:
    """
    OpenAIのLLMを使用して、論文のアブストを要約する。

    Args:
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
            {"role": "user", "content": PROMPT.format(abstract)},
        ],
        temperature=temperature,
    )
    return response["choices"][0]["message"]["content"]
