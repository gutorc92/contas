from django.db import models

# Create your models here.
class Category(models.Model):
    description = models.CharField(max_length=200,help_text='testando')

    def __str__(self):
        return self.description

class StatementType(models.Model):
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.description

class Statement(models.Model):
    description = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=20,decimal_places=2)
    date = models.DateField()   
    categories = models.ManyToManyField(Category)
    st_type = models.ForeignKey(StatementType,related_name="statements")


    
