#coding=utf-8
from bottle import route,run,request,abort,static_file
from transitions.extensions import GraphMachine
from transitions import Machine
import requests
import os
import json
import pandas as pd
import sys

GRAPH_URL="https://graph.facebook.com/v2.6"
PAGE_TOKEN="EAAIRVs2seX4BAIwlMS5x1y6ZBzGXnQSZAtVNzpOS5NuZCFkWZCWV9ZBgwP8LrFhpZCn0DfAbtDlR4HIDPs0rW4IY9Lfs5fk4MTECZBZBlfxVZCQdZApM8RHg8ZAIhfLCryYNCg1uPtk8m5uSBVizrU0spUuSqk04GZCvhjzj8bsXiEJZCFgZDZD"
VERIFY_TOKEN="1234"

state1_time = 0

ans = ''

def random_ans():
	import random
	digit = ('0123456789')
	global ans
	ans = ''.join(random.sample(digit, 4))
	return ans

ans = random_ans()

def send_text_message(name,text):
	url="{0}/me/messages?access_token={1}".format(GRAPH_URL,PAGE_TOKEN)
	ctx={
		"recipient":{
			"id":name
		},
		"message":{
			"text":text
		}
	}
	response=requests.post(url,json=ctx)
	if response.status_code!=200:
		print("Unable to send message: "+response.text)
	return response
def send_image_message(name,text):
	url="{0}/me/messages?access_token={1}".format(GRAPH_URL,PAGE_TOKEN)
	ctx={
		"recipient":{
			"id":name
		},
		"message":{
			"attachment":{
				"type":"image",
				"payload":{
					"url":text
				}
			}
		}
	}
	response=requests.post(url,json=ctx)
	if response.status_code!=200:
		print("Unable to send message: "+response.text)
	return response

def NLP_func(text):
	dict1 = pd.read_excel('dict1.xls')
	dict2 = pd.read_excel('dict2.xls')
	dict3 = pd.read_excel('dict3.xls')

	chinese = text

	i = 0
	word = ''
	string = ''
	start = 0
	end = 4
	validate = False

	if(end>=len(chinese)):
		end=len(chinese)
	while end <= len(chinese):
		validate = False
		for word in dict1.sword:
			if chinese[start:end] == word:
				print(word)
				string = string + "\n" + word
				validate = True
				start = end
				end = end+2
				if(end>=len(chinese)):
					end=len(chinese)
		if validate == False:
			for word in dict2.sword:
				if chinese[start:end] == word:
					print(word)
					string = string + "\n" + word
					validate = True
					start = end
					end = end+2
					if(end>=len(chinese)):
						end=len(chinese)
			if validate == False:
				for word in dict3.sword:
					if chinese[start:end] == word:
						print(word)
						string = string + "\n" + word
						validate = True
						start = end
						end = end+2
						if(end>=len(chinese)):
							end=len(chinese)
				if validate == False:
					end-=1
		if start==end:
			break
	return string

count = 0

def Game(name,text):
	global count
	global ans
	word = ''
	while 1:
		count += 1
		a, b = 0, 0
		while 1:
			word = text
			if len(word) == 4:
				break
		for i in range(4):
			if word[i] == ans[i]:
				a += 1
			elif word[i] in ans:
				b += 1
		result = str(a) + 'A' + str(b) +'B' 
		if word == ans:
			return 'Correct!! Use ' + str(count) + ' times'
		else :
			return result
		
		

