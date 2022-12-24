import tkinter as tk
from PIL import Image, ImageTk
import random
import copy

# 1. FRAME SETUP

# Switch between page frames
def raise_frame(frame):
    frame.tkraise()

# Switch to game window from start window
def started_game():
    raise_frame(game_window)
    canvas.after(1000, countdown_timer) # countdown text (center)

# Switch to end game window
def change_to_end_screen(final_score):
    raise_frame(end_window)
    # 3. END SCREEN
    cv = tk.Canvas(end_window, width = 30*20, height = 31*20, highlightthickness=0)
    cv.create_image(0, 0, image = new_background, anchor = "nw")
    cv.pack()

    # Display game over and score text
    cv.create_rectangle(180, 270, 420, 370, fill="black")
    cv.create_text(300, 300, text = "GAME OVER", fill = "Yellow", anchor = "center", font = ("lucida console", 30))
    cv.create_text(300, 350, text = f"SCORE: {final_score}", fill = "Yellow", anchor = "center", font = ("lucida console", 25))

    # Display the restart and exit button
    tk.Button(end_window, text = "RESTART", fg = "yellow", bg = "black", activeforeground = "yellow", activebackground = "blue", bd = 0, font = ("lucida console", 15), width = 10, height = 1, command = restarted_game).pack()
    tk.Button(end_window, text = "EXIT", fg = "yellow", bg = "black", activeforeground = "yellow", activebackground = "blue", bd = 0, font = ("lucida console", 15), width = 8, height = 1, command = window.destroy).pack()

# Switch to game window from end window
def restarted_game():
    raise_frame(game_window)
    restart()

# 2. MATH LOGIC

def int1_int2_sum(): 
    int1 = random.choice(easy_mode_range)
    int2 = random.choice(easy_mode_range)
    soln = int1 + int2
    return int1, int2, soln

# Returns either a,b,c or d that can be used to assign the correct solution to. 
def soln_assigner():
    return random.choice(option_letters)

# Takes in the sum of the two integers as an input and returns a a,b,c,d dictionary, with one of the options being correct
def assigned_options(soln):
    edited_option_dd = copy.deepcopy(option_dd_initial)
    edited_possible_soln = copy.deepcopy(possible_soln)
    assigned_soln_slot = soln_assigner() #stores a letter a,b,c or d to assign the correct solution to
    edited_option_dd[assigned_soln_slot] = soln #takes the stored correct assignmed slot and changes the False to the solution
    edited_possible_soln.remove(soln) #removes the solution from the possible solution as it has already been assigned.
    
    for option in option_letters:
        if option == assigned_soln_slot:
            continue
        else:
            other_assigned_option = random.choice(edited_possible_soln)
            edited_option_dd[option] = other_assigned_option
            edited_possible_soln.remove(other_assigned_option)
    return edited_option_dd 

# 3. GAME SETUP

# Generates the initial two random integers and gives the following values at 0,1,2,3 respectively - 0: integer 1, integer 2, sum, dictionary of scrambled options to be displayed
def start_game():
    initial_parameters = int1_int2_sum()
    display_dd = assigned_options(initial_parameters[2])
    return initial_parameters[0], initial_parameters[1], initial_parameters[2], display_dd

