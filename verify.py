def is_correct_empty_placeholder(instruction):
    if instruction.arg1 != 'FF':
        return 1
    elif instruction.arg2 != 'FF':
        return 2
    elif instruction.arg3 != 'FF':
        return 3
    else:
        return 0
