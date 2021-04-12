
import instruction
import sys
import pyparsing


def core(location: str):
    asm_file = open(location)
    content_lines = asm_file.readlines()
    content = ''
    comment_filter = pyparsing.pythonStyleComment.suppress()
    for line in content_lines:
        temp_content = comment_filter.transformString(line)
        if not temp_content.isspace():
            content += comment_filter.transformString(line)
    a = instruction.File(content)
    a.compile()
    f = open(location+'.bin', 'wb')
    for line in a.bin:
        f.write(line)
    f.flush()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    core(sys.argv[1])
