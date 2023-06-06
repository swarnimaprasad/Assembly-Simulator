import mem
import EE
import sys
if(mem.check()==False):
    PC=0
    halt=False
    while(not(halt)):
        instruct=mem.fetchData(PC)
        new_PC=EE.execute(instruct)
        sys.stdout.write(str(bin(PC)[2:].zfill(7)+"        "))
        sys.stdout.write(str(EE.RF("R0")+" "+EE.RF("R1")+" "+EE.RF("R2")+" "+EE.RF("R3")+" "+EE.RF("R4")+" "+EE.RF("R5")+" "+EE.RF("R6")+" "+EE.RF("FLAGS")+"\n"))
        if new_PC=="Halt":
            halt=True
        elif new_PC=="normal":
            PC+=1
        else:
            PC=new_PC
    binary=mem.memorydump()
    for i in binary:
        sys.stdout.write(i)
else:
    quit