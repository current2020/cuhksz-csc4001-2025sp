# CUHKSZ-CSC4303-2025sp Project

This is the project repo for the software engineering course of cuhksz-csc4303-2025sp.

In this project, we are required to use both differential testing and metamorphic testing to debug a Go simulator.

The `simulator_correct.py` includes the correct code for the Go simulator. It simulates a Go game simplified from the standard Go game, and the rules are a little bit different. Meanwhile, the `simulator_buggy` folder holds some sample buggy simulators. Our goal is trying to detect bugs in the simulator codes (including hidden ones).

The `grader.py`, `generator_diff.py`, `generator_meta.py` and `checker.py` are for the bug detection. For each detection, we have 100 iterations of chances to detect bugs, and in each iteration we are allowed to generate an input file no more than 1000 lines.

We are also allowed to submit our own buggy simulator `simulator_buggy.py` to challenge other students' bug detecter. But we are not allowed to change the control flow or introduce some very specific bugs.

For my project report, see [here](report.md).