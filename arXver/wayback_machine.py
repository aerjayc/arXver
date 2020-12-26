import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from utils import validate_url


def get_fast_wayback_machine(url,
                             user_agent="arXver/0.3.0"):
    """Return a dict of archive URLS and metadata."""

    # validate url
    assert validate_url(url), f'Invalid URL: "{url}"'

    # get fast url
    wayback_endpoint = 'http://web.archive.org/cdx/search/cdz'
    params = {'url': url,
              'fastLatest': True,
              'output': 'json'
              }

    # create Session
    # based on https://stackoverflow.com/a/35504626/11905538
    sess = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    sess.mount('http://', HTTPAdapter(max_retries=retries))
    sess.mount('https://', HTTPAdapter(max_retries=retries))

    get_kwargs = {'timeout': 30,
                  'allow_redirects': True,
                  'params': params,
                  'headers': {'User-Agent': user_agent}
                  }
    response = sess.get(wayback_endpoint, **get_kwargs)

    return response.json()
