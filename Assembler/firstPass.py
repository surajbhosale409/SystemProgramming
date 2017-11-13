import re

symDefInstr=[' equ ',' db ',' dw ',' dd ',' dq ',' resb ',' resw ',' resd ',' resq ',':']
cntrlScope=['jmp','call','je','jg','jl','global','extern']
dataSizes={' db ':1,' resb ':1,' dw ':2,' resw ':2,' dd ':4,' resd ':4,' dq ':8,' resq ':8}
symTab={}
litTab={}

def alreadyNotDef(sym):
    if sym in symTab:
       arg=symTab[sym]
       if arg[1]=="Def":
          return 0
       else: 
          return 1
    else:
       return -1


def addToSymTab(sym,lc,defstat,size,val):
   if alreadyNotDef(sym)==-1:
      symTab[sym]=[lc,defstat,size,val]
   
   elif alreadyNotDef(sym)==1 and defstat=="Def":  
      symTab[sym]=[lc,defstat,size,val]
   
   elif alreadyNotDef(sym)==0 and defstat=="Def":
       print "Error: Symbol ",sym," is Redefined at line ",lc



def calcSize(ls,i):
    if i==" db ":
        values=ls[2]
        ls=values.replace('"','')
        ls=ls.replace(',','')
        size=len(ls)
        return [values,size]
    elif i in [' dd ',' dw ',' dq ']:
        values=ls[2]
        ls=values.split(",")
        size=dataSizes[i]*len(ls)
        return [values,size]
    elif i in [' resb ',' resd ',' resw ',' resq ']:
        q=ls[2]
        size=dataSizes[i]*q
        return ['NULL',size]
    elif i==' equ ':
        return [' - ',4]


def addLitFromLine(l,lc):
    l=re.split(' |,',l)
    litno=len(litTab)+1
    i=0
    if len(l)==3:
        try:
            i=int(l[2])
            key="L"+str(litno)
            litTab[key]=[str(i),str(lc)]
        except ValueError:
            if len(l[2])==3 and l[2][0]=="'" and l[2][2]=="'":
                key="L"+str(litno)
                litTab[key]=[l[2],str(lc)]
            


def generateSymLitTab(f):
    lc=1
    textSection=0
    for l in f:
        l=l.strip()
        if l=="section .text":
            textSection=1

        if l != "":
            if textSection==1:
               addLitFromLine(l,lc)

            for i in symDefInstr+cntrlScope:
                if i in cntrlScope and i in l:
                    sym=l.split()
                    addToSymTab(sym[1],str(lc),'Undef',' - ',' - ')
                if i in symDefInstr and i in l:
                    if i==':':
                       sym=l.split(':')
                       addToSymTab(sym[0],str(lc),'Def',' - ',' - ')
                    else:
                       sym=l.split()
                       ls=calcSize(sym,i)
                       value=ls[0]
                       size=ls[1]
                       addToSymTab(sym[0],str(lc),'Def',str(size),str(value))
            lc+=1          


def firstPass():
    f=open('p.asm','r')
    generateSymLitTab(f)



firstPass()

print "SYMBOL TABLE"
print "Symbol\tLine\tD/U\tSize\tValue"
for sym in symTab:
    print sym,"\t"+"\t".join(symTab[sym])

print "\n\nLITERAL TABLE"
print "Literal\tValue\tLine No"
for lit in litTab:
    print lit,"\t"+"\t".join(litTab[lit])


