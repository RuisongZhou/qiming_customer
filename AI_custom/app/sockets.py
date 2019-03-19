import urllib.request
import sys
import ssl
import json

def send_question(data):
    #获取token
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    client_id='ph0piB3mha30Q1K7pzSaFduO'
    client_secret='waKw4GDEv0G0VkbwrrbeKY7LPNbqEspV'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
    request_token=urllib.request.Request(host)
    request_token.add_header('Content-Type', 'application/json; charset=UTF-8')
    response_token = urllib.request.urlopen(request_token)
    content_token = response_token.read()
    if not content_token:
        print("No content_token")
    else:
        string=content_token.decode('utf-8')
        jsonData = json.loads(string)
        access_token=jsonData["access_token"]
        #print(access_token)
        url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token='+ access_token
        post_data  = {
            "bot_session": "",
            #开发者需要在客户端生成的唯一id，用来定位请求，响应中会返回该字段。对话中每轮请求都需要一个log_id
            "log_id": "7758521",
            "request": {
                "bernard_level": 1,
                "client_session": "{\"client_results\":\"\", \"candidate_options\":[]}",
                # 问题
                "query": data,
                "query_info": {
                    "asr_candidates": [],
                    "source": "KEYBOARD",
                    "type": "TEXT"
                },
                "updates": "",
                #与技能对话的用户id
                "user_id": "88888"
            },
            "bot_id": 18333,
            "version": "2.0"
        }
        try:
            encoded_data = json.dumps(post_data).encode('utf-8')
            headers = {'Content-Type': 'application/json'}
            request = urllib.request.Request(url, data=encoded_data, headers=headers)
            response =urllib.request.urlopen(request)
            content = response.read()
            result1 = content.decode('utf-8')
            Data=json.loads(result1)
            qu_res_chosen=Data["result"]["response"]["qu_res"]["qu_res_chosen"]
            # qu_res_chosen获取类型为string
            Data_qu_res_chosen=json.loads(qu_res_chosen)
            return Data_qu_res_chosen["slots"][0]['normalized_word']
        except:
            return "抱歉，听不懂您的问题"

if __name__ == "__main__":
    request = send_question("启明学院在哪")
    print(request)

