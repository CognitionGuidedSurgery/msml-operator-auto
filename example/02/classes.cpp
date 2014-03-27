#include "classes.h"

std::vector<int> squares1(int num) {
  std::vector<int> vec;
  
  for(int i=0; i<num;i++)
    vec.push_back(i*i);
  return vec;	
}

std::vector<int>* squares2(int num) {
  std::vector<int>* vec = new std::vector<int>;
  for(int i=0; i<num;i++)
    vec->push_back(i*i);
  return vec;
}

std::shared_ptr<std::vector<int>> squares3(int num) {
  std::shared_ptr<std::vector<int>> vec (new std::vector<int>);
  for(int i=0; i<num;i++)
    vec->push_back(i*i);
  return vec;
}
