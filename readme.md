# HTM1

HTM1 is an esoteric programming language designed to look like HTML, loosely inspired by languages like Whitespace and Shakespeare. Valid HTM1 ~~is valid HTML~~ is almost valid HTML - the parser is a bit janky. 

HTM1 was created in an evening for HackNotts 24.

## Language rules

Commands in HTM1 operate on an infinite set of stacks of integers. I thought stacks were more fun than your average Turing tape, and it means nothing needs more than two parameters. Like any good language, there's built-in Unicode support.

There are 9 commands, each with up to two parameters:
1. Pop from stack x and push straight to stack y
2. Execute operation y on stack x
3. Break from loop
4. Push y to stack x
5. Input to stack x with mode y
6. Output from stack x with mode y
7. If stack x == stack y then execute children
8. Loop over children
9. Flip stack x
These 

Command 2 allows for 9 operations:
0. 
