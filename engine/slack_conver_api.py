import requests
import os
from slack import WebClient
import sys
import json
from slackapp_env import *

headers = {
              'Authorization': 'Bearer ' + SLACK_USER_TOKEN,
                'Content-Type': 'application/json' 
        }

class slackconvapi:
    def __init__(self, incident_id, username = 'NA', in_status = 'NA'):
        self.inid = incident_id
        self.uname = username
        self.in_status = in_status               
                
    def sl_create_ch(self):
        ##check if channel exists for IN
        channel_name = 'sl-' + self.inid.lower()
        payload_data = {}
        payload_data['name'] = channel_name.lower()
        payload_json_data = json.dumps(payload_data)
        #payload = "{\"name\":\"" + channel_name + "\"}"
        print(payload_json_data)

        response = requests.request("POST", slack_url + 'conversations.create', headers=headers, data = payload_json_data)
        print(response.text.encode('utf8'))
        create_ch_data = json.loads(response.text.encode('utf8'))
        if create_ch_data['ok']:
            print(create_ch_data['channel']['id'], create_ch_data['channel']['name'], create_ch_data['channel']['created'])
        else:
            print('Error in channel creation')
        print(create_ch_data['channel']['id'])
        add_user_to_ch(create_ch_data['channel']['id'],'U019R63BEFR')
        add_user_to_ch(create_ch_data['channel']['id'],'U01AFMMM5B6')
        add_user_to_ch(create_ch_data['channel']['id'],'U01B4UXV750')
        add_user_to_ch(create_ch_data['channel']['id'],'U01A9V76542')

    def get_user_list(self):
        payload_data = {}
        response = requests.request("GET", slack_url + 'users.list', headers=headers, data = payload_data)
        print(response.text.encode('utf8'))
        #U019R63BEFR U01AFMMM5B6
        create_usr_data = json.loads(response.text.encode('utf8'))
        if create_usr_data['ok']:
            print(create_usr_data['members']['id'], create_usr_data['members']['name'], create_usr_data['members']['real_name'])
        else:
            print('Error in Fetching User Data')   

    def post_msg(self, channel_id):
        payload_data = {}
        payload_data['channel'] = channel_id
        payload_data['text'] = 'Hi ! I am Rakshak, Your Virtual Assitant for this Issue Investigation. Use /help to see how can I be useful in this investigation'
        payload_json_data = json.dumps(payload_data)

        response = requests.request("POST", slack_url + 'chat.postMessage', headers=headers, data = payload_json_data)

        print(response.text.encode('utf8'))
        #U019R63BEFR U01AFMMM5B6
        create_usr_data = json.loads(response.text.encode('utf8'))
        if create_usr_data['ok']:
            print('Initial Msg Posted')
        else:
            print('Error in Posting Msg')


def add_user_to_ch(channel_id, user_id):
    payload_data = {}
    payload_data['channel'] = channel_id
    payload_data['users'] = user_id
    payload_json_data = json.dumps(payload_data)

    response = requests.request("POST", slack_url + 'conversations.invite', headers=headers, data = payload_json_data)

    print(response.text.encode('utf8'))
    #U019R63BEFR U01AFMMM5B6
    create_usr_data = json.loads(response.text.encode('utf8'))
    if create_usr_data['ok']:
        print('User Added to Channel')
    else:
        print('Error in Adding User')

# create_ch = slackconvapi('IN12343')
# create_ch.sl_create_ch()

inputAction = sys.argv[1]
incidentNumber = sys.argv[2]
if inputAction == "createChannel" :
    print(incidentNumber)
    create_ch = slackconvapi(incidentNumber)
    create_ch.sl_create_ch()
    sys.stdout.flush()