
Tungsten
=======

Tungsten is a statically typed, interpreted language that borrows its syntax heavily from Python, Ruby, and Go. Tungsten doesn't try to break any new ground as far as awesome language features are concerned. Tungsten exists to be a learning experience and not much more.

The language and interpreter are in a state of flux currently, what might work right now might very well be incorrect in ten minutes. 

Directory Structure
-------

```
/
    grammar/ # language grammar
    parser/  # parts of the interpreter that are involved from scanning to ir code generation
    vm/      # everything beyond ir code generation (virtual machine)
    test/    # tests
    tools/   # helpful tools for debugging
```

Running Tungsten
-------

The easiest way to run tungsten currently is `python3 runner.py` code will be accepted on stdin and will be interpreted after EOF has been sent. There is a basic repl that can be run with `python3 runner.py -i` but it's not as stable as using stdin.

Syntax
-------

The language is largely unimplemented currently, so this section will remain pretty empty until then. But here is a code snippet that illustrated most of the supported features currently:

```
some_num Int = 5
another_var Bool = true
x Int = some_num + 3

def add(a Int, b Int) Int:
  return a + b

print(add(some_num, x))
print(not another_var)

count Int = 5
while count > 0:
  print(count)
if count == 0:
  count = 3
elif count < 0:
  count = -1
else: 
  count = 2
```

Some important things to note:
- all indentation must be in increments of 2 spaces
- all functions must end with a return statement
- types found after a variable name
- a variable must be defined with a type before it can be used
- variables can currently only have an Int or Bool type



