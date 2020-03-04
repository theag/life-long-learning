from django.db import models
from django.forms import ModelForm
from django.core.validators import RegexValidator

class Location(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
        
class Year(models.Model):
    value = models.PositiveSmallIntegerField()

class Member(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12,validators=[RegexValidator(regex='^\d{3}-\d{3}-\d{4}$',message="Phone number must be of the form XXX-XXX-XXXX")])
    membership_years = models.ManyToManyField('Year')
    notes = models.TextField(blank=True)
    
    def membership_years_display(self):
        rv = ''
        for y in self.membership_years.all().order_by(value):
            if len(rv) > 0:
                rv += ', '
            rv += y
        return rv

class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        
#class Course(models.Model):
    