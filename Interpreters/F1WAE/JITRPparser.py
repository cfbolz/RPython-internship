import RPtreeClass

# Build associativity of braces


# To optmisize: calculate size of stack and dic beforehand
def BuildAssociativity(fileToUse):
    """ Build a associative table of braces. """

    bracketMap = {}
    leftstack = []

    pc = 0
    for char in fileToUse:
        if char == '(' or char == '{':
            leftstack.append(pc)
        elif char == ')':
            left = leftstack.pop()
            if fileToUse[left] != '(':
                raise ValueError("Should be } at " + str(pc))
            right = pc
            bracketMap[left] = right
            bracketMap[right] = left
        elif char == '}':
            left = leftstack.pop()
            if fileToUse[left] != '{':
                raise ValueError("Should be ) at "+str(pc))
            right = pc
            bracketMap[left] = right
            bracketMap[right] = left
        else:
                pass
        pc += 1
            
    return bracketMap


# Spliting the original code into blocks

def belong(n,s,e):
    return n<e and n>=s

def FilterDic(dictry, start, end):
    """Return a new dictionnary containning only pairing of indices between start and (end-1) inclued."""

    newDic ={}
    for i,k in dictry.items():
        if belong(i,start,end) and belong(k,start,end):
            newDic[i-start]=k-start
        elif belong(i,start,end) and not belong(k,start,end):
            raise ValueError("Not a valid bracket matching")
        else:
            pass
    return newDic

def CutWord(string,i):
    """Find the first blank character following string[i] in string. If there's none, return the length of the list."""
    
    if string[i] in (' ','\n','\t'):
        return i
    else:
        try:
            return CutWord(string,i+1)
        except IndexError:
            return i+1
        

def SplittingCode(fileToUse, bracketMap):
    """ Splits the code into meaningful blocks. """

    pc = 0
    length = len(fileToUse)
    blocks = []
    
    while pc<length:
        ch = fileToUse[pc]
        if (ch in (' ', '\t', '\n')):
            pass
        elif ch =='(' or ch=='{':
            matchingBracket = bracketMap[pc] + 1
            assert(matchingBracket >=0 )
            block = fileToUse[pc:matchingBracket]
            newDic = FilterDic(bracketMap, pc, matchingBracket)
            blocks.append((block, newDic))
            pc = matchingBracket
        else:
            end = CutWord(fileToUse,pc)
            assert(end >= 0)
            blocks.append((fileToUse[pc:end], {}))
            pc = end
        pc += 1
            
    return blocks


# Parsing function

def ParseFunc((block, dic)):
    """ Given a block defining a function, return the correspondant representation. There are only simple spaces. """

    n = dic[0]
    if not (block[0] == '{' and block[n] == '}'):
        raise ValueError("Not a function block :\n"+ block)
    else:
        assert(n>=0)
        workingBlock = block[1:n]
        dic2 = FilterDic(dic,1,n)
        subBlocks = SplittingCode(workingBlock, dic2)
        #
        if len(subBlocks) != 2:
            raise ValueError("Only two sub-blocks expected in block :\n"+block)
        else:
            declaration, dd = subBlocks[0]
            #
            if len(dd.values()) != 2 :
                raise ValueError("No sub-blocks expected inside of :\n" + declaration)
            #
            end = dd[0]
            assert(end>=0)
            declareList = declaration[1:end].split(" ")
            if len(declareList) != 2:
                raise ValueError("Wrong declaration: \n" + declaration + "\nExpected form: <id> <id>")
            name = declareList[0]
            argName = declareList[1]
                
            bodyTree = ParseF1WAE(subBlocks[1])

    return name, RPtreeClass.Func(name,argName,bodyTree)

##Block of functions to define an identifier or a number
# Can't use .isalpha() ;-(
alphaOrUnd = ('a','z','e','r','t','y','u','i','o','p','q','s','d','f','g','h','j','k','l','m','w','x','c','v','b','n','_')
digit = ('0','1','2','3','4','5','6','7','8','9')

def isAlphaOrUndChar(c):
    """ Check if the forst character belongs to alphaOrUnd. """
    try:
        return c[0] in alphaOrUnd
    except IndexError:
        return False

def isAlphaNumOrUnd(c):
    """ Check if every character is either in alphaOrUnd or in digit. """

    length =len(c)
    pc = 0
    answer = True
    while answer and pc < length:
        answer = answer and (c[pc] in alphaOrUnd or c[pc] in digit)
        pc +=1
    return answer and length >0
        
def IsIdentifier(word):
    """True if word is a correct identifier."""
    
    return (isAlphaOrUndChar(word) and isAlphaNumOrUnd(word))

