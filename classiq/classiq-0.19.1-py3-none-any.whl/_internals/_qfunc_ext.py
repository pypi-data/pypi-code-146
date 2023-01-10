from importlib.machinery import SOURCE_SUFFIXES

CUSTOM_FUNCTION_SUFFIX = ".qfunc"

# The following line enables user-defined functions in separate .qfunc files
SOURCE_SUFFIXES.append(CUSTOM_FUNCTION_SUFFIX)
