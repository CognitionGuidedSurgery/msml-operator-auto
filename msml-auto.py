#!/usr/bin/python


import re
import os
import collections
from operator import attrgetter

from path import path
from jinja2 import Environment, PackageLoader


class Operator(object):
    def __init__(self, name, input=[], output=[], parameters=[]):
        self.name = name
        self.native_name = name

        self.input = input
        self.output = output
        self.parameters = parameters

        self._module = None

    def types_list(self):
        get_type = attrgetter("type")
        return '[%s]' % ','.join(map(get_type, self.input + self.parameters))


Slot = collections.namedtuple("Slot", "name,type,format")

find_msml_comments = re.compile(r'/\*\*MSML(?P<meta>.*?)\*/', re.DOTALL | re.MULTILINE)
#find_msml_macro = re.compile(r'^(?P<meta>MSML_OPERATOR\(.*?\))', re.DOTALL | re.MULTILINE)

jenv = Environment(loader=PackageLoader("msml-auto", "."))

operator_template = jenv.get_template("operator_tpl.xml")
py_module_template = jenv.get_template("wrapper_module_tpl.py")


def MSML_OPERATOR(name, input=[], output=[], parameters=[]):
    return Operator(name, input, output, parameters)


def test_regex_comment():
    with open("example/01/src/square.h") as f:
        content = f.read()

    matches = find_msml_comments.findall(content)

    for m in matches:
        print m
        print "-" * 80


def extract_msml_information(filename):
    def flatten_str(s):
        return s.replace('\n', ' ').replace("\r", " ")

    with open(filename) as handle:
        content = handle.read()

    matches = find_msml_comments.findall(content)

    return map(lambda x: eval(x, globals()), map(lambda x: x, matches))


def write_xml_files(dir, operators, wrapper_name):
    for op in operators:
        op.module = wrapper_name
        assert isinstance(op, Operator)
        with open(dir / (op.name + ".xml"), "w") as handle:
            content = operator_template.render(
                o=op
            )
            handle.write(content)


def write_py_wrapper(dir, operators, wrapper_name, native_name):
    with open(dir / (wrapper_name + ".py"), "w") as handle:
        content = py_module_template.render(
            native_module=native_name,
            operators=operators
        )
        handle.write(content)


from pprint import pprint


def test_import_ex01():
    #for example 01 only
    import importlib
    import sys
    sys.path.append("/home/weigl/workspace/msml/src/") #msml
    sys.path.append(path.getcwd()/"gen")

    sq = importlib.import_module("simple")  #load square

    print "ADD:", sq.add(2, 3), "==5"
    print "SQR:", sq.square(2), "==4"
    print


def system(cmd):
    print "EXEC: ", cmd
    os.system(cmd)


def main():
    #test comment regex
    #test_regex_comment()

    fil = path("example/01/simple.h")
    info = extract_msml_information(fil)
    pprint(info)

    output_dir = ((fil.dirname()) / "gen").rmdir_p().mkdir_p()
    wrapper_name = "%s" % fil.namebase
    native_name = "%s_native" % fil.namebase
    print "Output", output_dir
    write_xml_files(output_dir, info, wrapper_name)
    write_py_wrapper(output_dir, info, wrapper_name, native_name)


    ##
    output_dir.dirname().chdir()
    swig_module_name = "%s_native" % fil.namebase

    system("swig -c++ -python  {file}.i".format(
        #module = swig_module_name,
        file=fil.namebase
    ))

    system("g++ -shared -I/usr/include/python2.7 -fPIC "
           "-o _{name}_native.so {name}.cpp {name}_wrap.cxx".format(
        name=fil.namebase
    ))

    system("mv _{name}_native.so {name}_native.py gen/".format(
        name=fil.namebase))

    test_import_ex01()


__name__ == "__main__" and main()