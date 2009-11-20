# A quine is a program that can reproduce its' own source code- much more
# difficult than it sounds!!! Here is a pair of programs that work for each
# others' source code. 
#
# Original Author: Frank Stajano

# Female, "X", version of the program that prints the source code for the male.

from string import replace
def r(s):return replace(replace(replace(s,"x","$"),"y","x"),"$","y")
z='from string import replace\012def r(s):return replace(replace(replace(s,"x","$"),"y","x"),"$","y")\012z=%s;';x='y=%s;print z%%`z`+y%%`r(y)`';print z%`z`+x%`r(x)`

# The male then repeats the same action for the female code. 

from string import replace
def r(s):return replace(replace(replace(s,"x","$"),"y","x"),"$","y")
z='from string import replace\012def r(s):return replace(replace(replace(s,"x","$"),"y","x"),"$","y")\012z=%s;';y='x=%s;print z%%`z`+x%%`r(x)`';print z%`z`+y%`r(y)`
