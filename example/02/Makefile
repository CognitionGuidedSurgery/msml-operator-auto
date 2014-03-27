CXX = g++
CXXFLAGS = -shared -fPIC -std=c++0x 
CXXINC   = -I/usr/include/python2.7


default:
	swig -python -c++ -shadow classes.i 	
	$(CXX) $(CXXFLAGS) $(CXXINC) -o _classes.so \
		classes.h classes.cpp classes_wrap.cxx	

clean:
	rm *cxx
	rm *so
	rm *py
