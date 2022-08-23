from asyncio.windows_events import NULL
from contextlib import nullcontext
import discord
from discord.ext import commands
import json
import os
import random


intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='ready', intents = intents)


#bot commnads decorator can be used to register any bot.commands
@bot.command
async def on_ready():
	print('Ready Player积分商人在线营业')

@bot.event
async def on_member_join(member):
	with open('users.json','r') as f:
		users=json.load(f)
	
	await update_data(users,member)

	with open('users.json','w') as f:
		json.dump(users,f)

# @bot.event
# async def on_message(message):
# 	with open('users.json','r') as f:
# 		users=json.load(f)


# 	await add_exp(users,message.author,1)
# 	await update_data(users,message.author)
# 	#send a message to server for level up
# 	await check_level_up(users,message.author,message.channel)

# 	with open('users.json','w') as f:
# 		json.dump(users,f)


def checkUser(author):
	with open('users.json','r') as f:
		users=json.load(f)
	hasUser = False
	if len(users) > 0:
		for user in users:
			if author.id == user["userId"]:
				hasUser = True
				continue
	if hasUser == False :
		username = author.display_name
		userId = author.id
		newUser = {
			"username": username,
			"userId" : userId,
			"score": 0,
			"level": "silver",
			"time": NULL
		}
		users.append(newUser)
	with open('users.json','w') as f:
		json.dump(users,f)

#TODO: return the score that the user can get from sending message
# image : +10
# text : +1
def updateScore(message):
	#check if the message is a pic
	earnedPoints = 1
	embeds = message.embeds
	print(len(embeds))
	if len(embeds) > 0:
		for embed in embeds:
			if embed.type == "image":
				earnedPoints = 10
				print("The embed type is image")
	with open('users.json','r') as f:
		users=json.load(f)
	author = message.author
	for user in users:
		print("The original score is " + str(user["score"]))
		score = user["score"] + earnedPoints
		print("The updated score is " + str(score))
		#TODO:opeartion regarding level up after adding the earned points
		level = user["level"]
		time = user["time"]
		if author.id == user["userId"]:
			user["score"] = score
			user["level"] = level
			user["time"] = time
			print(user)
		
	with open('users.json','w') as f:
		json.dump(users,f)

@bot.event
async def on_message(message):
	#ignore if the message is coming from the bot
	if message.author.id == 846860035783131216:
		return
	#check if the user already exists in db/json, and the new user will be created if it does not exist
	checkUser(message.author)
	#check how many points can be added to the user regarding its sent message
	updateScore(message)

	channel = message.channel
	if message.content == "使用":
		await channel.send("Ready Player 积分商人使用规则如下")
	if message.content == "info":
		username = message.author.display_name
		score = 0
		level = "silver"
		with open('users.json','r') as f:
			users=json.load(f)
		for user in users:
			if message.author.id == user["userId"]:
				score = user["score"]
				level = user["level"]
				continue
		await channel.send("The current user is " + username)
		await channel.send("The user score is " + str(score))
		await channel.send("The user level is " + level)


##########3await voice channels
async def on_voice_state_update(member,before,after):
	with open('users.json','r') as f:
		users=json.load(f)
	if not before.channel and after.channel:
		users[user.id]["time"] = time.time()
	elif before.channel and not after.channel and member.id in data:
		minutes = (time.time() - users[user.id]) // 60
		await add_exp(users,message.author,minutes)
	await update_data(users,message.author)
	await level_up(users,message.author,message.channel)


	#with open('users.json','w') as f:
		#json.dump(users,f)


########wait pictures
#async def on_picture(picture):
	#with open('users.json','r') as f:
		#users=json.load(f)


	#with open('users.json','w') as f:
		#json.dump(users,f)

##########await streaming in voice channels
#async def on_streaming(param):
	#with open('users.json','r') as f:
		#users=json.load(f)


	#ith open('users.json','w') as f:
		#json.dump(users,f)

async def update_data(users,user):
	if not user.id in users:
		users[user.id]={}
		users[user.id]['exp']=0
		#levels will vary from iron, silver,gold, platinum, and diamond
		users[user.id]['level']='iron'

#可以手动添加exp
async def add_exp(users,user,exp):
	users[user.id]['exp']+=exp


async def level_up(users,user,channel):
	experience=users[user.id]['exp']
	lvl_start=users[user.id]['level']
	####score time sereis 还没实现
	score=int(experience/87)
	if score>=50 and score<60:
		lvl_end='silver'
	if score>=60 and score<70:
		lvl_end='gold'
	if score>=70 and score<80:
		lvl_end='platinum'
	if score>=80 and score<90:
		lvl_end='diamond'
	if score>=90:
		lvl_end='diamond+'
	else:
		lvl='iron'
	if lvl_start != lvl_end:
		await bot.send_message(channel,'{} 已经努力升级到了{}'.format(user.mention,lvl_end))
		users[user.id][level]=lvl.end

#level lookup in specific channel
# async def check_level(users,user,channel):
# 	if message.channel.id=='966066693556306010'：
# 	print(users[user.id]['level']
	

#一些与用户的指令交互功能



bot.run(TOKEN)




########Notes##################
#account for everyone who is in th guild
#inquiere current account score; implement totol score calculation logics:total score= attendance score recent two wweeks+last two wweeks+70%+last month*30%+ past months*5%+ current guild member*10=....
#current value/8700*100
#ranking system

#Ready_silver(50-60)  鼓励奖 兑换小屋+小礼物
#Ready_gold(60-70)
#Readyplatinum(70-80)
#Readt_diamond(80-90) 可以兑换管理权限

#score adding logics: stay in channel+1/min, streaming in channel+ 1.5/minutes/ attend actiivty, manulaly+500-1000/event（according)+ send_message(文字:+1/message, 图片or视频链接：+3/message）
#to participation)  

#可能获得的最高分数 (12*60*1.25*30+3000)+(300*10)=5700+3000=8700






