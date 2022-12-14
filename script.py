# -*- coding: utf-8 -*-
"""script.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UW4QXOMAv5C1uybIhUSkIFQxlwi397TC

# **Prepare Data**
"""
#pip install pandasql

import pandas as pd
import pandasql as ps
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("car_sales.csv")

df.head()

df['booking_date']= pd.to_datetime(df['booking_date'])
df['invoice_date']= pd.to_datetime(df['invoice_date'])
df['delivery_date']= pd.to_datetime(df['delivery_date'])
df.info()
df.head()

"""# **NLP2SQL**"""

#pip install openai

import openai

key = "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"
openai.api_key = key

#response = openai.Completion.create(engine="text-davinci-002", prompt="Say this is a test", temperature=0, max_tokens=100)




"""# **PandaSQL**"""

query = """select * from df where invoice_date not null"""
#query = gpt.get_top_reply(prompt).replace("output: ","")
print(query)

ps.sqldf(query, locals())
df3 = ps.sqldf(query, locals())
df3.info()
df3.head()

# save figure
plt.figure(figsize=(8, 5))
plt.suptitle("Report")
#sns.histplot(data=df3, x="source", hue="source", shrink=.8, legend=True)
ax = sns.histplot(data=df3, x="zone", hue="zone", shrink=.8, legend=True).get_figure() #x==continue , y==number
ax.savefig('zone.png')

"""# **Line Bot SDK**"""

#pip install pyngrok

#pip install line-bot-sdk


import json
import os
from flask import Flask, request, make_response, abort
from pyngrok import ngrok
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from linebot import *
from linebot.models import *

port_no = 5000

#Flask
app = Flask(__name__)
#ngrok.set_auth_token("2HQgO3WIl0uxBbjgf4bejj41ybL_648ursQGYpv5qrAffExbk")
ngrok.set_auth_token("2HQgODtPv4bCsGSW5QTooQuZMkl_6EvGy6petKP4ftb5oEmq7")
public_url =  ngrok.connect(port_no).public_url

