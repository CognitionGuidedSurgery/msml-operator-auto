msml-operator-auto
==================

Proof-of-Concept for Autogenerating MSML-Operators

    Author: Alexander Weigl <uiduw@student.kit.edu>
    Version: 0.0.1 
    Date: 2014-03-27
    License: gplv3

Following steps are considered:

1. Write your C++-Operator (one source, one header file)
   Example: `simple.{h,cpp}`
2. Put MSML Operator comments into the header file (*Note* This is a Python constructor):
```cpp
/**MSML
Operator(name, inputs, outputs, parameters) 
*/
```
3. Write a small swig interface:
```swig
% module simple_native
%{
#include simple.h
%}
%include simple.h
```
4. Run msml-auto.py
  * Creation of operator XML-Files (based on comments)
  * create a msml wrapper module
  * Swig run (create `<name>_wraps.cxx` and a wrapper module)
  * `g++` run (creates shared object `_<name>_wraps.sh`)
  * move everything to the right place 
  * and test it



### TODO


* Creates a `setup.py` for operator and sharedobject
* More flexible for project layouts (include, lib paths, ...)

