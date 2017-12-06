from django import template
from users.models import FamilyRelationship
register = template.Library()

@register.filter(name="isadmin")
def is_admin(user):
    print(user.pk)
    print(user.hasGroup("admin"))
    return user.hasGroup("admin")

@register.filter(name="isprofessor")
def is_professor(user):
    return user.hasGroup("professor")

@register.filter(name="isstudent")
def is_student(user):
    return user.hasGroup("student")

@register.filter(name="invitation")
def invitation(user, family):
    if FamilyRelationship.objects.get(user_id=user.pk, family_id=family.pk).status == FamilyRelationship.STATUS_CHOICES[1][0]:
        return True
    return False

@register.filter(name="invitationid")
def invitationid(user, family):
    return FamilyRelationship.objects.get(user_id=user.pk, family_id=family.pk).pk
