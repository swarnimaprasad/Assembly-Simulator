import InstructionDictionary as instruct
import sys,json
dict_opcode=instruct.opcodes
dict_register=instruct.registers

list_error=[]

def a_chk_instruction_reg_name(type, input):
    if type == "instruction":
        if input not in ["add", "sub", "mov", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt"]:
            list_error.append("Syntax Error: Invalid instruction name")
            return True
    elif type == "register":
        if input not in ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "FLAGS"]:
            list_error.append("Syntax Error: Invalid register name")
            return True
    return False

def b_chkvariable(input, listofvariables):
    if input not in listofvariables:
        list_error.append("Syntax Error: Undefined variable used")
        return True
    return False

def c_chklabels(input, listoflabels):
    if input not in listoflabels:
        list_error.append("Syntax Error: Undefined register used")
        return True
    return False

def d_chkflags(input_start,input_var):
    for i in input_start:
        if "FLAGS" in i and "mov" not in i:
            list_error.append("Syntax Error: Illegal use of FLAGS register")
            list_error.append(input_start.index(i)-len(input_var))
            return True
        elif "FLAGS" in i and "mov" in i:
            if i.index("FLAGS")!=i.index("mov")+2:
                list_error.append("Syntax Error: Illegal use of FLAGS register")
                list_error.append(input_start.index(i)-len(input_var))
                return True
    return False
    
def e_chkimmediate(immediate):
    if int(float(immediate[1:]))!=float(immediate[1:]):
        list_error.append("Syntax Error: Immediate value is float")
        return True
    if not (0 <= int(immediate[1:]) <= 127):
        list_error.append("Syntax Error: Illegal immediate value (not between 0 and 127)")
        return True
    return False

def f_chklabel_mis(input,list_label):
    if not(input.isnumeric()):
        if input not in list_label:
            list_error.append("Syntax Error: Label not found")
            return True
    return False

def f_chkvar_label(input, listoflabels, listofvariables):
    if not(input.isnumeric()):
        if input in listoflabels and input not in listofvariables:
            list_error.append("Syntax Error: Label cannot be used as variable")
            return True
    return False

def f_chklabel_var(input, listoflabels, listofvariables):
    if not(input.isnumeric()):
        if input not in listoflabels and input in listofvariables:
            list_error.append("Syntax Error: variable cannot be used as label")
            return True
    return False

def g_chkvariable_dec(input_start,input_var):
    check=1
    for i in input_start:
        if i==[]:
            return False
        if i[0]=="var" and check==1:
            check=1
        elif i[0]!="var" and check==1:
            check =0
        elif i[0]=="var" and check==0:
            list_error.append("Syntax Error: Variable not defined at start")
            list_error.append(input_start.index(i)-len(input_var))
            return True
        elif i[0]!="var" and check==0:
            pass
    return False

def h_chkhlt(instruction, pc, last):
    if instruction == "hlt" and pc != last:
        list_error.append("Syntax Error: Halt instruction not at the end of program")
        return True
    return False

def i_chkhlt_mis(input_start,input_var):
    line_error=0
    for i in input_start:
        if "hlt" in i:
            line_error=i
            return False
    list_error.append("Syntax Error: Halt instruction not found in the program")
    list_error.append(input_start.index(i)-len(input_var))
    return True

