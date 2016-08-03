import os
import json
import logging
from datetime import datetime

log = logging.getLogger(__name__)
log.setLevel(logging.INFO);
from pb_alarm import PB_Alarm
from slack_alarm import Slack_Alarm
from twilio_alarm import Twilio_Alarm
from ..utils import get_pokemon_name, get_alarm_config,get_args
#from Threading import Lock
class Notifications:

	def __init__(self):
		if not get_args().notifications:
			return
		filepath = os.path.dirname(os.path.dirname(__file__))
		with open(os.path.join(filepath, '..', 'alarms.json')) as file:
			settings = json.load(file)

			self.notify_list = settings["pokemon"]
			self.seen = {}
			self.alarms = []
			alarm_conf = get_alarm_config()
			alarm_settings = alarm_conf['alarms']
			for key,value in alarm_settings.iteritems():
				if value['active']:
					log.info("Init %s alarm",key)
					if key == 'pushbullet' :
						#pb_auth = auth_settings['pushbullet']
						self.alarms.append(PB_Alarm(value['api_key'],alarm_conf['url'],value['channel']))
					elif key == 'slack' :
						self.alarms.append(Slack_Alarm(value['api_key'], value['channel']))
					elif key == 'twilio' :
						self.alarms.append(Twilio_Alarm(value['account_sid'],
														value['auth_token'],
														value['to_nr'],
														value['from_nr']))
					else:
						log.info("Alarm type not found: " + alarm['type'])
			
				
	def notify_pkmns(self, pkmn):
		for id in pkmn:
			if id not in self.seen and pkmn[id]['disappear_time'] > datetime.utcnow():
				pkinfo = {
					'name': get_pokemon_name(pkmn[id]['pokemon_id']),
					'lat': pkmn[id]['latitude'],
					'lng': pkmn[id]['longitude'],
					'disappear_time': pkmn[id]['disappear_time']
				}
				self.seen[id] = pkinfo
				if(self.notify_list[pkinfo['name']] == "True"):
					log.info(pkinfo['name']+" notification has been triggered!")
					log.info("Encounter ID:" + str(id))
					for alarm in self.alarms:
						alarm.pokemon_alert(pkinfo)
		self.clear_stale()

	#clear stale so that the seen set doesn't get too large
	def clear_stale(self):
		old = []
		for id in self.seen.keys():
			if self.seen[id]['disappear_time'] < datetime.utcnow() :
				old.append(id)
		for id in old:
			del self.seen[id]

	def notify_lures(self, lures):
		raise NotImplementedError("This method is not yet implimented.")
		
	def notify_gyms(self, gyms):
		raise NotImplementedError("This method is not yet implimented.")
	