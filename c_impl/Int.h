
#ifndef INT_BUILTIN
#define INT_BUILTIN

#include <stdlib.h>

struct Int_Class_Builtin_ {
};

typedef struct Int_Class_Builtin_* Int_Class_Builtin;

struct Int_Object_Builtin_ {
    Int_Class_Builtin class;
    int value;
};

typedef struct Int_Object_Builtin_* Int;

Int Int_new(Int_Class_Builtin class, int value);
void Int_delete(Int self);
#endif