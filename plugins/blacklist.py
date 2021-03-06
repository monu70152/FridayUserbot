# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
import logging
from database.blacklistdb import (
    add_to_blacklist,
    blacklists_del,
    del_blacklist,
    get_chat_blacklist,
    is_blacklist_in_db,
)
from main_startup.core.decorators import friday_on_cmd, listen
from main_startup.helper_func.basic_helpers import (
    edit_or_reply,
    edit_or_send_as_file,
    get_text,
)
from main_startup.helper_func.logger_s import LogIt


@friday_on_cmd(
    [
        "saveblacklist",
        "saveblockist",
        "addblacklist",
        "addblocklist",
        "blacklist",
        "textblacklist",
    ],
    cmd_help={
        "help": "Adds Text Blacklist / Blocklist!",
        "example": "{ch}blacklist porn",
    },
)
async def addblacklist(client, message):
    pablo = await edit_or_reply(message, "`Processing..`")
    blacklist = get_text(message)
    if not blacklist:
        await pablo.edit("`Give Word To Blacklist!`")
        return
    if is_blacklist_in_db(message.chat.id, blacklist):
        await pablo.edit("`Given Word Already Blacklisted!`")
        return
    blacklist = blacklist.lower()
    add_to_blacklist(blacklist, message.chat.id)
    await pablo.edit(f"`{blacklist}` `Successfully Added To Blacklist`")


@friday_on_cmd(
    ["listblacklist", "listblocklist"],
    cmd_help={"help": "Check Blacklist List!", "example": "{ch}listblocklist"},
)
async def listblacklist(client, message):
    pablo = await edit_or_reply(message, "`Processing..`")
    if not get_chat_blacklist(message.chat.id):
        await pablo.edit("This Chat Has No Blacklist")
        return
    OUT_STR = "Blacklists in the Current Chat:\n"
    for midhun in get_chat_blacklist(message.chat.id):
        OUT_STR += f"👉 `{midhun['trigger']}` \n"
    await edit_or_send_as_file(OUT_STR, pablo, client, "Blacklist", "blacklist")


@friday_on_cmd(
    ["delblacklist", "rmblacklist", "delblockist", "rmblocklist"],
    cmd_help={
        "help": "Remove Text From Blacklist / Blocklist!",
        "example": "{ch}blacklist porn",
    },
)
async def delblacklist(client, message):
    pablo = await edit_or_reply(message, "`Processing..`")
    blacklist = get_text(message)
    if not blacklist:
        await pablo.edit("`Give Word To Remove From Blacklist!`")
        return
    if not is_blacklist_in_db(message.chat.id, blacklist):
        await pablo.edit("`Given Word Is Not Blacklisted!`")
        return
    blacklist = blacklist.lower()
    del_blacklist(blacklist, message.chat.id)
    await pablo.edit(f"`{blacklist}` `Successfully Removed From Blacklist`")


@listen(filters.incoming & ~filters.edited & filters.group)
async def activeblack(client, message):
    if not get_chat_blacklist(message.chat.id):
        message.continue_propagation()
    owo = message.text
    if owo is None:
        message.continue_propagation()
    owoo = owo.lower()
    tges = owoo.split(" ")
    for owo in tges:
        if is_blacklist_in_db(message.chat.id, owo):
            try:
                await message.delete()
            except Exception as e:
                logging.error(f"[Blacklist] {e}")
                log = LogIt(message)
                await log.log_msg(
                    client,
                    f"**Blacklist Warning**\n\nI am Not Admin In **{message.chat.title}**, So I cannot Delete That Group's Blacklist messages",
                )


@friday_on_cmd(
    ["delblacklists", "rmblacklists", "delblockists", "rmblocklists"],
    cmd_help={
        "help": "Remove Everything From Blocklist!",
        "example": "{ch}delblacklists",
    },
)
async def delblacklists(client, message):
    pablo = await edit_or_reply(message, "`Processing..`")
    if not get_chat_blacklist(message.chat.id):
        await pablo.edit("This Chat Has No Blacklist")
        return
    blacklists_del(message.chat.id)
    await pablo.edit("`All Chat Blacklists Have Been Removed!`")
