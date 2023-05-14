import InstructionDictionary as instruct

dict_opcode=instruct.opcodes
dict_register=instruct.registers


def addition(reg1, reg2 ,reg3,dict_opcode,dict_register):
    opcode=dict_opcode["add"]
    reg1=dict_register[reg1]
    reg2=dict_register[reg2]
    reg3=dict_register[reg3]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(reg2)-len(reg3))+reg1+reg2+reg3
    return binary

def subtraction(reg1, reg2 ,reg3,dict_opcode,dict_register):
    opcode=dict_opcode["sub"]
    reg1=dict_register[reg1]
    reg2=dict_register[reg2]
    reg3=dict_register[reg3]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(reg2)-len(reg3))+reg1+reg2+reg3
    return binary

def moveimm(reg1,Imm,dict_opcode,dict_register):
    opcode=dict_opcode["mov"][0]
    reg1=dict_register[reg1]
    Imm=bin(int(Imm[1:]))[2:]
    Imm="0"*(7-len(Imm))+Imm    
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(Imm))+reg1+Imm
    return binary

def movereg(reg1,reg2,dict_opcode,dict_register):
    opcode=dict_opcode["mov"][1]
    reg1=dict_register[reg1]
    reg2=dict_register[reg2]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(reg2))+reg1+reg2
    return binary

def load(reg1,memory_addr,dict_opcode,dict_register,dict_var):
    if memory_addr.isnumeric()!=True:
        for i in dict_var:
            if dict_var[i]==memory_addr:
                memory_addr=i
    opcode=dict_opcode["ld"]
    reg1=dict_register[reg1]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(memory_addr))+reg1+memory_addr
    return binary

def store(reg1,memory_addr,dict_opcode,dict_register,dict_var):
    if memory_addr.isnumeric()!=True:
        for i in dict_var:
            if dict_var[i]==memory_addr:
                memory_addr=i
    opcode=dict_opcode["st"]
    reg1=dict_register[reg1]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(memory_addr))+reg1+memory_addr
    return binary

def multiplaction(reg1, reg2 ,reg3,dict_opcode,dict_register):
    opcode=dict_opcode["mul"]
    reg1=dict_register[reg1]
    reg2=dict_register[reg2]
    reg3=dict_register[reg3]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(reg2)-len(reg3))+reg1+reg2+reg3
    return binary

def division(reg1, reg2 ,dict_opcode,dict_register):
    
    opcode=dict_opcode["div"]
    reg1=dict_register[reg1]
    reg2=dict_register[reg2]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(reg2))+reg1+reg2
    return binary

def right_shift(reg1,Imm,dict_opcode,dict_register):
    opcode=dict_opcode["rs"][0]
    Imm=bin(int(Imm[1:]))[2:]
    Imm="0"*(7-len(Imm))+Imm  
    reg1=dict_register[reg1]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(Imm))+reg1+Imm
    return binary

def left_shift(reg1,Imm,dict_opcode,dict_register):
    opcode=dict_opcode["ls"][0]
    Imm=bin(int(Imm[1:]))[2:]
    Imm="0"*(7-len(Imm))+Imm  
    reg1=dict_register[reg1]
    binary=opcode+"0"*(16-len(opcode)-len(reg1)-len(Imm))+reg1+Imm
    return binary
