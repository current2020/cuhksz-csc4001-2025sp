# CSC4001 Project

郑晗骏 ZHENG Hanjun

122090797

## Differential Testing

### Core Concept

Differential testing involves executing the target program and a correct program with the same input. If the target program is bug-free, the two outputs will be consistent. But if there is some differences in the two outputs, it suggests that there are some bugs in the target program.

### My Implementation

In this project, our program has 100 iteration of chances to find bug in each buggy program. My generator adopts different strategies during iterations. And to ensure that its behavior is different between iterations while unchanged between runs,  parameter `t` is set as the random seed every time.

Below are more detailed explanations for different strategies adopted and utility functions implemented.

#### generate_random_skip_code()

This is a utility function to randomly generate one line that represents an invalid move.

The invalid moves it generates will be one of the 5 genres:

1. an empty line
2. include only one number
3. include more than two numbers
4. position that is out of border
5. include invalid characters

But they that not includes invalid moves that tries to insert at a position which is already occupied.

#### strategy_complete_random()

The main simple strategy.

It generates many lines of random moves (including some invalid ones).

#### strategy_few_moves()

basically same as the strategy above.

But it only generates a few lines (even zero lines).

#### strategy_full()

This is designed to deal with the buggy simulator `1.py`.

It generates input moves where one player keeps filling the board while the other keeps skipping his turn.

## Metamorphic Testing

### Core Concept

Metamorphic testing relies on some known properties of the behavior that a correct program should have. The key point is to find special relationships where if the two inputs follow a certain relation, the two outputs will also preserve a certain relation. Metamorphic testing utilizes such relationships. It generate one input and alter it into another input according to some rules. The target program will be executed with the two input. Then it will check that if the two outputs follow the expected relationships. If not, it suggests that there is a bug in the target program.

### My Implementation

Similar to differential testing, my program adopts different strategies between different iterations and set `t` as the random seed. But there are much more different strategies than differential testing.

Below are the detailed explaination of each strategy.

#### strategy_capture_rect()

This strategy focuses on the mechanism of capturing. It uses what will happen when one player captures the other player's stones as the special relationship.

**Input 1: **will be one player filling a rectangle area on the board and the other player doing nothing.

**Input 2: **will be similar to input 1, but the other player will put stones to capture the stones in that rectangle.

**Relation in outputs: **For positions where it has a stone in input 1, it will be empty in the input 2, since the stons should have been correctly captured. But for the neighboring positions which is empty in input 1, they will be occupied in input 2 with the other player's stones, since it has to be that to capture all the stones.

#### strategy_full()

This is designed to deal with the buggy simulator `1.py`.

**Input 1:** will be one player keeps filling all positions while the other player keeps skipping his turn.

**Input 2:** will be empty.

**Relation in outputs:** The two output should be identical. Since filling the board with all one's own stones will result in all stones being captured, which should have the same output as an empty input.

#### strategy_transformation()

This strategy focuses on the symmetry of the game. The game is played on a square-shaped board and none of the rules is direction specific. The symmetry group has an order of $8$, consisting of $4$ rotations (by $0^\circ, 90^\circ, 180^\circ, 270^\circ$) and $4$ reflections (across two midlines and two diagonals). This strategy utilize all other $7$ except the identity transformation.

**Input 1:** will be a random input.

**Input 2:** will be the input 1 after some transformation.

**Relation in outputs:** After applying the same transformation, output 1 should be consistent with output 2.

#### strategy_black_and_white()

This strategy focuses on the symmetry between the two players. The rules are the same of both players, except that black goes first and white goes second. If the order is reversed, the black and white will also be reversed in the output. We can simulate that by adding odd number of invalid moves at the beginning of the input.

**Input 1:** will be a random input

**Input 2:** will be input 1 after inserting odd number of invalid moves at its beginning.

**Relation in outputs:** the black and white is reversed.

#### strategy_standard_identity()

During the process of a game, there might be stone being captured and there might not be. But it cannot be distinguished from the fianl output. Beside, the order of the uncaptured stones being placed also can be be distinguished from the fianl output. If we construct an input from another input where all uncaptured stones all being placed by random order, the two inputs should have identical outputs.

Besides, completely randomly generating the input by a uniform distribution over all positions might not be a perfect idea, since many of the moves will be just trying to insert stones to an occupied position. Maybe generating the next move according to the current simulated game state will be better.

**Input 1:** wil be a random input

**Input 2:** will be the corresponding input constructed according to the above description.

**Relation in outputs:** the two inputs should have identical outputs.

