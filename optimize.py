# from recipie 20.16

from opcode import opmap, HAVE_ARGUMENT, EXTENDED_ARG
globals().update(opmap)
def _insert_constant(value, i, code, constants):
    '''insert LOAD_CONST for value at code[i:i+3]. Reuse and existing
       constant if values coincide, otherwise append new value to the
       list of constants; return index of the value in constants'''

    for pos, v in enumerate(constants):
	if v is value: break
    else:
	pos = len(constants)
	constants.append(value)
    code[i] = LOAD_CONST
    code[i+1] = pos & 0xff
    code[i+2] = pos >> 8
    return pos
def _arg_at(i, code):
    '''return argument number of the optcode at code[i]'''
    return code[i+1] | (code[i+2] << 8)

def _make_constants(f, builtin_only=False, stoplist=(), verbose=False):
    # bail at once, innocuosly, if we're in Jython, IronPython, etc
    try: co = f.func_code
    except AttributeError: return f
    # we'll modify the bytecodes and consts, so make a list of them
    newcode= [ord(i) for i in co.co_code]
    codelen = len(newcode)
    newconsts = list(co.co_consts)
    names = co.co_names
    # Depending on whether we're binding only builtins, or ordinary globals
    # too, we build a dictionary 'env' to look up name->value mappings, and we
    # build set 'stoplist' to selectively override and cancel such lookups
    import __builtin__
    env = vars(__builtin__).copy()
    if builtin_only:
	stoplist = set(stoplist)
	stoplist.update(f.func_globals)
    else:
	env.update(f.func_globals)
    # First pass converts global lookups into lookup of constants
    i = 0
    while i < codelen:
	opcode= newcode[i]
	# bail out in difficult cases: optimize common cases only
	if opcode in (EXTENDED_ARG, STORE_GLOBAL):
	    return f
	if opcode == LOAD_GLOBAL:
	    oparg = _arg_at(i,newcode)
	    name = names[oparg]
	    if name in env and name not in stoplist:
		# get the constant index to use instead
		pos = _insert_constant(env[name], i, newcode, newconsts)
		if verbose: print '%r -> %r[%d]' % (name, newconsts[pos], pos)
	# move accurately to the next bytecode, skipping any arg if any
	i += 1
	if opcode >= HAVE_ARGUMENT:
	    i += 2
    # Second pass folds tuples of constants and constant attribute lookups
    i = 0
    while i < codelen:
	newtuple = []
	while newcode[i] == LOAD_CONST:
	    oparg = _arg_at(i, newcode)
	    newtuple.append(newconsts[oparg])
	    i += 3
	oparg = newcode[i]
	if not newtuple:
	    i += 1
	    if opcode >= HAVE_ARGUMENT:
		i += 2
	    continue
	if opcode == LOAD_ATTR:
	    obj = newtuple[-1]
	    oparg = _arg_at(i, newcode)
	    name = names[oparg]
	    try:
		value = getattr(obj, name)
	    except AttributeError:
		continue
	    deletions = 1
	elif opcode == BUILD_TUPLE:
	    oparg = _arg_at(i, newcode)
	    if oparg != len(newtuple):
		continue
	    deletions = len(newtuple)
	    value = tuple(newtuple)
	else:
	    continue
	reljump = deletions * 3
	newcode[i-reljump] = JUMP_FORWARD
	newcode[i-reljump+1] = (reljump-3) & 0xff
	newcode[i-reljump+2] = (reljump-3) >> 8
	pos = _insert_constant(value, i, newcode, newconsts)
	if verbose: print "new folded constant: %r[%d]" % (value, pos)
	i += 3
    codestr = ''.join(chr(i) for i in newcode)
    codeobj = type(co)(co.co_argcount, co.co_nlocals, co.co_stacksize,
		       co.co_flags, codestr, tuple(newconsts), co.co_names,
		       co.co_varnames, co.co_filename, co.co_name,
		       co.co_firstlineno, co.co_lnotab, co.co_freevars,
		       co.co_cellvars)
    return type(f)(codeobj, f.func_globals, f.func_name, f.func_defaults,
		   f.func_closure)

# optimize thyself!
_insert_constant = _make_constants(_insert_constant)
_make_constants = _make_constants(_make_constants)
import types
@_make_constants
def bind_all(mc, builtin_only=False, stoplist=(), verbose=False):
    '''Recursively apply constant binding to functions in a module class.'''
    try:
	d = vars(mc)
    except TypeError:
	return
    for k, v in d.items():
	if type(v) is types.FunctionType:
	    newv = _make_constants(v, builtin_only, stoplist, verbose)
	    setattr(mc, k, newv)
	elif type(v) in (type, types.ClassType):
	    bind_all(v, builtin_only, stoplist, verbose)
@_make_constants
def make_constants(builtin_only=False, stoplist=[], verbose=False):
    ''' Call this metadecorator to obtain a decorator which optimizes
        global references by constant binding on a specific function.'''
    if type(builtin_only) == types.FunctionType:
	return _make_constants(builtin_only,False,stoplist=stoplist,verbose=verbose)
    return lambda f: _make_constants(f,
				     builtin_only=builtin_only,
				     stoplist=stoplist,
				     verbose=verbose)
