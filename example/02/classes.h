#include <vector>
#include <string>
#include <memory>

std::vector<int> squares1(int);

std::vector<int>* squares2(int); 

std::shared_ptr<std::vector<int> > squares3(int);
