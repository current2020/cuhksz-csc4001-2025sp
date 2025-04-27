import sys

def transform_rotate_0(x, y):
    return x, y

def transform_rotate_90(x, y):
    return y, 20-x

def transform_rotate_180(x, y):
    return 20-x, 20-y

def transform_rotate_270(x, y):
    return 20-y, x

def transform_symmetry_hor(x, y):
    return 20-x, y

def transform_symmetry_ver(x, y):
    return x, 20-y

def transform_symmetry_dia1(x, y):
    return y, x

def transform_symmetry_dia2(x, y):
    return 20-y, 20-x

def strategy_identical(t, board1, board2):
    for r in range(19):
        for c in range(19):
            if board1[r][c] != board2[r][c]:
                return '1'
    return '0'

def strategy_transformation(t, board1, board2):
    opt = t % 7
    transformer = transform_rotate_0
    if opt == 0:
        transformer = transform_rotate_90
    elif opt == 1:
        transformer = transform_rotate_180
    elif opt == 2:
        transformer = transform_rotate_270
    elif opt == 3:
        transformer = transform_symmetry_hor
    elif opt == 4:
        transformer = transform_symmetry_ver
    elif opt == 5:
        transformer = transform_symmetry_dia1
    elif opt == 6:
        transformer = transform_symmetry_dia2

    for x in range(1, 20):
        for y in range(1, 20):
            x2, y2 = transformer(x, y)
            if board1[x-1][y-1] != board2[x2-1][y2-1]:
                return '1'
    return '0'

def strategy_black_and_white(t, board1, board2):
    for r in range(19):
        for c in range(19):
            if board1[r][c] == '.':
                if board2[r][c] != '.':
                    return '1'
            elif board1[r][c] == 'B':
                if board2[r][c] != 'W':
                    return '1'
            elif board1[r][c] == 'W':
                if board2[r][c] != 'B':
                    return '1'
    return '0'

def strategy_capture_rect(t, board1, board2):
    is_captured_black = t % 2
    captured_color = 'W'
    capturing_color = 'B'
    if is_captured_black:
        captured_color = 'B'
        capturing_color = 'W'
    for r in range(19):
        for c in range(19):
            if board1[r][c] != captured_color:
                continue
            if board2[r][c] != '.':
                return '1'
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 19 and 0 <= nc < 19:
                    if board1[nr][nc] == '.' and board2[nr][nc] != capturing_color:
                        return '1'
    return '0'

strategies = []
strategies.append((0, 8, strategy_capture_rect))
strategies.append((8, 10, strategy_identical))
strategies.append((10, 31, strategy_transformation))
strategies.append((31, 50, strategy_black_and_white))
strategies.append((50, 100, strategy_identical))

def check(t, s1, s2):
    
    # Implement your code here.
    # Do not modify the main function.
    # You may define additional helper functions if needed.
    t = int(t)

    board1 = []
    board2 = []
    for line in s1:
        board1.append(line.strip().split())
    for line in s2:
        board2.append(line.strip().split())

    for l, r, strategy in strategies:
        if l <= t and t < r:
            return strategy(t, board1, board2)
    return '0'
    '''
    return '0' if you assume there is no bug triggered
    return '1' if you assume there is bug triggered
    '''

if __name__ == '__main__':

    t = sys.argv[1]
    inname1 = sys.argv[2]
    inname2 = sys.argv[3]
    outname = sys.argv[4]
    fin1 = open(inname1, "r")
    fin2 = open(inname2, "r")
    s1 = fin1.readlines()
    s2 = fin2.readlines()
    fin1.close()
    fin2.close()
    fout = open(outname, "w")
    fout.write(check(t, s1, s2))
    fout.close()