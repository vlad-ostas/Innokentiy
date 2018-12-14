import random

import requests
import vk_api
from config import *


def write_msg(user_id, text):
    vk_bot.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': random.randint(0, 1000)})


def write_msg_attach(user_id, text, att_url):
    vk_bot.method('messages.send', {'user_id' :user_id,
                                    'attachment' : att_url,
                                    'message' : text,
                                    'random_id' : random.randint(0, 1000)})


vk_bot = vk_api.VkApi(token=TOKEN)
long_poll = vk_bot.method('messages.getLongPollServer', {'need_pts': 1, 'lp_version': 3})
server, key, ts = long_poll['server'], long_poll['key'], long_poll["ts"]
print("готов к работе" + str(long_poll))
# ) ^


while True:
    long_poll = requests.get(
        'https://{server}?act={act}&key={key}&ts={ts}&wait=500'.format(server=server, act='a_check', key=key,
                                                                       ts=ts)).json()

    update = long_poll['updates']
    if update[0][0] == 4:
        print(update)
        user_id = update[0][3]
        if (update[0][6] == 'Кто ты?') or (update[0][6] == 'Кто ты'):
            group_info = vk_bot.method('groups.getById', {'group_id': GROUP_ID, 'fields': 'name'})
            write_msg(user_id, 'Я - ' + group_info[0]['name'])
        else:
            user_name = vk_bot.method('users.get', {'user_ids': user_id})
            write_msg(user_id, 'Привет, ' + (user_name[0]['first_name']))
            print(str(user_name[0]['first_name']) + ' ' +
                str(user_name[0]['last_name']) + ' написал(а) боту - ' + str(update[0][6]))  # msg for us

    # Меняем ts для следующего запроса
    ts = long_poll['ts']
