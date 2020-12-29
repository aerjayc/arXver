from pyarchiver import wayback_machine, utils
from pyarchiver import user_agent, common_user_agent
import os.path
from pathlib import Path
import time
import argparse


def submit_unarchived(urls, save_dir=None, overwrite=False, force=False,
                      query_pause=2, submit_pause=5, user_agent=user_agent):

    if save_dir is not None:
        Path(save_dir).mkdir(parents=True, exist_ok=True)

    archived_urls = dict()
    for i, url in enumerate(urls):
        print(url, '- ', end='', flush=True)
        results = wayback_machine.query_wayback(url, limit=-1, statuscode=200,
                                                user_agent=user_agent)
        time.sleep(query_pause)
        if results:
            archived_urls[url] = results[0][0]
            print('Already archived at', archived_urls[url])

            if not force:
                continue

        response = wayback_machine.submit_wayback(url, user_agent=user_agent)
        archived_urls[url] = response.url
        print('Submitted to', response.url)
        if i < (len(urls) - 1):     # don't sleep after the last url
            time.sleep(submit_pause)

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('urls_file', help='file containing urls to archive')
    parser.add_argument('-s', '--save', metavar='DIR',
                        help='where to save the raw htmls')
    parser.add_argument('-f', '--force', action='store_true',
                        help='submit url even if already archived')
    parser.add_argument('-w', '--overwrite', action='store_true',
                        help='overwrite file if it exists')
    parser.add_argument('-t', '--time_delay', metavar='SECS', default=5, type=int,
                        help='time delay between archive submissions')
    parser.add_argument('-u', '--user_agent')
    parser.add_argument('--spoof', action='store_true',  help='use a common user agent')
    args = parser.parse_args()

    if args.spoof:
        user_agent = common_user_agent
    urls = utils.extract_urls(args.urls_file)

    submit_unarchived(urls, save_dir=args.save, submit_pause=args.time_delay,
                      force=args.force, overwrite=args.overwrite,
                      user_agent=user_agent)

