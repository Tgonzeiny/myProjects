import random

#Importing the random package to generate random numbers

 

#intializes the game and matrix

def start_game():

    #Defines the empty 4x4 matrix
    matrix = [[0 for i in range(4)] for i in range(4)]

    #Commands for the user
    print("commands: ")

    print("W to move up ")

    print("S to move down")

    print("D to move right ")

    print("A to move left ")

    print("Q to quit ")


    #Calls the add_new function to add two random cells
    #With a 2 inside to start the game
    add_new_2(matrix)
    add_new_2(matrix)

 

    #Intiates a loop to so that the user can play the game.
    #It does this through checking the current state function to see if the user has won or lost
    while(get_current_state(matrix) == "con"):

        #Prints the row in the terminal in a clean way
        for row in matrix:
            for k  in row:
                print(k,end ="\t")
            print()

        #asks for an input so the program can check movement
        move = input("Enter a movement: ")

        #Checks if the user wants to move up
        if move == "W":
            matrix, change = move_up(matrix)

        #Checks if the user wants to move down
        elif move == "S":
            matrix, change = move_down(matrix)

        #Checks if the user wants to move right
        elif move == "D":
            matrix, change = move_right(matrix)

        #Checks if the user wants to move left
        elif move == "A":
            matrix, change = move_left(matrix)

        #Checks if the user wants to quit
        elif move == "Q":
            break;
        
        else:
            print ("Please enter a valid movement")

        #Checks if there was a change to add a 2 to the matrix
        if change == True:
            add_new_2(matrix)

    return matrix

 
#Adds a random 2 to the matrix by using random number generation
def add_new_2(matrix):

    r = random.randint(0,3)
    c = random.randint(0,3)

    while(matrix[r][c] != 0):
        r = random.randint(0,3)
        c = random.randint(0,3)
    matrix[r][c] = 2


#Gets the current state of the game to see if the game is over
#This is done by checking each cell in the matrix
def get_current_state(matrix):
    for i in range(4):
        for j in range(4):
            if(matrix[i][j])==2048:
                print ("You win!!")
                return "win"

    for i in range(4):
        for j in range(4):
            if(matrix[i][j])==0:
                return "con"
            
    for i in range(3):
        for j in range(3):
            if(matrix[i][j] == matrix[i+1][j] or matrix[i][j] == matrix[i][j+1]):
                return "con"

    for j in range(3):
        if(matrix[3][j] == matrix[3][j+1]):
            return "con"

    for i in range(3):
        if(matrix[i][3] == matrix[i+1][3]):
            return "con"

    print ("YOU LOST")
    return "lost"

 
#Compresses the matrix to combine two cells in order to continue the game
#Uses new matrix to build the changed matrix and returns it back to the move function
def compress (matrix):
    change = False
    new_matrix = [[0 for i in range(4)] for i in range(4)]
    for i in range(4):
        pos = 0
        for j in range(4):
            if (matrix[i][j] != 0):
                new_matrix[i][pos] = matrix[i][j]
                if(j != pos):
                    change = True
                pos += 1
    return new_matrix, change
 
#The merge function combines the cells by taking the number inside each cell and multiplying by itself
def merge(matrix):
    change = False
    for i in range(4):
        for j in range(3):
            if(matrix[i][j] == matrix[i][j+1] and matrix[i][j] != 0):
                matrix[i][j] = matrix[i][j]*2
                matrix[i][j+1] = 0
                change = True
    return matrix, change

#Reverse similar to the compress function reverses the matrix to allow the cells to combine to continue the game
#Utilizes the append method to reverse the matrix and build the new matrix to later set equal to the original matrix
def reverse(matrix):
    new_matrix =[]
    for i in range(4):
        new_matrix.append([])
        for j  in range(4):
            new_matrix[i].append(matrix[i][3-j])
    return new_matrix

 
#Transposes the matrix in order to allow cells to combine
#Utilizes the append method to transpose the function to create a new matrix that will be used later.
def transpose(matrix):
    new_matrix = []
    for i in range(4):
        new_matrix.append([])
        for j in range(4):
            new_matrix[i].append(matrix[j][i])
    return new_matrix


#Moves the matrix to the left by 1 by utilizes the compress and merge functions
#Then utilizes change and temp in order to track if a change was made
def move_left(matrix):
    new_matrix, change1 = compress(matrix)
    new_matrix, change2 = merge(new_matrix)
    change = change1 or change2
    new_matrix, temp = compress(new_matrix)
    return new_matrix, change or temp


#Moves the matrix to the right by 1 by utilizes the reverse function and move left function to simplify the move
def move_right(matrix):
    new_matrix = reverse(matrix)
    new_matrix, change = move_left(new_matrix)
    new_matrix = reverse(new_matrix)
    return new_matrix, change

 
#Moves the matrix up by 1 by utilizing the transpose and move left functions
def move_up(matrix):
    new_matrix = transpose(matrix)
    new_matrix, change= move_left(new_matrix)
    new_matrix = transpose(new_matrix)
    return new_matrix, change


#moves the matrix down 1 by utilizing transpose and move right function to simplify the move
def move_down(matrix):
    new_matrix = transpose(matrix)
    new_matrix, change = move_right(new_matrix)
    new_matrix = transpose(new_matrix)
    return new_matrix, change

 
#Intializes the game
start_game()