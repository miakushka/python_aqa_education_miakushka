import os
import re
import queue

import requests
from bs4 import BeautifulSoup
from colorama import Fore


class Browser:
    last_url = None
    sites_full_path = None
    directory = None

    def __init__(self):
        # create a queue to keep sites history
        self.queue = queue.LifoQueue()

    def user_command(self, command):
        command = command.split(" ")

        url = command[0]
        if url == "exit":
            return False

        # check if user don't specify sites directory and if it is not specified previously
        if len(command) != 2 and self.directory is None:
            print("Please specify saved sites directory name")
            return True
        # save directory to global variable to use it in the future
        if self.directory is None:
            self.directory = command[1]

        if url == "back":
            try:
                url_name = self.queue.get(timeout=1)
                print(url_name)
                self.__print_site_content(self.__get_saved_site_content(url_name))
                self.last_url = url_name
            except IndexError:
                ...
                # do nothing if history is empty
            finally:
                return True

        if not self.__validate_url(url):
            print("There is an error in URL entered. Please try again.")
            return True
        else:
            if self.last_url is not None:
                # keep last visited url in the history
                self.queue.put(self.last_url)

            site_content = self.__get_site(url)
            self.__save_site(url, self.directory, site_content)
            self.__print_site_content(site_content)
            self.last_url = url
            return True

    def __get_site(self, url):
        site = requests.get(f'https://{url}')
        return site.content.decode()

    def __save_site(self, url, directory, content):
        self.sites_full_path = f'sites\\{directory}'
        if not os.access(self.sites_full_path, os.F_OK):
            os.makedirs(self.sites_full_path)
        site_content = open(f'{self.sites_full_path}\\{url}.html', 'w',
                            encoding="utf-8")  # decided to keep the site as html
        site_content.write(content)
        site_content.close()

    def __get_saved_site_content(self, url):
        site = open(f'{self.sites_full_path}\\{url}.html', 'r', encoding="utf-8")
        site_content = site.read()
        site.close()
        return site_content

    def __print_site_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        tags_to_scrape = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li"}
        results = soup.find_all(tags_to_scrape)
        for tag in results:
            text = tag.get_text()
            if tag.name == "a" and "href" in tag.attrs:
                print(Fore.BLUE + text)
            else:
                print(Fore.WHITE + text)
            print(Fore.RESET)

    def __validate_url(self, url):
        pattern = re.compile(".*\.")
        if pattern.match(url):
            return True
        return False


# ====================================================================================================================


browser = Browser()


def main():
    while True:
        command = input("URL (without https://) or command: ")
        if not browser.user_command(command):
            break


if __name__ == "__main__":
    main()