def IsNumber(c):
    """ True iff the string is only made of digits and non-empty."""

    length =len(c)
    pc = 0
    answer = True
    while answer and pc < length:
        answer = answer and c[pc] in digit
        pc +=1
    return answer and length>0
##

## Replace str.partition(' ') unavailable with TTC
def partitionSpace(word):
    """ Same as string method partition(' ') """

    length = len(word)
    pc = 0
    head = tail = ''
    while pc < length:
        if word[pc]==' ':
            assert(pc>=0)
            head = word[0:pc]
            tail = word[pc+1:length]
            break
        else:
            pc += 1

    return head, tail

##Replace str.qplit() available, but we need the number of spaces deleted at the beging of the word
def StripSpace(word):
    """ Same as str.split(' ') but also return the number of spaces deleted at the begining. """

    beg = 0
    end = len(word)
    count = 0

    while beg < end:
        if word[beg] == ' ':
            count += 1
            beg += 1
        else:
            break

    while end > beg:
        end -= 1
        if word[end] != ' ':
            break
        
    if beg == end == len(word):
        return '', len(word)
    else:
        end += 1
        assert(end>=0)
        return word[beg: end], count
##

def ParseF1WAE((block, dic)):
    """Parses <F1WAE>. Only simple spaces."""

    if block[0] == '{':
        raise ValueError("Function declaration is not allowed in <F1WAE> :\n" + block)
    #
    elif block[0] == '(':
        lastPos = dic[0]
        assert(lastPos >= 0)
        blockContent, count = StripSpace(block[1:lastPos])
        # First word in blockContent allows to identify the case
        head, tail = partitionSpace(blockContent)
        #
        if head == 'with':
            bodyWith = SplittingCode(tail, FilterDic(dic,len(head+' ')+1+count,dic[0]))
            if len(bodyWith) != 2:
                raise ValueError("Two expressions expected following keyword 'with':\n" + block)
            else:
                falseApp = ParseF1WAE(bodyWith[0]) #Same syntax as an App
                if not(isinstance(falseApp, RPtreeClass.App)):
                    raise ValueError("Wrong assignement in with block:\n" + block)
                else:
                    return RPtreeClass.With(falseApp.funName, falseApp.arg, ParseF1WAE(bodyWith[1]))
            #
        elif head[0] in ('+','-','*','/','%'): # Treats the case were space is forgotten after operator
            bodyOp = SplittingCode((head[1:len(head)] + tail),FilterDic(dic,len(head+' ')+1+count,dic[0]))
            if len(bodyOp) != 2:
                raise ValueError("Two expressions expected following operator :\n" + block)
            else:
                return RPtreeClass.Op(head[0], ParseF1WAE(bodyOp[0]), ParseF1WAE(bodyOp[1]))
            #
        else: # An App or a parenthesized Num or Id
            bodyApp =  SplittingCode(tail, FilterDic(dic,len(head+' ')+1+count,dic[0]))
            lenght = len(bodyApp)
            if lenght == 0: # Parenthesized Num or Id
                return ParseF1WAE((head, FilterDic(dic,1,dic[0])))
            elif lenght == 1: #An App
                return RPtreeClass.App(head, ParseF1WAE(bodyApp[0]))
        #
    else:
        #
        if IsIdentifier(block):
            return RPtreeClass.Id(block)
        elif IsNumber(block):
            return RPtreeClass.Num(int(block))
        else:
            raise ValueError("Syntax Error in identifier :\n" + block)

def Parse(myFile):
    """ The global parsing function. """
    
    myFile = (myFile.replace('\n',' ')).replace('\t',' ')
    # There are only simple spaces. Makes it easier to deal with.
    bracketMap = BuildAssociativity(myFile)
    codeInPieces = SplittingCode(myFile, bracketMap)
    #
    funcToDefine = []
    prog = []
    #
    for couple in codeInPieces:
        s,d = couple
        if s[0] == '{':
            funcToDefine.append((s,d))
        else:
            prog.append((s,d))
    #
    try: # Check that BNF is respected
        prog[1]
        raise ValueError("Only one <Prog> is allowed.")
    except IndexError:
        pass
    #
    # Create the function dictionnary
    funcDict = {}
    for funcDef in funcToDefine:
        name, descr = ParseFunc(funcDef)
        try:
            uselessVar = funcDict[name]
            raise ValueError("Function "+name+" already defined.")
        except KeyError:
            funcDict[name] = descr
    #
    # Create AST of main program
    ast = ParseF1WAE(prog[0])

    return ast, funcDict
    
