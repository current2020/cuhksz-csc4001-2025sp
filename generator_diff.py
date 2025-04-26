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

def strategy_complete_random(t):
    random.seed(t)
    res = ""

    num = random.randint(800, 1000)
    invalid_portion = 1 # out of 100
    for _ in range(num):
        do_gen_invalid = random.randint(1, 100)
        if do_gen_invalid <= invalid_portion:
            res += generate_random_skip_code()
        else:
            res += str(random.randint(1, 19)) + " " + str(random.randint(1, 19)) + "\n"
        
    return res

def strategy_few_moves(t):
    random.seed(t)
    res = ""

    num = random.randint(0, 6)
    invalid_portion = 40 # out of 100
    for _ in range(num):
        do_gen_invalid = random.randint(1, 100)
        if do_gen_invalid <= invalid_portion:
            res += generate_random_skip_code()
        else:
            res += str(random.randint(1, 19)) + " " + str(random.randint(1, 19)) + "\n"
        
    return res

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

    return res

strategies = []
strategies.append((0, 4, strategy_full))
strategies.append((4, 10, strategy_few_moves))
strategies.append((10, 1000, strategy_complete_random))

def generator(t):

    # Implement your code here.
    # Do not modify the main function.
    # You may define additional helper functions if needed.
    t = int(t)
    for l, r, strategy in strategies:
        if l <= t and t < r:
            return strategy(t)
    return "Unreachable"

if __name__ == '__main__':

    t = sys.argv[1]
    outname = sys.argv[2]
    fout = open(outname, "w")
    fout.write(generator(t))
    fout.close()