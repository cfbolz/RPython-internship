import treeClass
import parser
import sys

##########################
# Class Function for CPS #
##########################

class Contk:
    def __init__(self):
        pass
    
    def apply(self,arg):
        return ExpVal(arg)

class Idk(Contk):
    def __init__(self):
        pass
    
    def apply(self,arg):
        return ExpVal(arg)

class Opk(Contk):
    def __init__(self,argLeft,op,k):
        self.argLeft=argLeft
        self.op=op
        self.k=k


    def apply(self,arg):
        if self.op == '+':
            return self.k.apply(self.argLeft + arg)
        elif self.op == '-':
            return self.k.apply(self.argLeft - arg)
        elif self.op == '*':
            return self.k.apply(self.argLeft * arg)
        elif self.op == '/':
            return self.k.apply(self.argLeft / arg)
        elif self.op == '%':
            return self.k.apply(self.argLeft % arg)
        elif self.op == '=':
            if self.argLeft - arg == 0:
                return self.k.apply(1)
            else:
                return self.k.apply(0)
        else:
            print("Parsing Error, symobl "+ self.op +" shouldn't be here.")
            return ExpVal(2)

class OpLeftk(Contk):
    def __init__(self, exprRight, funDict, env, k, op):
        self.exprRight=exprRight
        self.funDict=funDict
        self.env=env
        self.k=k
        self.op=op

    def apply(self, arg):
        return Interpk(self.exprRight,self.funDict,self.env, Opk(arg,self.op,self.k))

class Appk(Contk):
    def __init__(self, funName, funDict, k):
        self.funName=funName
        self.funDict=funDict
        self.k=k

    def apply(self, arg):
        if self.funName in self.funDict.keys():
            g=self.funDict[self.funName]
            return Interpk(g.body,self.funDict, {g.argName: arg}, self.k)
        else:
            print("Invalid function : " + self.funName)
            return ExpVal(2)

class Ifk(Contk):
    def __init__(self, true, false, funDict, env, k):
        self.true=true
        self.false=false
        self.funDict=funDict
        self.env=env
        self.k=k

    def apply(self,arg):
        if arg != 0:
            return Interpk(self.true, self.funDict, self.env, self.k)
        else:
            return Interpk(self.false, self.funDict, self.env, self.k)


#####################
# Bounce Definition #
#####################

class Bounce:
    def __init__(self):
        pass

class ExpVal(Bounce):
    def __init__(self,val):
        self.val=val

class BounceFun(Bounce):
    def __init__(self,arg,funDict,env,funName,k):
        self.arg=arg
        self.funDict=funDict
        self.env=env
        self.funName=funName
        self.k=k
        
    def bounce(self):
        return Interpk(self.arg, self.funDict, self.env, Appk(self.funName, self.funDict, self.k))

def Trampoline(bouncer):
    """Execute the trampoline while there's still one to do"""
    
    if isinstance(bouncer,ExpVal):
        return bouncer.val
    elif isinstance(bouncer, BounceFun):
        return Trampoline(bouncer.bounce())
    else:
        print("Not a Bounce!")
        return 2

#############################    
#Interpret CPS - Trampoline #
#############################

def Interpk(expr, funDict, env, k):
    """ Interpret the ifF1WAE AST given a set of defined functions. We use deferred substituion and eagerness."""

    #
    if isinstance(expr, treeClass.Num):
        return k.apply(expr.n)
    #
    elif isinstance(expr, treeClass.Op):
        k2 = OpLeftk(expr.rhs, funDict, env, k, expr.op)
        return Interpk(expr.lhs, funDict, env, k2)
    #
    elif isinstance(expr, treeClass.With):
        
        val = Trampoline(Interpk(expr.nameExpr, funDict, env, Idk()))
        env[expr.name] = val #Eager
        return Interpk(expr.body, funDict, env, k)
    #
    elif isinstance(expr, treeClass.Id):
        if expr.name in env.keys():
            return k.apply(env[expr.name])
        else:
            print("Interpret Error: free identifier :\n" + expr.name)
            return k.apply(2)
    #
    elif isinstance(expr, treeClass.App):
        return BounceFun(expr.arg, funDict, env, expr.funName, k)
    #
    elif isinstance(expr, treeClass.If):
        return Interpk(expr.cond,funDict,env,Ifk(expr.ctrue,expr.cfalse,funDict,env,k))
    #
    else: # Not an <ifF1WAE>
        print("Argument of Interpk is not a <ifF1WAE>:\n")
        return k.apply(2)
    #

#############################    
# Translation and execution #
#############################

def Main(file):
    t,d = parser.Parse(file)
    bou = Interpk(t,d,{},Idk())
    j = Trampoline(bou)
    print("the answer is :" + str(j))

import os

def run(fp):
    program_envents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_envents += read
    os.close(fp)
    Main(program_envents)

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
