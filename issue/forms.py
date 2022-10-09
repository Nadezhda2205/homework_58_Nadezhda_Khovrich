from issue.models import Task
from django.forms import ModelForm, CharField
from django.core.exceptions import ValidationError


def max_length_validator(string):
    if len(string) > 20:
        raise ValidationError('Максимальная длина строки 20 символов')
    return string

def min_length_validator(string):
    if len(string) < 5:
        raise ValidationError('Минимальная длина строки 5 символов')
    return string


class TaskForm(ModelForm):
    summary = CharField(label='Заголовок', validators=(max_length_validator, min_length_validator))
    
    class Meta:
        model = Task
        fields = ['summary', 'description',  'status',  'type']
