__author__ = 'Alexander Weigl'

from msml.model.exceptions import MSMLUnknownModuleWarning
from warnings import warn
try:
    import {{native_module}} as cpp
except ImportError, e:
    import sys
    warn("Could not import {{native_module}}\n"
         "This is the C++-Modul. Have you successfully compiled and installed it?\n"
         "Error is %s\n"
         "sys.path is %s" % (e, sys.path),
         MSMLUnknownModuleWarning, 0)



def _bool(s):
    return s in ("on", "True", "true", "yes")


def __convert(converters, values):
    from itertools import starmap
    args = list(starmap(lambda conv, val: conv(val), zip(converters,values)))
    return args


{% for o in operators %}
def {{o.name}}(*args):  #{o|populate_args}
    converters = {{o.types_list()}}
    values = __convert(converters, args)
    return cpp.{{o.native_name}}(*values)
{% endfor %}
