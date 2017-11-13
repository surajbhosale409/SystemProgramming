import re

registers={"eax":["REG32","000"],"ebx":["REG32","001"],"ecx":["REG32","010"],"edx":["REG32","011"],"esi":["REG32","100"],"edi":["REG32","101"],"ebp":["REG32","110"],"esp":["REG32","111"],"ax":["REG16","000"],"bx":["REG16","001"],"cx":["REG16","010"],"dx":["REG16","011"],"si":["REG16","100"],"di":["REG16","101"],"bp":["REG16","110"],"sp":["REG16","111"],"al":["REG8","000"],"ah":["REG8","000"],"bl":["REG8","001"],"bh":["REG8","001"],"cl":["REG8","010"],"ch":["REG8","010"],"dl":["REG8","011"],"dh":["REG8","011"]}

###list containing ascii values of allowed charset for symbols###
symcharset=range(65,91)+range(97,123)+range(0,10)+range(95,96)


symDefInstr=[' equ ',' db ',' dw ',' dd ',' dq ',' resb ',' resw ',' resd ',' resq ',':']
cntrlScope=['jmp','call','je','jg','jl','global','extern']
dataSizes={' db ':1,' resb ':1,' dw ':2,' resw ':2,' dd ':4,' resd ':4,' dq ':8,' resq ':8}

### DATA STRUCTURES FOR STORING SYMBOL TABLE,LITERAL TABLE,ERROR TABLE,Intermediate Code ###
symTab={}
litTab={}
intermCode=[]
errorTab={}


def alreadyNotDef(sym):
    if sym in symTab:
       arg=symTab[sym]
       if arg[2]=="Def":
          return 0
       else:
          return 1
    else:
       return -1


def addToSymTab(sym,sid,lc,defstat,size,addr,val):
    try:

        ###ERROR CHECKING###
        if int(sym[0]):
            err="Error: Invalid Symbol "+sym+" at Line no "+str(lc)+", Symbol cannot be starting with a number"
            addToErrTab(err,lc)
            print err
        ###################

    except ValueError:

            ###ERROR CHECKING###
            for char in sym:
                if ord(char) not in symcharset:
                    err="Error: Symbol "+sym+" Contains Invalid character at line no "+str(lc)
                    addToErrTab(err,lc)
                    print err
                    return
            ####################

            if alreadyNotDef(sym)==-1:
                symTab[sym]=[sid,lc,defstat,size,addr,val]

            elif alreadyNotDef(sym)==1 and defstat=="Def":
                symTab[sym]=[symTab[sym][0],lc,defstat,size,addr,val]

            ###ERROR CHECKING###
            elif alreadyNotDef(sym)==0 and defstat=="Def":
                err="Error: Symbol "+str(sym)+" is Redefined at line "+str(lc)
                addToErrTab(err,lc)
                print err
            ###################



def calcSize(ls,i,lc):
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

        ###ERROR CHECKING###
        if int(q)<1:
            err="Error: Argument for "+i+" cannot be negative i.e. "+str(q)
            addToErrTab(err,lc)
            print err
            return ['NULL','NULL']
        ###################

        size=dataSizes[i]*q
        return ['NULL',size]
    elif i==' equ ':
        return [' - ',4]


def addToErrTab(err,lc):
    errno=len(errorTab)+1
    key="E"+str(errno)
    errorTab[key]=[str(lc),err]


def undefSymErr():
    for sym in symTab:
        if symTab[sym][2]=="Undef":
            err="Error: Symbol "+sym+" on line no "+symTab[sym][1]+" is not defined"
            addToErrTab(err,symTab[sym][1])
            print err



def generateIntermCode(l,ls,stat):
    s=""
    if stat=="db":
        l+="\t\t\t"+symTab[ls[0]][4]
    elif stat=="i":
           fmt=ls[0]
           if len(ls)==3:
                for reg in registers:
                    if ls[1]==reg:
                        fmt+=" "+registers[reg][0]
                        ls[1]=registers[reg][1]
                    if ls[2]==reg:
                        fmt+=" "+registers[reg][0]
                        ls[2]=registers[reg][1]
                for sym in symTab:
                    if ls[2]==sym:
                        fmt+=" IMM"
                        ls[2]=registers["ebp"][1]+"["+symTab[sym][4]+"]"
                for key in litTab:
                    if ls[2]==litTab[key][0]:
                        fmt+=" IMM"
                        ls[2]=registers["ebp"][1]+" "+key


                l+="\t\t11 "+ls[1]+" "+ls[2]+"\t\t"+fmt


           if len(ls)==2:
                for reg in registers:
                    if ls[1]==reg:
                        ls[1]="( "+registers[reg][0]+" , "+registers[reg][1]+" )"
                l+="\t\t11 "+ls[0]+" "+ls[1]



    intermCode.append(l)








