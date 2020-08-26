from wayback_machine import get_fast_wayback_machine
import time


def check_urls(urls, sleep_duration=5):

    for url in urls:
        print(f"{url} - ", end="", flush=True)
        archive = get_fast_wayback_machine(url)

        if archive:
            print(f"✔️  ")
        if not archive:
            # archive it
            print(f"❌ ")

        time.sleep(sleep_duration)
