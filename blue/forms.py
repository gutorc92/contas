from django.forms import ModelForm,DateInput
from .models import Category, Statement,StatementType

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['description']

class StatementTypeForm(ModelForm):
    
    class Meta:
        model = StatementType
        fields = "__all__"

class StatementForm(ModelForm):
    class Meta:
        model = Statement
        fields = ['description','value','date','categories','st_type']
        widgets = {
            'date': DateInput(format = ['%d/%m/%y']),
        }
