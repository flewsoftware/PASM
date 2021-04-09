from enum import Enum


class Opcodes(Enum):
    HLT = '00'
    LOAD = '01'
    ADD = '02'
    SUB = '03'
    DIV = '04'
    JMP = '05'
    RJMP = '06'
    JMPTL = '07'
    VMCALL = '08'
    EQ = '09'
    JEQ = '0A'
    NEQ = '0B'
    JNEQ = '0C'
    SWP = '0D'
    AND = '0E'
    OR = '0F'
    NOT = '10'
    GET = '11'
    LOCKR = '12'
    IGl = 'igl'


def get_opcode(opcode: str) -> Opcodes:
    return Opcodes[opcode.upper()]
