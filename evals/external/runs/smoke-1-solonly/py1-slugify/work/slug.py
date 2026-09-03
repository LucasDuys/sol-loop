import re


def slugify(text):
    return re.sub(r"[\W_]+", "-", text.lower()).strip("-")
