from django import forms

class CodeForm(forms.Form):
    user_name = forms.CharField(label='Name', max_length=30)
    code = forms.CharField(label='Code', widget=forms.Textarea)

    def clean_code(self):
        code = self.cleaned_data['code']
        code = code.split('\n')
        #TODO: run code against test cases

        return code