__author__ = 'dan'

from bs4 import BeautifulSoup

import re


class PlayerListParser:
    def __init__(self):
        self.active_only = False
        self.player_ids = []
        self.regex = re.compile('/players/[a-z]/([a-z0-9]+)\.shtml')

    def parse(self, data):
        """
        Perform parsing on the provided data.
        """

        # Reset the list of player ids
        self.player_ids = []

        soup = BeautifulSoup(data)

        entries = soup.find_all('blockquote')
        for entry in entries:
            anchors = entry.find_all('a')
            for anchor in anchors:
                if anchor.parent.name == 'b' or not self.active_only:
                    m = self.regex.match(anchor.attrs['href'])
                    self.player_ids.append(m.group(1))