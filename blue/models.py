from django.db import models
from django.contrib.auth import get_user_model
from users.models import Family
# Create your models here.
class Category(models.Model):
    description = models.CharField(max_length=200)
    family = models.ForeignKey(Family, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.description
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'pk':self.pk})

class StatementType(models.Model):
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.description

class Statement(models.Model):
    description = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=20,decimal_places=2)
    date = models.DateField()   
    categories = models.ForeignKey(Category,blank=True, null=True,
            related_name='statements', 
            on_delete=models.SET_NULL)
    st_type = models.ForeignKey(StatementType,blank=True, null=True,
            related_name="statements", 
            on_delete=models.SET_NULL)
    user = models.ForeignKey(get_user_model(),blank=True, null=True,
            related_name="statements", 
            on_delete=models.SET_NULL)


    
