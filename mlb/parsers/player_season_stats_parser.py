from mlb.constants.mlb_constants import MLBConstants

__author__ = 'dan'

from bs4 import BeautifulSoup

import re


class PlayerSeasonStatsParser:
    def __init__(self):
        self.player_data = {}

        self.pitching_standard_season_regex = re.compile("pitching_standard\.(\d+)")

    def parse(self, data):
        """
        Parses data from a player's season stats page.
        """
        soup = BeautifulSoup(data)

        # Find player's name and position
        self.player_data["name"] = soup.find("span", attrs={"itemprop": "name"}).text
        self.player_data["position"] = soup.find("span", attrs={"itemprop": "role"}).text

        # Parse the Standard Pitching table.
        pitching_standard_entries = soup.find_all(id=re.compile(self.pitching_standard_season_regex))

        for entry in pitching_standard_entries:
            tds = entry.find_all("td")

            i = 0
            season = 0
            for td in tds:
                if i == 0:
                    season = int(td.text)

                    if MLBConstants.STANDARD_PITCHING not in self.player_data:
                        self.player_data[MLBConstants.STANDARD_PITCHING] = {}

                    self.player_data[MLBConstants.STANDARD_PITCHING][season] = {}
                elif i == 1:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.AGE] = self.resolve_value(td.text, "int")
                elif i == 2:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.TEAM] = td.text
                elif i == 3:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.LEAGUE] = td.text
                elif i == 4:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.WINS] = self.resolve_value(td.text, "int")
                elif i == 5:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.LOSSES] = self.resolve_value(td.text, "int")
                elif i == 6:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.WIN_LOSS_PCT] = self.resolve_value(td.text, "float")
                elif i == 7:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.ERA] = self.resolve_value(td.text, "float")
                elif i == 8:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.GAMES] = self.resolve_value(td.text, "int")
                elif i == 9:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.GAMES_STARTED] = self.resolve_value(td.text, "int")
                elif i == 10:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.GAMES_FINISHED] = self.resolve_value(td.text, "int")
                elif i == 11:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.COMPLETE_GAMES] = self.resolve_value(td.text, "int")
                elif i == 12:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.SHUT_OUTS] = self.resolve_value(td.text, "int")
                elif i == 13:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.SAVES] = self.resolve_value(td.text, "int")
                elif i == 14:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.INNINGS_PITCHED] = self.resolve_value(td.text, "float")
                elif i == 15:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.HITS] = self.resolve_value(td.text, "int")
                elif i == 16:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.RUNS] = self.resolve_value(td.text, "int")
                elif i == 17:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.EARNED_RUNS] = self.resolve_value(td.text, "int")
                elif i == 18:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.HOME_RUNS] = self.resolve_value(td.text, "int")
                elif i == 19:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.WALKS] = self.resolve_value(td.text, "int")
                elif i == 20:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.INTENTIONAL_WALKS] = self.resolve_value(td.text, "int")
                elif i == 21:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.STRIKE_OUTS] = self.resolve_value(td.text, "int")
                elif i == 22:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.HIT_BY_PITCH] = self.resolve_value(td.text, "int")
                elif i == 23:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.BALKS] = self.resolve_value(td.text, "int")
                elif i == 24:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.WILD_PITCHES] = self.resolve_value(td.text, "int")
                elif i == 25:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.BATTERS_FACED] = self.resolve_value(td.text, "int")
                elif i == 26:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.ERA_PLUS] = self.resolve_value(td.text, "float")
                elif i == 27:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.WHIP] = self.resolve_value(td.text, "float")
                elif i == 28:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.HITS_PER_9_INNINGS] = self.resolve_value(td.text, "float")
                elif i == 29:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.HOME_RUNS_PER_9_INNINGS] = self.resolve_value(td.text, "float")
                elif i == 30:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.WALKS_PER_9_INNINGS] = self.resolve_value(td.text, "float")
                elif i == 31:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.STRIKE_OUTS_PER_9_INNINGS] = self.resolve_value(td.text, "float")
                elif i == 32:
                    self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.STRIKE_OUT_TO_WALK_RATIO] = self.resolve_value(td.text, "float")


                i += 1

    def resolve_value(self, value, type):
        """
        Convenience method for gracefully casting values to int or float.
        """

        new_val = 0
        try:
            if type == "int":
                new_val = int(value)
            elif type == "float":
                new_val = float(value)
            else:
                new_val = value
        except ValueError:
            pass

        return new_val