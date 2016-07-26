import logging
import json

from datetime import datetime, timedelta
from ..utils import get_pokemon_name

log = logging.getLogger(__name__)

class Alarm(object):
	
	def __init__(self,url="http://maps.google.com"):
		self.url = url
		
	def pokemon_alert(self, pokemon):
		raise NotImplementedError("This is an abstract method")
		
	def gmaps_link(self,lat, lng):
			latLon = '{},{}'.format(repr(lat), repr(lng))
			return '{}?q={}'.format(self.url,latLon)
		
def pkmn_time_text(time):
		s = (time - datetime.utcnow()).total_seconds()

		(m, s) = divmod(s, 60)
		(h, m) = divmod(m, 60)
		d = timedelta(hours = h, minutes = m, seconds = s)

		disappear_time = datetime.now() + d
		#log.info("time: {}, s: {}, m: {}, h: {}, delta: {} + output: {}".format(time,s,m,h,d,disappear_time))
		return "Available until %s (%dm %ds)." % (disappear_time.strftime("%H:%M:%S"),m,s)

	
		