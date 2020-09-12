class Player():
    def __init__(self, name):
        '''
        Object representing a player. 
        name:   a string chosen by the user. eg 'Alice', 'Bob'
        marker: char representation of the marker for a player. eg 'x' or 'o'.
                will be defaulted to 'x' for player 1, 'o' for player 2.
        id:     integer representing player id. Currently not used.
        '''
        self.name = name
        self.marker = ""
        self.id = 0

class Tictactoe():
    def __init__(self):
        '''      
        players: list of Player objects (only 2 players expected)
        board:   a 2d matrix representing the game state. unplayed cells are
                 represented by integers. played cells are represented by
                 the player's marker.
        n:       Positive integer representing the number of rows for tic tac toe. Minimum is 3. 
        unplayed_cells: integer representing how many unplayed cells there are.
        '''
        self.players = []
        self.board = []
        self.n = 0
        self.unplayed_cells = 0

    def createBoard(self, n=3):
        '''
        Updates self.board to represent tic tac toe starting game state. 
        Eg for n=3: [[1,2,3],[4,5,6,],[7,8,9]]
        '''
        self.n = n
        self.unplayed_cells = n**2
        for i in range(n):
            cur_row = [0] * n
            for j in range(n):
                cur_row[j] = (i*n) + j + 1
            self.board.append(cur_row)
        

    def printBoard(self):
        '''
        Does not return anything.
        prints the board state to console. Will print in user friendly manner.
        '''
        for i, row in enumerate(self.board):
            s = ""
            for val in row:
                val = " "+str(val)
                s += " {} |".format(str(val))
            print(s[:-1])
            if i != len(self.board)-1:
                dashes = "-" * len(s[:-1])
                print(dashes)

    def setPlayers(self):
        '''
        Does not return anything.
        Prompts user for player name, and inserts Player objects into self.players.
        '''
        name = str(input("Enter name for Player 1\n"))
        p1 = Player(name)
        p1.marker = "x"
        p1.id = 1
        name = str(input("Enter name for Player 2\n"))
        p2 = Player(name)
        p2.marker = "o"
        p2.id = 2
        self.players.append(p1)
        self.players.append(p2)

    def locationToIndex(self, loc):
        '''
        Takes a int location referring to the board. Returns a tuple of integers
        which are indexes corresponding to the location on the board.
        Eg: given a board [[1,2,3],[4,5,6],[7,8,9]], locationToIndex(3) will
        return (0, 2).
        loc: integer representing a "box" on the tic tac toe board.
        '''
        row = int((loc-1)/self.n)
        col = ((loc-1)%self.n)
        return (row, col)

    def checkWinningMove(self, player, row, col):
        ''' 
        Returns false if move played is not a winning move.
        Returns true if move played is a winning move.
        Is called everytime a move is made on the board.
        player: player object for which we are checking the winning move.
        row: row index of marker that has just been placed.
        col: col index of marker that has just been placed.
        '''
        cur_marker = player.marker

        # --- Helper Function --
        def searchDirection(board, row, col, row_displace, col_displace, marker):
            ''' Returns true or false.
            Starting from row and col index, take 2 steps in a direction to search for
            3 markers in a row.
            Each step, offset row and col by row_displace, col_displace.
            row_displace: an integer representing how much of row index to displace each step.
            col_displace: an integer representing how much of col index to displace each step.
            marker: a string representing the marker we are searching for.
            '''
            count = 0
            while True: 
                # Check if current indexes are out of bounds
                if row < 0 or col < 0 or row >= len(board) or col >= len(board):
                    return False
                # In each step, move row and col by displacement amount.
                if board[row][col] == cur_marker:
                    count += 1
                    row += row_displace
                    col += col_displace
                else:  
                    return False
                if count >= 3:
                    return True
        
        # -- Helper Function --
        def searchAllDirections(board, row, col, marker):
            '''
            Returns true/false.
            calls searchDirections with 8 different row and col displacements
            from a given starting row/col.
            '''
            for r_displace in range(-1,2):
                for c_displace in range(-1,2):
                    if r_displace == 0 and c_displace == 0: 
                        continue
                    if searchDirection(self.board, row, col, r_displace, c_displace, marker):
                        return True
            else: return False 
        
        # Search the 8 directions, return True if winning move found.
        if searchAllDirections(self.board, row, col, cur_marker):
            return True
        
        # To handle cases where the winning move is in the middle of a 3 in a row. 
        for r_displace in range(-1,2):
            for c_displace in range(-1,2):
                if searchAllDirections(self.board, row+r_displace, col+c_displace, cur_marker):
                    return True
        
        # If no winning move found, return False.
        return False
            
    def checkValidMove(self, loc):
        '''
        Returns true or false. Prompts user for where they want to 
        place their marker. Updates self.board.
        loc: represents a "box" in the tic tac toe board.
        '''
        if loc <= 0:
            print("Please enter value larger than 0")
            return False
        if loc > self.n**2:
            print("Please enter a value smaller than {}".format(self.n**2))
            return False
        # Check if location contains a player's marker
        row, col = self.locationToIndex(loc)
        for p in self.players:
            if p.marker == self.board[row][col]:
                print("This cell is occupied. Please choose different cell.")
                return False
        return True

    def playRound(self):
        '''
        Returns an integer player.id if a winner is found. Return 0 if winner not found.
        Returns -1 if draw game.
        Plays a single round for each player.'''
        for player in self.players:
            if self.unplayed_cells == 0:
                return -1
            # Show board state
            self.printBoard()
            # Only exit this while loop if valid move is played.
            while True:
                location = int(input("{}, choose a box to place an {} into\n".format(player.name, player.marker)))
                if self.checkValidMove(location):
                    row, col = self.locationToIndex(location)
                    self.board[row][col] = player.marker
                    break
            # Update unplayed cells count.
            self.unplayed_cells -= 1
            # Check if win
            if self.checkWinningMove(player, row, col):
                print("Congrats {}! You won!".format(player.name))
                return player.id
        return 0
            
                

    def getN(self):
        '''
        Prompt user for how many rows for tic tac toe game. returns an integer. 
        Handles invalid inputs.
        '''
        while True:
            try:
                n = int(input("How many rows do you want to play?\n"))
                if n < 3:
                    print("Minimum number of rows is 3.")
                    continue
            except ValueError:
                print("Sorry, please enter an integer")
            else:
                break
        return n

    def play(self):
        '''Starts the game. Game terminates when winner is found.'''
        n = self.getN()
        self.createBoard(n=n)
        self.setPlayers()
        while True:
            # playRound returns player ID (some positive integer) if winner is found.
            result = self.playRound()
            if result > 0:
                self.printBoard()
                return
            if result == -1:
                self.printBoard()
                print("Draw game!")
                return
                
            
                            
            
        

        
            
        




