import json
import InstructionDictionary as instruct
Reg_value={}
for i in instruct.registers:
    Reg_value[instruct.registers[i]]="0"*16
with open("memory.json","r") as memory:
    json_dump=json.load(memory)
    binary=json_dump["binary"]

def RF(reg):
    return Reg_value[instruct.registers[reg]]

def add(reg1,reg2,reg3):
    reg2_value=Reg_value[reg2]
    reg3_value=Reg_value[reg3]
    reg1_value=(bin(int("0b"+reg2_value,2)+int("0b"+reg3_value,2))[2:]).zfill(16)
    if int("0b"+reg1_value,2)>=128:
        flags_value="0"*12+"1"+"0"*3
        reg1_value="0"*16
    else:
        flags_value="0"*16
    Reg_value[reg1]=reg1_value
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def sub(reg1,reg2,reg3):
    reg2_value=Reg_value[reg2]
    reg3_value=Reg_value[reg3]
    reg1_value=(bin(int("0b"+reg2_value,2)-int("0b"+reg3_value,2))[2:]).zfill(16)
    if int("0b"+reg1_value,2)<0:
        flags_value="0"*12+"1"+"0"*3
        reg1_value="0"*16
    else:
        flags_value="0"*16
    Reg_value[reg1]=reg1_value
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def mul(reg1,reg2,reg3):
    reg2_value=Reg_value[reg2]
    reg3_value=Reg_value[reg3]
    reg1_value=(bin(int("0b"+reg2_value,2)*int("0b"+reg3_value,2))[2:]).zfill(16)
    if int("0b"+reg1_value,2)>=128:
        flags_value="0"*12+"1"+"0"*3
        reg1_value="0"*16
    else:
        flags_value="0"*16
    Reg_value[reg1]=reg1_value
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def xor(reg1,reg2,reg3):
    reg2_value=Reg_value[reg2]
    reg3_value=Reg_value[reg3]
    reg1_value=(bin(int("0b"+reg2_value,2) ^ int("0b"+reg3_value,2))[2:]).zfill(16)
    Reg_value[reg1]=reg1_value
    flags_value="0"*16
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def Or(reg1,reg2,reg3):
    reg2_value=Reg_value[reg2]
    reg3_value=Reg_value[reg3]
    reg1_value=(bin(int("0b"+reg2_value,2) | int("0b"+reg3_value,2))[2:]).zfill(16)
    Reg_value[reg1]=reg1_value
    flags_value="0"*16
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def And(reg1,reg2,reg3):
    reg2_value=Reg_value[reg2]
    reg3_value=Reg_value[reg3]
    reg1_value=(bin(int("0b"+reg2_value,2) & int("0b"+reg3_value,2))[2:]).zfill(16)
    Reg_value[reg1]=reg1_value
    flags_value="0"*16
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def movImm(reg1,imm):
    reg1_value=imm.zfill(16)
    Reg_value[reg1]=reg1_value
    flags_value="0"*16
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def rs(reg1,imm):
    reg1_value=Reg_value[reg1]
    reg1_value=int("0b"+reg1_value,2)
    reg1_value=reg1_value>>imm
    reg1_value=bin(reg1_value)[2:0].zfill(16)
    Reg_value[reg1]=reg1_value
    flags_value="0"*16
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def ls(reg1,imm):
    reg1_value=Reg_value[reg1]
    reg1_value=int("0b"+reg1_value,2)
    reg1_value=reg1_value<<imm
    reg1_value=bin(reg1_value)[2:0].zfill(16)
    Reg_value[reg1]=reg1_value
    flags_value="0"*16
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def movreg(reg1,reg2):
    reg2_value=Reg_value[reg2]
    reg1_value=reg2_value
    reg2_value="0"*16
    Reg_value[reg1]=reg1_value
    Reg_value[reg2]=reg2_value
    flags_value="0"*16
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def divide(reg3,reg4):
    if Reg_value[reg4]=="0"*16:
        flags_value="0"*12+"1"+"0"*3
        R0_value="0"*16
        R1_value="0"*16
    else:
        flags_value="0"*16
        reg3_value=Reg_value[reg3]
        reg4_value=Reg_value[reg4]
        R0_value=bin(int("0b"+reg3_value,2)//int("0b"+reg4_value,2))[2:].zfill(16)
        R1_value=bin(int("0b"+reg3_value,2)%int("0b"+reg4_value,2))[2:].zfill(16)
    Reg_value[instruct.registers["R0"]]=R0_value
    Reg_value[instruct.registers["R1"]]=R1_value
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def invert(reg1,reg2):
    reg2_value=Reg_value[reg2]
    reg1_value=bin(~int("0b"+reg2_value,2))[2:].zfill(16)
    Reg_value[reg1]=reg1_value
    flags_value="0"*16
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def compare(reg1,reg2):
    reg1_value=Reg_value[reg1]
    reg2_value=Reg_value[reg2]
    int_reg1_value=int("0b"+reg1_value,2)
    int_reg2_value=int("0b"+reg2_value,2)
    if int_reg1_value>int_reg2_value:
        flags_value="0"*14+"1"+"0"
    elif reg1_value==reg2_value:
        flags_value="0"*15+"1"
    elif reg1_value<reg2_value:
        flags_value="0"*13+"1"+"0"*2
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def load(reg1,mem_addr):
    int_mem_addr=int("0b"+mem_addr,2)
    reg1_value=binary[int_mem_addr]
    if "\n" in reg1_value:
        reg1_value=reg1_value[:len(reg1_value)-1]
    Reg_value[reg1]=reg1_value
    flags_value="0"*16
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def store(reg1,mem_addr):
    int_mem_addr=int("0b"+mem_addr,2)
    reg1_value=Reg_value[reg1]
    binary[int_mem_addr]=reg1_value+"\n"
    flags_value="0"*16
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return -1

def jmp(mem_addr):
    int_mem_addr=int("0b"+mem_addr,2)
    flags_value="0"*16
    Reg_value[instruct.registers["FLAGS"]]=flags_value
    return int_mem_addr

def jlt(mem_addr):
    flags_value=Reg_value[instruct.registers["FLAGS"]]
    if flags_value[13]=="1":
        int_mem_addr=int("0b"+mem_addr,2)
        flags_value="0"*16
        Reg_value[instruct.registers["FLAGS"]]=flags_value
        return int_mem_addr
    else:
        flags_value="0"*16
        Reg_value[instruct.registers["FLAGS"]]=flags_value
        return -1

def jgt(mem_addr):
    flags_value=Reg_value[instruct.registers["FLAGS"]]
    if flags_value[14]=="1":
        int_mem_addr=int("0b"+mem_addr,2)
        flags_value="0"*16
        Reg_value[instruct.registers["FLAGS"]]=flags_value
        return int_mem_addr
    else:
        flags_value="0"*16
        Reg_value[instruct.registers["FLAGS"]]=flags_value
        return -1

def je(mem_addr):
    flags_value=Reg_value[instruct.registers["FLAGS"]]
    if flags_value[15]=="1":
        int_mem_addr=int("0b"+mem_addr,2)
        flags_value="0"*16
        Reg_value[instruct.registers["FLAGS"]]=flags_value
        return int_mem_addr
    else:
        flags_value="0"*16
        Reg_value[instruct.registers["FLAGS"]]=flags_value
        return -1


def execute(instruction):
    if instruction[0:5]=="00000":
        pc=add(instruction[7:10],instruction[10:13],instruction[13:16])
    elif instruction[0:5]=="00001":
        pc=sub(instruction[7:10],instruction[10:13],instruction[13:16])
    elif instruction[0:5]=="00110":
        pc=mul(instruction[7:10],instruction[10:13],instruction[13:16])
    elif instruction[0:5]=="01010":
        pc=xor(instruction[7:10],instruction[10:13],instruction[13:16])
    elif instruction[0:5]=="01011":
        pc=Or(instruction[7:10],instruction[10:13],instruction[13:16])
    elif instruction[0:5]=="01100":
        pc=And(instruction[7:10],instruction[10:13],instruction[13:16])
    elif instruction[0:5]=="00010":
        pc=movImm(instruction[6:9],instruction[9:16])
    elif instruction[0:5]=="01000":
        pc=rs(instruction[6:9],instruction[9:16])
    elif instruction[0:5]=="01001":
        pc=ls(instruction[6:9],instruction[9:16])
    elif instruction[0:5]=="00011":
        pc=movreg(instruction[10:13],instruction[13:16])
    elif instruction[0:5]=="01101":
        pc=invert(instruction[10:13],instruction[13:16])
    elif instruction[0:5]=="01110":
        pc=compare(instruction[10:13],instruction[13:16])
    elif instruction[0:5]=="00100":
        pc=load(instruction[6:9],instruction[9:16])
    elif instruction[0:5]=="00101":
        pc=store(instruction[6:9],instruction[9:16])
    elif instruction[0:5]=="01111":
        pc=jmp(instruction[9:16])
    elif instruction[0:5]=="11100":
        pc=jlt(instruction[9:16])
    elif instruction[0:5]=="11101":
        pc=jgt(instruction[9:16])
    elif instruction[0:5]=="11111":
        pc=je(instruction[9:16])
    elif instruction[0:5]=="11010":
        flags_value="0"*16
        Reg_value[instruct.registers["FLAGS"]]=flags_value
        json_dict=dict()
        json_dict["binary"]=binary
        json_dict={"binary":binary,"error":[]}
        with open("memory.json","w") as memory:
            json.dump(json_dict,memory)
        return "Halt"
    if pc==-1:
        return "normal"
    else:
        return pc
    
