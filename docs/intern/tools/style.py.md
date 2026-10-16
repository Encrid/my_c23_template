# tools/style.py

`style.py` checks the style of the C code of the project.
The style is the Epitech C Coding Style, version 3.1, with two changes of the template.
That style comes from the Linux Kernel Coding Style, and from the book Clean Code of Robert C. Martin.
`tools/c23.py` checks the spellings that C23 gives to some rules.

```sh
python tools/style.py [--root <folder>]
```

## Why the style exists

With the style, every file looks as if one person wrote it.
Thus it is easier to read the code, to debug it, to maintain it, to reuse it and to test it.

The style is a convention of syntax only. Code that obeys the style can still be incorrect.
Obey the style from the first line. That is easier than a change of finished code.

If no rule decides a choice, select the option that makes the code clearer.
This document cannot name each type of unclear code. Do not write unclear code that this document does not name.

## The changes of the template

The template changes two rules of the original style:

- G1: the legal notice has a line of the copyright and a line of the licence. It gives no path and no description of the file.
- F6: no file has a comment that is not the legal notice. The original lets a comment describe a function.

## The files

`style.py` checks each file `.c` and `.h` of the project, but not the files of `tests/data`.
`tools/layout.py` checks the rules O1 and O4, because they apply to each file of the project.
`[style]` of `tools/toolchain.toml` gives the limits of the rules F3, F4, F5, O3 and C1.

## The self-test

Before it reads the files, `style.py` checks itself:

1. For each rule that it checks, it reads a short text that breaks the rule. The rule must find a fault in the text.
2. It reads a short clean text. No rule but G1, H1 and H2 can find a fault in it.

If the self-test fails, `style.py` stops: `the checker itself: <faults>`.

## Output

`style.py` gives its faults to `report` of `tools/shared.py`, in the order of the paths and of the lines.
A fault is `<path>:<line>: <rule> <what>`.
`report` writes each fault on its own line, then stops: `faults: <number>`. If there is no fault, it writes `no fault in <number> files`.

## O - The files

### O1 - The contents of the repository

The repository holds only the files that are necessary to build the project, to test it and to understand it.
Do not track a file that a build makes, for example a file `.o`, `.a`, `.so`, `.dll` or `.exe`.
Do not track a temporary file, for example `a.out`, a file `.d`, or a name that ends with `~`.
A build puts its files into `build`, which git ignores.
`tools/layout.py` checks this rule.

### O2 - The extension of a file

A source in C has the extension `.c` or `.h`, and no other extension.
`style.py` reads only these files, and `tools/layout.py` permits only files `.h` in `include`.
A person checks the files of `src`, because `src` can also hold other inputs of a build.

### O3 - The coherence of a file

A source matches one logical entity, and holds all the functions of that entity.
If a file has more than 5 functions, divide the entity into smaller entities. Put each smaller entity into its own file.
`style.py` checks the number of the functions. `[style] functions` gives the limit.

### O4 - The names of the files and of the folders

The name of a file tells which logical entity the file holds. Thus the name is clear, precise and explicit.
For example, `string.c` and `algo.c` are bad names. `string_toolbox.c` and `pathfinding.c` are better names.

Each name of a file or of a folder is in English and in snake case: lower case letters, digits and underscores only.
This rule applies to each file of the project, also to a document.
A name that a tool requires, which starts with a dot, is an exception.
You can use an abbreviation if it makes the name much shorter and keeps its meaning.
`tools/layout.py` checks this rule.

## G - The global scope

### G1 - The legal notice

Each source starts with the legal notice of `tools/header.txt`, between `/*` and `*/`, each line after `** `:

```text
/*
** Copyright (C) <year> <holder>
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
```

`docs/intern/tools/header.txt.md` gives the values of `<year>` and `<holder>`.
A file can have more lines of the copyright, one line for each holder.
Thus each project keeps the lines of the template in the files of the template.
If a file holds code of a different holder, add a line for that holder below the first line:

```text
/*
** Copyright (C) 2026 <holder>
** Copyright (C) 2005-2020 Rich Felker, et al. (musl, MIT)
**
** Under the GNU Affero General Public License, version 3 only: see license.
*/
```

The legal notice gives no path and no description of the file.
`style.py` checks this rule.

### G2 - The separation of the functions

In a source, exactly one empty line follows each function, if the function is not at the end of the file.
`style.py` checks this rule.

### G3 - The indentation of the directives

Indent each directive of the preprocessor by its level. Each level is 4 spaces.
`#if`, `#ifdef` and `#ifndef` open a level, and `#endif` closes it. `#else` and `#elif` are at the level of their `#if`.

Do not put a space between `#` and the name of the directive.
The rule L2 also applies to the directives.
`style.py` checks this rule.

