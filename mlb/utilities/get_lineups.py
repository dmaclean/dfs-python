import logging
import random
import sys
import time

from httplib import HTTPConnection
from mlb.parsers.rotoworld_lineup_scraper import RotoworldLineupScraper

__author__ = 'dan'


class LineupScraper:
	def __init__(self):
			self.source = "site"

	def fetch_data(self, url, log_to_console):
		"""
		Makes connection to baseball-reference and downloads data from URL.
		"""
		successful = False
		data = ""

		while not successful:
			try:
				conn = HTTPConnection("www.rotowire.com", timeout=5)
				conn.request("GET", url)
				resp = conn.getresponse()
				if resp.status == 301:
					resp = self.resolve_http_redirect(url, 3)

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
				logging.error("Issue connecting to rotowire ({}).  Retrying in 10 seconds...".format(err))
				time.sleep(10)

		#time.sleep(5 + (5 * random.random()))
		return data

	def readCLI(self):
		for arg in sys.argv:
			pieces = arg.split("=")
			if pieces[0] == "source":
				self.source = pieces[1]

	def process(self):
		start = time.time()

		if self.source == "site":
			data = self.fetch_data("/baseball/daily_lineups.htm", True)
		else:
			data = open(self.source)
		rotoworld_scraper = RotoworldLineupScraper()
		rotoworld_scraper.parse(data)

		end = time.time()
		print "Scraped starting line-ups in {} minutes".format((end-start)/60.0)

if __name__ == '__main__':
	scraper = LineupScraper()
	scraper.process()