%module classes

%include "std_vector.i"

%{
#include "classes.h"
%}

namespace std {
  %template(vectori) vector<int>;
}

%include "classes.h"
