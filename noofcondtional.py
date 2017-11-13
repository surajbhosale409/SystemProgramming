

def countBlocks():
   i=0
   w=0
   fr=0
   f=open("sample.c","r")
   for line in f:
        line=line.rstrip("\n")
        if "if (" in line or "if(" in line:
            i+=1
        elif "while (" in line or "while(" in line:
            w+=1
        elif "for (" in line or "for(" in line:
            fr+=1
        
   print "No of if blocks: ",i,"\nNo of while loops: ",w,"\nNo of for loops: ",fr


countBlocks()
