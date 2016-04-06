 # template for "Stopwatch: The Game"
import simplegui

# define global variables
count = 0
INTERVAL = 100
won = 0
trials = 0
tenth = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    minute = 0
    second = t/10
    tenth = t%10
    if(second < 10):
        print_sec = str(0) + str(second)
    else:
        print_sec = str(second)
    if(second >= 60):
        minute = second/60
        second = second%60
    return str(minute) + ":" + print_sec + "." + str(tenth)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()

def stop():
    timer.stop()
    global trials
    trials += 1
    if(count%10 == 0):
        global won
        won += 1

def reset():
    global count,won,trials
    count = 0
    won = 0
    trials = 0
    timer.stop()

# define event handler for timer with 0.1 sec interval

def tick():
    global count
    count += 1
    frame.set_draw_handler(draw)
    
# define draw handler
def draw(canvas):
    global won,trials
    canvas.draw_text(format(count),(65,85), 40, "White")
    canvas.draw_text(str(won)+"/"+str(trials),(160,25),25,"Yellow")
    
# create frame
frame = simplegui.create_frame("Stopwatch",200,150)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

# register event handlers
timer = simplegui.create_timer(100, tick)
frame.set_draw_handler(draw)
# start frame
frame.start()

# Please remember to review the grading rubric