# Displays "3...", "2...", "1...", "Go!!" before the timer starts running   
def countdown_timer():
    global countdown
    countdown -= 0.01
    if (2 < countdown <= 3):
        canvas.itemconfig(lbl_countdown, text = "3...")
        canvas.after(10, countdown_timer)
        # restrict movement when countdown is happening
        window.bind("<w>", stop)
        window.bind("<a>", stop)
        window.bind("<s>", stop)
        window.bind("<d>", stop)
    elif (1 < countdown <= 2):
        canvas.itemconfig(lbl_countdown, text = "2...")
        canvas.after(10, countdown_timer)
        # restrict movement when countdown is happening
        window.bind("<w>", stop)
        window.bind("<a>", stop)
        window.bind("<s>", stop)
        window.bind("<d>", stop)
    elif (0 < countdown <= 1):
        canvas.itemconfig(lbl_countdown, text = "1...")
        canvas.after(10, countdown_timer)
        # restrict movement when countdown is happening
        window.bind("<w>", stop)
        window.bind("<a>", stop)
        window.bind("<s>", stop)
        window.bind("<d>", stop)
    elif (-0.1 < countdown <= 0):
        canvas.itemconfig(lbl_countdown, text = "Go!!")
        canvas.after(10, countdown_timer)
    elif (countdown <= 0.1):
        # when countdown is up, remove countdown text, display question, options, update timer & score
        canvas.after(1000, update_question_options(integer1, integer2, display_dict))
        canvas.after(1000, updated_timer)
        canvas.itemconfig(lbl_countdown, text = "")
        canvas.itemconfig(lbl_score, text = f"SCORE: {score}")
        countdown = 3

# Displays amount of time left
def updated_timer():
    global timer
    if (timer > 5):
        timer -= 1
        canvas.itemconfig(lbl_timer, text= f"TIME: {timer}")
        canvas.after(1000, updated_timer)
    elif (0.1 < timer <= 5):
        timer -= 0.1
        canvas.itemconfig(lbl_timer, text= f"TIME: {round(timer, 2)}")
        canvas.after(100, updated_timer)
    elif (timer <= 0.1):
        canvas.itemconfig(lbl_timer, text = "Times Up!")
        window.bind("<w>", stop)
        window.bind("<s>", stop)
        window.bind("<a>", stop)
        window.bind("<d>", stop)
        canvas.itemconfig(pacman, image = pacman4_image)
        canvas.itemconfig(lbl_equation, text = "")
        canvas.itemconfig(lbl_options1, text = "")
        canvas.itemconfig(lbl_options2, text = "")
        final_score = int(canvas.itemcget(lbl_score, "text")[7:])
        change_to_end_screen(final_score)
        timer = 60

# Displays the question and options
def update_question_options(integer1, integer2, display_dict):
    canvas.itemconfig(lbl_equation, text = f"{integer1} + {integer2} = ?")
    canvas.itemconfig(lbl_options1, text = f"A:{display_dict['a']} B:{display_dict['b']}")
    canvas.itemconfig(lbl_options2, text = f"C:{display_dict['c']} D:{display_dict['d']}")

# Spawn boxes for options (A, B, C, D) to match ghost colors and create text within the box to match letters
def spawn_options(options_coords):
    A = canvas.create_rectangle(options_coords[0][0], options_coords[0][1], options_coords[0][0]+20, options_coords[0][1]+20, fill="red", tag="a")
    A_text = canvas.create_text(options_coords[0][0]+6, options_coords[0][1]+3, fill="black", anchor="nw", text="A", tag="a")
    B = canvas.create_rectangle(options_coords[1][0], options_coords[1][1], options_coords[1][0]+20, options_coords[1][1]+20, fill="pink", tag="b")
    B_text = canvas.create_text(options_coords[1][0]+6, options_coords[1][1]+3, fill="black", anchor="nw", text="B", tag="b")
    C = canvas.create_rectangle(options_coords[2][0], options_coords[2][1], options_coords[2][0]+20, options_coords[2][1]+20, fill="#1fd655", tag="c")
    C_text = canvas.create_text(options_coords[2][0]+6, options_coords[2][1]+3, fill="black", anchor="nw", text="C", tag="c")
    D = canvas.create_rectangle(options_coords[3][0], options_coords[3][1], options_coords[3][0]+20, options_coords[3][1]+20, fill="cyan", tag="d")
    D_text = canvas.create_text(options_coords[3][0]+6, options_coords[3][1]+3, fill="black", anchor="nw", text="D", tag="d")

# Open and resize pacman image
def create_images(filepath):
    images_dir = "pacmath\\images\\" # change depending on directory
    image = Image.open(images_dir + filepath) # open image using pillow
    resized_image = image.resize((20, 20)) # resize image to fit 20x20 box
    new_image = ImageTk.PhotoImage(resized_image) # initialise photo image option
    return new_image

