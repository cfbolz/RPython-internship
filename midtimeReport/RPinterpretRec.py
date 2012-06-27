import treeClass
import parser
import sys

######################    
#Interpret Recursive #
######################
 
def Interpret(expr, funDict, env):
    """ Interpret the ifF1WAE AST given a set of defined functions. We use deferred substituion and eagerness."""

    if isinstance(expr, treeClass.Num):
        return expr.n
    #
    elif isinstance(expr, treeClass.Op):
        left = Interpret(expr.lhs, funDict, env)
        right = Interpret(expr.rhs, funDict, env)
        if expr.op == '+':
            return left + right
        elif expr.op == '-':
            return left - right
        elif expr.op == '*':
            return left * right
        elif expr.op == '/':
            return left/right
        elif expr.op == '%':
            return left % right
        elif expr.op == '=':
            if left == right:
                return 1
            else:
                return 0
        else:
            print("Parsing Error, symobl "+ expr.op+" shouldn't be here.")
            return 2
    #
    elif isinstance(expr, treeClass.With):
        val = Interpret(expr.nameExpr, funDict, env)
        env[expr.name] = val #Eager
        return Interpret(expr.body, funDict, env)
    #
    elif isinstance(expr, treeClass.Id):
        if expr.name in env.keys():
            return env[expr.name] 
        else:
            print("Interpret Error: free identifier :\n" + expr.name)
            return 2
    #
    elif isinstance(expr, treeClass.App):
        if expr.funName in funDict.keys():
            #
            funDef = funDict[expr.funName]
            val = Interpret(expr.arg, funDict, env)
            #
            if not isinstance(funDef, treeClass.Func):
                print("Wrong Dictionnary.")
            #
            newCont = {funDef.argName: val} # Eager
            return Interpret(funDef.body, funDict, newCont)
        #
        else:
            print("Invalid function : " + expr.funName)
            return 2
    #
    elif isinstance(expr, treeClass.If):
        condition = Interpret(expr.cond, funDict, env)
        if condition != 0: #True
            return Interpret(expr.ctrue, funDict, env)
        else:
            return Interpret(expr.cfalse, funDict, env)
    #
    else: # Not an <ifF1WAE>
        print("Argument of Interpret is not a <ifF1WAE>:\n")
        return 2        

#############################    
# Translation and execution #
#############################

def Main(file):
    t,d = parser.Parse(file)
    j = Interpret(t,d,{})
    print("the answer is :" + str(j))

import os

def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    os.close(fp)
    Main(program_contents)

def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "You must supply a filename"
        return 1

    run(os.open(filename, os.O_RDONLY, 0777))
    return 0

def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point(sys.argv)
