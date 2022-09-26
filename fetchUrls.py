import os
import subprocess
import sys
import time

# target=str(sys.argv[1])
collected_urls=[]

def get_urls(target):
    #start=time.time()

    # Using waybackurls and gau to fetch list of urls
    domains=subprocess.Popen(("cat", target), stdout=subprocess.PIPE)
    wayback_output=subprocess.check_output("waybackurls",stdin=domains.stdout,universal_newlines=True)
    gau_output=subprocess.check_output("gau",stdin=domains.stdout,universal_newlines=True)

    collected_urls.append(wayback_output)
    collected_urls.append(gau_output)
    # for url in collected_urls:
    #     print(url.strip('\n'))

    #time_taken=time.time()-start
    #print(f"{time_taken:.2f}s")






