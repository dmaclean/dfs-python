__author__ = 'dan'

from httplib import HTTPConnection
from mlb.parsers.player_list_parser import PlayerListParser

import logging
import time


class BaseballReferenceScraper:
    """
    Scraper for baseball-reference.com
    """

    def __init__(self):
        self.source = "site"

        self.player_list_parser = PlayerListParser()

    def process(self):
        self.process_players()

    def fetch_data(self, url, log_to_console):
        """
        Makes connection to baseball-reference and downloads data from URL.
        """
        successful = False
        data = ""

        while not successful:
            try:
                conn = HTTPConnection("www.baseball-reference.com", timeout=5)
                conn.request("GET", url)
                resp = conn.getresponse()
                content_type = resp.getheader("content-type")

                encoding = None
                if content_type.find("charset=") > -1:
                    encoding = content_type.split("charset=")[1]

                if log_to_console:
                    print "{} for {}".format(resp.status, url)

                if encoding:
                    data = resp.read().decode(encoding, 'ignore')
                else:
                    data = resp.read()

                conn.close()
                successful = True
            except Exception, err:
                logging.error("Issue connecting to basketball-reference ({}).  Retrying in 10 seconds...".format(err))
                time.sleep(10)

        return data

    def process_players(self):
        """
        Performs fetching of player data.
        """
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
                    "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        #alphabet = ["a"]

        for letter in alphabet:
            url = "/players/{}/".format(letter)
            data = self.fetch_data(url, True)

            self.player_list_parser.parse(data)

            for id in self.player_list_parser.player_ids:
                player_url = "{}{}.shtml".format(url, id)

                player_page_data = self.fetch_data(player_url, True)
                print player_page_data

if __name__ == '__main__':
    scraper = BaseballReferenceScraper()
    scraper.process()