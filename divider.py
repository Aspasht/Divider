import argparse
import grequests
import concurrent.futures
import requests
from urllib.parse import urlparse
import time
import httpx
import asyncio
import re
from fetchUrls import get_urls, collected_urls

include = [".json", ".txt", ".xml", ".jsp", ".exe", ".config", ".log", ".aspx", ".git", ".config.php", ".php",
           ".old.php", ".rhtml", ".php.sample", ".php}", ".xml.asp", ".cfg.php", "js.aspx", ".new.php", ".inc.html",
           ".jspx", ".mysqli", ".db", ".rsp.php", ".rsp", ".zip.php", ".tar", ".tar.gz", ".sh", ".py", ".shtml"]

urls = []
unique_urls = []
output = []


def get_target_file():
    if args.fetch:
        target_file = 'collected_urls.txt'
        get_ext(target_file)
    else:
        target_file = args.file
        get_ext(target_file)


def get_ext(url_file):
    with open(url_file, 'r') as f:
        for url in f:
            for ext in include:
                if url.endswith(ext + "\n"):
                    url.rstrip("\n")
                    urls.append(url.strip())
                else:
                    pass


def find_unique():
    for url in urls:
        if url not in unique_urls:
            unique_urls.append(url)
            if not args.request:
                if not args.grequest:
                    if args.output:
                        output.append(url)
                print(url)
            else:
                pass
        else:
            pass


# async def send_request():
#     async with httpx.AsyncClient() as client:
#         for url in unique_urls:
#             try:
#                 response = await client.get(url, follow_redirects=True, timeout=1)
#                 if (response.status_code != 400) and (response.status_code != 404) and (response.status_code != 301):
#                     output.append(url)
#                     print(f'{url} Status:{response.status_code}')
#                 else:
#                     pass
#             except:
#                 pass
#                 #print(f"[-] Failed to parse {url} !")


def load_url(url):
    response = requests.get(url)
    code = str(response.status_code)
    if (response.status_code != 400) and (response.status_code != 404) and (response.status_code != 301):
        output.append(f'{url} Status:{response.status_code}')
        print(f'{url} Status:{response.status_code}')
        # print(output)
    else:
        pass
    # print(f"{res.url} {code}")


def send_request():
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(load_url, url): url for url in unique_urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                load_url(url)


def use_grequests():
    req = (grequests.get(url) for url in unique_urls)
    res = grequests.map(req)
    rex = re.findall(r'\d+', str(res))

    l = []
    for a, b in zip(rex, list(urls)):
        l.append(b + " " + "Status:" + str(a))

    for url in l:

        if not url.endswith("Status:404"):
            output.append(url)
            print(url)
        else:
            pass


def save_output(data):
    filename = args.output
    with open(filename, "a") as f:
        for url in data:
            f.write(url + "\n")


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=False, help="Please add target file as argument!")
    parser.add_argument("--req", "--request", dest="request", action='store_true', required=False,
                        help="Send request for previously generated urls!")
    parser.add_argument("--greq", "--grequest", dest="grequest", action="store_true", required=False,
                        help="Send request for previously generated urls using grequest!")
    parser.add_argument("--fetch", "--fetch", dest="fetch", default=False, required=False,
                        help="Fetch urls using tools like waybackurls and gau {must be preinstalled}! ")
    parser.add_argument("-o", "--output", required=False,
                        default=False, help="Save output to a file!")

    args = parser.parse_args()

    # Initial start time
    start = time.time()

    # Check if file passed as an arguments or not
    file_input = args.file

    if file_input:
        get_target_file()
        find_unique()
    elif args.fetch:
        get_urls(args.fetch)
        with open("collected_urls.txt", "w") as f:
            for url in collected_urls:
                f.write(url)

        get_target_file()
        find_unique()
    else:
        print("Please check help section using [-h] or [--help] flag!")
        print("Please provide either [-f] or [--fetch] for initializing process!")

    # Check provided flags to request
    if args.request:
        # asyncio.run(send_request())
        send_request()
    elif args.grequest:
        use_grequests()
    else:
        pass

    # save outputs
    if args.output:
        save_output(output)
    else:
        pass

    time_taken = time.time() - start

    print(f'Process finished in {time_taken:.2f}s !')
