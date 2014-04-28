__author__ = 'dan'

from bs4 import BeautifulSoup

import re


class PlayerListParser:
	def __init__(self):
		self.active_only = False
		self.active_player_ids = []
		self.retired_player_ids = []
		self.odd_player_ids = []
		self.regex = re.compile('/players/([a-z])/([a-z0-9_\.\']+)\.shtml')

	def parse(self, data, letter):
		"""
		Perform parsing on the provided data.
		"""

		# Reset the list of player ids
		self.active_player_ids = []
		self.retired_player_ids = []
		self.odd_player_ids = []

		soup = BeautifulSoup(data)

		entries = soup.find_all('blockquote')
		for entry in entries:
			anchors = entry.find_all('a')
			for anchor in anchors:
				m = self.regex.match(anchor.attrs['href'])

				if m is None:
					print anchor

				if m.group(1) != letter:
					self.odd_player_ids.append([m.group(1), m.group(2)])
				else:
					# Active player
					if anchor.parent.name == 'b':
						self.active_player_ids.append(m.group(2))
					else:
						self.retired_player_ids.append(m.group(2))