from pynput import keyboard
from threading import Thread
from time import sleep

def on_press(key, abortKey='esc'):    
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys    

    print('pressed %s' % (k))
    if k == abortKey:
        print('end loop ...')
        return False  # stop listener

def loop_fun():
    while True:
        print('sleeping')
        sleep(10)
        
if __name__ == '__main__':
    abortKey = 't'
    listener = keyboard.Listener(on_press=on_press, abortKey=abortKey)
    listener.start()  # start to listen on a separate thread

    # start thread with loop
    Thread(target=loop_fun, args=(), name='loop_fun', daemon=True).start()

    listener.join() # wait for abortKey
    print("fin de loop")