# 4. GAME MECHANICS

# Move pacman
def move(direction):
    # Get currenct position of pacman
    current_x, current_y = canvas.coords(pacman)[0], canvas.coords(pacman)[1]

    for k, v in grid.items():
        if (current_x, current_y) == v[3]: # if current coords of pacman exist within grid, get current tile and box
            tile = v[1]
            current_box = k

            # Eat the food
            if tile == 1: # if pacman is on a food tile, delete the box from food_dict to replace with empty tile, add current coords to eaten_dict
                canvas.delete(food_dict[current_box])
                eaten_dict[current_box] = (current_x, current_y)

            # Check for wall
            wall = {2: "vertical", 3: "horizontal", 4: "top left", 5: "top right", 6: "bottom left", 7: "bottom right"}
            wall_check = [wall_up(wall, current_box), wall_down(wall, current_box), wall_left(wall, current_box), wall_right(wall, current_box)] # if there is a wall on top, restrict movement upwards, and so on
            window.bind("<w>", stop) if wall_check[0] == True else window.bind("<w>", up)
            window.bind("<s>", stop) if wall_check[1] == True else window.bind("<s>", down)
            window.bind("<a>", stop) if wall_check[2] == True else window.bind("<a>", left)
            window.bind("<d>", stop) if wall_check[3] == True else window.bind("<d>", right)

            # Check if can hop from left edge to right edge and vice versa
            if (current_x, current_y) == (0, 16*20) and direction == "left":
                canvas.move(pacman, 29*20, 0)
            elif (current_x, current_y) == (29*20, 16*20) and direction == "right":
                canvas.move(pacman, -29*20, 0)

            # Check if pacman is at the right option
            for possible_box in options_box[0]: 
                if current_box == possible_box: # pacman is on a box that contains an option
                    score = int(canvas.itemcget(lbl_score, "text")[7:]) # display new score
                    if (current_box == correct_option[0][1]): # pacman is on the right box
                        canvas.delete(correct_option[0][0]) # delete the right box
                        score += 10 # add score
                        wrong_options.clear() # clear dictionary of wrong option

                        # Change question
                        assignments = start_game() # get new questions and options
                        integer1 = assignments[0]
                        integer2 = assignments[1]
                        display_dict = assignments[3]
                        integer_total = integer1 + integer2
                        update_question_options(integer1, integer2, display_dict) # update question and options display

                        # Respawn food and options
                        for k, v in spawn.items():
                            canvas.delete("a", "b", "c", "d") # delete all options
                        spawn.clear() # clear spawn dictionary

                        for eaten_box, eaten_coords in eaten_dict.items():
                            if eaten_coords != correct_option[0][2]: # do not spawn food at current location
                                (eaten_x, eaten_y) = eaten_coords
                                food = canvas.create_rectangle(eaten_x+7, eaten_y+7, eaten_x+13, eaten_y+13, fill="orange", outline="orange") # respawn food
                                food_dict[eaten_box] = food
                                food_list.append(eaten_box)

                        eaten_dict.clear() # clear eaten dictionary
                        eaten_dict[correct_option[0][1]] = correct_option[0][2] # include respawn location
                        options_box.clear() # clear options dictionary
                        options_box.append(random.choices(food_list, k=4)) # get new random options from food_list
                        options_coords = [grid[i][3] for i in options_box[0]] # get new coords from new options
                        spawn_options(options_coords) # spawn new options

                        # Get new spawn dictionary
                        for i in range(len(options_box[0])):
                            spawn[options_letters[i]] = [options_box[0][i], options_coords[i]]

                        # Get new correct_option dictionary
                        for letter, number in display_dict.items():
                            if number == integer_total:
                                correct_option[0] = [letter, spawn[letter][0], spawn[letter][1]]

                    else: # pacman is not on the right box
                        for k, v in spawn.items():
                            if (v[0] == current_box and v[0] not in wrong_options): # check for revisiting to avoid subtracting extra points
                                canvas.delete(k) # delete the box for wrong option
                                score -= 10 # subtract score
                                wrong_options[v[0]] = "wrong" # add current box to dictionary of wrong_options that have been visited

                    canvas.itemconfig(lbl_score, text = f"SCORE: {score}") # update score

                    if score > highscore[-1]:
                        highscore.append(score)
                        canvas.itemconfig(lbl_highscore, text = f"HIGHSCORE: {highscore[-1]}") # update highscore

