import InstructionDictionary as instruct

dict_opcode=instruct.opcodes
dict_register=instruct.registers

list_error=[]

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

