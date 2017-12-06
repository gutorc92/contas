from django.forms import ModelForm,DateInput, HiddenInput
from django.forms import Select
from .models import Category, Statement,StatementType

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['description']

    def save(self, user):
        category = super(CategoryForm, self).save(commit=False)
        category.save()
        for fa in user.family.all():
            category.family.add(fa)
        category.save()

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
            'st_type': HiddenInput(),
            'categories': Select(),
        }

    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs:
            self.categories = kwargs['initial']['categories'] if 'categories' in kwargs['initial'] else None
        super(StatementForm, self).__init__(*args, **kwargs)
        if self.categories:
            self.fields['categories'].queryset = self.categories

    def save(self, user):
        st = super(StatementForm, self).save(commit=False)
        st.user = user
        st.save()
        return True
