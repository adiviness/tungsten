
#ifndef BOOL_BUILTIN
#define BOOL_BUILTIN

#include <stdlib.h>
#include <stdbool.h>

struct Bool_Class_Builtin_ {
};

typedef struct Bool_Class_Builtin_* Bool_Class_Builtin;

struct Bool_Object_Builtin_ {
    Bool_Class_Builtin class;
    bool value;
};

typedef struct Bool_Object_Builtin_* Bool;


Bool Bool_new(Bool_Class_Builtin class, bool value);
void Bool_delete(Bool self);

#endif