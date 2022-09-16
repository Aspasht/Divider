# Divider
Gather interesting urls with extensions from a given file.

# What this will do
   This will process files generated by tools like waybackurls,gau,etc containing urls and grab only urls ending with file extensions. 

# Installation
      Clone the repository:
            git clone https://github.com/Aspasht/Divider.git
            
     Install dependencies:
            pip install -r Requirements.txt     


# Available Commands
      $ python divider.py -f myurlfile.txt
      $ python divider.py -f myurlfile.txt -req=True



# Example
    $ cat myUrls.txt
        https://example.com/test/test3
        https://example.com/test.css
        https://example.com/robots.txt
        https://example.com/sitemap.xml
        https://example.com/test?q=testvalue

    $ python divider.py -f myUrls.txt
        https://example.com/robots.txt
        https://example.com/sitemap.xml
    
# Usage
    usage: divider.py [-h] -f FILE [-req REQUEST]
    options:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  Please add target file as argument!
      -req REQUEST, --request Send request for previously generated urls (default=False)!

