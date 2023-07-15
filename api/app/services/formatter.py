import re


def format_summary(summary):
    forrmat_fn = lambda summary: ("・" + "\n    ・".join(summary["summary"]))  # noqa

    formatted_summary = f"""
    Title:
    {summary["title"]}

    Abstract:
    {summary["abstract"]}

    Summary:
    {forrmat_fn(summary)}

    Meta:
    ・url: {summary["meta"]["url_pdf"]}
    ・repo: {summary["meta"]["url_repo"]}
    ・star: {summary["meta"]["stars"]}
    ・framework: {summary["meta"]["framework"]}
    ・title: {summary["meta"]["title"]}
    """
    return re.sub(" ", "", formatted_summary)
