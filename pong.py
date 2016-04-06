  # Implementation of classic arcade game Pong

import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [1,-1]
increase = 3
direction = RIGHT

score1 = 0
score2 = 0

paddle1_pos = [HALF_PAD_WIDTH,HEIGHT/2]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2]
position1 = paddle1_pos
position2 = paddle2_pos
paddle1_vel = [0,0]
paddle2_vel = [0,0]
acc = 10

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, increase # these are vectors stored as lists
    increase = 3
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    v1 = random.randrange(120,240)
    v2 = random.randrange(60,180)
    modulo = math.sqrt(v1**2 + v2**2)
    if (direction == RIGHT):
        ball_vel = [v1/modulo,-v2/modulo]
    elif (direction == LEFT):
        ball_vel = [-v1/modulo,-v2/modulo]
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [1,-1]
    
    spawn_ball(direction)

def reset():
    global direction, score1, score2
    if(direction == RIGHT):
        direction = LEFT
    else:
        direction = RIGHT
#    position1 = [HALF_PAD_WIDTH,HEIGHT/2]
#    position2 = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2]
    score1 = 0
    score2 = 0
    new_game()
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    global increase, direction
    
    
    ball_pos[0] += increase*ball_vel[0]
    ball_pos[1] += increase*ball_vel[1]
    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        
    if (ball_pos[0] <= PAD_WIDTH + BALL_RADIUS):
        if(ball_pos[1] >= position1[1] - HALF_PAD_HEIGHT and
           ball_pos[1] <= position1[1] + HALF_PAD_HEIGHT):
                ball_vel[0] = - ball_vel[0]
                increase *= 1.1
        else:
            score2 += 1
            direction = RIGHT
            new_game()
    
    if (ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS):
        if(ball_pos[1] >= position2[1] - HALF_PAD_HEIGHT and
           ball_pos[1] <= position2[1] + HALF_PAD_HEIGHT):
                ball_vel[0] = - ball_vel[0]
                increase *= 1.1
        else:
            score1 += 1
            direction = LEFT
            new_game()
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    
    # draw paddles

    position1[1] += paddle1_vel[1]
    
    if(position1[1] <= HALF_PAD_HEIGHT):
        position1[1] = HALF_PAD_HEIGHT
    
    if(position1[1] >= HEIGHT - HALF_PAD_HEIGHT):
        position1[1] = HEIGHT - HALF_PAD_HEIGHT
        
    canvas.draw_polygon([(0, position1[1] + HALF_PAD_HEIGHT),
                         (0, position1[1] - HALF_PAD_HEIGHT),
                         (PAD_WIDTH, position1[1] - HALF_PAD_HEIGHT),
                         (PAD_WIDTH, position1[1] + HALF_PAD_HEIGHT)],1,"White","White")
    
    position2[1] += paddle2_vel[1]                        
    
    if(position2[1] <= HALF_PAD_HEIGHT):
        position2[1] = HALF_PAD_HEIGHT
    
    if(position2[1] >= HEIGHT - HALF_PAD_HEIGHT):
        position2[1] = HEIGHT - HALF_PAD_HEIGHT
    
    canvas.draw_polygon([(WIDTH - PAD_WIDTH, position2[1] + HALF_PAD_HEIGHT),
                         (WIDTH - PAD_WIDTH, position2[1] - HALF_PAD_HEIGHT),
                         (WIDTH, position2[1] - HALF_PAD_HEIGHT),
                         (WIDTH, position2[1] + HALF_PAD_HEIGHT)],1,"White","White")                     
    # draw scores
    
    canvas.draw_text(str(score1), (180,80), 50, "White")
    canvas.draw_text(str(score2), (400,80), 50, "White")
                     
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if(key == simplegui.KEY_MAP["w"]):
        paddle1_vel[1] -= acc
    if(key == simplegui.KEY_MAP["s"]):
        paddle1_vel[1] += acc
    
    if(key == simplegui.KEY_MAP["up"]):
        paddle2_vel[1] -= acc
    if(key == simplegui.KEY_MAP["down"]):
        paddle2_vel[1] += acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if(key == simplegui.KEY_MAP["w"]):
        paddle1_vel[1] = 0
    if(key == simplegui.KEY_MAP["s"]):
        paddle1_vel[1] = 0
    
    if(key == simplegui.KEY_MAP["up"]):
        paddle2_vel[1] = 0
    if(key == simplegui.KEY_MAP["down"]):
        paddle2_vel[1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
Reset = frame.add_button("Reset", reset, 50)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()