class TocMachine(GraphMachine):		#set the function when state transition
	def __init__(self,**machine_configs):
		self.machine=GraphMachine(model=self,**machine_configs)

	def force_state1(self,event):
		print("force going to state1")
		if event.get("message"):
			text=event["message"]["text"]
			print(text)
			if text.lower() == "go back":
				return True
		return False

	def is_going_to_state1(self,event):
		if event.get("message"):
			text=event["message"]["text"]
			return text.lower()=="hello"
		return False
	def is_going_to_chinese(self,event):
		if event.get("message"):
			text=event["message"]["text"]
			return text.lower()=="can you speak chinese?"
		return False
		
	def is_going_to_test(self,event):
		if event.get("message"):
			text=event["message"]["text"]
			return text.lower()=="test"
		return False
	def is_going_to_state3(self,event):
		if event.get("message"):
			text=event["message"]["text"]
			return text.lower() == "give me image"
		return False
	
	def is_going_to_image(self,event):
		if event.get("message"):
			text=event["message"]["text"]
			return text.lower()=="please"
		return False
	def is_going_to_NLP(self,event):
		if event.get("message"):
			text=event["message"]["text"]
			print(text)
			if text.lower() == "nlp":
				return True
		return False
	def is_going_to_str(self,event):
		print("im going to str")
		if event.get("message"):
			text=event["message"]["text"]
			print(text)
			for ch in text:
				if u'\u4e00' <= ch <= u'\u9fff':
					return True
			return False
		return False

	def is_going_to_game(self,event):
		if event.get("message"):
			text=event["message"]["text"]
			print(text)
			if text.lower() == "game":
				return True
		return False
	def is_going_to_guess(self,event):
		print("im going to str")
		if event.get("message"):
			text=event["message"]["text"]
			print(text)
			if len(text) == 4:
				return True
		return False

	def on_enter_state1(self, event):
		print("I'm entering state1")
		global state1_time
		state1_time = state1_time + 1
		sender_id=event['sender']['id']
		if state1_time == 1:
			responese=send_text_message(sender_id,"Hello")
		responese=send_text_message(sender_id,"How can I help you?\n1.Can you speak Chinese?\n2.Give me image\n3.NLP\n4.Game")
		print(machine.state)
		# self.go_back1()
	def on_exit_state1(self,event):   #add a event
		print("Leaving state1")

	def on_enter_chinese(self, event):
		print("I'm entering chinese")
		sender_id=event['sender']['id']
		responese=send_text_message(sender_id,"不會")
		self.go_back_state1(event)
	def on_exit_chinese(self,event):
		print("Leaving chinese")

	def on_enter_NLP(self, event):
		print("I'm entering NLP")
		sender_id=event['sender']['id']
		responese=send_text_message(sender_id,"請輸入中文句子...")
	def on_exit_NLP(self,event):
		print("Leaving NLP")

	def on_enter_str(self, event):
		print("I'm entering str")
		text=event["message"]["text"]
		string = NLP_func(text)
		sender_id=event['sender']['id']
		responese=send_text_message(sender_id,string)
		self.go_back_state1(event)
	def on_exit_str(self,event):
		print("Leaving str")

	def on_enter_game(self, event):
		print("I'm entering game")
		global ans
		print(ans)
		sender_id=event['sender']['id']
		responese=send_text_message(sender_id,"請輸入4位數字...")
	def on_exit_game(self,event):
		print("Leaving game")

	def on_enter_guess(self, event):
		print("I'm entering guess")
		text=event["message"]["text"]
		sender_id=event['sender']['id']
		string = Game(sender_id,text)
		if 'C' == string[0]:
			responese=send_text_message(sender_id,string)
			global ans
			ans = random_ans()
			self.go_back_state1(event)
		else:
			responese=send_text_message(sender_id,string)
			self.go_back_game(event)
	def on_exit_guess(self,event):
		print("Leaving guess")

	def on_enter_test(self, event):
		print("I'm entering test")
		sender_id=event['sender']['id']
		responese=send_text_message(sender_id,"OK")
		self.go_back()
	def on_exit_test(self):
		print("Leaving test")

	def on_enter_state3(self, event):
		print("I'm entering state3")
		show_fsm()
		sender_id=event['sender']['id']
		responese=send_text_message(sender_id,"NO")
		responese=send_text_message(sender_id,"░░░░░░██░░░░░░\n░░░░░█░░█░░░░░\n░░░░░█░░█░░░░░ \n░░░░░█░░█░░░░░\n░░░░░█░░█░░░░░\n░░████░░███░░░\n███░░█░░█░░██░\n█░█░░█░░█░░█░█\n█░░░░░░░░░░█░█\n█░░░░░░░░░░░░█\n█░░░░░░░░░░██░\n███░░░░░░░██░░\n░▀▀███████░░░░")
		responese=send_text_message(sender_id,"Say please")
		# self.go_back()
	def on_exit_state3(self,event):
		print("Leaving state3")

	def on_enter_image(self, event):
		print("I'm entering image")
		sender_id=event['sender']['id']
		responese=send_image_message(sender_id, "https://i.imgur.com/78kebjH.jpg?1")
		self.go_back_state1(event)
	def on_exit_image(self,event):
		print("Leaving image")



