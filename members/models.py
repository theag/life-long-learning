from django.db import models
from django import forms
from django.core.validators import RegexValidator
import re

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
    courses_taken = models.ManyToManyField('Class')
    
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
        if len(self.class_set.all()) > 0:
            return "Yes"
        else:
            return "No"
            
    def is_valid_membership_years(self, str):
        print(str)
        m = re.search('^ *\d{4}( *, *\d{4})* *$',str)
        print(m)
        return m is not None
    
    def set_membership_years(self, str):
        a = str.split(',')
        years = []
        for v in a:
            y = int(v)
            year = Year.objects.get(value=y)
            if year is None:
                year = Year(value=y)
                year.save()
            years.append(year)
        self.membership_years.set(years)
        self.save()

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return name
    
class Class(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    year = models.ForeignKey(Year,on_delete=models.CASCADE)
    FALL = 1
    SPRING = 2
    SEMESTER_CHOICES = [(FALL, 'Fall'), (SPRING, 'Spring')]
    SEMESTER_ABREVIATIONS = {FALL:'FA',SPRING:'SP'}
    semester = models.IntegerField(choices=SEMESTER_CHOICES,default=FALL)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    instructor = models.ForeignKey(Member,on_delete=models.CASCADE)
    student_count = models.IntegerField(default=0)
    
    def when(self):
        return "{} {}".format(self.year, Class.SEMESTER_ABREVIATIONS[self.semester])
    
# FORMS
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ['courses_taken','membership_years']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
    
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['year','semester','location','instructor','student_count']
        widgets = {'year':forms.Select()}