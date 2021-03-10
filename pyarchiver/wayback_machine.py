import requests
import urllib.parse
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from . import utils
from . import user_agent


def query_wayback(url, fastLatest=False, limit=None, statuscode=None,
                  user_agent=user_agent):
    """Return a dict of archive URLS and metadata."""

    # validate url
    assert utils.validate_url(url), f'Invalid URL: "{url}"'

    # get fast url
    wayback_endpoint = 'https://web.archive.org/cdx/search/cdx'
    params = {'url': url,
              'fastLatest': fastLatest,
              'output': 'json'
              }
    if limit:
        params['limit'] = limit
    if statuscode:
        params['filter'] = f'statuscode:{statuscode}'

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
    response.raise_for_status()

    results = []
    if response.json():
        column_names = response.json()[0]
        for row in response.json()[1:]:
            result = dict(zip(column_names, row))
            archive_url = (f"https://web.archive.org/web/{result['timestamp']}/"
                          + result['original'])
            results.append((archive_url, result['statuscode']))

    return results

def submit_wayback(url, user_agent=user_agent, session=None):

    # validate url
    assert utils.validate_url(url), f'Invalid URL: "{url}"'

    if session is None:
        session = requests.Session()

    base_url = 'https://web.archive.org/web/'
    payload = {'url_preload': url}
    headers = {'User-Agent': user_agent}
    response = session.post(base_url, data=payload, headers=headers)
    if response.status_code == 523:
        print('Status Code 523: Origin Is Unreachable.',
              'Maybe', url, 'is down?')
        return None

    response.raise_for_status()

    return response

