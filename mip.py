import tkinter as tk


class node():
    value: int
    parents = []
    children = []
    heuristic_values: bool

    def __init__(self, value):
        self.value = value
        self.children = []
        self.parents = []

def createTree(value: int):
    root = node(value)
    generatenodes(root)
    return root


def generatenodes(root: node):
    if (root.value == 0): return
    if (len(root.children) > 0):
        if (allchildren1(root)):
            return
    add3children(root.value, root)
    for child in root.children:
        generatenodes(child)


def allchildren1(root: node):
    for child in root.children:
        if (child.value != 0):
            return False
    return True


def add3children(value, root):
    if (value - 3 >= 0):
        t3 = node(value - 3)
        t3.parents.append(root)
        cs = hasCousinNode(t3)
        if (cs != None):
            if root not in cs.parents:
                cs.parents.append(root)
            if cs not in root.children:
                root.children.append(cs)
        else:
            if t3 not in root.children:
                root.children.append(t3)
    if (value - 2 >= 0):
        t2 = node(value - 2)
        t2.parents.append(root)
        cs = hasCousinNode(t2)
        if (cs != None):
            if root not in cs.parents:
                cs.parents.append(root)
            if cs not in root.children:
                root.children.append(cs)
        else:
            if t2 not in root.children:
                root.children.append(t2)
    if (value - 1 >= 0):
        t1 = node(value - 1)
        t1.parents.append(root)
        cs = hasCousinNode(t1)
        if (cs != None):
            if root not in cs.parents:
                cs.parents.append(root)
            if cs not in root.children:
                root.children.append(cs)
        else:
            if t1 not in root.children:
                root.children.append(t1)


def hasCousinNode(thisnode: node):
    if (len(thisnode.parents) == 0): return None
    if (len(thisnode.parents[0].parents) == 0): return None
    for i in range(0, len(thisnode.parents)):
        for grandnode in thisnode.parents[i].parents:
            for parentnode in grandnode.children:
                for siblingnode in parentnode.children:
                    if (siblingnode.value == thisnode.value):
                        return siblingnode
    return None


def eveluate(root: node, level_is_max):
    if root.value == 0:
        if level_is_max:
            root.heuristic_values = True
        else:
            root.heuristic_values = False
        return
    a = not level_is_max
    for child in root.children:
        if (not hasattr(child, "heuristic_values")):
            eveluate(child, a)
    minnode = False
    maxnode = False
    for child in root.children:
        if child.heuristic_values==True:
             maxnode = True
        else:
             minnode = True

    if level_is_max:
        root.heuristic_values = True if maxnode else False
    else:
        root.heuristic_values = False if minnode else True
    return root

def gonext(root: node, thevalue: int):
    for child in root.children:
        if(child.value == thevalue):
            return child
    return None

def getnext(root: node, player_is_maximizer):
    for child in root.children:
        if(child.heuristic_values == player_is_maximizer):
            return child
    return root.children[0]
# Define variables
root = tk.Tk()
root.geometry("400x400")
root.title("Nim Game")
root.resizable(False, False)

title_descr_label = tk.Label(
    root,
    text="Welcome to the Nim Game! There is a pile of 8 sticks. On each turn, a player can take 1, 2, or 3 sticks. The player who takes the last stick loses the game. To start the game press OK.",
    wraplength=350,
)
title_descr_label.pack()
thisnode = None
start_button = tk.Button(root, text="Ok", command=lambda: new_game())
start_button.pack()

player_choice = tk.StringVar()
pile_label = tk.Label(root, text="Sticks Left: 8")
pile_label.pack()

game_status_box = tk.Text(root, height=7, width=26)
game_status_box.insert(tk.END, "Sticks: ||||||||")
game_status_box.pack()

user_move_box = tk.Text(root, height=7, width=26)
user_move_box.insert(tk.END, "")
user_move_box.pack()

game_description = tk.Label(root, text="")
game_description.pack()

computer_first = False

def new_game():
    global sticks_left, thisnode
    sticks_left = 8
    # d = generate_tree()
    thisnode = createTree(8)
    thisnode = eveluate(thisnode, True)
    pile_label.config(text="Sticks Left: " + str(sticks_left))
    game_status_box.delete(1.0, tk.END)
    game_status_box.insert(tk.END, "Sticks: " + "|" * sticks_left)
    user_move_box.delete(1.0, tk.END)
    game_description.config(text="Do you want to start first? (y/n):")
    button_y.config(command=lambda: config_first_player_and_start())
    button_n.config(command=lambda: config_first_ai_and_start())

def config_first_ai_and_start():
    global computer_first, sticks_left
    if sticks_left==8:
        computer_first = True
        go_computer()

def config_first_player_and_start():
    global computer_first, sticks_left
    if sticks_left==8:
        computer_first = False
        go_player()

def go_player():
    global sticks_left
    game_description.config(text="Your turn. How many sticks do you want to take?")
    button_1.config(command=lambda: remove_sticks(1))
    button_2.config(command=lambda: remove_sticks(2))
    button_3.config(command=lambda: remove_sticks(3))


def remove_sticks(num_sticks):
    global sticks_left, thisnode
    if num_sticks > sticks_left:
        user_move_box.insert(tk.END, "Invalid choice. Try again.\n")
        return
    sticks_taken = num_sticks
    sticks_left -= sticks_taken
    if sticks_left < 0:
        sticks_left = 0
    pile_label.config(text="Sticks Left: " + str(sticks_left))
    game_status_box.delete(1.0, tk.END)
    game_status_box.insert(tk.END, "Sticks: " + "|" * sticks_left)
    if sticks_taken == 1:
        user_move_box.insert(tk.END, "You removed 1 stick.\n")
    else:
        user_move_box.insert(tk.END, "You removed {} sticks.\n".format(sticks_taken))
    thisnode = gonext(thisnode, thisnode.value -sticks_taken)
    if sticks_left == 0:
        game_description.config(text="You lose! Play again?")
        button_y.config(command=new_game)
        button_n.config(command=root.destroy)
    else:
        go_computer()


def go_computer():
    global sticks_left, thisnode, computer_first
    game_description.config(text="Computer's turn...")
    thiscount = thisnode.value
    thisnode = getnext(thisnode, computer_first)
    sticks_taken = thiscount-thisnode.value #computer_play(sticks_left)
    sticks_left -= sticks_taken
    pile_label.config(text="Sticks Left: " + str(sticks_left))
    game_status_box.delete(1.0, tk.END)
    game_status_box.insert(tk.END, "Sticks: " + "|" * sticks_left)
    if sticks_taken == 1:
        user_move_box.insert(tk.END, "Computer removed 1 stick.\n")
    else:
        user_move_box.insert(tk.END, "Computer removed {} sticks.\n".format(sticks_taken))
    if sticks_left == 0:
        game_description.config(text="You win! Play again?")
        button_y.config(command=new_game)
        button_n.config(command=root.destroy)
    else:
        go_player()


button_y = tk.Button(root, text="Yes")
button_y.pack(side=tk.LEFT)

button_n = tk.Button(root, text="No")
button_n.pack(side=tk.LEFT)

# Define buttons

button_1 = tk.Button(root, text="1", width=1, height=1, padx=1, pady=1)
button_1.pack(side=tk.RIGHT, padx=1)

button_2 = tk.Button(root, text="2", width=1, height=1, padx=1, pady=1)
button_2.pack(side=tk.RIGHT, padx=1)

button_3 = tk.Button(root, text="3", width=1, height=1, padx=1, pady=1)
button_3.pack(side=tk.RIGHT, padx=1)

root.mainloop()
