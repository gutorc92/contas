from django.db import models

# Create your models here.
class Category(models.Model):
    description = models.CharField(max_length=200,help_text='testando')

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
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    st_type = models.ForeignKey(StatementType,related_name="statements", on_delete=models.CASCADE)


    