def addLitFromLine(l,lc):
    line=l
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

            ###ERROR CHECKING###
            elif (l[2] not in registers) and (l[2] not in symTab) and ("dword" not in l[2]):
                addToSymTab(l[2],"S"+str(len(symTab)+1),str(lc),"Undef","-","-")
                err="Error: Invalid Operand 2 "+l[2]+" for Instruction at line no "+str(lc)
                addToErrTab(err,lc)
                print err
            ###################




def calcAddr():
    if len(symTab)==0:
        return 0
    else:
        tsize=0
        try:
            for sym in symTab:
                tsize+=int(symTab[sym][3])

            return tsize
        except ValueError:
            return "-"



def generateSymLitErrTabIntermCode(f):
    lc=1
    textSection=0
    dataSection=0
    bssSection=0
    skipFlag=0
    for l in f:
        skipFlag=0
        l=l.strip()
        if l=="section .text":
            textSection=1
            bssSection=0
            generateIntermCode(l,[],"default")
        if l=="section .data":
            dataSection=1
            generateIntermCode(l,[],"default")
        if l=="section .bss":
            bssSection=1
            dataSection=0
            generateIntermCode(l,[],"default")

        if bssSection==1:
            ###ERROR CHECKING###
            for i in [' db ',' dw ',' dd ',' dq ']:
                if i in l:
                    err="Error: Instrunction "+i+" should not be in section .bss, Error at line no "+str(lc)
                    addToErrTab(err,lc)
                    print err
                    skipFlag=1
            ####################


        if textSection==1:
            ###ERROR CHECKING###
            for i in symDefInstr:
                if i!=':' and i in l:
                    err="Error: Instrunction "+i+" should not be in section .text, Error at line no "+str(lc)
                    addToErrTab(err,lc)
                    print err
                    skipFlag=1
            ####################
            if skipFlag==0:
                addLitFromLine(l,lc)

        for i in symDefInstr+cntrlScope:
            if i in cntrlScope and i in l and skipFlag==0:
               sym=l.split()
               addToSymTab(sym[1],"S"+str(lc),str(lc),'Undef',' - ',' - ',' - ')
            if i in symDefInstr and i in l and skipFlag==0:
               if i==':':
                  sym=l.split(':')
                  addToSymTab(sym[0],"S"+str(len(symTab)+1),str(lc),'Def',' - ',' - ',' - ')
               else:
                  sym=l.split()
                  ls=calcSize(sym,i,lc)
                  addr=calcAddr()
                  value=ls[0]
                  size=ls[1]
                  if size!="NULL":
                    addToSymTab(sym[0],"S"+str(lc),str(lc),'Def',str(size),str(addr),str(value))
                  generateIntermCode(l,sym,"db")

        if textSection==1:
            if l!="section .text" and "global" not in l and "extern" not in l :
                tokens=re.split(" |,",l)
                generateIntermCode(l,tokens,"i")

        lc+=1
    undefSymErr()


def firstPass():
    f=open('p.asm','r')
    generateSymLitErrTabIntermCode(f)


###calling firstpass of the assembler###
firstPass()



###Code for just displaying tables generated in first pass and the intermediate code###

print "\n\nSYMBOL TABLE:"
print "Symbol\tSID\tLine\tD/U\tSize\tAddress\tValue"
for sym in symTab:
    print sym,"\t"+"\t".join(symTab[sym])

print "\n\nLITERAL TABLE:"
print "Literal\tValue\tLine No"
for lit in litTab:
    print lit,"\t"+"\t".join(litTab[lit])

print "\n\nIntermediate Code:\n"
for l in intermCode:
    print l

print "\n\nERROR TABLE:"
print "ERR_ID\tLine No\tERROR"
for err in errorTab:
    print err,"\t"+"\t".join(errorTab[err])


