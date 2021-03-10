import re
from urllib.parse import urlparse

# from https://stackoverflow.com/a/6041965/15116703 (modified)
URL_RAW_REGEX = "(?P<protocol>http|ftp|https)(://(?:www\.)?)(?P<domain>[\w_-]+(?:(?:\.[\w_-]+)+))(?P<relpath>[\w.,@?^=%&:/~+#*\-]*[\w@?^=%&/~+#-])?"


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

def extract_urls(string):
    """Returns a list of all urls in a string"""

    pattern = re.compile(URL_RAW_REGEX, re.IGNORECASE)
    urls = []
    for word in string.split():
        urls.extend(re.findall(pattern, word))

    return urls

def extract_urls_from_file(fname):
    """Returns a list of all urls in a file given its filename"""

    pattern = re.compile(URL_RAW_REGEX, re.IGNORECASE)
    urls = {}
    with open(fname, 'r') as f:
        for url in extract_urls(f.read()):
            domain = url[2]
            if domain not in urls:
                urls[domain] = []
            urls[domain].append(''.join(url))

    return urls

def url_to_filename(url, extension=None, sep=' ', ignore_fragment=False):
    """Converts a URL to a legal filename"""

    parsed = urlparse(url)

    # strip protocol and www.
    if parsed.netloc.startswith('www.'):
        filename = parsed.netloc[4:]
    else:
        filename = parsed.netloc

    filename += parsed.path + parsed.params + parsed.query
    if not ignore_fragment:
        filename += parsed.fragment

    filename = re.sub(r'[\/:*"<>|]', sep, filename)
    filename = re.sub(rf'\{sep}' + '{2,}', sep, filename)    # remove extra `sep`s
    # TODO: remove only the `sep`s that were introduced, and not those from the
    #       original string

    filename = filename.strip()
    if extension:
        if not extension.startswith('.'):
            filename += '.'
        filename += extension

    return filename
