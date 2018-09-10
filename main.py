import keyboard
# import easygui
import time
import _thread
from playsound import playsound

work_time = 25 #int(easygui.integerbox(msg="How long should work periods be?", default="25"))
sbreak_time = 5 #int(easygui.integerbox(msg="How long should short breaks be?", default="5"))
lbreak_time = 15 #int(easygui.integerbox(msg="How long should long breaks be?", default="15"))

mode = 0
counter = 0
paused = False
lefted = False

def get_counter():
    if mode == 5:
        number = lbreak_time * 60
    elif mode % 2 == 1:
        number = sbreak_time * 60
    else:
        number = work_time * 60
    cmn = counter-number
    if counter < number:
        return f"-{abs(cmn) // 60}:{abs(cmn) % 60}"
    elif counter >= number:
        return f"{cmn // 60}:{cmn % 60}"

def play_alarm():
    _thread.start_new_thread(playsound, ("alarm.wav",))

def up():
    global paused
    paused = not paused
    if paused:
        print("PAUSED")
    else:
        print("UNPAUSED")

def down():
    global mode, counter, lefted
    if mode % 2 == 0 and counter >= work_time * 60:
        mode = mode + 1 % 6
        print(get_counter())
        if mode == 5:
            print("long break")
        else:
            print("short break")
        counter = 0
    else:
        print(get_counter())

def left():
    global lefted
    lefted = True
    print("You will be notified")


uph = keyboard.add_hotkey("right shift+up", up)
dnh = keyboard.add_hotkey("right shift+down", down)
lfh = keyboard.add_hotkey("right shift+left", left)

while True:
    time.sleep(1)
    if not paused:
        counter += 1
        if mode % 2 == 1 and counter >= sbreak_time * 60:
            mode = mode + 1 % 6
            print("work time")
            print(get_counter())
            play_alarm()
            counter = 0
        elif mode == 5 and counter >= lbreak_time * 60:
            mode = 0
            print("work time")
            print(get_counter())
            play_alarm()
            counter = 0
        elif mode % 2 == 0 and counter >= work_time * 60 and lefted:
            mode = mode + 1 % 6
            print(get_counter())
            if mode == 5:
                print("long break")
            else:
                print("short break")
            lefted = False
            play_alarm()
            counter = 0

keyboard.remove_hotkey(uph)
keyboard.remove_hotkey(dnh)
keyboard.remove_hotkey(lfh)
