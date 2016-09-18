# -*- coding: utf-8 -*-
import requests
import json
import measure_temp

def post_to_slack(text):
    payload = {
        "channel": "#fridge",
        "text": text
    }
    headers = {"content-type": "application/json"}
    requests.post("https://hooks.slack.com/services/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", data=json.dumps(payload), headers=headers)

if __name__ == '__main__':
    sensor = measure_temp.connect('/dev/ttyACM0', 9600)
    temp = (json.loads(measure_temp.measure(sensor)))["temperature"]
    if temp <= 10:
        text = "只今の冷蔵庫の温度は%s℃です。安心してください、冷えてますよ。" % temp
    else:
        text = "只今の冷蔵庫の温度は%s℃です。気をつけてください、壊れたかもしれませんよ。" % temp
    post_to_slack(text)
