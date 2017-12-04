from django import template

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
