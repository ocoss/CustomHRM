from django import forms
import re

class CodeForm(forms.Form):
    problem = forms.CharField(label="Problem", widget=forms.HiddenInput)
    user_name = forms.CharField(label='Name', max_length=30)
    code = forms.CharField(label='Code', widget=forms.Textarea)

    def clean_code(self):
        code = self.cleaned_data['code']
        code = code.split('\n')
        # NOTES:
        # '*' is used to represent an empty spot in memory.
        # It is assumed that DEFINE statements occur at the end of the solution.
        
        VALID_COMMANDS = ['INBOX', 'OUTBOX', 'JUMP', 'JUMPZ', 'JUMPN', 'COPYTO',
                          'COPYFROM', 'BUMPUP', 'BUMPDN', 'ADD', 'SUB']
        LETTERS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
                    'p','q','r','s','t','u','v','w','x','y','z']
        LBL_PTRN = re.compile('[a-zA-Z]+:')
        INIT_MEMORY = []
        PARSED_CODE = []
        LABELS = {}

        # attempt to parse code
        try:
            for line in code:
                line = line.split()
                # ignore empty lines
                if not line:
                    continue
                if line[0] in VALID_COMMANDS:
                    PARSED_CODE.append(line)
                elif LBL_PTRN.match(line[0]):
                    lbl = line[0][:-1]
                    if lbl in LABELS.keys():
                        raise Exception
                    LABELS[lbl] = len(CODE)
                elif line[0] == 'DEFINE':
                    break
        except:
            raise forms.ValidationError("Failed to parse code.")

        # run code


        return code
