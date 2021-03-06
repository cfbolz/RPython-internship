import treeClass
import parser
import sys
 
def Interpret(tree, funDict, contVar):
    """ Interpret the F1WAE AST given a set of defined functions. We use deferred substituion and eagerness."""

     
    # try:
    assert(isinstance(tree,treeClass.F1WAE))
        #
    if isinstance(tree, treeClass.Num):
        return tree.n
    #
    elif isinstance(tree, treeClass.Op):
        assert(tree.op in ('+','-','*','/','%','='))
        left = Interpret(tree.lhs, funDict, contVar)
        right = Interpret(tree.rhs, funDict, contVar)
        if tree.op == '+':
            return left + right
        elif tree.op == '-':
            return left - right
        elif tree.op == '*':
            return left * right
        elif tree.op == '/':
            return left/right
        elif tree.op == '%':
            return left % right
        # elif tree.op == '=':
        else:
            if left == right:
                return 1
            else:
                return 0
            # else:
            #         raise ValueError("Parsing Error, symobl "+ tree.op+" shouldn't be here.")
        #
    elif isinstance(tree, treeClass.With):
        val = Interpret(tree.nameExpr, funDict, contVar)
        contVar[tree.name] = val #Eager
        return Interpret(tree.body, funDict, contVar)
    #
    elif isinstance(tree, treeClass.Id):
        #try:
        return contVar[tree.name] 
        #except KeyError:
        #   pass
                #raise ValueError("Interpret Error: free identifier :\n" + tree.name)
        #
    elif isinstance(tree, treeClass.App):
        #try:
        #
        funDef = funDict[tree.funName]
        val = Interpret(tree.arg, funDict, contVar)
        assert(isinstance(funDef,treeClass.Func))
        # if not isinstance(funDef, treeClass.Func):
        #     raise ValueError("Wrong Dictionnary.")
        newCont = {funDef.argName: val} # Eager
        return Interpret(funDef.body, funDict, newCont)
            #
            # except KeyError:
            #  raise ValueError("Invalid function : " + tree.funName)
        #
        #elif isinstance(tree, treeClass.If):
    else:
        assert(isinstance(tree,treeClass.If))
        condition = Interpret(tree.cond, funDict, contVar)
        if condition != 0: #True
            return Interpret(tree.ctrue, funDict, contVar)
        else:
            return Interpret(tree.cfalse, funDict, contVar)
        #
        # else: # Not an <F1WAE>
              #    raise ValueError("Argument of Interpret is not a <F1WAE>:\n")
        #
        # except ValueError as text
        #raise ValueError(text)
            
        
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
