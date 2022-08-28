from asyncio.windows_events import NULL
from contextlib import nullcontext
import discord
from discord.ext import commands
import json
import os
import random
from dotenv import load_dotenv
from pathlib import Path
from utils import *


dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

#TOKEN should be added here
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='$', intents = intents)

#TODO: add rules for the bot
@bot.command()
async def on_ready(message):
	await message.channel.send("rules will be displayed as below")

@bot.command()
async def info(message):
	author = message.author
	user = get_user(author.id)
	username = user[0][1]
	score = user[0][2]
	level = user[0][3]
	tillNextLevel = 0 #need to calcualte the rule based on the standard
	await message.channel.send(username+"的当前分数是"+str(score))
	await message.channel.send(username+"的当前等级是"+str(level))
	await message.channel.send("距离下一个等级还有"+str(tillNextLevel)+"分")

# @bot.event
# async def on_member_join(member):
# 	with open('users.json','r') as f:
# 		users=json.load(f)
	
# 	await update_data(users,member)

# 	with open('users.json','w') as f:
# 		json.dump(users,f)

def checkUser(message):
	author = message.author
	user = get_user(author.id)
	if not user:
		print("No such user exists, new user is added")
		username = author.display_name
		userId = author.id
		create_user(userId, username)
	else:
		print(user[0][1]) #0:ID, 1:username, 2: score, 3: level, 4: time 
		print("The user exists")

# TODO: return the score that the user can get from sending message
# image : +10
# text : +1
def updateScore(message):
	#check if the message is a pic
	earnedPoints = 1
	attachments = message.attachments
	imageTpye = ["jpg", "png"]
	if(len(attachments) != 0):
		for attachment in attachments:
			fileType = attachment.url.split('.')[-1]
			if(fileType in imageTpye):
				earnedPoints = 5
	
	author = message.author
	user = get_user(author.id)
	updatedScore = user[0][2]+earnedPoints
	updatedLevel = user[0][3] #TODO: calcualte if the level is changed
	updatedUser = {
		"score": updatedScore,
		"level": updatedLevel
	}
	update_user(author.id, updatedUser)

@bot.event
async def on_message(message):
	#ignore if the message is coming from the bot
	if message.author.id == 846860035783131216:
		return
	#check if the user already exists in db/json, and the new user will be created if it does not exist
	checkUser(message)
	#check how many points can be added to the user regarding its sent message
	updateScore(message)
	await bot.process_commands(message)


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