def call_list(dict_instruc,i,list_print,list_var,list_labels,dict_instuc_main):
    if dict_instruc[i]==[]:
        return 0
    if a_chk_instruction_reg_name("instruction",dict_instruc[i][0]):
        return 1
    if dict_instruc[i][0]=="add":
        if len(dict_instruc[i])>4:
            raise 
        if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or a_chk_instruction_reg_name("register",dict_instruc[i][2]) or a_chk_instruction_reg_name("register",dict_instruc[i][3]):
            return 1
        list_print.append(addition(dict_instruc[i][1],dict_instruc[i][2],dict_instruc[i][3],dict_opcode,dict_register))
    elif dict_instruc[i][0]=="sub":
        if len(dict_instruc[i])>4:
            raise 
        if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or a_chk_instruction_reg_name("register",dict_instruc[i][2]) or a_chk_instruction_reg_name("register",dict_instruc[i][3]):
            return 1
        list_print.append(subtraction(dict_instruc[i][1],dict_instruc[i][2],dict_instruc[i][3],dict_opcode,dict_register))
    elif dict_instruc[i][0]=="mov":
        if len(dict_instruc[i])>3:
            raise 
        if "$" in dict_instruc[i][2]:
            if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or e_chkimmediate(dict_instruc[i][2]):
                return 1
            list_print.append(moveimm(dict_instruc[i][1],dict_instruc[i][2],dict_opcode,dict_register))
        else:
            if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or a_chk_instruction_reg_name("register",dict_instruc[i][2]):
                return 1
            list_print.append(movereg(dict_instruc[i][1],dict_instruc[i][2],dict_opcode,dict_register))
    elif dict_instruc[i][0]=="ld":
        if len(dict_instruc[i])>3:
            raise 
        if f_chkvar_label(dict_instruc[i][2], list_labels, list_var):
            return 1
        if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or b_chkvariable(dict_instruc[i][2],list_var):
                return 1
        list_print.append(load(dict_instruc[i][1],dict_instruc[i][2],dict_opcode,dict_register,dict_var))
    elif dict_instruc[i][0]=="st":
        if len(dict_instruc[i])>3:
            raise 
        if f_chkvar_label(dict_instruc[i][2], list_labels, list_var):
            return 1
        if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or b_chkvariable(dict_instruc[i][2],list_var):
                return 1
        list_print.append(store(dict_instruc[i][1],dict_instruc[i][2],dict_opcode,dict_register,dict_var))
    elif dict_instruc[i][0]=="mul":
        if len(dict_instruc[i])>4:
            raise 
        if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or a_chk_instruction_reg_name("register",dict_instruc[i][2]) or a_chk_instruction_reg_name("register",dict_instruc[i][3]):
            return 1
        list_print.append(multiplaction(dict_instruc[i][1],dict_instruc[i][2],dict_instruc[i][3],dict_opcode,dict_register))
    elif dict_instruc[i][0]=="div":
        if len(dict_instruc[i])>3:
            raise 
        if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or a_chk_instruction_reg_name("register",dict_instruc[i][2]):
            return 1
        list_print.append(division(dict_instruc[i][1],dict_instruc[i][2],dict_opcode,dict_register))
    elif dict_instruc[i][0]=="rs":
        if len(dict_instruc[i])>3:
            raise 
        if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or e_chkimmediate(dict_instruc[i][2]):
            return 1
        list_print.append(right_shift(dict_instruc[i][1],dict_instruc[i][2],dict_opcode,dict_register))
    elif dict_instruc[i][0]=="ls":
        if len(dict_instruc[i])>3:
            raise 
        if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or e_chkimmediate(dict_instruc[i][2]):
            return 1
        list_print.append(left_shift(dict_instruc[i][1],dict_instruc[i][2],dict_opcode,dict_register))
    elif dict_instruc[i][0]=="xor":
        if len(dict_instruc[i])>4:
            raise 
        if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or a_chk_instruction_reg_name("register",dict_instruc[i][2]) or a_chk_instruction_reg_name("register",dict_instruc[i][3]):
            return 1
        list_print.append(xor(dict_instruc[i][1],dict_instruc[i][2],dict_instruc[i][3],dict_opcode,dict_register))
    elif dict_instruc[i][0]=="or":
        if len(dict_instruc[i])>4:
            raise 
        if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or a_chk_instruction_reg_name("register",dict_instruc[i][2]) or a_chk_instruction_reg_name("register",dict_instruc[i][3]):
            return 1
        list_print.append(Or(dict_instruc[i][1],dict_instruc[i][2],dict_instruc[i][3],dict_opcode,dict_register))
    elif dict_instruc[i][0]=="and":
        if len(dict_instruc[i])>4:
            raise 
        if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or a_chk_instruction_reg_name("register",dict_instruc[i][2]) or a_chk_instruction_reg_name("register",dict_instruc[i][3]):
            return 1
        list_print.append(And(dict_instruc[i][1],dict_instruc[i][2],dict_instruc[i][3],dict_opcode,dict_register))
    elif dict_instruc[i][0]=="not":
        if len(dict_instruc[i])>3:
            raise 
        if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or a_chk_instruction_reg_name("register",dict_instruc[i][2]):
            return 1
        list_print.append(invert(dict_instruc[i][1],dict_instruc[i][2],dict_opcode,dict_register))
    elif dict_instruc[i][0]=="cmp":
        if len(dict_instruc[i])>3:
            raise 
        if a_chk_instruction_reg_name("register",dict_instruc[i][1]) or a_chk_instruction_reg_name("register",dict_instruc[i][2]):
            return 1
        list_print.append(compare(dict_instruc[i][1],dict_instruc[i][2],dict_opcode,dict_register))
    elif dict_instruc[i][0]=="jmp":
        if len(dict_instruc[i])>2:
            raise 
        if f_chklabel_var(dict_instruc[i][1], list_labels, list_var,):
            return 1
        if f_chklabel_mis(dict_instruc[i][1],list_labels):
            return 1
        list_print.append(jmp(dict_instruc[i][1],dict_opcode,dict_instruc,dict_instuc_main))
    elif dict_instruc[i][0]=="jlt":
        if len(dict_instruc[i])>2:
            raise 
        if f_chklabel_var(dict_instruc[i][1], list_labels, list_var):
            return 1
        if f_chklabel_mis(dict_instruc[i][1],list_labels):
            return 1
        list_print.append(jlt(dict_instruc[i][1],dict_opcode,dict_instruc,dict_instuc_main))
    elif dict_instruc[i][0]=="jgt":
        if len(dict_instruc[i])>2:
            raise 
        if f_chklabel_var(dict_instruc[i][1], list_labels, list_var):
            return 1
        if f_chklabel_mis(dict_instruc[i][1],list_labels):
            return 1
        list_print.append(jgt(dict_instruc[i][1],dict_opcode,dict_instruc,dict_instuc_main))
    elif dict_instruc[i][0]=="je":
        if len(dict_instruc[i])>2:
            raise 
        if f_chklabel_var(dict_instruc[i][1], list_labels, list_var):
            return 1
        if f_chklabel_mis(dict_instruc[i][1],list_labels):
            return 1
        list_print.append(je(dict_instruc[i][1],dict_opcode,dict_instruc,dict_instuc_main))
    elif dict_instruc[i][0]=="hlt":
        if len(dict_instruc[i])>1:
            raise 
        if h_chkhlt("hlt",i,list(dict_instruc.keys())[-1]):
            return 1
        list_print.append(halt(dict_opcode))
    return 0

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

