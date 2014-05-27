from httplib import HTTPConnection
import logging
import time
import urlparse

__author__ = 'dan'


class MLBUtilities:
	def __init__(self):
		pass

	@staticmethod
	def resolve_value(value, type):
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

	# Recursively follow redirects until there isn't a location header
	# From http://www.zacwitte.com/resolving-http-redirects-in-python
	@staticmethod
	def resolve_http_redirect(self, url, depth=0):
		if depth > 10:
			raise Exception("Redirected "+depth+" times, giving up.")
		o = urlparse.urlparse(url,allow_fragments=True)
		conn = HTTPConnection(o.netloc)
		path = o.path
		if o.query:
			path +='?'+o.query
		conn.request("HEAD", path)
		res = conn.getresponse()
		headers = dict(res.getheaders())
		if headers.has_key('location') and headers['location'] != url:
			return self.resolve_http_redirect(headers['location'], depth+1)
		else:
			return res

	@staticmethod
	def fetch_data(site, url, log_to_console):
		"""
		Makes connection to baseball-reference and downloads data from URL.
		"""
		successful = False
		data = ""

		while not successful:
			try:
				conn = HTTPConnection(site, timeout=5)
				conn.request("GET", url)
				resp = conn.getresponse()
				if resp.status == 301:
					resp = MLBUtilities.resolve_http_redirect(url, 3)

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
				logging.error("Issue connecting to {} ({}).  Retrying in 10 seconds...".format(site, err))
				time.sleep(10)

		#time.sleep(5 + (5 * random.random()))
		return data