# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from database import db_x

chatbot_user_db = db_x["chatbotuserdb"]
cbb = db_x["blacklisted_users"]


def add_chatbotuser(user_id):
    chatbot_user_db.insert_one({"user_id": user_id})


def rmchatbotuser(user_id):
    chatbot_user_db.delete_one({"user_id": user_id})


def get_all_chatbotusers():
    lol = list(chatbot_user_db.find())
    return lol


def is_chatbotuser_in_db(user_id):
    k = chatbot_user_db.find_one({"user_id": user_id})
    if k:
        return True
    else:
        return False


def add_blacklisted_user(user_id):
    cbb.insert_one({"user_id": user_id})


def rm_blacklisted_user(user_id):
    cbb.delete_one({"user_id": user_id})


def is_user_blacklisted(user_id):
    b = cbb.find_one({"user_id": user_id})
    if b:
        return True
    else:
        return False
