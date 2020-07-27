import re


def link_header_parser(string):
    """Parse Link header field."""

    exp = re.compile(r'<(\S+)>;\s*rel="([^"]+)",?\s*')

    # if want to catch "'" users, use this:
    # exp = re.compile(r'<(\S+)>;\s*rel=("([^"]+)"|'([^"]+)'),?\s*')

    matches = re.findall(exp, string)

    return dict((rel, url) for url, rel in matches)


def validate_url(string):
    """Return True if `string` is a valid url, else return False.

    Based on https://stackoverflow.com/a/7160778/11905538
    """

    regex = re.compile(
        r'^(?:http|ftp)s?://'   # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'           # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'            # optional port
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE)

    return re.match(regex, string) is not None

