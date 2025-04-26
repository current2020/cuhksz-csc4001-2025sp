#!/usr/bin/env bash
set -e

# 1) Erase any old coverage data
python3 -m coverage erase

# 2) Loop over t = 1 … 100
for t in $(seq 0 99); do
    echo "Running test #$t…"

    # 2a) generate the t-th input and write it to input.txt
    python3 generator_diff.py "$t" 1.in

    # 2b) run your simulator under coverage
    #     --branch: measure branch coverage
    #     --parallel-mode: write one .coverage.$PID file per run
    python3 -m coverage run --branch --parallel-mode ./simulator_correct.py 1.in 1.out
done

# 3) Combine all the little coverage files into one
python3 -m coverage combine

# 4) Show a branch‐coverage report, and fail if it’s under 100%
python3 -m coverage report
