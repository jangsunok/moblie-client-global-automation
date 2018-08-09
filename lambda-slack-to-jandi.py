# -*- coding: utf-8 -*- 

import httplib
import json

def lambda_handler(event, context):
    connectInfo = []
    if event.get('attachments', None) :
        for attachment in event['attachments']:
            connectInfo.append({"title":"", "description":attachment['text']})
        
    conn = httplib.HTTPSConnection('wh.jandi.com')
    headers = {'Accept':'application/vnd.tosslab.jandi-v2+json', 'Content-Type':'application/json'}
    payloads = json.dumps({
        "body" : event['text'],
        "connectColor" : "#0099A6",
        "connectInfo":connectInfo
    })

    conn.request('POST', '/connect-api/webhook/JANDI_TEAM_ID/JANDI_TOPIC_ID', payloads, headers)
    conn.getresponse()
    conn.close()	
