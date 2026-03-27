import nltk

def download_nltk_resources():
    resources = [
        "punkt",
        "punkt_tab",
        "perluniprops",
        "nonbreaking_prefixes"
    ]

    for resource in resources:
        try:
            nltk.data.find(f"tokenizers/{resource}")
        except LookupError:
            nltk.download(resource)