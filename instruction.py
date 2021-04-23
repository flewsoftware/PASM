from opcode import Opcodes, get_opcode
from tools import check, get_hex
import binascii
import verify
from enum import Enum

import logging

log = logging.getLogger("logger")
log.setLevel(logging.DEBUG)


class MessageType(Enum):
    InstructionWarning = 0
    InstructionError = 1
    InstructionGood = 3


class Instruction:
    def __init__(self, opcode: Opcodes, arg1: str, arg2: str, arg3: str, special: bool):
        self.opcode = opcode
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.special = special

    def __cverify__(self) -> (MessageType, str):
        if self.opcode == Opcodes.HLT:
            correct_placeholders = verify.is_correct_empty_placeholder(self)
            if correct_placeholders != 0:
                return MessageType.InstructionWarning, 'arg:' + str(correct_placeholders) + \
                    ' 0x1F not used as placeholder for unneeded argument'
        elif self.opcode == Opcodes.LOAD:
            if self.arg1 == '1F' and not self.special:
                return MessageType.InstructionError, 'arg: 1 trying to LOAD value to 0x1F register is illegal'

        return MessageType.InstructionGood, ''

    def __get_compiled__(self):
        return binascii.unhexlify(''.join(str(self.opcode.value))) \
            + binascii.unhexlify(''.join(self.arg1)) \
            + binascii.unhexlify(''.join(self.arg2)) \
            + binascii.unhexlify(''.join(self.arg3))


load_zero_instruction = Instruction(Opcodes.LOAD, '1F', '00', '00', True)


class File:
    def __init__(self, content: str):
        self.content = content
        self.bin = []

    def compile(self) -> (MessageType, str):
        content_lines = self.content.split('\n')
        self.bin.append(get_hex(load_zero_instruction))
        line = 1
        for content_line in content_lines:

            content_line_raw_instruction = content_line.split(' ')
            log.info(content_line_raw_instruction)

            if content_line_raw_instruction[0] == '':
                continue
            elif len(content_line_raw_instruction) < 4:
                log.error("Error: instruction over/under 4 parts line:", line)

            content_line_instruction_opcode = get_opcode(
                content_line_raw_instruction[0])
            content_line_instruction_arg1 = content_line_raw_instruction[1]
            content_line_instruction_arg2 = content_line_raw_instruction[2]
            content_line_instruction_arg3 = content_line_raw_instruction[3]
            temp_instruction = Instruction(content_line_instruction_opcode,
                                           content_line_instruction_arg1,
                                           content_line_instruction_arg2,
                                           content_line_instruction_arg3,
                                           False)

            message_type, message = check(temp_instruction)
            if message_type == MessageType.InstructionError:
                log.error("Error:", message, "Line", line)
                exit(4)
            elif message_type == MessageType.InstructionWarning:
                log.warning("Warning:", message, "Line:", line)
            else:
                log.info("Done Line:", line)
                self.bin.append(get_hex(temp_instruction))
            line = line + 1
