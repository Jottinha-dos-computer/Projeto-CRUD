from django import forms
from .models import ToDo

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['task_name', 'task_start', 'task_end']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task_start'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date',
                'placeholder':
                'yyyy-mm-dd',
                'class': 'form-control'
            }
        )
        self.fields['task_end'].widget =  forms.widgets.DateInput(
            attrs={
                'type': 'date',
                'placeholder':
                'yyyy-mm-dd',
                'class': 'form-control'
            }
        )
        
class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=100)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
