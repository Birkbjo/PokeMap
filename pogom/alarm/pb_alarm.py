import logging

from alarm import Alarm, pkmn_time_text
from pushbullet import PushBullet

log = logging.getLogger(__name__)

class PB_Alarm(Alarm):
	
	def __init__(self, api_key,url):
		Alarm.__init__(self,url)
		self.client = PushBullet(api_key) 
		log.info("PB_Alarm initialized.")
		
	def pokemon_alert(self, pokemon):
		notification_text = "A wild " + pokemon['name'].title() + " has appeared!"
		google_maps_link = self.gmaps_link(pokemon["lat"], pokemon["lng"])
		time_text =  pkmn_time_text(pokemon['disappear_time'])
		push = self.client.push_link(notification_text, google_maps_link, body=time_text)
	