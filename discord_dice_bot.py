import discord
from discord.ext import commands
import numpy as np
bot=discord.Client()
bot=commands.Bot(command_prefix="#Prefix you want to use for your bot")#Even though this bot does not depend on it
@bot.event
async def on_ready():
    print("{0.user} is online".format(bot))
@bot.event
async def on_message(message):
    if message.content.startswith("!"):
        dice_str="+"+message.content.lower()[1:]
        dice_str=dice_str.translate(str.maketrans({"!":"/+/+","\n":""}))
        lines=dice_str.split("/+/")
        result_list=[]
        results=""
        for dices in lines:
            result=0
            result_str=f"{dices[1:]}-->"
            result_str_2=""
            tmp_dices=dices.rstrip()
            tmp_dices=tmp_dices.lstrip()
            tmp_dices=tmp_dices.translate(str.maketrans({"+":"/+"," ":"/+","-":"/-","\n":"/+"}))
            tmp_dices=tmp_dices.split("/")
            for dice in tmp_dices[1:]:
                die_result,die_result_list=roll_dice(die)(dice)
                result_str_2+=f"{dice} {die_result_list}"
                result+=die_result
            result_str+=f" {result} ({result_str_2})"
            result_list.append(result_str)
            results+=str(result)+"  "
        to_sent_message='\n'.join(result_list)
        await message.channel.send(f"{message.author}-->{results[:-2]}\n```{to_sent_message}```")

def roll_dice(die):
    if "+" in die:
        if "d" in die:
            tmp=die.split("d")
            if len(tmp)==2:
                die_num=int(tmp[0])
                die_type=int(tmp[1])+1
                result = np.random.randint(1,die_type+1,die_num)
                return np.sum(result),list(result)
        else:
            return int(die),[int(die)]
    elif "-" in die:
        if "d" in die:
            tmp=die.split("d")
            if len(tmp)==2:
                die_num=int(tmp[0][1:])
                die_type=int(tmp[1])+1
                result = np.random.randint(1,die_type+1,die_num)
                return -np.sum(result),list(result)
        else:
            return -int(die),[-int(die)]
bot.run("#Bot's token")