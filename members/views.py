from django.shortcuts import render, redirect
from .models import Member, MemberForm, Year, Course, CourseForm, Class, ClassForm, Location
import datetime

def do_year_check():
    now = datetime.datetime.now()
    y = Year.objects.get(value=now.year)
    if not y:
        y = Year(value=now.year)
        y.save()

def index(request):
    do_year_check()
    context = {'years':Year.objects.all(),'members':Member.objects.all()}
    try:
        action = request.POST['action']
        if action == 'delete':
            Member.objects.get(pk=request.POST['member_id']).delete()
        elif action == "search":
            if len(request.POST['name']) != 0:
                context['members'] = context['members'].filter(first_name__contains=request.POST['name']).union(context['members'].filter(last_name__contains=request.POST['name']))
            if int(request.POST['membership_year']) != -1:
                context['members'] = context['members'].filter(membership_years__pk=request.POST['membership_year'])
            context['name'] = request.POST['name']
            context['membership_year'] = int(request.POST['membership_year'])
    except KeyError:
        pass
    context['members'] = context['members'].order_by('last_name','first_name')
    return render(request, 'members/index.html', context)

def add(request):
    if request.POST:
        m = MemberForm(request.POST)
        if m.is_valid():
            m.save()
            return redirect('members:index')
        else:
            context = {'form':m, 'add':'add', 'header':'Add New Member'}
        return render(request, 'members/edit.html', context)
    else:
        context = {'form':MemberForm(), 'add':'add', 'header':'Add New Member'}
        return render(request, 'members/edit.html', context)
        
def edit(request, member_id):
    m = Member.objects.get(pk=member_id)
    if request.POST:
        mf = MemberForm(request.POST, instance=m)
        if mf.is_valid():
            mf.save()
            return redirect('members:index')
        else:
            context = {'form':mf, 'header':'Edit Member'}
            return render(request, 'members/edit.html', context)
    else:
        context = {'form':MemberForm(instance=m), 'header':'Edit Member'}
        return render(request, 'members/edit.html', context)
#courses
def courses(request):
    do_year_check()
    context = {'years':Year.objects.all(),
        'courses':Course.objects.all(),
        'members':Member.objects.all(),
        'semesters':Class.SEMESTER_CHOICES,
        'locations':Location.objects.all()}
    try:
        action = request.POST['action']
        if action == 'delete':
            Course.objects.get(pk=request.POST['course_id']).delete()
        elif action == "search":
            if len(request.POST['name']) != 0:
                context['courses'] = context['courses'].filter(name__contains=request.POST['name'])
            if int(request.POST['year']) != -1:
                context['courses'] = context['courses'].filter(class__year__pk=int(request.POST['year']))
            if int(request.POST['instructor']) != -1:
                context['courses'] = context['courses'].filter(class__instructor__pk=int(request.POST['instructor']))
            if int(request.POST['semester']) != -1:
                context['courses'] = context['courses'].filter(class__semester=int(request.POST['semester']))
            if int(request.POST['location']) != -1:
                context['courses'] = context['courses'].filter(class__location__pk=int(request.POST['location']))
            context['name'] = request.POST['name']
            context['year'] = int(request.POST['year'])
            context['instructor'] = int(request.POST['instructor'])
            context['semester'] = int(request.POST['semester'])
            context['location'] = int(request.POST['location'])
    except KeyError:
        pass
    context['courses'] = context['courses'].order_by('name')
    return render(request, 'members/courses.html', context)

def add_course(request):
    if request.POST:
        c = CourseForm(request.POST,prefix='course')
        l = ClassForm(request.POST,prefix='class')
        bad = True
        if c.is_valid():
            if l.is_valid():
                print(l)
                bad = False
                co = c.save()
                cl = l.save(commit=False)
                cl.course = co
                cl.save()
                if request.POST['action'] == 'add+':
                    return redirect('members:edit_course',c.instance.id)
                else:
                    return redirect('members:courses')
        if bad:
            context = {'form':c, 'cform':l, 'add':'add', 'header':'Add New Course'}
            return render(request, 'members/edit_course.html', context)
            
    else:
        context = {'form':CourseForm(prefix='course'), 'cform':ClassForm(prefix='class'), 'add':'add', 'header':'Add New Course'}
        return render(request, 'members/edit_course.html', context)

def edit_course(request, course_id):
    c = Course.objects.get(pk=course_id)
    context = {'header':'Edit Course','coursei':c}
    if request.POST:
        cf = CourseForm(request.POST, instance=c, prefix='course')
        context['form'] = cf
        context['sel_class'] = int(request.POST['sel_class'])
        action = request.POST['action']
        if action.startswith('add'):
            good = True
            if cf.is_valid():
                cf.save()
            else:
                good = False
            if request.POST['sel_class'] == "-1":
                l = ClassForm(request.POST,prefix='class')
                if l.is_valid():
                    cl = l.save(commit=False)
                    cl.course = c
                    cl.save()
                    
                else:
                    good = False
            elif request.POST['sel_class'] != "-2":
                l = ClassForm(request.POST,prefix='class',instance=Class.objects.get(pk=request.POST['sel_class']))
                if l.is_valid():
                    l.save()
                else:
                    good = False
            if good:
                if request.POST['action'] == 'add+':
                    return redirect('members:edit_course',c.id)
                else:
                    return redirect('members:courses')
            else:
                return render(request, 'members/edit_course.html', context)
        elif action == "change":
            if request.POST['sel_class'] == "-1":
                context['cform'] = ClassForm(prefix='class')
            elif request.POST['sel_class'] != "-2":
                context['cform'] = ClassForm(prefix='class',instance=Class.objects.get(pk=request.POST['sel_class']))
        elif action == "delete":
            Class.objects.get(pk=request.POST['sel_class']).delete()
            context['sel_class'] = -2
    else:
        context['form'] = CourseForm(instance=c,prefix='course')
    return render(request, 'members/edit_course.html', context)