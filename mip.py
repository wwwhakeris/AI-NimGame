import random
import tkinter as tk
from anytree import Node, RenderTree


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

description_label = tk.Label(
    root,
    text="Welcome to the Nim Game! There is a pile of 8 sticks. On each turn, a player can take 1, 2, or 3 sticks. The player who takes the last stick loses the game. To start the game press OK.",
    wraplength=350,
)
description_label.pack()
thisnode = None
start_button = tk.Button(root, text="Ok", command=lambda: start_new_game())
start_button.pack()

player_choice = tk.StringVar()
pile_label = tk.Label(root, text="Sticks Left: 8")
pile_label.pack()

text_box1 = tk.Text(root, height=7, width=26)
text_box1.insert(tk.END, "Sticks: ||||||||")
text_box1.pack()

text_box2 = tk.Text(root, height=7, width=26)
text_box2.insert(tk.END, "")
text_box2.pack()

description = tk.Label(root, text="")
description.pack()

computer_first = False

def start_new_game():
    global sticks_left, thisnode
    sticks_left = 8
    # d = generate_tree()
    thisnode = createTree(8)
    thisnode = eveluate(thisnode, True)
    pile_label.config(text="Sticks Left: " + str(sticks_left))
    text_box1.delete(1.0, tk.END)
    text_box1.insert(tk.END, "Sticks: " + "|" * sticks_left)
    text_box2.delete(1.0, tk.END)
    description.config(text="Do you want to start first? (y/n):")
    button_y.config(command=lambda: config_first_player_and_start())
    button_n.config(command=lambda: config_first_ai_and_start())

def config_first_ai_and_start():
    global computer_first, sticks_left
    if sticks_left==8:
        computer_first = True
        computer_turn()

def config_first_player_and_start():
    global computer_first, sticks_left
    if sticks_left==8:
        computer_first = False
        player_turn()

def player_turn():
    global sticks_left
    description.config(text="Your turn. How many sticks do you want to take?")
    button_1.config(command=lambda: remove_sticks(1))
    button_2.config(command=lambda: remove_sticks(2))
    button_3.config(command=lambda: remove_sticks(3))


def remove_sticks(num_sticks):
    global sticks_left, thisnode
    if num_sticks > sticks_left:
        text_box2.insert(tk.END, "Invalid choice. Try again.\n")
        return
    sticks_taken = num_sticks
    sticks_left -= sticks_taken
    if sticks_left < 0:
        sticks_left = 0
    pile_label.config(text="Sticks Left: " + str(sticks_left))
    text_box1.delete(1.0, tk.END)
    text_box1.insert(tk.END, "Sticks: " + "|" * sticks_left)
    if sticks_taken == 1:
        text_box2.insert(tk.END, "You removed 1 stick.\n")
    else:
        text_box2.insert(tk.END, "You removed {} sticks.\n".format(sticks_taken))
    thisnode = gonext(thisnode, thisnode.value -sticks_taken)
    if sticks_left == 0:
        description.config(text="You lose! Play again?")
        button_y.config(command=start_new_game)
        button_n.config(command=root.destroy)
    else:
        computer_turn()


def computer_turn():
    global sticks_left, thisnode, computer_first
    description.config(text="Computer's turn...")
    thiscount = thisnode.value
    thisnode = getnext(thisnode, computer_first)
    sticks_taken = thiscount-thisnode.value #computer_play(sticks_left)
    sticks_left -= sticks_taken
    pile_label.config(text="Sticks Left: " + str(sticks_left))
    text_box1.delete(1.0, tk.END)
    text_box1.insert(tk.END, "Sticks: " + "|" * sticks_left)
    if sticks_taken == 1:
        text_box2.insert(tk.END, "Computer removed 1 stick.\n")
    else:
        text_box2.insert(tk.END, "Computer removed {} sticks.\n".format(sticks_taken))
    if sticks_left == 0:
        description.config(text="You win! Play again?")
        button_y.config(command=start_new_game)
        button_n.config(command=root.destroy)
    else:
        player_turn()


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


def print_pile(pile):
    print("Current pile: ", end="")
    for i in range(pile):
        print("|", end="")
    print(" ({} counters)".format(pile))


def get_player_choice(pile):
    while True:
        choice = int(input("Enter number of counters to remove (1-3): "))
        if choice > 0 and choice <= min(pile, 3):
            return choice
        print("Invalid choice, try again")


def get_computer_choice(pile):
    if pile % 4 != 0:
        return pile % 4
    # Check if there is a way to win the game
    if (pile - 1) % 4 == 0:
        return 3
    elif (pile - 2) % 4 == 0:
        return 2
    elif (pile - 3) % 4 == 0:
        return 1
    else:
        return random.randint(1, min(pile, 3))

def evaluate(pile, maximizing_player):
    if pile == 0:
        if maximizing_player:
            return 1  # current player loses
        else:
            return -1  # current player wins
    return 0