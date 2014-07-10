
#include "Int.h"

Int Int_new(Int_Class_Builtin class, int value) {
    Int self = (Int)malloc(sizeof(struct Int_Object_Builtin_));
    self->class = class;
    self->value = value;
    return self;
}  

void Int_delete(Int self) {
    self->class = NULL;
    free(self);
}