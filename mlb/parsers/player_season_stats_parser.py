__author__ = 'dan'

from bs4 import BeautifulSoup


class PlayerSeasonStatsParser:
    def __init__(self):
        self.player_data = {}

    def parse(self, data):
        """
        Parses data from a player's season stats page.
        """
        soup = BeautifulSoup(data)

        # Find player's name and position
        self.player_data["name"] = soup.find("span", attrs={"itemprop": "name"}).text
        self.player_data["position"] = soup.find("span", attrs={"itemprop": "role"}).text