import numpy as np

def is_win(board):
    """Checks if there is a winner, according to the rules. 

    Returns:
        tuple(bool, str): tuple which contains bool if there is a win and a str which says which player won.
    """
    winning_player = ''
    is_win = False
    # Check win for blue player
    if board[3] > 0 or (board >= 0).all():
        
        is_win = True
        winning_player = 'Blue'
        
    
    # Check win for red player
    if board[59] < 0 or (board <= 0).all():
        
        is_win = True
        winning_player = 'Red'
    
    #if is_win:
        #print('win')
    return (is_win, winning_player)



file = open('MVC/minimax/cache_1.csv')
cache = np.loadtxt(file, delimiter=',')

inputs = np.delete(cache, -1, 1)
inputs = np.unique(inputs, axis=0)
print(len(inputs))
labels = []

for i in inputs:
    win_data = is_win(i)
    if win_data[0] is False:
        labels.append(0)
    elif win_data[0] is True and win_data[1] == 'Red':
        labels.append(1)
    elif win_data[0] is True and win_data[1] == 'Blue':
        labels.append(-1)

labels = np.array(labels)
#print(labels)
print(len(np.argwhere(labels != 0)))