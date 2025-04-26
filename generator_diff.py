import sys

def generator(t):

    # Implement your code here.
    # Do not modify the main function.
    # You may define additional helper functions if needed.
    
    return "2 2"

if __name__ == '__main__':

    t = sys.argv[1]
    outname = sys.argv[2]
    fout = open(outname, "w")
    fout.write(generator(t))
    fout.close()