
TODO List
=======

Language features to add 
-------
    - operator assignments (x += 3)
    - list constructors (x = [], x = [1, 2, 3])
    - dictionary constructors (x = {}, instantiation with values syntax TBD)
    - ruby symbols (x = :some_symbol)
    - parentheses
    - ranges
        - [1..4] = [1, 2, 3 4]
        - [1...4] = [1, 2, 3]
    - object inheritence

Scanner
-------
    - keep track of line numbers
    - refactor scan method

Testing
-------
    - create tests for scanner
    - create tests for parser
    - create tests for ast
        - test expression tree transformations
    - create tests for symbol table

Symbol Table
-------
    - finish class symbol tables
    - add traversing rules for rest of ast nodes
