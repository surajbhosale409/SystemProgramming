
symDefInstr=[' equ ',' db ',' dw ',' dd ',' dq ',' resb ',' resw ',' resd ',' resq ',':']
controlChng=['jmp','call','je','jg','jl']
#dataSizes={['db','resb']:1,['dw','resw']:2,['dd','resd']:4,['dq','resq']:8}
symTab={}


def alreadyNotIn(sym):
    if sym in symTab:
        return 0
    else:
        return 1

def addToSymTab(sym,line,defstat):
    if alreadyNotIn(sym):
        symTab[sym]=[lc,defstat]

def generateSymTab():
    f=open('p.asm','r')
    lc=1
    for l in f:
        l=l.strip()
        for i in symDefInstr:
            if i in l:
                if i==':':
                    sym=l.split(':')
                    addToSymTab(sym[0],lc,'Def')
                else:
                    sym=l.split()
                    addToSymTab(sym[0],lc,'Def')
        for i in controlChng:
            if i in l:
                sym=l.split()
                symTab[sym[1]]=lc
        lc+=1

generateSymTab()


print "Symbol\tLine"
for sym in symTab:
    print sym,"\t",symTab[sym]