machine=TocMachine(		#set state and transition
	states=[
		"user",
		"state1",
		"test",
		"chinese",
		"state3",	#fake image
		"image",
		"NLP",
		"str",
		"game",
		"guess"
	],
	transitions=[
		{
			"trigger":"advance",
			"source":"user",
			"dest":"state1",
			"conditions":"is_going_to_state1"
		},
		{
			"trigger":"advance",
			"source":"user",
			"dest":"test",
			"conditions":"is_going_to_test"
		},
		{
			"trigger":"advance",
			"source":"state1",
			"dest":"state3",
			"conditions":"is_going_to_state3"
		},
		{
			"trigger":"advance",
			"source":"state3",
			"dest":"image",
			"conditions":"is_going_to_image"
		},
		{
			"trigger":"advance",
			"source":"state1",
			"dest":"chinese",
			"conditions":"is_going_to_chinese"
		},
		{
			"trigger":"advance",
			"source":"state1",
			"dest":"NLP",
			"conditions":"is_going_to_NLP"
		},
		{
			"trigger":"advance",
			"source":"NLP",
			"dest":"str",
			"conditions":"is_going_to_str"
		},
		{
			"trigger":"advance",
			"source":"state1",
			"dest":"game",
			"conditions":"is_going_to_game"
		},
		{
			"trigger":"advance",
			"source":"game",
			"dest":"guess",
			"conditions":"is_going_to_guess"
		},

		{
			"trigger":"go_back_state1",
			"source":[
				"chinese",
				"image",
				"str",
				"game",
				"guess"
			],
			"dest":"state1"
		},
		{
			"trigger":"go_back_game",
			"source":"guess",
			"dest":"game"
		},
		{
			"trigger":"force_go_back_state1",
			"source":"game",
			"dest":"state1",
			"conditions":"force_state1"
		},
		{
			"trigger":"go_back",
			"source":[
				"test"
				# "chinese",
				# "image",
				# "state1",
				# "chinese",
				# "state3"
			],
			"dest":"user"
		}
	],
	initial="user",
	auto_transitions=False,
	show_conditions=True,
)


@route("/webhook",method=["GET","POST"])
def webhook():
#method="GET"
	if request.method == "GET":
		mode=request.GET.get("hub.mode")
		verify_token=request.GET.get("hub.verify_token")
		challenge=request.GET.get("hub.challenge")
		if mode=="subscribe" and verify_token==VERIFY_TOKEN:
			print("WEBHOOK_VERIFIED")
			return challenge
		else:
			abort(403)
#method="POST"
	else:
		body=request.json
		if body["object"]=="page":
			event=body["entry"][0]["messaging"][0]
			text=event["message"]["text"]
			print(text)
			if 't' == text[0]:
				print('OK')
			machine.advance(event)
			return "OK"

def show_fsm():
	machine.get_graph().draw("fsm.png",prog="dot",format="png")
	return static_file("fsm.png",root="./",mimetype="image/png")

if __name__ == "__main__":
	show_fsm()
	global ans
	print(ans)
	run(host="localhost",port=5006,debug=True)