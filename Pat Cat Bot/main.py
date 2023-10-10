import asyncio
from db2python import DataBase
import json
import random
import time
import threading

import discord
from discord.ext import commands

config = json.load(open("config.json"))

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=config["Prefix"], intents=intents)
bot.remove_command("help")

db = DataBase("Users")

@bot.event
async def on_ready():
    for guild in bot.guilds:
        # айдишник моего чата 718407653822300201
        print(f"in {guild.name} ({guild.id}) you have: ")
        for user in guild.members:
            # айди серого 566887175371751427
            print(f"    {user} ({user.id})")
            if not user.bot and db.get_user(user.id) is None:
                db.add_new_user(user.mention, user.id)               
            else:
                pass
    
    print(f"\nBot is ready\n")

@bot.event
async def on_member_join(member: discord.Member):
    if not member.bot and db.get_user(member.id) is None:
        db.add_new_user(member.mention, member.id)

@bot.command(aliases=["погладить", "гладить", "страстные поглаживания котёнка"])
async def pat(ctx: commands.Context):
    print("pat command")
    time = db.get_time(ctx.author.id)
    print(time)
    amount = random.randint(1, 5)
    if time == []:
        await ctx.send("couldn't find information about user")
        return
    
    if  time[1] == 0 and time[2] == 0:
        db.add_count_to_user(ctx.author.id, amount)
        db.reset_timer_to_max(ctx.author.id)
        count = db.get_count(ctx.author.id)
        # 2 3 4 - раза кроме 12 13 14
        s_count = "раз" if str(count)[-1] not in ["2","3","4"] or count in [12,13,14] else "раза" 
        await ctx.send(f"Вы погладили кота {amount} {s_count}! Ваш счёт поглаживаний: {count}")
    else:
        # проблема что секунды в интах => 12345 будут идти одной цифрой а не двумя
        seconds = f"{time[2]}".zfill(2)
        strings = [f"Кот убежал за пивом, он вернется только через: {time[1]}:{seconds}", f"Котик отдыхает за границей, вернется через: {time[1]}:{seconds}"]
        await ctx.send(strings[random.randint(0, len(strings))])

@bot.command(aliases=["статистика", "стата", "статы"])
async def stats(ctx: commands.Context, mention: discord.Member = None):
    if mention == None:
        count = db.get_count(ctx.author.id)
        s_count = "раз" if str(count)[-1] not in ["2","3","4"] or count in [12,13,14] else "раза"
        await ctx.send(f"За всё время вы погладили котика {count} {s_count}")
    else:
        count = db.get_count(mention.id)
        s_count = "раз" if str(count)[-1] not in ["2","3","4"] or count in [12,13,14] else "раза"
        await ctx.send(f"За всё время {mention} погладил котика {count} {s_count}")
        
@bot.command(name= "reset")
async def reset(ctx: commands.Context, mention: discord.Member = None ):
    if mention == None:
        db.reset_timer_to_min(ctx.author.id)
        await ctx.send("you have reseted your timer")
    else:
        db.reset_timer_to_min(mention.id)
        await ctx.send(f"set the time of {mention.name} ({mention.id}) to 0")

@bot.command(name="test")
async def test(ctx: commands.Context, msg):
    print()
    db.test()
    await ctx.send("check console")

def close_db():
    db.close_db()

# def change_timer():
#     while True:
#         print("changed")
#         db.change_timer(1)
#         time.sleep(1)

# def run_bot_and_timer():
#     task1 = threading.Thread(target=bot.run, args=(config["Token"],))
#     task2 = threading.Thread(target=change_timer)
#     task1.start()
#     task2.start()
#     task1.join()
#     task2.join()

# run_bot_and_timer()

async def change_timer():
    while True:
        db.change_timer(1)
        await asyncio.sleep(1)

def Run():
    db.open_db()
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(token=config["Token"]))
    loop.create_task(change_timer())
    loop.run_forever()

Run()