```c
#ifndef WIN32
    #if defined(__i386__) || defined(__x86_64__)
        constexpr size_t PAGE_SIZE = 4096;
    #else
        #error "Unknown architecture"
    #endif
#endif
```

### G4 - The global variables

Define each constant that is not trivial as a constant global variable.
Do not use a global variable that is not constant, if possible.
A variable is constant only if `const` or `constexpr` marks it. Be careful: the rules of `const` can be surprising.
`style.py` reports each global variable that is not constant.

```c
constexpr double GOLDEN_RATIO = 1.61803398875;
```

### G5 - static

Mark a global variable or a function with `static` if no other compilation unit uses it.
Be careful: `static` has more than one use.
`style.py` reports a function of a file `.c` that is not `static`, if no header of the project declares it.
It does not report `main`, a function that a macro defines, or a function whose declaration holds `dllexport` or `visibility`.
It does not report a function whose declaration holds a word that ends with `EXPORT` or `_API` either.

## F - The functions

### F1 - The coherence of a function

A function does one thing only. It does not mix levels of abstraction.
A function has one responsibility: only one reason can change it.
For example, a call to `malloc()`, a call to `allocate_user()` and a call to `create_user()` are at three different levels of abstraction.
No program checks this rule.

### F2 - The names of the functions

The name of a function tells the task of the function, and contains a verb.
For example, `voyals_nb()` and `dijkstra()` are bad names. `get_voyals_number()` and `search_shortest_path()` are better names.
Each name of a function is in English and in snake case.
You can use an abbreviation if it makes the name much shorter and keeps its meaning.

The verb tells if the call changes something.
A function that answers yes or no starts with `is_` or `has_`. A function that gives a value and changes nothing starts with `get_`.
The name of each other function starts with the verb of its action.
If the name starts with the name of the owner of the function, keep the owner first, for example `storage_is_alive()`.

This code obeys the rule:

```c
bool has_moved(const storage_t *r, uint64_t id);
set_t *get_set(storage_t *r, uint32_t slot);
uint64_t hash_type(const type_t *type);
```

This code breaks the rule:

```c
bool moved(const storage_t *r, uint64_t id);
set_t *set_of(storage_t *r, uint32_t slot);
uint64_t fingerprint(const type_t *type);
```

`style.py` checks the snake case. A person checks the verb.

### F3 - The number of columns

A line has at most 80 columns. `[style] columns` gives the limit.
A column is not a character. A tab is one character, and it moves the next character to the next multiple of 8 columns.
`style.py` checks this rule.

### F4 - The number of lines

Keep the body of a function as short as possible.
The body of a function has at most 20 lines. `[style] lines` gives the limit.
A longer function probably does too many tasks.
The body is the lines between the line of the opening bracket and the line of the closing bracket.
`style.py` checks this rule.

This function has a body of 2 lines:

```c
int main(void)
{
    printf("hello, world\n");
    return (0);
}
```

### F5 - The arguments

Declare the arguments of a function as ISO C declares them.
A function that takes no argument takes `void` in its declaration.
C23 lets `f()` declare a function with no argument, but this rule requires `f(void)`.

This code obeys the rule:

```c
phys_addr_t alloc_frame(void);
```

This code breaks the rule:

```c
phys_addr_t alloc_frame();
```

A function has at most 4 arguments. `[style] arguments` gives the limit.
A variadic function is permitted. Its `...` counts as one argument.

Give a structure to a function through a pointer, and not as a copy.
`style.py` checks `void` and the number of the arguments. A person checks the structures.

### F6 - The comments

No file has a comment that is not the legal notice.
A function explains itself with its name, its arguments and its code.
If a function needs a comment, make the function shorter or divide it.
`style.py` checks this rule.

## L - The layout in a function

### L1 - The contents of a line

A line holds one statement only. `style.py` reports these lines:

- a line with more than one statement,
- a condition of `if`, `while` or `switch` that holds an assignment,
- a condition and its statement on one line,
- statements that a comma joins,
- a line with more than one assignment.

This code breaks the rule:

```c
a = b = c = 0;
a++; b++;
if ((ptr = malloc(sizeof(struct my_struct))) != nullptr)
if (cond) return (ptr);
a = do_something(), 5;
```

### L2 - The indentation

Each level of indentation is 4 spaces. Do not use a tab for indentation.
A `case` is one level in its `switch`. The statements of a `case` are one level in the `case`.
A closing bracket is at the level of the statement that it closes.
`style.py` checks this rule.

```c
switch (kind) {
    case SCHEMA_BOOL:
        return (1);
    default:
        return (0);
}
```

### L3 - The spaces

Put a space after a comma. Put a space after a keyword that has arguments, for example `if`, `while` and `return`.
Do not put a space between the name of a function and its parenthesis. Do not put a space after a unary operator.

