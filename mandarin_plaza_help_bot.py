import json

main_content=json.load(open(r"D:\bot_python\vigilant-telegram\mandarin_plaza_help_bot\main_content.json"))

current_language="it"

def content_languaged():
    for c in main_content['contents']:
        if c['lang']==current_language:
            return c

print(content_languaged())