from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from users.models import Family
import datetime
import calendar

# Create your models here.
class CategoryManager(models.Manager):

    def filter_by_range(self, pk_user, st_type, month = None, year=None):
        month = month if month is not None else datetime.date.today().month
        year = year if year is not None else datetime.date.today().year
        _, num_days = calendar.monthrange(year, month)
        last_day = datetime.date(year, month, num_days)
        first_day = datetime.date(year, month, 1)
        return self.get_queryset().filter(statements__user__pk=pk_user, 
                statements__st_type_id = st_type,
                statements__date__range=[first_day, last_day])

    def sum_by_range(self, pk_user, st_type, month=None, year=None):
        return self.filter_by_range(pk_user, st_type, month, year).annotate(total=Sum("statements__value"))

class Category(models.Model):
    description = models.CharField(_("description"), max_length=200)
    family = models.ManyToManyField(Family)
    objects = CategoryManager()

    def __str__(self):
        return self.description
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'pk':self.pk})

   
class StatementTypeManager(models.Manager):

    def filter_by_range(self, pk_user, month = None, year=None):
        month = month if month is not None else datetime.date.today().month
        year = year if year is not None else datetime.date.today().year
        _, num_days = calendar.monthrange(year, month)
        last_day = datetime.date(year, month, num_days)
        first_day = datetime.date(year, month, 1)
        return self.get_queryset().filter(statements__user__pk=pk_user, 
                statements__date__range=[first_day, last_day])

    def sum_by_range(self, pk_user, month=None, year=None):
        return self.filter_by_range(pk_user, month, year).annotate(total=Sum("statements__value"))
 
class StatementType(models.Model):
    description = models.CharField(_("description"), max_length=100)

    objects = StatementTypeManager()
    
    def __str__(self):
        return self.description

    def get_color(self):
        if "Outcome" in self.description:
            return "#ff0000"
        elif "Income" in self.description:
            return "#33cc33"
   
        

class Statement(models.Model):
    description = models.CharField(_("Description"), max_length=200)
    value = models.DecimalField(_("Value"), max_digits=20,decimal_places=2)
    date = models.DateField(_("Date"))   
    categories = models.ForeignKey(Category,blank=True, null=True,
            related_name='statements', 
            on_delete=models.SET_NULL)
    st_type = models.ForeignKey(StatementType,blank=True, null=True,
            related_name="statements", 
            on_delete=models.SET_NULL)
    user = models.ForeignKey(get_user_model(),blank=True, null=True,
            related_name="statements", 
            on_delete=models.SET_NULL)

