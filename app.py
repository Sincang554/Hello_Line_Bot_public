from flask import Flask, request, abort
from datetime import datetime
from collections import deque
from module import my_pickle as mp

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('')
handler = WebhookHandler('')

dataFormatter = "%H:%M"

@app.route('/')
def test():
    return 'OK'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    content = event.message.text
    try:
        time_dic = mp.pickle_load('time_dic')
        time_list = time_dic[user_id]
    except:
        time_list = deque()
    if event.message.text == 'reset':
        time_dic[user_id] = deque()
        mp.pickle_dump(time_dic, 'time_dic')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='reset'))
        return
        
    try:
        time = datetime.strptime(content, dataFormatter)
        time_list.append(time)
        comment = str(len(time_list))+' days later,\n you have to get up at '+(time_list[-1].strftime("%H:%M"))
    except:
        comment = ''
        if content == 'check':
            i=0
            for time in time_list:
                i+=1
                comment += str(i)+' days later: '+time.strftime(dataFormatter)+'\n'
        elif content == 'get up':
            now = datetime.strptime(f'{datetime.now().hour}:{datetime.now().minute}', dataFormatter)
            if now <= time_list.popleft():
                comment = 'Good morning!'
            else:
                comment = 'You are late.'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=comment))
    time_dic[user_id] = time_list
    mp.pickle_dump(time_dic, 'time_dic')


if __name__ == "__main__":
    app.run()