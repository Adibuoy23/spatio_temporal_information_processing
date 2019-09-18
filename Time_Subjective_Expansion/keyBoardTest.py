from psychopy.hardware import keyboard
from psychopy import core

kb = keyboard.Keyboard()
             
# during your trial
kb.clock.reset()  # when you want to start the timer from
waiting = True

while waiting:
    keys = kb.getKeys(['space', 'quit'], waitRelease=True)
    print(keys)
    if 'quit' in keys:
        print(key.name, key.rt, key.duration)
        core.quit()

    if 'space' in keys:
        for key in keys:
            print(key.name, key.rt, key.duration)
        waiting=False