Put a space on the two sides of each binary operator and of each ternary operator.
`sizeof` is a unary operator. Thus write `sizeof(x)`.
A line does not end with white space.
`style.py` checks this rule.

This code obeys the rule:

```c
return (1);
break;
sum = term1 + 2 * term2;
s = sizeof(struct file);
i++;
```

This code breaks the rule:

```c
return(1);
i ++;
```

### L4 - The curly brackets

Put an opening bracket at the end of its line. The opening bracket of a function is alone on its line.
A closing bracket is alone on its line. Only `else` can follow it on the same line.
A block of one line does not need brackets.
`style.py` checks this rule.

This code obeys the rule:

```c
while (cond) {
    do_something();
}
if (cond) {
    do_something();
} else {
    do_something_else();
}
if (cond)
    return (ptr);
```

This code breaks the rule:

```c
if (cond) {return (ptr);}
if (cond)
{
    do_something();
}
int print_env(void) {
    return (0);
}
```

### L5 - The declarations of the variables

Declare the variables at the start of the function.
You can declare the counter of a `for` loop in the loop.
You can declare a variable and give it a value on the same line.
Declare one variable on a line.
`style.py` checks this rule.

This code obeys the rule:

```c
int main(void)
{
    int forty_two = 42;
    int max = 12;

    for (int i = 0; i < max; i++)
        calculate_gcd(forty_two, max);
    return (0);
}
```

This code breaks the rule two times:

```c
long calculate_gcd(long a, long b)
{
    long biggest, smallest;

    biggest = MAX(a, b);
    long rest;
    return (biggest);
}
```

### L6 - The empty lines

One empty line separates the declarations of the variables from the rest of the function.
A function has no other empty line.
`style.py` checks this rule.

This code obeys the rule:

```c
int sys_open(char const *path)
{
    int fd = thread_reserve_fd();
    struct filehandler *fhandler = nullptr;

    if (fd < 0)
        return (-1);
    thread_set_fd_handler(fd, fhandler);
    return (fd);
}
```

This code breaks the rule:

```c
int sys_open(char const *path)
{
    int fd = thread_reserve_fd();

    if (fd < 0)
        return (-1);

    return (fd);
}
```

## V - The variables and the types

### V1 - The names of the identifiers

Each identifier is in English and in snake case.
The name of a type that `typedef` defines ends with `_t`.
The names of the macros, of the global constants and of the items of an `enum` are in upper case, for example `UPPER_CASE`.
A constant in a function can also have a name in upper case.

You can use an abbreviation if it makes the name much shorter and keeps its meaning.
`style.py` checks the case and `_t`. A person checks the English.

This code obeys the rule:

```c
#define IS_PAGE_ALIGNED(x) (!((x) & (PAGE_SIZE - 1)))

enum arch : uint32_t {
    I386 = 0,
    X86_64,
    ARM,
};

constexpr double PI = 3.14159;
typedef struct int_couple pixel_t;
```

This code breaks the rule:

```c
typedef int age;
```

### V2 - The structures

Put variables into a structure only if they make one coherent entity.
Keep a structure as small as possible.
No program checks this rule.

This code obeys the rule:

```c
struct person {
    char *name;
    unsigned int age;
    float salary;
};
```

This code breaks the rule:

```c
struct trashy {
    struct person player;
    unsigned int width;
    unsigned int length;
    unsigned int score;
    int i;
};
```

### V3 - The pointers

Attach the pointer symbol `*` to the name of the variable, with no space.
This rule applies to a pointer only. A multiplication is not a pointer.
`style.py` checks this rule.

This code obeys the rule:

```c
int *a;
int a = 3 * b;
int strlen(char const *str);
```

This code breaks the rule:

```c
int* a;
```

## C - The control structures

Each control structure is permitted, if no rule refuses it.

### C1 - The conditional branches

A chain of `if` and `else` has at most 3 branches. `[style] branches` gives the limit.
In place of a longer chain, use an array of pointers to functions, or a `switch`.

Do not nest conditional branches 3 levels deep. `[style] depth` gives the limit of 2 levels.
If a function needs more levels, divide it into smaller functions.
`style.py` counts `if`, `while`, `for`, `switch` and `do` as levels. An `else if` is not a new level.
An exception of this rule gives the cyclomatic complexity of the function as its reason.

This code obeys the rule:

```c
if (a)
    do_something();
else if (b)
    do_something_else();
else
    do_something_more();
while (a)
    if (b)
        do_something();
```

This code breaks the rule two times:

```c
if (a)
    do_something();
else if (b)
    do_something_else();
else if (c)
    do_something_more();
else
    do_one_last_thing();
while (a)
    for (;;)
        if (b)
            do_something();
```

### C2 - The ternary operator

Use a ternary only if it stays simple and easy to read.
Do not nest or chain ternaries.
Do not use a ternary to control the flow of the program.
`style.py` checks this rule.

