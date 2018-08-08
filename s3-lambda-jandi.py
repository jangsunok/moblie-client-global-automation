# -*- coding: utf-8 -*- 

'''
해당 람다는 client-resource-storage라는 이름의 S3 storage에 업데이트가 생길 경우,  
Jandi에 Update가 발생하였음을 안내하는 message를 전송하는 역할을 합니다.

'''


import httplib
import json

def lambda_handler(event, context):

    conn = httplib.HTTPSConnection('wh.jandi.com')
    headers = {'Accept':'application/vnd.tosslab.jandi-v2+json', 'Content-Type':'application/json'}
    payloads = json.dumps({
        "body" : "Client-Resource-Storage is updated. please update your local client-resource-storage",
        "connectColor" : "#0099A6",
        "connectInfo":[
            {"title":"eventName", "description":event['Records'][0]['eventName']},
            {"title":"fileName", "description":event['Records'][0]['s3']['object']['key']}
        ]
    })

    conn.request('POST', '/connect-api/webhook/JANDI_TEAM_ID/JANDI_TOPIC_ID', payloads, headers)
    conn.getresponse()
    conn.close()
    