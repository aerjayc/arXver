import re
import requests


def get_first_archive_today(url,
                            domain="archive.md",
                            user_agent="arXver/0.2.0"):
    """Return URL of the first and last archive in archive.today.

    If `url` is an invalid URL, the function raises an AssertionError.
    If archive.today responds with status code 404, the function returns False.
    Else, if a memento is found, it returns the URL of the earliest one.
    If none are found, it returns None.
    """

    # validate url
    assert validate_url(url), f'Invalid URL: "{url}"'

    # get timegate url (use HEAD request)
    timegate_url = f'http://{domain}/timegate/{url}'

    headers = {'User-Agent': user_agent}

    response = requests.head(timegate_url, headers=headers)
    if response.status_code == 404:
        return False

    # parse response to get first memento
    links = link_header_parser(response.headers['Link'])
    if not links:
        return None

    if 'first memento' in links:
        return links['first memento']

    if 'first last memento' in links:   # when there is only 1 memento
        return links['first last memento']

    for rel, archive_url in links.items():
        # in case there is a `rel` with substring 'memento' aside from above
        if 'memento' in rel:
            return archive_url

    return None


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
