# This is the section for the Sudoku Solver on my Website

# Important Note: 

This file does not have the JavaScript or Web-needed functions. Simply a command-line interface; no GUI (possibly will add one later).

## Can be found on my Website

The Sudoku Solver program has a nifty visual app on my website found 
[here](https://andrew-morgan-website.herokuapp.com/programming-repo/sudoku-solver). 

## What Can the Program Do?

The Sudoku Solver can solve N-by-N puzzles using backtracking and intelligent searching algorithms. By N-by-N 
Sudoku boards, I mean boards like: 6 by 6 (36 total numbers to fill) or 9 by 9 (default; 81 total numbers to fill) 
or 12 by 12 (144 total numbers to fill). It is important to note that the numbers must not be prime (n != prime).

The solution is fast, but does struggle with larger boards as the complexity blows up (I mean 15 by 15 or larger). 
These larger boards need more initial squares filled in or the algorithm takes some time. This is caused by my 
algorithm implementing more generic searching algorithm and not a Sudoku puzzle-specific algorithm. Regardless, my 
algorithm far surpasses the speed for solving Sudoku's with pure brute-force backtracking.

I use 2 primary forms of heuristics:

1. Variable selection: I choose the variable (cell of the puzzle) that has the *LEAST* number of viable options.

2. Value Selection: For that variable I select (from 1.), I select the value of that cell to be the *LEAST 
   constraining* to allow other cells to have the most number of options.
   
3. Finally, I use basic inferencing to ensure that the value selected does not cause other variables to become 
impossible to fill.
   
I used the 3rd Edition of Artificial Intelligence: A Modern Approach by Stuart J Russell and Peter Norvig which 
is considered the best intro to AI textbook (quite good and well-written, as well). Can be found 
[here](https://cs.calvin.edu/courses/cs/344/kvlinden/resources/AIMA-3rd-edition.pdf)

## Requirements 

The requirements to run are python (version 3), Math (sqrt), Random (choice, randint), intertools (default), time (default)



