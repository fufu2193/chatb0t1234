import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
#แก้เป็น *
from linebot.models import *
app = Flask(__name__)
#แก้ ToKen
# get channel_secret and channel_access_token from your environment variable
channel_secret = '3bc43487276a8b3e609faa62b5395b24'
channel_access_token = 'nGemH19Ovnd3U8FIJ+yTWidcuRJehkjSPuPPrWxHxhqjVGUvk810lkWtcOF4g7bqPslnw/a/j6IX5XJq5m0FJWub3A9HcMAtiZFFKguzy86vyQ+yqjlKOsYZ7ntb9jPp/3Mz5uur75u1Q7hwxOv89AdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(channel_access_token) #ตัวส่ง api
handler = WebhookHandler(channel_secret)

#แก้ route
@app.route("/webhook", methods=['POST'])
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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    ##Function reply token
    # line_bot_api.reply_message(
    #     event.reply_token, #ได้ reply token
    #     TextSendMessage(text=event.message.text) #ส่ง text
    # )

    Reply_token = event.reply_token
    text_fromuser = event.message.text  ##ข้อความจากยูสเซอ

    # #เซ็ตข้อความประเภท text
    # text_tosend_1= TextSendMessage(text='KATUN',quick_reply=None)
    # text_tosend_2 = TextSendMessage(text='KKK',quick_reply=None)
    # line_bot_api.reply_message(Reply_token,messages = [text_tosend_1,text_tosend_2])

    #เซ็ตข้อความประเภท image
    # image_message_1 = ImageSendMessage(
    #     original_content_url='https://images2.minutemediacdn.com/image/upload/c_crop,h_1193,w_2121,x_0,y_64/f_auto,q_auto,w_1100/v1565279671/shape/mentalfloss/578211-gettyimages-542930526.jpg'
    #     ,preview_image_url='https://images2.minutemediacdn.com/image/upload/c_crop,h_1193,w_2121,x_0,y_64/f_auto,q_auto,w_1100/v1565279671/shape/mentalfloss/578211-gettyimages-542930526.jpg'
    # )


    # line_bot_api.reply_message(Reply_token,messages = [image_message_1])


    
    
    
    if 'เช็คราคา' in text_fromuser:
        from Resource.bxAPI import GetBxPrice
        from random import randint
        num = randint(1,10)
        data = GetBxPrice(Number_to_get=num) #เก็บจำนวนข้อมูล

        from Resource.flexmessage import setCarousel,setbubble

        flex = setCarousel(data)

        from Resource.reply import SetMenuMessage_Object , send_flex
        flex = SetMenuMessage_Object(flex)
        send_flex(Reply_token,file_data=flex,bot_access_key=channel_access_token)

    else:
        text_list = ['ฉันไม่เข้าใจที่คุณพูด กรุณาลองใหม่อีกครั้งค่ะ','ขอโทษค่ะ ไม่ทราบว่าคุณหมายถึงอะไรค่ะ','กรุณาลองใหม่อีกครั้งค่ะ']

        from random import choice
        text_data  = choice(text_list)

        text = TextSendMessage(text=text_data)
        line_bot_api.reply_message(Reply_token,text)
   
@handler.add(FollowEvent)
def RegisRichmenu(event) :
    print('Blockkkkkkkkk')
    userid = event.source.user_id
    disname = line_bot_api.get_profile(user_id=userid).display_name
    print(disname)
    botton_1 = QuickReplyButton(action=MessageAction(label='เช็คราคา',text='เช็คราคา'))
    botton_2 = QuickReplyButton(action=MessageAction(label='เช็คข่าวสาร',text='เช็คข่าวสาร'))
    qbtn = QuickReply([botton_1,botton_2])

    text = TextSendMessage(text= 'สวัสดีคุณ {} ยินดีต้อนรับสู่บริการแชตบอท'.format(disname))
    text_2 = TextSendMessage(text= 'กรุณาเลือกเมนูที่ท่านต้องการ',quick_reply=qbtn)

    line_bot_api.link_rich_menu_to_user(userid,'richmenu-54c6e33a6f05562526c62fc8b0e003bb')
    line_bot_api.reply_message(event.reply_token,messages=[text,text_2])

if __name__ == "__main__":
    app.run(port=200)
