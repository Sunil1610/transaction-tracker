
import re
import unicodedata


def remove_leading_special_chars(s):
    return re.sub(r"^[^A-Za-z0-9]+", "", s)

def remove_ending_special_char(s):
    return ''.join(c for c in s if not unicodedata.category(c).startswith('C'))

def replace_whitespace(s, char):
    s = re.sub(r'\s+', char, s)
    s = re.sub(r'\\n+', char, s)
    return s