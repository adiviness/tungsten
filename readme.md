
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

The easiest way to run tungsten currently is `python3 runner.py` code will be accepted on stdin and will be interpreted after EOF has been sent. There isn't a repl yet.

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
```
