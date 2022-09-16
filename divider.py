import argparse
import time


include = [".json", ".txt", ".xml", ".jsp", ".exe", ".config", ".log", ".aspx", ".git", ".config.php", ".php",
           ".old.php", ".rhtml", ".php.sample", ".php}", ".xml.asp", ".cfg.php", "js.aspx", ".new.php", ".inc.html",
           ".jspx", ".mysqli", ".db", ".rsp.php", ".rsp", ".zip.php"]


def get_target_file():
    with open(args.file, 'r') as f:
        for url in f:
            for ext in include:
                if url.endswith(ext + "\n"):
                    url.rstrip("\n")
                    print(url,end=" ")
                else:
                    pass


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True,help="Please add target file as argument!")
    args = parser.parse_args()

    # Initial start time
    start = time.time()

    # Check passed arguments
    if args.file:
        get_target_file()
        # main()
    else:
        pass

    # Check process time
    end = time.time()
    time_taken = end - start

    print(f'Process finished in {time_taken:.2f}s !')
