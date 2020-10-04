import requests
import os
from slack import WebClient
import sys
import json
import time
from slackapp_env import *

headers = {
              'Authorization': 'Bearer ' + SLACK_USER_TOKEN,
                'Content-Type': 'application/json' 
        }

class slackconvapi:
    def __init__(self, incident_id, username, in_status = 'NA'):
        self.inid = incident_id
        self.uname = username
        self.in_status = in_status               

    def sl_get_ch_link(self):
        ch_list_url = "https://slack.com/api/conversations.list"
        headers = {'Authorization': 'Bearer ' + SLACK_USER_TOKEN}
        payload = {}
        response = requests.request("POST", ch_list_url, headers=headers, data = payload)
        # print(response.text.encode('utf8'))
        channel_name = self.inid.lower()
        channel_list= json.loads(response.text.encode('utf8'))
        if("channels" in channel_list):
            channels = channel_list["channels"]
            for channel in channels:
                if(channel["name"] == channel_name):
                    print(slack_rakshaq_url + channel["id"])
                    return

        print("Channel not created")

    def sl_create_ch(self):
        ##check if channel exists for IN
        # channel_name = 'sl-' + self.inid.lower()      
        channel_name = self.inid.lower()
        ch_create_url = "https://slack.com/api/conversations.create?name="+channel_name+"&pretty=1"

        payload = {}
        headers = {'Authorization': 'Bearer ' + SLACK_USER_TOKEN}

        response = requests.request("POST", ch_create_url, headers=headers, data = payload)

        # print(response.text.encode('utf8'))
        payload_json_data = {}
        create_ch_data = json.loads(response.text.encode('utf8'))
        # print(create_ch_data['ok'])
        if("error" in create_ch_data):            
            if(create_ch_data['error'] == "name_taken"):
                slackconvapi.sl_get_ch_link(self)
                return
            else:
                print(create_ch_data['error'])
                return

        if create_ch_data['ok']:
            # print(create_ch_data['channel']['id'], create_ch_data['channel']['name'], create_ch_data['channel']['created'])
            print(slack_rakshaq_url + create_ch_data['channel']['id'])
            time.sleep(1)
            slackconvapi.add_user_to_ch(create_ch_data['channel']['id'],'U019R63BEFR')
            slackconvapi.add_user_to_ch(create_ch_data['channel']['id'],'U01AFMMM5B6')
            slackconvapi.add_user_to_ch(create_ch_data['channel']['id'],'U01B4UXV750')
            slackconvapi.add_user_to_ch(create_ch_data['channel']['id'],'U01A9V76542')
            #post mesages
            print("+++++Sending First Message+++++++++++")
            slackconvapi.post_ini_msg(create_ch_data['channel']['id'])
            ##Bot User D01BDBMBU93
            slackconvapi.add_user_to_ch(create_ch_data['channel']['id'],'U01BV3BMQ81')
        else:
            print('Error in channel creation')


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
        payload_data['text'] = 'Hi !'
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
        channel_id = str(channel_id.strip())
        print("Channel Id:", channel_id)
        headers = {'Authorization': 'Bearer ' + SLACK_USER_TOKEN}

        add_usr_url = "https://slack.com/api/conversations.invite?channel="+channel_id+"&users="+user_id
        payload  = {}
        response = requests.request("POST", add_usr_url, headers=headers, data = payload)

        print(response.text.encode('utf8'))
        #U019R63BEFR U01AFMMM5B6
        create_usr_data = json.loads(response.text.encode('utf8'))
        if create_usr_data['ok']:
            print('User Added to Channel')
        else:
            print('Error in Adding User')

    def post_ini_msg(channel_id):
        post_ini_msg_url = "https://slack.com/api/chat.postMessage?channel="+channel_id+"&text=NA"
        #post_ini_msg_url = "https://slack.com/api/chat.postMessage?channel=C01AZPGER6U&text=NA"
        #payload = "{\n    \"channel\": \""+channel_id+"\",\n\t\"blocks\": [\n\t\t{\n\t\t\t\"type\": \"section\",\n\t\t\t\"text\": {\n\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\"text\": \"Hello From Rakshak :wave: \\n Your Personal Assistant !\"\n\t\t\t}\n\t\t},\n\t\t{\n\t\t\t\"type\": \"section\",\n\t\t\t\"text\": {\n\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\"text\": \"I can do following Tasks :\"\n\t\t\t}\n\t\t},\n\t\t{\n\t\t\t\"type\": \"section\",\n\t\t\t\"text\": {\n\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\"text\": \"• Schedule meetings \\n • Send Periodic Notifications to Stakeholders \\n • Scan and bring email here for you \\n • Generate Meeting Texts \\n • Produde up-to-date summaries \\n • Update IN's \\n • Notiy your Team when you start working on IN's \\n• Close IN's\"\n\t\t\t}\n\t\t},\n\t\t{\n\t\t\t\"type\": \"section\",\n\t\t\t\"text\": {\n\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\"text\": \"Hope I will be able to help you ! You can chat with me anytime.\"\n\t\t\t}\n\t\t}\n\t]\n}"
        payload = "{\n    \"channel\": \"%s\",\n\t\"blocks\": [\n\t\t{\n\t\t\t\"type\": \"section\",\n\t\t\t\"text\": {\n\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\"text\": \"Hello From Rakshak :wave: \\n Your Personal Assistant !\"\n\t\t\t}\n\t\t},\n\t\t{\n\t\t\t\"type\": \"section\",\n\t\t\t\"text\": {\n\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\"text\": \"I can do following Tasks :\"\n\t\t\t}\n\t\t},\n\t\t{\n\t\t\t\"type\": \"section\",\n\t\t\t\"text\": {\n\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\"text\": \"• Schedule meetings \\n • Send Periodic Notifications to Stakeholders \\n • Scan and bring email here for you \\n • Generate Meeting Texts \\n • Produde up-to-date summaries \\n • Update IN's \\n • Notiy your Team when you start working on IN's \\n• Close IN's\"\n\t\t\t}\n\t\t},\n\t\t{\n\t\t\t\"type\": \"section\",\n\t\t\t\"text\": {\n\t\t\t\t\"type\": \"mrkdwn\",\n\t\t\t\t\"text\": \"Hope I will be able to help you ! You can chat with me anytime.\"\n\t\t\t}\n\t\t}\n\t]\n}"
        payload = payload % channel_id
        payload = payload.encode('utf8')
        print(payload)
        headers = {
        'Authorization': 'Bearer ' + SLACK_USER_TOKEN,
        'Content-Type': 'application/json',
        'Cookie': 'b=4y3ul187n7tsvz7b656gejmdp'
        }

        response = requests.request("POST", post_ini_msg_url, headers=headers, data = payload)

        print(response.text.encode('utf8'))       

# create_ch = slackconvapi('in0000012')
# # create_ch.sl_get_ch_link()
# create_ch.sl_create_ch()

inputAction = sys.argv[1]
incidentNumber = sys.argv[2]
slackUserID = sys.argv[3]
if inputAction == "createChannel" :
    # print(incidentNumber)
    create_ch = slackconvapi(incidentNumber,slackUserID)
    create_ch.sl_create_ch()
    sys.stdout.flush()

if inputAction == "getChannel" :
    # print(incidentNumber)
    create_ch = slackconvapi(incidentNumber,slackUserID)
    create_ch.sl_get_ch_link()
    sys.stdout.flush()