This code obeys the rule:

```c
parity_t year_parity = (year % 2 == 0) ? EVEN : ODD;
return (a > 0 ? a : 0);
```

This code breaks the rule:

```c
int a = b > 10 ? c < 20 ? 50 : 80 : e == 2 ? 4 : 8;
already_checked ? go_there() : check();
```

### C3 - goto

Do not use `goto`. It quickly makes the code difficult to read.
In rare cases, `goto` makes the code clearer or faster, for example in the handling of errors. Then give the reason in an exception.
`style.py` checks this rule.

## A - The advanced rules

### A1 - The constant pointers

If a function does not change the data of a pointer, mark the pointer `const`.
This applies to a parameter and to a variable of the function.
No program checks this rule.

### A2 - The types

Use the most precise type for the data, for example `size_t`, `ptrdiff_t`, `uint8_t` or `int32_t`.
No program checks this rule.

This code obeys the rule:

```c
unsigned int counter;
size_t get_obj_size(void const *object);
```

This code breaks the rule:

```c
int counter;
unsigned int get_obj_size(void const *object);
```

## H - The headers

### H1 - The contents of a header

A header holds only these items:

- the prototypes of functions,
- the declarations of types,
- the declarations of global variables,
- macros,
- functions `static inline`.

These items are only in headers.
A header includes a different header only if it is necessary.
`style.py` checks the items. A person checks the includes.

### H2 - The include guard

Protect each header from a second inclusion.
The first two directives are `#ifndef` and `#define` of the same name, or one of them is `#pragma once`.
`style.py` checks this rule.

### H3 - The macros

Do not use a macro for a constant. Use a typed `constexpr`.
A macro holds one statement only.
A macro with no arguments can give the text between the braces of a type: its fields or its values.
Thus a type and the text that describes it are the same text.
`style.py` checks this rule.

This code obeys the rule:

```c
constexpr double PI = 3.14159265358979323846;
#define DELTA(a, b, c) ((b) * (b) - 4 * (a) * (c))
#define POSITION_FIELDS { float x; float y; }
```

This code breaks the rule:

```c
#define PI 3.14159265358979323846
#define LOOP_COUNTER 0
#define PRINT_NEXT(num) {num++; printf("%d", num);}
```

## Exceptions

A file can break a rule only if an exception names the rule and the file, and gives a full and correct reason.
A good reason looks at the long term: clean code, easy reading, flexibility, or a speed that you measured.
Write the reason in the exception, and not in a comment of the code.

Each exception is a table `[[style.exception]]` of `project.toml`.
`docs/extern/project.toml.md`, *[[style.exception]]* gives its keys.
`style.py` reports each fault that no exception excuses, and each exception that excuses no fault.
An exception whose path matches no file excuses no fault too. Thus no exception stays after its reason or its file goes.
The line of an exception that excuses nothing is `project.toml:1: <rule> the exception for '<path>' excuses nothing`.

## Functions

| Function | Result |
| --- | --- |
| `Source(path, text)` | A file of C: its lines, its comments, its directives, and its code without comments and strings. |
| `tokens_of(code, start, end)` | Gives the tokens of a part of the code, with their positions. |
| `closing(code, at)` | Gives the position of the bracket that closes the bracket at `at`. |
| `opening(code, at)` | Gives the position of the bracket that opens the bracket at `at`. |
| `top_level(text, what)` | Tells if the text holds the character `what` out of all brackets. |
| `constant_in(text)` | Tells if a declaration declares a constant. |
| `parameters(text)` | Gives the number of the parameters of a list: -1 for an empty list, and 0 for `void`. |
| `Function(...)` | A function of a file: its name, its parameters, its brackets and the text before its name. |
| `file_scope(src)` | Gives the functions and the statements of the file scope. |
| `blank_lines(src, first, last)` | Gives the empty lines from `first` to `last`. |
| `check_lines(src)` | Checks each line: F3, L2, L3 and V3. |
| `check_file(src, functions)` | Checks the file: G1, F6, O3, G2, G3, V1, H1, H2 and H3. |
| `check_outside(src, statements, functions, declared)` | Checks the file scope: V1, H1, G4, F5 and G5. |
| `check_parameters(src, line, params, name)` | Checks the parameters of a function: F5. |
| `check_function(src, f)` | Checks the body of a function: F2, F4, F5, L1, L2, L4, L5, L6, V1, C1, C2 and C3. |
| `check(path, text, declared)` | Gives the faults of one file. `declared` holds the names that the headers of the project declare. |
| `exceptions()` | Gives the exceptions of `[[style.exception]]`. |
| `ours()` | Gives the files that `style.py` checks. |
| `prototypes()` | Gives the names that the headers of the project declare. |
| `self_test()` | Gives the faults of the self-test. |
| `main()` | Runs the self-test, checks the files, and writes the faults. |
