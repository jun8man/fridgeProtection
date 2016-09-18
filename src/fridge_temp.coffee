# Description:
#   Return fridge temperature.

child_process = require 'child_process'

user_id_list = ["junya"]

get_temperature = (msg, key) ->
    if msg.message.user.name in user_id_list
        child_process.exec "python /home/yamajun/GitRepos/fridgeProtection/src/measure_temp.py", (error, stdout, stderr) ->
            if !error
                try
                    json_data = JSON.parse(stdout)
                    temp = json_data["temperature"]
                    if key is "temp"
                        msg.reply "Current temperature of your fridge is #{temp}℃. It's stable." if temp <= 10
                        msg.reply "Current temperature of your fridge is #{temp}℃. I'm doubting your fridge is in some trouble." if temp > 10
                    if key is "温度"
                        msg.reply "只今の冷蔵庫の温度は#{temp}℃です。安心してください、冷えてますよ。" if temp <= 10
                        msg.reply "只今の冷蔵庫の温度は#{temp}℃です。気をつけてください、壊れたかもしれませんよ。" if temp > 10
                catch e
                    msg.reply "#{e}"
            else
                msg.reply "#{error}"
    else
        msg.reply "Who are you?"

module.exports = (robot) ->
    robot.respond /.*温度.*/i, (msg) ->
        get_temperature(msg, "温度")
        return
    robot.respond /.*temp.*/i, (msg) ->
        get_temperature(msg, "temp")
        return
