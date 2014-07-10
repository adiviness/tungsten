
#include "Bool.h"

Bool Bool_new(Bool_Class_Builtin class, bool value) {
    Bool self = (Bool)malloc(sizeof(struct Bool_Object_Builtin_));
    self->class = class;
    self->value = value;
    return self;
}

void Bool_delete(Bool self) {
    self->class = NULL;
    free(self);
}
        