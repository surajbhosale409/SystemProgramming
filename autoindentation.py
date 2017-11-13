blocks=['if','else','while','for','{']

f=open("code.c","r")
fdata=f.read()

f=open("code.c","w")
indentation=0

for line in fdata:
        if blocks[0] in line or blocks[1] in line or blocks[2] in line or blocks[3] in line or blocks[4] in line:           indentation=1
        elif indentation==1:
            line="\t"+line
        else:
           indentation=0
        f.write(line)


        