# Wall checks
def wall_up(wall, current_box):
    return True if (grid[current_box - 30][1] in wall) else False

def wall_down(wall, current_box):
    return True if (grid[current_box + 30][1] in wall) else False

def wall_left(wall, current_box):
    return True if (grid[current_box - 1][1] in wall) else False

def wall_right(wall, current_box):
    return True if (grid[current_box + 1][1] in wall) else False

# Restart game
def restart():
    # Clear displays
    canvas.itemconfig(lbl_restart, text = "")
    canvas.delete(food_dict[765])

    # Reset variables
    score = 0

    # Reset displays
    canvas.itemconfig(pacman, image = right2_image)
    canvas.moveto(pacman, 14*20, 25*20)
    canvas.after(1000, countdown_timer)
    canvas.itemconfig(lbl_score, text = f"SCORE: {score}")
    canvas.itemconfig(lbl_timer, text = f"TIME: {timer}")

    # Respawn food and options
    for k, v in spawn.items():
        canvas.delete("a", "b", "c", "d") # delete all options
        eaten_dict[v[0]] = v[1] # include option locations
    spawn.clear() # clear spawn dictionary

    for eaten_box, eaten_coords in eaten_dict.items():
        if eaten_coords != (280, 500):
            if eaten_coords != correct_option[0][2]: # do not spawn food at current location
                (eaten_x, eaten_y) = eaten_coords
                food = canvas.create_rectangle(eaten_x+7, eaten_y+7, eaten_x+13, eaten_y+13, fill="orange", outline="orange") # respawn food
                food_dict[eaten_box] = food
                food_list.append(eaten_box)

    food_list.remove(765) # remove pacman spawn from possible location to spawn options
    eaten_dict.clear() # clear eaten dictionary
    eaten_dict[correct_option[0][1]] = correct_option[0][2] # include respawn location
    options_box.clear() # clear options dictionary
    options_box.append(random.choices(food_list, k=4)) # get new random options from food_list
    options_coords = [grid[i][3] for i in options_box[0]] # get new coords from new options
    spawn_options(options_coords) # spawn new options

    # Get new spawn dictionary
    for i in range(len(options_box[0])):
        spawn[options_letters[i]] = [options_box[0][i], options_coords[i]]

    # Get new correct_option dictionary
    for letter, number in display_dict.items():
        if number == integer_total:
            correct_option[0] = [letter, spawn[letter][0], spawn[letter][1]]

# Keybind movements to alternate between 2 pacman images with each keypress
def up(e):
    if canvas.coords(pacman)[1] % 40:
        canvas.itemconfig(pacman, image = up2_image)
        canvas.move(pacman, 0, -20)
        canvas.itemconfig(pacman, image = up3_image)
    else:
        canvas.itemconfig(pacman, image = up3_image)
        canvas.move(pacman, 0, -20)
        canvas.itemconfig(pacman, image = up2_image)
    move(direction="up")

def down(e):
    if canvas.coords(pacman)[1] % 40:
        canvas.itemconfig(pacman, image = down2_image)
        canvas.move(pacman, 0, 20)
        canvas.itemconfig(pacman, image = down3_image)
    else:
        canvas.itemconfig(pacman, image = down3_image)
        canvas.move(pacman, 0, 20)
        canvas.itemconfig(pacman, image = down2_image)
    move(direction="down")