try:
    list_error=[]

    input_start=sys.stdin.readlines()

    for i in range(len(input_start)):
        if "/n" in input_start[i]:
            input_start[i]=input_start[i][:-1]
        input_start[i]=list(input_start[i].split())
    dict_instruc=dict()
    dict_var=dict()
    list_var=[]
    list_labels=[]
    counter=0
    for i in input_start:
        if i==[]:
            counter+=1
            continue
        if i[0]!="var":
            temp=bin(counter)[2:]
            temp="0"*(7-len(temp))+temp
            if ":" in i[0]:
                dict_instruc[temp]={i[0][:-1]:list(i[1:])}
                list_labels.append(i[0][:-1])
                counter+=1
            else:
                dict_instruc[temp]=i
                counter+=1
    for i in input_start:
        if i==[]:
            counter+=1
            continue
        if i[0]=="var":
            temp=bin(counter)[2:]
            temp="0"*(7-len(temp))+temp
            dict_var[temp]=i[1]
            list_var.append(i[1])
            counter+=1
    list_print=[]
    error=0
    for j in range(len(list_var)):
        for i in range(j+1,len(list_var)):
            if list_var[i]==list_var[j]:
                list_error.append("Variable defined twice")
                list_error.append(i-len(list_var))
                error=1
                break
        if error==1:
            break
    list_label_2=[]
    if error!=1:
        for i in dict_instruc:
            if type(dict_instruc[i])==dict:
                list_label_2.append([i,list(dict_instruc[i].keys())[0]])
        for i in range(len(list_label_2)):
            for j in range(i+1,len(list_label_2)):
                if list_label_2[i][1]==list_label_2[j][1]:
                    list_error.append("Label defined twice")
                    list_error.append(j)
                    error=1
                    break

    if error!=1:
        if(g_chkvariable_dec(input_start,list_var) or d_chkflags(input_start,list_var) or i_chkhlt_mis(input_start,list_var)):
            error=1

    if error!=1:
        for i in dict_instruc:
            if type(dict_instruc[i])==list:
                if call_list(dict_instruc,i,list_print,list_var,list_labels,dict_instruc)==1:
                    list_error.append(i)
                    error=1
                    break
            elif type(dict_instruc[i])==dict:
                for j in dict_instruc[i]:
                    if call_list(dict_instruc[i],j,list_print,list_var,list_labels,dict_instruc)==1:
                        list_error.append(i)
                        error=1
                        break
    if error==1:
        if type(list_error[1])!=int:
            sys.stdout.write("Error generated at line number: "+str(int("0b"+list_error[1],2)+len(list_var)+1)+"\n"+list_error[0]+"\n")
        else:
            sys.stdout.write("Error generated at line number: "+str(list_error[1]+len(list_var)+1)+"\n"+list_error[0]+"\n")
    else:
        if len(list_print)>128:
            list_error.append("Program length exceeded 128 lines.\n")
            sys.stdout.write("Program length exceeded 128 lines."+"\n")
        else:
            for i in list_print:
                sys.stdout.write(i+"\n")
            if(len(list_print)<128):
                while(len(list_print)!=128):
                    list_print.append("0"*16)
except :
    sys.stdout.write("Syntax Error: General Syntax Error at line: "+str(int("0b"+str(i),2)+len(list_var)+1)+"\n")
    list_error.append("Syntax Error: General Syntax Error at line: "+str(int("0b"+str(i),2)+len(list_var)+1)+"\n")
json_dict={"binary":list_print,"error":list_error}
with open("memory.json","w") as memory:
    json.dump(json_dict,memory)
