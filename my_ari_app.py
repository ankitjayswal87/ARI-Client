import websockets
import asyncio
import json
import requests
import time
import config as cf
from ari_class import ARIClass

ari = ARIClass()

async def ari_events(user,password,app):
	#url = "ws://localhost:8088/ari/events?api_key=asterisk:asterisk&app=hello-world"
	url = "ws://localhost:8088/ari/events?api_key="+user+":"+password+"&app="+app
	async with websockets.connect(url) as ws:
		while True:
			msg = await ws.recv()
			msg = json.loads(msg)
			event_type = msg['type']
			print(event_type)
			if(event_type=='StasisStart'):
				channelid = msg['channel']['id']
				print(channelid)
				ari.play_ringing(channelid)
				time.sleep(2)
				ari.stop_ringing(channelid)
				ari.answer_call(channelid)
				ari.play_prompt(channelid,'hello-world')
				#ari.play_music_on_hold(channelid,"default")
				#bridge_id = ari.create_bridge("test_bridge","holding")
				#print("BridgeID:"+bridge_id)
				#ari.delete_bridge("9a08aeb0-c793-4a64-b3a3-5d1dc9221eae")
				#ari.add_channel_in_bridge("6a465983-1010-48c8-84b1-9e0422b353ba",channelid)
				#ari.play_music_on_hold_on_bridge("67bd133e-89e9-4bda-845c-025865c49120","default")

				#Get all bridge details and print them for every bridge
				res = ari.get_all_bridges_details()
				for i in range(len(res)):
					print(res[i]['id']+res[i]['technology']+res[i]['bridge_type']+res[i]['bridge_class']+res[i]['creator']+res[i]['name']+str(res[i]['channels'])+res[i]['creationtime']+res[i]['video_mode'])
			
			elif(event_type=='ChannelDtmfReceived'):
				channelid = msg['channel']['id']
				digit = msg['digit']
				if(digit=='1'):
					ari.continue_in_dialplan(channelid)
				else:
					ari.play_dtmf(channelid,digit)
			elif(event_type=='StasisEnd'):
				channelid = msg['channel']['id']
				#ari.hangup_call(channelid)

asyncio.get_event_loop().run_until_complete(ari_events(cf.USER,cf.PASS,cf.APP))
