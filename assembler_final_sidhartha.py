import InstructionDictionary as instruct

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