line_bot_api = LineBotApi('kWeq23t6pFxFPzPWc25LPgBBND7RU0fgBzIylupasm7jyqh/3ZxrYMFAOr92sf6KOXE+hyWnbVm0fQONiMWIJbMRFST/kxGMGFEKM42sJgzKa1Suk7onQrrGn9IYcs9KmFq2txTZMuwxnWwDmt2BqAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('367fb0e9c752a3fa548a1424f7aa8527')

@app.route("/callback", methods=['POST'])
def callback():
    req = request.get_json(silent=True, force=True)
    intent_name = req["queryResult"]["intent"]["displayName"]
    intent_name_split = intent_name.split()
    text = req['originalDetectIntentRequest']['payload']['data']['message']['text']
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    disname = line_bot_api.get_profile(id).display_name

    print('id = ' + id)
    print('name = ' + disname)
    print('text = ' + text)
    print('intent = ' + intent_name)
    print('reply_token = ' + reply_token)

    if intent_name_split[0] == "SaleReport":
        SaleReport(text, intent_name, reply_token)
    elif intent_name_split[0] == "DealerPerformance":
        DealerPerformance(text, intent_name, reply_token)
    elif intent_name_split[0] == "HelloMADT":
        nlp(text, intent_name, reply_token)
    else:
        nlp(text, intent_name, reply_token)

    # if intent_name == "SaleReport - Region - All":
    #     #reply(reply_token)
    #     reply_image(text, intent_name, reply_token)
    # elif intent_name == "SaleReport - Region - Some - Model":
    #     reply_image(text, intent_name, reply_token)
    # elif intent_name == "customized viz - custom":
    #     reply_viz(text, reply_token)
    # else:
    #     nlp(text, reply_token)

    return 'OK'

def reply(reply_token):
    text_message = TextSendMessage(text='?????????????????????????????????')
    line_bot_api.reply_message(reply_token,text_message)

def nlp(text, intent_name, reply_token):

    # nlp_return = gpt.get_top_reply(text).replace("output: ","")
    # text_message = TextSendMessage(text=nlp_return)
    response = openai.Completion.create(engine="text-davinci-002", prompt=text, temperature=0, max_tokens=100)
    text_message = TextSendMessage(text=response['choices'][0]['text'].replace('\n',''))
    print(response)
    line_bot_api.reply_message(reply_token,text_message)

def DealerPerformance(text, intent_name, reply_token):
    text_message = 'xxx'
    line_bot_api.reply_message(reply_token,text_message)

def SaleReport(text, intent_name, reply_token):

    #Get File
    link_file = 'https://drive.google.com/file/d/1x4OY0hWaQQpxJF9x6E-0PhxGeOaUiCAs/view?usp=sharing'
    _,_,_,_,_,id,_ = link_file.split('/')
    downloaded = drive.CreateFile({'id':id})
    downloaded.GetContentFile('car_sales.csv')
    df = pd.read_csv("car_sales.csv")
    df['booking_date']= pd.to_datetime(df['booking_date'])
    df['invoice_date']= pd.to_datetime(df['invoice_date'])
    df['delivery_date']= pd.to_datetime(df['delivery_date'])

    if intent_name == "SaleReport - Region - All":
      dimension = "region"
      sql = f"""select * from df where invoice_date not null"""
    elif intent_name == "SaleReport - Region - Some - Model":
      dimension = "region"
      sql = f"""select * from df where invoice_date not null and model = '{text}'"""
    elif intent_name == "SaleReport - Zone - All":
      dimension = "zone"
      sql = f"""select * from df where invoice_date not null"""
    elif intent_name == "SaleReport - Zone - Some - Model":
      dimension = "zone"
      sql = f"""select * from df where invoice_date not null and model = '{text}'"""

    print(sql)
    df4 = ps.sqldf(sql, locals())
    # df4.info()
    # df4.head()
    # # save figure
    plt.figure(figsize=(8, 5))
    plt.suptitle("Sale Report")
    ax = sns.histplot(data=df4, x=dimension, hue=dimension).get_figure() #x==continue , y==number
    ax.savefig('report_1.png')

    uploaded = drive.CreateFile({'title': 'report_1.png'})
    uploaded.SetContentFile('report_1.png')
    uploaded.Upload()
    image_message = ImageSendMessage(
        original_content_url=uploaded["thumbnailLink"][:-5],
        preview_image_url=uploaded["thumbnailLink"]
        )
    line_bot_api.reply_message(reply_token,image_message)

def reply_viz(text, reply_token):
    df = pd.read_csv("insurance.csv")
    texts = text.split()
    query = {"type":texts[0], "x":None, "y":None, "hue":None}
    for t in texts[1:]:
        if t == "??????????????????":
            query["x"] = texts[texts.index(t)+1]
        elif t == "?????????":
            query["y"] = texts[texts.index(t)+1]
        elif t == "????????????????????????????????????":
            query["hue"] = texts[texts.index(t)+1]

    plt.figure(figsize=(8, 5))
    if query["type"] == "?????????????????????":
        ax = sns.scatterplot(data=df, x=query["x"], y=query["y"], hue=query["hue"]).get_figure()
    elif query["type"] == "????????????????????????":
        ax = sns.lineplot(data=df, x=query["x"], y=query["y"], hue=query["hue"]).get_figure()
    elif query["type"] == "????????????????????????":
        ax = sns.countplot(data=df, x=query["x"], y=query["y"], hue=query["hue"]).get_figure()
    ax.savefig('plot.png')

    uploaded = drive.CreateFile({'title': 'plot.png'})
    uploaded.SetContentFile('plot.png')
    uploaded.Upload()
    image_message = ImageSendMessage(
        original_content_url=uploaded["thumbnailLink"][:-5],
        preview_image_url=uploaded["thumbnailLink"]
        )
    line_bot_api.reply_message(reply_token,image_message)

#Flask
if __name__ == '__main__':
    public_url_s = public_url.replace("http://","https://")
    print(f"To acces the Gloable link please click {public_url_s}/callback")
    print("Starting app on port %d" % port_no)
    app.run(debug=False, port=port_no, threaded=True)