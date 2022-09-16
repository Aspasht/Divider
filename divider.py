import argparse
import time
import httpx
import asyncio
from threading import Thread
from multiprocessing import Process

include = [".json", ".txt", ".xml", ".jsp", ".exe", ".config", ".log", ".aspx", ".git", ".config.php", ".php",
           ".old.php", ".rhtml", ".php.sample", ".php}", ".xml.asp", ".cfg.php", "js.aspx", ".new.php", ".inc.html",
           ".jspx", ".mysqli", ".db", ".rsp.php", ".rsp", ".zip.php"]

urls = []


def get_target_file():
    with open(args.file, 'r') as f:
        for url in f:
            for ext in include:
                if url.endswith(ext + "\n"):
                    url.rstrip("\n")
                    if args.request ==False:
                        print(url, end=" ")
                    else:
                        pass
                    urls.append(url.strip())
                else:
                    pass


async def send_request():
    async with httpx.AsyncClient() as client:
        for url in urls:
            try:
                response = await client.get(url,follow_redirects=False)
                if (response.status_code != 400) and (response.status_code != 404) and (response.status_code != 301):
                    print(f'{url} {response.status_code}')
                else:
                    pass
            except:
                pass


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, help="Please add target file as argument!")
    parser.add_argument("-req", "--request", default=False,required=False, help="Send request for previously generated urls!")
    args = parser.parse_args()

    # Initial start time
    start = time.time()

    # Check passed arguments
    if args.file:
        get_target_file()
    else:
        pass

    if args.request == "True":
        asyncio.run(send_request())
    else:
        pass
    # Check process time
    end = time.time()
    time_taken = end - start

    print(f'Process finished in {time_taken:.2f}s !')
