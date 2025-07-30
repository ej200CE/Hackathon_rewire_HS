import sys, pprint, importlib.util
print("shared found?", importlib.util.find_spec("shared"))
pprint.pp(sys.path[:3])   # show first few paths