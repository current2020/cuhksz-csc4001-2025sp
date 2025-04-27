import sys
import random
import string

default_skip_code = "Quuuuuux\n"

def generate_random_skip_code():
    # 1 empty line
    # 2 one number
    # 3 multi numbers
    # 4 invalid position
    # 5 invalid characters
    res = ""
    opt = random.randint(1, 5)
    if opt == 1:
        pass
    elif opt == 2:
        res += str(random.randint(1, 19))
    elif opt == 3:
        num = random.randint(3, 10)
        for _ in range(num):
            res += str(random.randint(1, 19)) + " "
    elif opt == 4:
        for _ in range(2):
            if random.randint(0, 1) == 0:
                res += str(random.randint(-10, 0)) + " "
            else:
                res += str(random.randint(20, 30)) + " "
    elif opt == 5:
        num = random.randint(1, 20)
        for _ in range(2):
            for _ in range(num):
                res += random.choice(string.ascii_letters + string.digits + string.punctuation)
            res += " "
    res += "\n"
    return res

def generate_complete_random(t):
    random.seed(t)
    res = ""

    num = random.randint(800, 1000)
    invalid_portion = 3 # out of 100
    for _ in range(num):
        do_gen_invalid = random.randint(1, 100)
        if do_gen_invalid <= invalid_portion:
            res += generate_random_skip_code()
        else:
            res += str(random.randint(1, 19)) + " " + str(random.randint(1, 19)) + "\n"
        
    return res

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

def get_opt_sequence(black_pos, white_pos):
    res = ""
    num_black = len(black_pos)
    num_white = len(white_pos)
    nxt_black = 0
    nxt_white = 0
    nxt_line = 0

    while nxt_black < num_black or nxt_white < num_white:
        nxt_line += 1
        if nxt_line % 2 == 1:
            if nxt_black < num_black:
                x, y = black_pos[nxt_black]
                nxt_black += 1
                res += f"{x} {y}\n"
            else:
                res += default_skip_code
        else:
            if nxt_white < num_white:
                x, y = white_pos[nxt_white]
                nxt_white += 1
                res += f"{x} {y}\n"
            else:
                res += default_skip_code

    return res

class GoBoard:
    def __init__(self, size=19):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]

    def place_stone(self, line, color):
        try:
            x, y = line.split()
            x = int(x) - 1
            y = int(y) - 1
            if x < 0 or x > 18 or y < 0 or y > 18:
                return
            if self.board[x][y] != '.':
                return
            self.board[x][y] = color
            self.check_captures()
        except:
            pass
    
    def check_captures(self):
        index = 0
        vis = [[-1 for _ in range(self.size)] for _ in range(self.size)]

        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != '.' and vis[r][c] == -1:
                    self.get_group(r, c, index, self.board[r][c], vis)
                    index = index + 1
    
        liberties = [0 for _ in range(index)]

        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == '.':
                    continue
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if self.board[nr][nc] == '.':
                            liberties[vis[r][c]] = 1
                            
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == '.':
                    continue
                if liberties[vis[r][c]] == 0:
                    self.board[r][c] = '.'

    
    def get_group(self, r, c, index, color, vis):

        vis[r][c] = index
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if vis[nr][nc] == - 1 and self.board[nr][nc] == color:
                        self.get_group(nr, nc, index, color, vis)

    def get_positions(self):
        distant = []
        close = []
        border = []
        occupied = []

        marks = [[0 for _ in range(self.size)] for _ in range(self.size)]

        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == '.':
                    if r == 0 or r == 18 or c == 0 or c == 18:
                        marks[r][c] = 2
                    continue

                marks[r][c] = 3
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if self.board[nr][nc] == '.':
                            marks[nr][nc] = 1
        
        for r in range(self.size):
            for c in range(self.size):
                if marks[r][c] == 0:
                    distant.append((r+1, c+1))
                elif marks[r][c] == 1:
                    close.append((r+1, c+1))
                elif marks[r][c] == 2:
                    border.append((r+1, c+1))
                elif marks[r][c] == 3:
                    occupied.append((r+1, c+1))

        return distant, close, border, occupied
    
    def get_black_and_white(self):
        black_pos = []
        white_pos = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 'B':
                    black_pos.append((r+1, c+1))
                if self.board[r][c] == 'W':
                    white_pos.append((r+1, c+1))
        return black_pos, white_pos

def get_nxt_line_from_choices(positions):
    if len(positions) == 0:
        return default_skip_code
    x, y = random.choice(positions)
    return f"{x} {y}\n"

