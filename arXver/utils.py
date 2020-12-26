import re

# from https://stackoverflow.com/a/29288898
URL_RAW_REGEX = (r"(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)"
                 r"(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|"
                 r"[-A-Z0-9+&@#/%=~_|$?!:,.])*"
                 r"(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|"
                 r"[A-Z0-9+&@#/%=~_|$])")


def link_header_parser(string):
    """Parse Link header field."""

    exp = re.compile(r'<(\S+)>;\s*rel="([^"]+)",?\s*')

    # if want to catch "'" users, use this:
    # exp = re.compile(r'<(\S+)>;\s*rel=("([^"]+)"|'([^"]+)'),?\s*')

    matches = re.findall(exp, string)

    return dict((rel, url) for url, rel in matches)


def validate_url(string):
    """Return True if `string` is a valid url, else return False."""

    regex = re.compile("^" + URL_RAW_REGEX + "$", re.IGNORECASE)

    return re.match(regex, string) is not None

def extract_urls(fname):
    """Returns a list of all urls in a file given its filename"""

    pattern = re.compile(URL_RAW_REGEX, re.IGNORECASE)
    urls = []
    with open(fname, 'r') as f:
        for line in f.readlines():
            urls.extend(re.findall(pattern, line))

    return urls

