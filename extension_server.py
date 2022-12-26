# this imports the SimpleServer library
import SimpleServer
# This imports the functions you defined in searchengine.py
from searchengine import create_index, search, textfiles_in_dir
# has the json.dumps function. So useful
import json
import re

"""
File: extension_server.py
---------------------
This starts a server! Go to http://localhost:8000 to enjoy it. Currently
the server only serves up the HTML. It does not search. Implement code in
the TODO parts of this file to make it work.
"""

# the directory of files to search over
DIRECTORY = 'bbcnews'
# perhaps you want to limit to only 10 responses per search..
MAX_RESPONSES_PER_REQUEST = 10


class SearchServer:
    def __init__(self):
        """
        load the data that we need to run the search engine. This happens
        once when the server is first created.
        """
        self.html = open('extension_client.html').read()
        self.index = None
        self.file_titles = None
        # TODO: Your code here. Change this code to load any data you want to use!

    def load_index(self):
        self.index = {}
        self.file_titles = {}
        create_index(
            textfiles_in_dir("bbcnews"),
            self.index,
            self.file_titles
        )

    # this is the server request callback function. You can't change its name or params!!!
    def handle_request(self, request):
        """
        This function gets called every time someone makes a request to our
        server. To handle a search, look for the query parameter with key "query"
        """
        # it is helpful to print out each request you receive!
        print(request)

        # if the command is empty, return the html for the search page
        if request.command == '':
            return self.html

        regex_document_match = re.match(r"^bbcnews(\d+\.txt)$", request.command)
        if regex_document_match:
            with open(f"bbcnews/{regex_document_match[1]}", "r") as f:
                content = f.read().replace('\n', '<br>')
                return f"""<div style="background-color: gray; padding: 30px;">{content}</div>"""

        # if the command is search, the client wants you to perform a search!
        if request.command == 'search':
            # right now we respond to a search request with an empty string.
            # TODO: Your code here. change this code to return the string version 
            # of a list of dicts. Use json.dumps(collection) to turn a list into a string
            found_filenames = search(self.index, query=request.get_params().get("query", ""))

            return json.dumps(
                [
                    {"title": self.file_titles[filename], "url": f"{filename}", "snippet": self.get_file_snippet(filename, 150)}
                    for filename in found_filenames
                ]
            )

    @staticmethod
    def get_file_snippet(path, length):
        with open(path, "r") as f:
            content = "<br>".join(f.read().split("\n")[1:]).strip("<br>")[:length]
        return f"""{content}..."""


def main():
    # make an instance of your Server
    handler = SearchServer()

    handler.load_index()
    # start the server to handle internet requests!
    SimpleServer.run_server(handler, 8000) # make the server


if __name__ == '__main__':
    main()
