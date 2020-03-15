from tkinter import *
import random

WIDTH = 900
HEIGHT = 300

# Scores for each player
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

# Speed Score
INITIAL_SPEED = 20

PAD_W = 10
PAD_H = 100

BALL_RADIUS = 40

#Ball speed
BALL_X_CHANGE = 20
BALL_Y_CHANGE = 0

root = Tk()
root.title("Ping Pong")

c = Canvas(root, width=WIDTH, height=HEIGHT, background="#00ee55")
c.pack()
# Left Line
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="black")
# Right Line
c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill="black")
# Center Line
c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="white")
# Ball
BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2,
					 HEIGHT/2-BALL_RADIUS/2,
					 WIDTH/2+BALL_RADIUS/2,
					 HEIGHT/2 + BALL_RADIUS/2, fill="#ffcc44")

# Pads
# Left Pad
LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H, width=PAD_W, fill="white")
# Right Pad
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2, PAD_H, width=PAD_W, fill="white")

# Score text
p_1_text = c.create_text(WIDTH - WIDTH/6, 
						PAD_H/4,
						text=PLAYER_1_SCORE, 
						font='Arial 20', 
						fill='aqua')
p_2_text = c.create_text(WIDTH/6, 
						PAD_H/4,
						text=PLAYER_2_SCORE, 
						font='Arial 20', 
						fill='aqua')

# Pad Speed
PAD_SPEED = 20
# Left Pad Speed
LEFT_PAD_SPEED = 0
# Right Pad Speed
RIGHT_PAD_SPEED = 0

# Ball Speed with every hit
BALL_SPEED_UP = 1.00
# Ball Max Speed
BALL_MAX_SPEED = 30
# Ball Min Speed horizontal
BALL_X_SPEED = 20
# Ball Min Speed vertical
BALL_Y_SPEED = 20
# Distance to right border
right_line_distance = WIDTH - PAD_W

# Scoring
def update_score(player):
	global PLAYER_1_SCORE, PLAYER_2_SCORE
	if player == 'right':
		PLAYER_1_SCORE+=1
		c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
	else:
		PLAYER_2_SCORE+=1
		c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

# Respawn
def spawn_ball():
	global BALL_X_SPEED
	c.coords(BALL, WIDTH/2-BALL_RADIUS/2,
			HEIGHT/2-BALL_RADIUS/2,
			WIDTH/2+BALL_RADIUS/2,
			HEIGHT/2+BALL_RADIUS/2)
	BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED)/abs(BALL_X_SPEED)

# Bounce Ball from rockets
def bounce(action):
	global BALL_X_SPEED, BALL_Y_SPEED
	if action == 'strike':
		BALL_Y_SPEED = random.randrange(-10, 10)
		if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
			BALL_X_SPEED *= -BALL_SPEED_UP
		else: 
			BALL_X_SPEED = -BALL_X_SPEED
	else:
		BALL_Y_SPEED = -BALL_Y_SPEED



#Movement Ball function
def move_ball():
	ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
	ball_center = (ball_top + ball_bot)/2
	# Vertical bounce
	if ball_right + BALL_X_SPEED < right_line_distance and ball_left + BALL_X_SPEED > PAD_W:
		c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
	elif ball_right == right_line_distance or ball_left == PAD_W:
		if ball_right > WIDTH / 2:
			if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
				bounce('strike')
			else:
				update_score('left')
				spawn_ball()
		else:
			if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
				bounce('strike')
			else:
				update_score('right')
				spawn_ball()
	else:
		if ball_right > WIDTH / 2:
			c.move(BALL, right_line_distance-ball_right, BALL_Y_SPEED)
		else:
			c.move(BALL, -ball_left + PAD_W, BALL_Y_SPEED)
	if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
		bounce('ricochet')


#Movement function
def move_pads():
	PADS = {LEFT_PAD:LEFT_PAD_SPEED,
			RIGHT_PAD:RIGHT_PAD_SPEED}
	for pad in PADS:
		c.move(pad, 0, PADS[pad])
		if c.coords(pad)[1] < 0:
			c.move(pad, 0, -c.coords(pad)[1])
		elif c.coords(pad)[3] > HEIGHT:
			c.move(pad, 0, HEIGHT - c.coords(pad)[3])



def main():
	move_ball()
	move_pads()
	root.after(30, main)

# Focus Canvas
c.focus_set()

# Button Configuration
def movement_handler(event):
	global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
	if event.keysym == '1':
		LEFT_PAD_SPEED = -PAD_SPEED
	elif event.keysym == '2':
		LEFT_PAD_SPEED = PAD_SPEED
	elif event.keysym == 'Up':
		RIGHT_PAD_SPEED = -PAD_SPEED
	elif event.keysym == 'Down':
		RIGHT_PAD_SPEED = PAD_SPEED

c.bind("<KeyPress>", movement_handler)

def stop_pad(event):
	global LEFT_PAD_SPEED, RIGHT_PAD_SPEED	
	if event.keysym in ('1', '2'):
		LEFT_PAD_SPEED = 0
	elif event.keysym in ('Up', 'Down'):
		RIGHT_PAD_SPEED = 0

c.bind("<KeyRelease>", stop_pad)

main()
root.mainloop()

