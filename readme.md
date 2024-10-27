# HTM1

HTM1 is an esoteric programming language designed to look like HTML, loosely inspired by languages like Whitespace and Shakespeare. Valid HTM1 ~~is valid HTML~~ is mostly valid HTML - the parser is a bit janky. Despite this most HTM1 files are able to be displayed in most modern web browsers with minimal damages.

HTM1 was created in less than 24 hours for HackNotts 24.

## Language rules

A HTM1 program wants a root `<htm1>` tag, which often confuses browsers since they aren't as easily tricked by the L actually being a 1. Executable commands are embedded in the tags, where each element represents at most one command.

- A command's **opcode** is denoted by the number of characters in the opening tag's `id`, or tag name if there's no `id` attribute
- Parameters are denoted by the number of letters in the element's classes, e.g. `class="hack notts"` makes x = 4 and y = 5. Surplus classes are ignored. This has a couple of exceptions:
	- Dashes in a class name separate between digits of the number, so `class="jacob-h"` gives 51
	- Instead of a word for a digit, you can just put the digit itself, so `class="jacob0"` gives 51. The number 0 can be written as `class="-"`, which we *think* is allowed in HTML. Digits don't need dashes between them.
	- The first character in a class attribute cannot be a number so must either be punctuation or a character

If an element doesn't pattern-match to any command, it just gets ignored.

There are example `.htm1` files in the `examples/` directorythat are helpful for getting to know the language.

### Commands

Commands in HTM1 operate on an *theoretically* infinite set of stacks of integers. We thought stacks were more fun than your average Turing tape, and it means no command needs more than two parameters. Like any good language, there's built-in Unicode support.

There are 9 commands, each with up to two parameters:

1. Pop from stack `x` and push straight to stack `y`
2. Execute operation `y` on stack `x`
3. Break from a loop
4. Push `y` to stack `x`
5. Input to stack `x` with mode `y`
6. Output from stack `x` with mode `y`
7. If stack `x` == stack `y` then execute any child elements
8. Loop over child elements
9. Flip stack `x`

Command IDs are 1-indexed because empty ID or tag names don't really make sense. They're in a weird order because we tried to assign the most commonly used IDs with the most commonly used tags.

#### Operators

Command 2 accepts 9 operations:

0. `+`
1. `-`
2. `*`
3. `/`
4. Delete
5. Duplicate
6. Not
7. `=`
8. `<`

The boolean operators consider 0 as false and anything else as true, with 1 as default.

#### Control Structures

An "if" command will execute its children if and only if the data at the top of the two given stacks are equal.

A "loop" command will repeatedly execute its children elements in order. This code endlessly outputs the number 5:

```
<mark class="i loveu"></mark>
<p id="torepeat"><output class="i hateyou"></output></p>
```

You might want to break from loops.

#### IO

Commands 5 and 6 accept a boolean "mode" as y:

0. Treat numbers as strings of digits, and IO them with a newline at the end
1. Treat numbers as indivual Unicode characters, and IO one character at a time

### Importing

You can import external HTM1 code with a cheeky `<a href="https://link.to/resource.htm1">`. HTM1 files are best served from a webserver, but for compatibility reasons you might want to override the MIME type to be `text/html`, otherwise browsers won't know what to do with it.

### CSS

If you want the interpreter to ignore certain elements, you should use `<sty1e>` (notice that's a 1 again, not an L). Elements inside this tag mimic the format of a CSS stylsheet, allowing you to specify which elements to ignore with the selectors. For example, to ignore any element with `class="boring"`:

```htm1
<sty1e>
	.boring {
		color: red;
	}
</sty1e>
```

Nothing will actually get colored red though, no browser will accept `<sty1e>` tags as CSS. It's just for decoration *(or misdirection)*. You can also import them with a `<1ink href="...">`, as you'd expect. Sty1ing for imported HTM1 files only applies to the imported code.

Be aware! Any data stored in attributes in a `<sty1e>` tag will be ignored.

## Usage

HTM1 is interpretted using python so written code can easily be run locally on your machine with minimal effort and installation.

1. Clone the git repo at https://github.com/Harvelon365/HTM1.git
2. Navigate to the cloned repo folder
3. Run the interpreter using the following command

```bash
	./main.py -f FILENAME
```

There are some optional arguments that are available that may help with troubleshooting:

`-d` or `--debug` : Enables debug output including full stack trace and conservative error messages

`-t` or `--test` : Run predefined test programs to test the interpreter integrity (is not run when a filename is provided)