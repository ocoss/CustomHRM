import fileinput
import re

# NOTES ------------------------------------------------------------------------
# '*' is used to represent an empty spot in memory.
# It is assumed that DEFINE statements occur at the end of the solution.


# INIT -------------------------------------------------------------------------
VALID_COMMANDS = ['INBOX', 'OUTBOX', 'JUMP', 'JUMPZ', 'JUMPN', 'COPYTO',
                  'COPYFROM', 'BUMPUP', 'BUMPDN', 'ADD', 'SUB'] #, 'DUMP']
LETTERS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q',
           'r','s','t','u','v','w','x','y','z']
LBL_PTRN = re.compile('[a-zA-Z]+:')
INIT_MEMORY = []
INPUTS = []
OUTPUTS = []
CODE = []
LABELS = {}

# READ FILES -------------------------------------------------------------------
case_num = 0
try:
    for line in fileinput.input():
        line = line.split()
        # ignore empty lines
        if not line:
            continue
        # check for special character
        if line[0] == '$':
            case_num += 1
            continue
        # read in initial memory
        if case_num == 0:
            for item in line:
                if item not in LETTERS and item != '*':
                    item = int(item)
                INIT_MEMORY.append(item)
        # read in inputs
        elif case_num == 1:
            INPUTS.append(line)
        # read in outputs
        elif case_num == 2:
            OUTPUTS.append(line)
        # read in solution code
        else:
            if line[0] in VALID_COMMANDS:
                CODE.append(line)
            elif LBL_PTRN.match(line[0]):
                lbl = line[0][:-1]
                if lbl in LABELS.keys():
                    raise Exception
                LABELS[lbl] = len(CODE)
            elif line[0] == 'DEFINE':
                break
except:
    print("Failed to parse files.")
    if case_num == 0:
        print("initial memory map has a syntax error")
    elif case_num == 1:
        print("inputs have a syntax error")
    elif case_num == 2:
        print("outputs have a syntax error")
    elif case_num == 3:
        print("code has a syntax error")
else:

    # print(INIT_MEMORY)
    # print(INPUTS)
    # print(OUTPUTS)
    # print(CODE)
    # print(LABELS)

# RUN CODE ---------------------------------------------------------------------
    total_steps = 0
    for case_input in INPUTS:
        # reinitialize variables
        inbox = case_input[:]
        outbox = []
        memory = INIT_MEMORY
        hands = '*'
        code_pointer = 0
        steps = 0

        try:
            # step through the code
            while code_pointer < len(CODE) and steps <= 5000:
                # increment speed counter
                steps += 1
                # get the line to process
                line = CODE[code_pointer]

                if line[0] == 'INBOX':
                    if len(inbox) == 0:
                        break
                    hands = inbox.pop(0)
                    if hands not in LETTERS:
                        hands = int(hands)

                elif line[0] == 'OUTBOX':
                    if hands == '*':
                        raise Exception()
                    outbox.append(str(hands))
                    hands = '*'

                elif line[0] == 'JUMP':
                    code_pointer = LABELS[line[1]]
                    continue

                elif line[0] == 'JUMPZ':
                    if hands == 0:
                        code_pointer = LABELS[line[1]]
                        continue

                elif line[0] == 'JUMPN':
                    if hands < 0:
                        code_pointer = LABELS[line[1]]
                        continue

                elif line[0] == 'COPYTO':
                    if hands == '*':
                        raise Exception
                    if line[1][0] == '[':
                        i = int(line[1][1:-1])
                        j = memory[i]
                    else:
                        j = int(line[1])
                    memory[j] = hands

                elif line[0] == 'COPYFROM':
                    if line[1][0] == '[':
                        i = int(line[1][1:-1])
                        j = memory[i]
                    else:
                        j = int(line[1])
                    if memory[j] == '*':
                        raise Exception
                    hands = memory[j]

                elif line[0] == 'BUMPUP':
                    if line[1][0] == '[':
                        i = int(line[1][1:-1])
                        j = memory[i]
                    else:
                        j = int(line[1])
                    memory[j] += 1
                    if memory[j] > 999:
                        raise Exception
                    hands = memory[j]

                elif line[0] == 'BUMPDN':
                    if line[1][0] == '[':
                        i = int(line[1][1:-1])
                        j = memory[i]
                    else:
                        j = int(line[1])
                    memory[j] -= 1
                    if memory[j] < -999:
                        raise Exception
                    hands = memory[j]

                elif line[0] == 'ADD':
                    if line[1][0] == '[':
                        i = int(line[1][1:-1])
                        j = memory[i]
                    else:
                        j = int(line[1])
                    if hands == '*'  or hands in LETTERS or memory[j] == '*' \
                        or memory[j] in LETTERS:
                        raise Exception
                    hands += memory[j]
                    if hands < -999 or hands > 999:
                        raise Exception

                elif line[0] == 'SUB':
                    if line[1][0] == '[':
                        i = int(line[1][1:-1])
                        j = memory[i]
                    else:
                        j = int(line[1])
                    if hands in LETTERS and memory[j] in LETTERS:
                        hands = LETTERS.index(hands) - LETTERS.index(memory[j])
                    elif hands == '*' or hands in LETTERS or memory[j] == '*' \
                         or memory[j] in LETTERS:
                        raise Exception
                    else:
                        hands -= memory[j]
                    if hands < -999 or hands > 999:
                        raise Exception

                # elif line[0] == 'DUMP':
                #     print(memory)

                code_pointer += 1

        except:
            print("Solution crashed.")
            print("Input: {}".format(' '.join(case_input)))
            break
        else:
            if steps > 5000:
                print("Solution took more than 5000 steps.")
                print("Input: {}".format(case_input))
            # validate output
            # print(outbox)
            if outbox == OUTPUTS[0]:
                OUTPUTS.pop(0)
                print("Succeeded in {} steps".format(steps))
                total_steps += steps
                continue
            print("Solution returned wrong output.")
            print("Input: {}".format(' '.join(case_input)))
            break

    else:
        print("Solution passed all cases!\n  Speed:{}\n  Size:{}".format(
                   int(total_steps/len(INPUTS)),len(CODE)))
