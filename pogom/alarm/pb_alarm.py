import logging

from alarm import Alarm, pkmn_time_text
from pushbullet import PushBullet

log = logging.getLogger(__name__)

class PB_Alarm(Alarm):
	
	def __init__(self, api_key,url,channel=None):
		Alarm.__init__(self,url)
		self.client = PushBullet(api_key)
		if channel:
			log.info(self.client.channels)
			self.client = self.client.get_channel(channel)
			self.client.push_note("PokeAlert initialized","Init")
		log.info("PB_Alarm initialized.")
		
	def pokemon_alert(self, pokemon):
		notification_text = "A wild " + pokemon['name'].title() + " has appeared!"
		google_maps_link = self.gmaps_link(pokemon["lat"], pokemon["lng"])
		time_text =  pkmn_time_text(pokemon['disappear_time'])
		push = self.client.push_link(notification_text, google_maps_link, body=time_text)
	