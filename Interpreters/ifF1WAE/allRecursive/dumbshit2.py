def base2(n,p):
    if n==0:
        if p==0:
            return []
        else:
            return ([0,] + base2(n,p-1))
    else:
        return ([n%2,] + base2(n/2,p-1))

def getGreenRed(n):
    liste = ['tree', 'funDict', 'contVar']
    lis = base2(n,3)
    greens = []
    reds = []
    
    i = 0
    while i <3:
        if lis[i]:
            greens.append(liste[i])
        else:
            reds.append(liste[i])
        i += 1

    print("For n == {} :\n jitdriver = JitDriver(greens={}, reds={}) \n \n".format(n,greens,reds))

k=0
while k<=7:
    getGreenRed(k)
    k += 1
    
        
        
