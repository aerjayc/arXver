from wayback_machine import get_fast_wayback_machine
import time


def check_urls(urls):

    for url in urls:
        print(f"{url} - ", end="", flush=True)
        archive = get_fast_wayback_machine(url)

        if archive:
            print(f"✔️  ")
        if not archive:
            # archive it
            print(f"❌ ")

        time.sleep(3)

    return archive
