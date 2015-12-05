from django import forms
import re

from problems.models import Problem, Test

class CodeForm(forms.Form):
    problem_slug = forms.CharField(label="Problem", widget=forms.HiddenInput)
    user_name = forms.CharField(label='Name', max_length=30)
    code = forms.CharField(label='Code', widget=forms.Textarea)

    def clean_code(self):
        code = self.cleaned_data['code']
        problem = Problem.objects.get(name_slug=self.cleaned_data['problem_slug'])
        tests = problem.test_set.all()
        
        # NOTES:
        # '*' is used to represent an empty spot in memory.
        # It is assumed that DEFINE statements occur at the end of the solution.
        
        VALID_COMMANDS = ['INBOX', 'OUTBOX', 'JUMP', 'JUMPZ', 'JUMPN', 'COPYTO',
                          'COPYFROM', 'BUMPUP', 'BUMPDN', 'ADD', 'SUB']
        LETTERS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
                    'p','q','r','s','t','u','v','w','x','y','z']
        LBL_PTRN = re.compile('[a-zA-Z]+:')
        INIT_MEMORY = problem.init_memory.split()
        PARSED_CODE = []
        LABELS = {}

        # attempt to parse code
        try:
            for line in code.split('\n'):
                line = line.split()
                # ignore empty lines
                if not line:
                    continue
                if line[0] in VALID_COMMANDS:
                    PARSED_CODE.append(line)
                elif LBL_PTRN.match(line[0]):
                    lbl = line[0][:-1]
                    if lbl in LABELS.keys():
                        raise forms.ValidationError("Failed to parse code: Invalid jump label.")
                    LABELS[lbl] = len(PARSED_CODE)
                elif line[0] == 'DEFINE':
                    break
        except forms.ValidationError as e:
            raise e
        except:
            raise forms.forms.ValidationError("Failed to parse code.")

        # run code
        total_steps = 0
        for test in tests:
            inbox = test.inbox.split()
            outbox = []
            memory = INIT_MEMORY
            hands = '*'
            code_pointer = 0
            steps = 0

            try:
                # step through the code
                while code_pointer < len(PARSED_CODE) and steps <= 5000:
                    # increment speed counter
                    steps += 1
                    # get the line to process
                    line = PARSED_CODE[code_pointer]

                    if line[0] == 'INBOX':
                        if len(inbox) == 0:
                            break
                        hands = inbox.pop(0)
                        if hands not in LETTERS:
                            hands = int(hands)

                    elif line[0] == 'OUTBOX':
                        if hands == '*':
                            raise forms.ValidationError("Code Crashed: Cannot outbox nothing.")
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
                            raise forms.ValidationError("Code Crashed: Cannot copy nothing.")
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
                            raise forms.ValidationError("Code Crashed: Cannot copy nothing.")
                        hands = memory[j]

                    elif line[0] == 'BUMPUP':
                        if line[1][0] == '[':
                            i = int(line[1][1:-1])
                            j = memory[i]
                        else:
                            j = int(line[1])
                        memory[j] += 1
                        if memory[j] > 999:
                            raise forms.ValidationError("Code Crashed: Value too large.")
                        hands = memory[j]

                    elif line[0] == 'BUMPDN':
                        if line[1][0] == '[':
                            i = int(line[1][1:-1])
                            j = memory[i]
                        else:
                            j = int(line[1])
                        memory[j] -= 1
                        if memory[j] < -999:
                            raise forms.ValidationError("Code Crashed: Value too small.")
                        hands = memory[j]

                    elif line[0] == 'ADD':
                        if line[1][0] == '[':
                            i = int(line[1][1:-1])
                            j = memory[i]
                        else:
                            j = int(line[1])
                        if hands == '*' or memory[j] == '*':
                            raise forms.ValidationError("Code Crashed: Cannot add with empty value.")
                        if hands in LETTERS or memory[j] in LETTERS:
                            raise forms.ValidationError("Code Crashed: Cannot add with letters.")
                        hands += memory[j]
                        if hands < -999:
                            raise forms.ValidationError("Code Crashed: Value too small.")
                        if hands > 999:
                            raise forms.ValidationError("Code Crashed: Value too large.")

                    elif line[0] == 'SUB':
                        if line[1][0] == '[':
                            i = int(line[1][1:-1])
                            j = memory[i]
                        else:
                            j = int(line[1])
                        if hands == '*' or memory[j] == '*':
                            raise forms.ValidationError("Code Crashed: Cannot add with empty value.") 
                        elif hands in LETTERS and memory[j] in LETTERS:
                            hands = LETTERS.index(hands) - LETTERS.index(memory[j])
                        elif hands in LETTERS or memory[j] in LETTERS:
                            raise forms.ValidationError("Code Crashed: Cannot subtract with mixed types.")
                        else:
                            hands -= memory[j]
                        if hands < -999:
                            raise forms.ValidationError("Code Crashed: Value too small.")
                        if hands > 999:
                            raise forms.ValidationError("Code Crashed: Value too large.")

                    code_pointer += 1
            except forms.ValidationError as e:
                raise e
            except:
                raise forms.ValidationError("Code Crashed.")

            # check for too slow solutions
            if steps > 5000:
                raise forms.ValidationError("Solution takes more than 5000 steps.")

            # check if output is valid
            if outbox == test.outbox.split():
                total_steps += steps
                continue
            raise forms.ValidationError("Solution produced wrong output.")

        # code has passed all cases
        self.cleaned_data['speed'] = int(total_steps/len(tests))
        self.cleaned_data['size'] = len(PARSED_CODE)

        return code