def strategy_standard_identity(t):
    random.seed(t)

    Go = GoBoard()
    color = 0
    res1 = ""

    num = random.randint(800, 1000)
    invalid_portion = 3 # out of 100
    for _ in range(num):
        do_gen_invalid = random.randint(1, 100)
        nxtline = default_skip_code
        if do_gen_invalid <= invalid_portion:
            nxtline = generate_random_skip_code()
        else:
            distant, close, border, occupied = Go.get_positions()
            opt = random.randint(1, 100)
            if 1 <= opt and opt <= 5:
                nxtline = get_nxt_line_from_choices(occupied)
            elif 6 <= opt and opt <= 30:
                nxtline = get_nxt_line_from_choices(border)
            elif 31 <= opt and opt <= 80:
                nxtline = get_nxt_line_from_choices(close)
            elif 81 <= opt and opt <= 100:
                nxtline = get_nxt_line_from_choices(distant)
        Go.place_stone(nxtline, 'B' if color == 0 else 'W')
        color = color ^ 1
        res1 += nxtline

    black_pos, white_pos = Go.get_black_and_white()
    res2 = get_opt_sequence(black_pos, white_pos)
        
    return res1, res2


def strategy_capture_rect(t):
    random.seed(t)

    is_captured_black = t % 2
    t //= 2
    is_sx_1 = t % 2
    t //= 2
    is_sy_1 = t % 2

    hi = random.randint(1, 10)
    wi = random.randint(1, 10)
    sx = sy = 1
    if not is_sx_1:
        sx = random.randint(2, 5)
    if not is_sy_1:
        sy = random.randint(2, 5)

    captured = []
    capturing = []
    for x in range(sx, sx + hi):
        for y in range(sy, sy + wi):
            captured.append((x, y))

    for y in range(sy, sy + wi):
        capturing.append((sx-1, y))
        capturing.append((sx+hi, y))
    for x in range(sx, sx + hi):
        capturing.append((x, sy-1))
        capturing.append((x, sy+wi))

    random.shuffle(captured)
    random.shuffle(capturing)

    if is_captured_black:
        return get_opt_sequence(captured, []), get_opt_sequence(captured, capturing)
    return get_opt_sequence([], captured), get_opt_sequence(capturing, captured)

def strategy_transformation(t):
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

    random.seed(t)
    res1 = ""
    res2 = ""

    num = random.randint(800, 1000)
    invalid_portion = 3 # out of 100
    for _ in range(num):
        do_gen_invalid = random.randint(1, 100)
        if do_gen_invalid <= invalid_portion:
            res1 += generate_random_skip_code()
            res2 += generate_random_skip_code()
        else:
            x = random.randint(1, 19)
            y = random.randint(1, 19)
            res1 += str(x) + " " + str(y) + "\n"
            x, y = transformer(x, y)
            res2 += str(x) + " " + str(y) + "\n"
        
    return res1, res2

def strategy_black_and_white(t):
    random.seed(t)
    num = random.randint(0, 2) * 2 + 1
    res1 = generate_complete_random(t)
    res2 = ""
    for _ in range(num):
        res2 += default_skip_code
    res2 += res1
    return res1, res2

def strategy_full(t):
    random.seed(t)
    res = ""

    if(t % 2 == 1):
        res += default_skip_code
    
    positions = []
    for idx in range(19 * 19):
        y = idx % 19 + 1
        x = idx // 19 + 1
        positions.append((x, y))

    if t >= 2:
        random.shuffle(positions)

    for x, y in positions:
        res += f"{x} {y}\n" + default_skip_code

    return res, ""

strategies = []
strategies.append((0, 8, strategy_capture_rect))
strategies.append((8, 10, strategy_full))
strategies.append((10, 31, strategy_transformation))
strategies.append((31, 50, strategy_black_and_white))
strategies.append((50, 100, strategy_standard_identity))

def generator(t):

    # Implement your code here.
    # Do not modify the main function.
    # You may define additional helper functions if needed.
    t = int(t)
    for l, r, strategy in strategies:
        if l <= t and t < r:
            return strategy(t)
    return "Unreachable", "Unreachable"

if __name__ == '__main__':

    t = sys.argv[1]
    outname1 = sys.argv[2]
    outname2 = sys.argv[3]
    fout1 = open(outname1, "w")
    fout2 = open(outname2, "w")
    s1, s2 = generator(t)
    fout1.write(s1)
    fout2.write(s2)
    fout1.close()
    fout2.close()