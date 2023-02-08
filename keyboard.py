from pynput import keyboard
import os
import math

#
# only from windows
#
#
cursor = 0
def get_data():
	#получение данных
	file = open("data.txt")
	text = file.readlines()
	file.close()
	return text

def wrtln(data):
	#сохранение изменений
	file = open("data.txt","w")
	file.writelines(data)
	file.close()

def menu():
	global cursor
	os.system("clear")
	print("""\t\t\t\t\tTODO LIST\n""")
	data = get_data()
	j = 0
	for i in data :
		if cursor == j :
			print(f"> {i}")
		else :
			print(f"  {i}")
		j += 1
		if j > len(data) or j > 20 :
			j = 0

def on_release(key):
	global cursor
	data = get_data()
	menu()
	if key == keyboard.Key.insert :
		t = input("введите задачу >> ")
		data.insert(0,f"[ ] - {t}")
		wrtln(data)

	if key == keyboard.Key.delete :
		data = get_data()
		data.pop(cursor)
		wrtln(data)
		cursor = 0

	if key ==  keyboard.Key.enter :
		if "[ ] " in data[cursor] :
			data[cursor] = data[cursor].replace("[ ]","[X]")
		elif  "[X] " in  data[cursor] :
			data[cursor] = data[cursor].replace("[X]","[ ]")
		wrtln(data)

	if key ==  keyboard.Key.tab :
		cursor += 1
		if cursor > len(get_data()) - 1 or cursor > 20 :
			cursor = 0
	menu()

menu()
with keyboard.Listener(on_release=on_release) as listener:
    listener.join()