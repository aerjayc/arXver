import requests
import re


def check_archive_today(url,
                        domain="archive.md",
                        user_agent="arXver/0.1.0"):
    """
    Checks if the url is already archived in archive.md
    """
    # validate url

    # get timegate url (use HEAD request)
    archive_today_url = f"http://{domain}/timegate/{url}"

    headers = {'User-Agent': user_agent}

    response = requests.head(archive_today_url, headers=headers)
    if response == 404:
        return False

    # parse response to get first memento
    links = link_header_parser(response.headers['Link'])
    if not links:
        return None

    if 'first memento' in links:
        return links['first memento']
    elif 'first last memento' in links:
        return links['first last memento']
    else:
        for rel, url in links:
            if 'memento' in rel:
                return links[rel]

    return None


def link_header_parser(string):
    """
    Parses the Link header, according to the spec:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Link
    """
    exp = re.compile(r'<(\S+)>;\s*rel="([^"]+)",?\s*')

    # if want to catch "'" users, use this:
    # exp = re.compile(r'<(\S+)>;\s*rel=("([^"]+)"|'([^"]+)'),?\s*')

    matches = re.findall(exp, string)

    return dict((rel, url) for url, rel in matches)