def left(e):
    if canvas.coords(pacman)[0] % 40:
        canvas.itemconfig(pacman, image = left2_image)
        canvas.move(pacman, -20, 0)
        canvas.itemconfig(pacman, image = left3_image)
    else:
        canvas.itemconfig(pacman, image = left3_image)
        canvas.move(pacman, -20, 0)
        canvas.itemconfig(pacman, image = left2_image)
    move(direction="left")

def right(e):
    if canvas.coords(pacman)[0] % 40:
        canvas.itemconfig(pacman, image = right2_image)
        canvas.move(pacman, 20, 0)
        canvas.itemconfig(pacman, image = right3_image)
    else:
        canvas.itemconfig(pacman, image = right3_image)
        canvas.move(pacman, 20, 0)
        canvas.itemconfig(pacman, image = right2_image)
    move(direction="right")

# Stop pacman from moving
def stop(e):
    canvas.move(pacman, 0, 0)
    move(direction="none")

# INITIALISE WINDOW

window = tk.Tk()
window.title("Pac-Math")

# Create three frames to switch between start screen, game screen and end screen
start_window = tk.Frame(window, bg = "black")
game_window = tk.Frame(window)
end_window = tk.Frame(window, bg = "black")

for frame in (start_window, game_window, end_window):
    frame.grid(row=0, column=0, sticky='news')

# Create background image
background_image = Image.open(r"pacmath\images\board.png")
resized_background = background_image.resize((30*20, 32*20))
new_background = ImageTk.PhotoImage(resized_background)

# 1. START SCREEN

# Create canvas
c = tk.Canvas(start_window, width = 30*20, height = 20*20, highlightthickness=0, bg = "black")
c.pack()

# Create text
x, y = 50, -100
# Letter p
c.create_rectangle(x+15, y+136, x+30, y+442, fill = "yellow", outline = "yellow")  
c.create_oval(x+15, y+136, x+75, y+272, fill = "yellow", outline = "yellow")
# Letter a
c.create_rectangle(x+60, y+306, x+75, y+442, fill = "yellow", outline = "yellow")
c.create_rectangle(x+60, y+306, x+105, y+374, fill = "yellow", outline = "yellow")
c.create_rectangle(x+90, y+306, x+105, y+442, fill = "yellow", outline = "yellow")
# Letter c
c.create_rectangle(x+120, y+306, x+135, y+442, fill = "yellow", outline = "yellow")
c.create_rectangle(x+120, y+306, x+165, y+357, fill = "yellow", outline = "yellow")
c.create_rectangle(x+120, y+391, x+165, y+442, fill = "yellow", outline = "yellow")
# Dash
c.create_rectangle(x+180, y+357, x+225, y+291, fill = "yellow", outline = "yellow")
# Letter m
c.create_rectangle(x+240, y+136, x+255, y+442, fill = "yellow", outline = "yellow")
c.create_rectangle(x+240, y+136, x+315, y+238, fill = "yellow", outline = "yellow")
c.create_rectangle(x+270, y+136, x+285, y+442, fill = "yellow", outline = "yellow")
c.create_rectangle(x+300, y+136, x+315, y+442, fill = "yellow", outline = "yellow")
# Letter a
c.create_rectangle(x+330, y+306, x+345, y+442, fill = "yellow", outline = "yellow")
c.create_rectangle(x+330, y+306, x+375, y+374, fill = "yellow", outline = "yellow")
c.create_rectangle(x+360, y+306, x+375, y+442, fill = "yellow", outline = "yellow")
# Letter t
c.create_rectangle(x+390, y+306, x+435, y+374, fill = "yellow", outline = "yellow")
c.create_rectangle(x+405, y+306, x+420, y+442, fill = "yellow", outline = "yellow")
# Letter h
c.create_rectangle(x+460, y+306, x+475, y+442, fill = "yellow", outline = "yellow")
c.create_rectangle(x+460, y+357, x+505, y+391, fill = "yellow", outline = "yellow")
c.create_rectangle(x+490, y+306, x+505, y+442, fill = "yellow", outline = "yellow")

