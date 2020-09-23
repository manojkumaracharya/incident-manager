import requests
import os
from slack import WebClient
import json
from slackapp_env import *

class slackconvapi:
    def __init__(self, incident_id, username = 'NA', in_status = 'NA'):
        self.inid = incident_id
        self.uname = username
        self.in_status = in_status

        headers = {
              'Authorization': 'Bearer ' + SLACK_USER_TOKEN,
                'Content-Type': 'application/json'
                }
    
    def sl_create_ch(self):
        ##check if channel exists for IN
        channel_name = 'sl-' + self.inid.lower()
        payload_data = {}
        payload_data['name'] = channel_name.lower()
        payload_json_data = json.dumps(payload_data)
        #payload = "{\"name\":\"" + channel_name + "\"}"

        response = requests.request("POST", slack_url + 'conversations.create', headers=headers, data = payload_json_data)
        print(response.text.encode('utf8'))
        create_ch_data = json.loads(response.text.encode('utf8'))
        if create_ch_data['ok']:
            print(create_ch_data['channel']['id'], create_ch_data['channel']['name'], create_ch_data['channel']['created'])
        else:
            print('Error in channel creation')

        ## Add User to Channel
        add_user_to_ch(create_ch_data['channel']['id'], 'U019R63BEFR') ## Hardcoded

    def get_user_list(self):
        payload_data = {}

        response = requests.request("GET", slack_url + 'users.list', headers=headers, data = payload)

        print(response.text.encode('utf8'))
        #U019R63BEFR U01AFMMM5B6
        create_usr_data = json.loads(response.text.encode('utf8'))
        if create_usr_data['ok']:
            print(create_usr_data['members']['id'], create_usr_data['members']['name'], create_usr_data['members']['real_name'])
        else:
            print('Error in Fetching User Data')

    def add_user_to_ch(self, channel_id, user_id):
        payload_data = {}
        payload_data['channel'] = channel_id
        payload_data['users'] = user_id
        payload_json_data = json.dumps(payload_data)

        response = requests.request("POST", slack_url + 'conversations.invite', headers=headers, data = payload)

        print(response.text.encode('utf8'))
        #U019R63BEFR U01AFMMM5B6
        create_usr_data = json.loads(response.text.encode('utf8'))
        if create_usr_data['ok']:
            print('User Added to Channel')
        else:
            print('Error in Adding User')

    def post_msg(self, channel_id):
        payload_data = {}
        payload_data['channel'] = channel_id
        payload_data['text'] = 'Hi ! I am Rakshak, Your Virtual Assitant for this Issue Investigation. Use /help to see how can I be useful in this investigation'
        payload_json_data = json.dumps(payload_data)

        response = requests.request("POST", slack_url + 'chat.postMessage', headers=headers, data = payload)

        print(response.text.encode('utf8'))
        #U019R63BEFR U01AFMMM5B6
        create_usr_data = json.loads(response.text.encode('utf8'))
        if create_usr_data['ok']:
            print('Initial Msg Posted')
        else:
            print('Error in Posting Msg')

    ## Write code to take input for IN Duration    

#https://rakshakhq.slack.com/archives/C01AZPGER6U

create_ch = slackconvapi('IN1234')
create_ch.sl_create_ch()