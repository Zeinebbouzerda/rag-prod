def clean(text: str) -> str:
    text = re.sub(r"\A---.*?---\s*", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"\{\*.*?\*\}", "", text)
    text = re.sub(r"^///.*$", "", text, flags=re.M)
    text = re.sub(r"[ \t]*\{\s*#[^}]*\}", "", text)        # ancres { #xxx }
    text = re.sub(r"^:::.*$", "", text, flags=re.M)         # directives ::: module
    text = re.sub(r"</?(small|abbr|details|summary)[^>]*>", "", text)  # balises HTML
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()