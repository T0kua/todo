from pynput import keyboard
import os
import ujson
import math

page = 1
cursor = 0
data = []
def get_data(tom=None,name=None):
	global data
	#tom,name = "answer","message"
	file = open("data.json")
	data = ujson.loads(file.readline())
	file.close()
	try:
		if tom == None:
			return data
		if name == None:
			return data[tom]
		return data[tom][name]
	except:
		return None
def menu():
	global cursor
	os.system("clear")
	print("""\t\t\t\t\tTODO LIST
""")
	data = get_data("task")
	j = 0
	for i in data :
		if cursor == j :
			try :
				print(f"> {i[:6]}{i.split('~')[1] }")
			except :
				print(f"> {i.split('~')[0] }")
		else :
			try :
				print(f"  {i[:6]}{i.split('~')[1] }")
			except :
				print(f"  {i.split('~')[0] }")
		j += 1
		if j > len(data) or j > 20 :
			j = 0
	print("\n")
	print(f"лист 1/{math.ceil(len(data) / 20)}")

def on_release(key):
	global cursor
	global data
	menu()
	#print(f'{key} released')
	if key == keyboard.Key.insert :
		t = input("введите задачу >> ")
		data["task"].insert(0," ")
		data["task"][0] =  f"[ ] - {t}"
		file = open("data.json","w")
		file.writelines(ujson.dumps(data))
		file.close()

	if key == keyboard.Key.delete :
		data["task"].pop(cursor)
		file = open("data.json","w")
		file.writelines(ujson.dumps(data))
		file.close()
		cursor = 0
	if key ==  keyboard.Key.enter :
		if "[ ] " in  repr(data["task"][cursor]) :
			data["task"][cursor] = (repr(data["task"][cursor]).replace("[ ]","[X]"))[1:-1]
		elif  "[X] " in  repr(data["task"][cursor]) :
			data["task"][cursor] = (repr(data["task"][cursor]).replace("[X]","[ ]"))[1:-1]
		file = open("data.json","w")
		file.writelines(ujson.dumps(data))
		file.close()
	if key ==  keyboard.Key.tab :
		cursor += 1
		data = get_data()
		if cursor > len(data["task"]) - 1 or cursor > 20 :
			cursor = 0
	if key == keyboard.Key.esc:
		# Stop listener
		return False
	menu()
print("press any key")
with keyboard.Listener(on_release=on_release) as listener:
    listener.join()