# Display the instructions
tk.Label(start_window, text = "1. Solve the math equation", fg = "yellow", bg = "black", font = ("lucida console", 15)).pack()
tk.Label(start_window, text = "2. Get to the right box", fg = "yellow", bg = "black", font = ("lucida console", 15)).pack()
tk.Label(start_window, text = "3. Score points!", fg = "yellow", bg = "black", font = ("lucida console", 15)).pack()
tk.Label(start_window, text = "Keys: WASD", fg = "yellow", bg = "black", font = ("lucida console", 15)).pack()

# Display the start button
tk.Button(start_window, text = "Click here to start", fg = "yellow", bg = "black", activeforeground = "yellow", activebackground = "blue", bd = 0, font = ("lucida console", 15), width = 20, height = 2, command = started_game).pack()

# 2. GAME SCREEN

# Create game window canvas
canvas = tk.Canvas(game_window, width=30*20, height=34*20, bg="black") # set window size to fit 34x30 size 20x20 boxes
canvas.pack()

#QUESTIONS, OPTIONS, SCORE, TIMER

# Unchanged Parameters
easy_mode_range = list(range(1,11))
possible_soln = list(range(max(easy_mode_range) + max(easy_mode_range)))
option_dd_initial = {'a':False,'b':False,'c':False,'d':False}
option_letters = ['a','b','c','d']

#Empty Parameters
score = 0
highscore = [0]
final_score = 0

#Dependent Variables
timer = 60
countdown = 3

assignments = start_game() 

#In game Placeholders
integer1 = assignments[0]
integer2 = assignments[1]
display_dict = assignments[3]
integer_total = integer1 + integer2

# Create text on canvas
lbl_countdown = canvas.create_text(14*20, 16*20, text = "", fill = "Yellow", anchor = "nw", font = ("lucida console", 15))
lbl_score = canvas.create_text(4*20, 7, text = f"SCORE: {score}", fill = "Yellow", anchor = "nw", font = ("lucida console", 15)) # score text (top)
lbl_timer = canvas.create_text(12*20, 7, text = f"TIME: {timer}", fill = "Yellow", anchor = "nw", font = ("lucida console", 15)) # timer text (top)
lbl_highscore = canvas.create_text(19*20, 7, text = f"HIGHSCORE: {highscore[-1]}", fill = "Yellow", anchor = "nw", font = ("lucida console", 15)) # highscore text (top)
# canvas.after(1000, lbl_timer)
lbl_equation = canvas.create_text(13*20+3, 15*20+7, text = "", fill = "Yellow", anchor = "nw", font = ("lucida console", 10)) # question text (center row 1)
lbl_options1 = canvas.create_text(13*20+3, 16*20+7, text = "", fill = "Yellow", anchor = "nw", font = ("lucida console", 10)) # A & B options text (center row 2)
lbl_options2 = canvas.create_text(13*20+3, 17*20+7, text = "", fill = "Yellow", anchor = "nw", font = ("lucida console", 10)) # C & D options text (center row 3)
lbl_restart = canvas.create_text(13*20, 16*20, text = "", fill = "Yellow", anchor = "nw", font = ("lucida console", 10))

# BOARD

