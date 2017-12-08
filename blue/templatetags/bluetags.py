from django import template
from users.models import FamilyRelationship
from blue.models import StatementType
register = template.Library()

@register.filter(name="stformat")
def stformat(st):
    if st.st_type == StatementType.objects.get(description='Outcome'):
        return "list-group-item-danger"
    elif st.st_type == StatementType.objects.get(description='Income'):
        return "list-group-item-success"
    else:
        return ""

@register.filter(name="vlformat")
def stformat(value):
   return "R$ " + str(value)
