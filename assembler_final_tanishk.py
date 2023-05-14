import InstructionDictionary as instruct

dict_opcode=instruct.opcodes
dict_register=instruct.registers

def xor(reg1, reg2 ,reg3,dict_opcode,dict_register):
    opcode=dict_opcode["xor"]
    reg1=dict_register[reg1]
    reg2=dict_register[reg2]
    reg3=dict_register[reg3]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(reg2)-len(reg3))+reg1+reg2+reg3
    return binary

def Or(reg1, reg2 ,reg3,dict_opcode,dict_register):
    opcode=dict_opcode["or"]
    reg1=dict_register[reg1]
    reg2=dict_register[reg2]
    reg3=dict_register[reg3]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(reg2)-len(reg3))+reg1+reg2+reg3
    return binary

def And(reg1, reg2 ,reg3,dict_opcode,dict_register):
    opcode=dict_opcode["and"]
    reg1=dict_register[reg1]
    reg2=dict_register[reg2]
    reg3=dict_register[reg3]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(reg2)-len(reg3))+reg1+reg2+reg3
    return binary

def invert(reg1,reg2,dict_opcode,dict_register):
    opcode=dict_opcode["not"]
    reg1=dict_register[reg1]
    reg2=dict_register[reg2]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(reg2))+reg1+reg2
    return binary

def compare(reg1,reg2,dict_opcode,dict_register):
    opcode=dict_opcode["cmp"]
    reg1=dict_register[reg1]
    reg2=dict_register[reg2]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(reg2))+reg1+reg2
    return binary

def jmp(memory_addr,dict_opcode,dict_instruc,dict_instuc_main):
    opcode=dict_opcode["jmp"]
    if memory_addr.isnumeric()!=True:
        for i in dict_instuc_main:
            if type(dict_instuc_main[i])==dict:
                if memory_addr in dict_instuc_main[i].keys():
                    memory_addr=i
    binary=opcode+"0"*(16-len(opcode)-len(memory_addr))+memory_addr
    return binary

def jlt(memory_addr,dict_opcode,dict_instruc,dict_instuc_main):
    opcode=dict_opcode["jlt"]
    if memory_addr.isnumeric()!=True:
        for i in dict_instuc_main:
            if type(dict_instuc_main[i])==dict:
                if memory_addr in dict_instuc_main[i].keys():
                    memory_addr=i
    binary=opcode+"0"*(16-len(opcode)-len(memory_addr))+memory_addr
    return binary

def jgt(memory_addr,dict_opcode,dict_instruc,dict_instuc_main):
    opcode=dict_opcode["jgt"]
    if memory_addr.isnumeric()!=True:
        for i in dict_instuc_main:
            if type(dict_instuc_main[i])==dict:
                if memory_addr in dict_instuc_main[i].keys():
                    memory_addr=i
    binary=opcode+"0"*(16-len(opcode)-len(memory_addr))+memory_addr
    return binary

def je(memory_addr,dict_opcode,dict_instruc,dict_instuc_main):
    opcode=dict_opcode["je"]
    if memory_addr.isnumeric()!=True:
        for i in dict_instuc_main:
            if type(dict_instuc_main[i])==dict:
                if memory_addr in dict_instuc_main[i].keys():
                    memory_addr=i
    binary=opcode+"0"*(16-len(opcode)-len(memory_addr))+memory_addr
    return binary

def halt(dict_opcode):
    opcode=dict_opcode["hlt"]
    binary=opcode+"0"*(16-len(opcode))
    return binary