# Get grid (list of lists)
# First list empty to display score, time and highscore
board_matrix = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5],
[2, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 2],
[2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
[2, 2, 1, 4, 3, 3, 5, 1, 4, 3, 3, 3, 5, 1, 2, 2, 1, 4, 3, 3, 3, 5, 1, 4, 3, 3, 5, 1, 2, 2],
[2, 2, 1, 2, 0, 0, 2, 1, 2, 0, 0, 0, 2, 1, 2, 2, 1, 2, 0, 0, 0, 2, 1, 2, 0, 0, 2, 1, 2, 2],
[2, 2, 1, 6, 3, 3, 7, 1, 6, 3, 3, 3, 7, 1, 6, 7, 1, 6, 3, 3, 3, 7, 1, 6, 3, 3, 7, 1, 2, 2],
[2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
[2, 2, 1, 4, 3, 3, 5, 1, 4, 5, 1, 4, 3, 3, 3, 3, 3, 3, 5, 1, 4, 5, 1, 4, 3, 3, 5, 1, 2, 2],
[2, 2, 1, 6, 3, 3, 7, 1, 2, 2, 1, 6, 3, 3, 5, 4, 3, 3, 7, 1, 2, 2, 1, 6, 3, 3, 7, 1, 2, 2],
[2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2],
[2, 6, 3, 3, 3, 3, 5, 1, 2, 6, 3, 3, 5, 1, 2, 2, 1, 4, 3, 3, 7, 2, 1, 4, 3, 3, 3, 3, 7, 2],
[2, 0, 0, 0, 0, 0, 2, 1, 2, 4, 3, 3, 7, 1, 6, 7, 1, 6, 3, 3, 5, 2, 1, 2, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 2],
[7, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 4, 3, 3, 9, 9, 3, 3, 5, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 6],
[3, 3, 3, 3, 3, 3, 7, 1, 6, 7, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 6, 7, 1, 6, 3, 3, 3, 3, 3, 3],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[3, 3, 3, 3, 3, 3, 5, 1, 4, 5, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 4, 5, 1, 4, 3, 3, 3, 3, 3, 3],
[5, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 6, 3, 3, 3, 3, 3, 3, 7, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 4],
[2, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 4, 3, 3, 3, 3, 3, 3, 5, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 2],
[2, 4, 3, 3, 3, 3, 7, 1, 6, 7, 1, 6, 3, 3, 5, 4, 3, 3, 7, 1, 6, 7, 1, 6, 3, 3, 3, 3, 5, 2],
[2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
[2, 2, 1, 4, 3, 3, 5, 1, 4, 3, 3, 3, 5, 1, 2, 2, 1, 4, 3, 3, 3, 5, 1, 4, 3, 3, 5, 1, 2, 2],
[2, 2, 1, 6, 3, 5, 2, 1, 6, 3, 3, 3, 7, 1, 6, 7, 1, 6, 3, 3, 3, 7, 1, 2, 4, 3, 7, 1, 2, 2],
[2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2],
[2, 6, 3, 5, 1, 2, 2, 1, 4, 5, 1, 4, 3, 3, 3, 3, 3, 3, 5, 1, 4, 5, 1, 2, 2, 1, 4, 3, 7, 2],
[2, 4, 3, 7, 1, 6, 7, 1, 2, 2, 1, 6, 3, 3, 5, 4, 3, 3, 7, 1, 2, 2, 1, 6, 7, 1, 6, 3, 5, 2],
[2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2],
[2, 2, 1, 4, 3, 3, 3, 3, 7, 6, 3, 3, 5, 1, 2, 2, 1, 4, 3, 3, 7, 6, 3, 3, 3, 3, 5, 1, 2, 2],
[2, 2, 1, 6, 3, 3, 3, 3, 3, 3, 3, 3, 7, 1, 6, 7, 1, 6, 3, 3, 3, 3, 3, 3, 3, 3, 7, 1, 2, 2],
[2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
[2, 6, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 7, 2],
[6, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 7]]
# Edited https://github.com/plemaster01/PythonPacman/blob/main/board.py

# Get a dictionary of the top left coordinates for each box
tile_x = 0
tile_y = 0
coords = {}
box = 1
for col in range(len(board_matrix)):
    for row in range(len(board_matrix[0])):
        # canvas.create_rectangle(row*20, col*20, (row+1)*20, (col+1)*20, outline="white") # display guiding grids
        coords[box] = (row*20, col*20)
        box += 1

# Turn number in list into tile design
grid = {} # create dictionary to store grid values
food_dict = {} # create dictionary to store food tiles
food_list = [] # create list to store food tiles to spawn options
eaten_dict = {} # create list to store food tile that have been eaten
eaten_dict[765] = (280, 500) # include spawn location

for i in range(len(board_matrix)):
    for j in range(len(board_matrix[0])):
        tile = board_matrix[i][j]
        current_box = i*len(board_matrix[0])+1+j
        tile_x, tile_y = coords[current_box]
        grid[current_box] = [(i, j), tile, current_box, (tile_x, tile_y)]
        # print(f"board_matrix[{i}][{j}], tile: {tile}, box: {current_box}, coords: {tile_x, tile_y}")
        # grid: {box: [(height, width index), tile type, box, (x, ycoords)]}

        # Turn tile numbers into tile design
        if tile == 1: # food
            food = canvas.create_rectangle(tile_x+7, tile_y+7, tile_x+13, tile_y+13, fill="orange", outline="orange")
            food_dict[current_box] = food
            food_list.append(current_box)
        elif tile == 2: # vertical wall
            canvas.create_rectangle(tile_x+7, tile_y, tile_x+13, tile_y+20, fill="blue", outline="blue")
        elif tile == 3: # horizontal wall
            canvas.create_rectangle(tile_x, tile_y+7, tile_x+20, tile_y+13, fill="blue", outline="blue")
        elif tile == 4: # top left corner
            canvas.create_rectangle(tile_x+7, tile_y+7, tile_x+13, tile_y+20, fill="blue", outline="blue")
            canvas.create_rectangle(tile_x+13, tile_y+7, tile_x+20, tile_y+13, fill="blue", outline="blue")
        elif tile == 5: # top right corner
            canvas.create_rectangle(tile_x, tile_y+7, tile_x+7, tile_y+13, fill="blue", outline="blue")
            canvas.create_rectangle(tile_x+7, tile_y+7, tile_x+13, tile_y+20, fill="blue", outline="blue")
        elif tile == 6: # bottom left corner
            canvas.create_rectangle(tile_x+7, tile_y, tile_x+13, tile_y+13, fill="blue", outline="blue")
            canvas.create_rectangle(tile_x+13, tile_y+7, tile_x+20, tile_y+13, fill="blue", outline="blue")
        elif tile == 7: # bottom right corner
            canvas.create_rectangle(tile_x+7, tile_y, tile_x+13, tile_y+13, fill="blue", outline="blue")
            canvas.create_rectangle(tile_x, tile_y+7, tile_x+7, tile_y+13, fill="blue", outline="blue")

# Get options for question
options_letters = ['a', 'b', 'c', 'd']
options_box = []
options_box.append(random.choices(food_list, k=4)) # randomly choose boxes from boxes that contain food
options_coords = [grid[i][3] for i in options_box[0]] # get coordinates of option boxes
spawn = {}
for i in range(len(options_box[0])):
    spawn[options_letters[i]] = [options_box[0][i], options_coords[i]]
    # spawn: {letter: [box, coords]}

# Get correct answer
correct_option = {}
for letter, number in display_dict.items():
    if number == integer_total:
        correct_option[0] = [letter, spawn[letter][0], spawn[letter][1]]
        # correct_option : {0: [letter, box, coords]}

wrong_options = {} # set dictionary to store wrong options that have been visited

# PACMAN

# Set default pacman variables
pacman_x, pacman_y = 14*20, 25*20 # spawn point
direction = "right" # initial direction

# Half opened mouth
up2_image = create_images("Pacman_2_up.png")
down2_image = create_images("Pacman_2_down.png")
left2_image = create_images("Pacman_2_left.png")
right2_image = create_images("Pacman_2_right.png")

# Completely opened mouth
up3_image = create_images("Pacman_3_up.png")
down3_image = create_images("Pacman_3_down.png")
left3_image = create_images("Pacman_3_left.png")
right3_image = create_images("Pacman_3_right.png")

pacman4_image = create_images("Pacman_4.png")

# Create initial pacman
pacman = canvas.create_image(pacman_x, pacman_y, image = right2_image, anchor="nw")

spawn_options(options_coords)
move(direction)

raise_frame(start_window)
window.mainloop()