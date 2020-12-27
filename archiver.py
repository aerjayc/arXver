from arXver import wayback_machine
from arXver import utils
import os.path
from pathlib import Path
import time


def submit_unarchived(urls, save_dir=None, overwrite=False,
                      query_pause=2, submit_pause=5):

    if save_dir is not None:
        print(save_dir, 'does not exist. Creating directory...')
        Path(save_dir).mkdir(parents=True, exist_ok=True)

    archived_urls = dict()
    for url in urls:
        print(url, '- ', end='', flush=True)
        results = wayback_machine.query_wayback(url, fastLatest=True, limit=1, statuscode=200)
        time.sleep(query_pause)
        if results:
            archived_urls[url] = results[0][0]
            print('Already archived at', archived_urls[url])
            continue

        response = wayback_machine.submit_wayback(url)
        time.sleep(submit_pause)
        archived_urls[url] = response.url
        print('Submitted to', response.url)

        if save_dir is not None:
            filename = utils.url_to_filename(url, extension='.html')
            filepath = os.path.join(save_dir, filename)

            if os.path.isfile(filepath) and not overwrite:
                print('\tSkipping', filename, '(file exists)...')
                continue
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print('\tSaved page to', filepath)

    return archived_urls
