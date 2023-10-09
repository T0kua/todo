import curses
import os
import keyboarde
dev = __file__.replace("main.py","")
def get_data():
    #получение данных
    file = open(f"{dev}data.txt")
    text = file.readlines()
    file.close()
    return text

def wrtln(data):
    #сохранение изменений
    file = open(f"{dev}data.txt","w")
    for x in range(len(data)):
        file.writelines(data[x])
        if x != len(data) -1:
            file.write("new_list_programm\n")
    file.close()
matrix = [[]]
for x in get_data():
    if x == "new_list_programm\n":
        matrix.append([])
    else:
        matrix[-1].append(x)
std = curses.initscr()
curses.curs_set(0)
curses.start_color()
std.keypad(True)
menu = cursor = 0
curses.init_pair(1, curses.COLOR_WHITE,curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLACK,curses.COLOR_WHITE)
row = int(os.popen("stty size","r").read().split()[1])#символов в строке
columms = int(os.popen("stty size","r").read().split()[0])#столбцы
credits = "TODO by sonju"
def draw(e = None,):
    exe = 1#сдвиг строк, 0 строка занята credits
    #дабавление credits и оформление фона
    std.addstr(0,row // 2,credits,curses.color_pair(2))
    std.addstr(0,0,f"{' ' * (row // 2)}",curses.color_pair(1))

    #отрисовка задач, выделенная подсвечвается
    for m in range(len(matrix[menu])):
        #std.refresh()
        if m != cursor:
            std.addstr(m + exe,0,f"{matrix[menu][m]}{(row - len(matrix[menu][m])) * ' '}",curses.color_pair(1))
        else:
            if (len(matrix[menu][m]) >= row):#если задача выделенна и большая она переносится на строку
                std.addstr(m + exe,0,f"{matrix[menu][m][0:]}{(row - len(matrix[menu][m])) * ' '}",curses.color_pair(2))#обрезает строку
                exe += len(matrix[menu][m]) // row#если задача занимает больше чем строка
            else:
                std.addstr(m + exe,0,f"{matrix[menu][m]}{(row - len(matrix[menu][m])) * ' '}",curses.color_pair(2))
    for x in range(len(matrix[menu]) + exe,columms - 1):#очистка нижней части окна
        std.addstr(x,0,f"{' ' * row}",curses.color_pair(1))
    if e != None:
        std.addstr(len(matrix[menu]) + exe + 1,0,f"вы нажали {e}####режим создания задачи: {mode_create}",curses.color_pair(1))
        tez = f"[{menu}|{len(matrix) - 1}]"
        std.addstr(len(matrix[menu]) + exe, row - len(tez),f"{tez}",curses.color_pair(2))
    if mode_create == True:
        std.addstr(len(matrix[menu]) + exe + 2,0,f"* {new_task} #####",curses.color_pair(2))
    return exe
std.addstr(0,10,"Здраствуйте господин!",curses.color_pair(1))#приветствие и да... это тоже костыль
e = std.getch()#костыль
mode_create = False
new_task = " "
while True:
    if cursor > len(matrix[menu]) and len(matrix[menu]) != 0:
        cursor -= 1#если курсор вышел за пределы меню
    draw(e)
    e = std.getch()
    try:#красивый ввод
        if mode_create == True:
            new_task = f"{new_task}{(keyboarde.slim(e))}".replace("Р","")
            new_task = new_task.replace("С","")
    except:
        pass
    if e == 27 and mode_create == False:#выход
        wrtln(matrix)
        curses.endwin()
        exit()
    elif e == 9 and mode_create == False:#ТАВ
        cursor += 1
        if cursor > len(matrix[menu]) - 1:
            cursor = 0
        draw(e)
    elif e == 10 and mode_create == True:#создание задачи
            mode_create = False
            matrix[menu].append(f"[ ] {new_task}\n")
            wrtln(matrix)
    elif e == 10 and mode_create == False:#вход в режим создания задачи
        if len(matrix[menu]) + 5 <= columms:
            mode_create = True
            new_task = ""
    elif e == 32 and mode_create == False:#метки
        if "[V]" in matrix[menu][cursor] :
            matrix[menu][cursor] = matrix[menu][cursor].replace("[V]","[X]")
            continue
        elif "[X]" in matrix[menu][cursor] :
            matrix[menu][cursor] = matrix[menu][cursor].replace("[X]","[ ]")
            continue
        elif "[ ]" in matrix[menu][cursor] :
            matrix[menu][cursor] = matrix[menu][cursor].replace("[ ]","[V]")
        wrtln(matrix)
    elif e == 263 and mode_create == True:#удаление
        new_task = new_task[:-1]
        draw(e)
    elif e == 261 and mode_create == False:#следующее меню
        menu += 1
        if menu > len(matrix) - 1:
            menu = 0
    elif e == 260 and mode_create == False:#предыдущее меню
        menu -= 1
        if menu < 0:
            menu = len(matrix) - 1
    elif e == 330 and mode_create == False:#удаление задачи
        if cursor <= len(matrix[menu]):
            try:
                matrix[menu].pop(cursor)
            except:
                pass
    elif e == 331 and mode_create == False and menu == len(matrix) - 1:#создание меню
        matrix.append([])
        menu += 1
        mode_create = True
        wrtln(matrix)
    elif e == 360 and mode_create == False and len(matrix[menu]) == 0:#удаление меню
        matrix.pop(menu)
        menu -= 1
        wrtln(matrix)
