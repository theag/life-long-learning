from django.db import models
from django import forms
from django.core.validators import RegexValidator

class Location(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
        
class Year(models.Model):
    class Meta:
        ordering = ['-value']
    value = models.PositiveSmallIntegerField()
    def __str__(self):
        return "{}".format(self.value)

class Member(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12,validators=[RegexValidator(regex='^\d{3}-\d{3}-\d{4}$',message="Phone number must be of the form XXX-XXX-XXXX")])
    membership_years = models.ManyToManyField('Year')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return "{}, {}".format(self.last_name,self.first_name)
    
    def membership_years_display(self):
        rv = ''
        for y in self.membership_years.all().order_by('value'):
            if len(rv) > 0:
                rv += ', '
            rv += "{}".format(y)
        return rv
        
    def is_instructor(self):
        if len(self.taught.all()) > 0:
            return "Yes"
        else:
            return "No"

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        widgets = {'membership_years':forms.CheckboxSelectMultiple(choices=[(i,i) for i in range(2010,2021)])}
        
class Course(models.Model):
    name = models.CharField(max_length=200)
    year = models.ForeignKey(Year,on_delete=models.CASCADE)
    instructor = models.ForeignKey(Member,on_delete=models.CASCADE,related_name='taught')
    description = models.TextField(blank=True)
    students = models.ManyToManyField(Member)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name','year','instructor','description']
    