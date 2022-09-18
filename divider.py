import argparse
import grequests
import time
import httpx
import asyncio
import re

include = [".json", ".txt", ".xml", ".jsp", ".exe", ".config", ".log", ".aspx", ".git", ".config.php", ".php",
           ".old.php", ".rhtml", ".php.sample", ".php}", ".xml.asp", ".cfg.php", "js.aspx", ".new.php", ".inc.html",
           ".jspx", ".mysqli", ".db", ".rsp.php", ".rsp", ".zip.php", ".tar", ".tar.gz", ".sh", ".py"]

urls = []
unique_urls = []
output = []


def get_target_file():
    with open(args.file, 'r') as f:
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
            if (args.request == False):
                if (args.grequest == False):
                    output.append(url)
                    print(url)
            else:
                pass
        else:
            pass


async def send_request():
    async with httpx.AsyncClient() as client:
        for url in unique_urls:
            try:
                response = await client.get(url, follow_redirects=False, timeout=1)
                if (response.status_code != 400) and (response.status_code != 404) and (response.status_code != 301):
                    output.append(url)
                    print(f'{url} Status:{response.status_code}')
                else:
                    pass
            except:
                pass


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


def save_output():
    with open(args.output, "w") as f:
        for url in output:
            f.write(url + "\n")


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, help="Please add target file as argument!")
    parser.add_argument("-req", "--request", type=bool, default=False, required=False,
                        help="Send request for previously generated urls!")
    parser.add_argument("-greq", "--grequest", type=bool, default=False, required=False,
                        help="Send request for previously generated urls using grequest!")
    parser.add_argument("-o", "--output", default=False, required=False,
                        help="Save output to a file!")
    args = parser.parse_args()

    # Initial start time
    start = time.perf_counter()

    # Check if file passed as an arguments or not
    if args.file:
        get_target_file()
        find_unique()
    else:
        pass

    # Check provided flags to request
    if args.request == True:
        asyncio.run(send_request())
    elif args.grequest == True:
        use_grequests()
    else:
        pass

    # save outputs
    if args.output:
        save_output()
    else:
        pass

    time_taken = (time.perf_counter() - start) / 60

    print(f'Process finished in {time_taken:.2f}s !')
