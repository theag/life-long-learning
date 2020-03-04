from django.shortcuts import render, redirect
from .models import Member, MemberForm, Year, Course, CourseForm

def index(request):
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

def courses(request):
    context = {'years':Year.objects.all(),'courses':Course.objects.all(),'members':Member.objects.all()}
    return render(request, 'members/courses.html', context)

def add_course(request):
    if request.POST:
        c = CourseForm(request.POST)
        if c.is_valid():
            c.save()
            if request.POST['action'] == 'add+':
                return redirect('members:edit_course',c.instance.id)
            else:
                return redirect('members:courses')
        else:
            context = {'form':c, 'add':'add', 'header':'Add New Course'}
            return render(request, 'members/edit_course.html', context)
    else:
        context = {'form':CourseForm(), 'add':'add', 'header':'Add New Course'}
        return render(request, 'members/edit_course.html', context)

def edit_course(request, course_id):
    c = Course.objects.get(pk=course_id)
    context = {'header':'Edit Course','members':Member.objects.all().exclude(pk=c.instructor.id).exclude(pk__in=c.students.all()),'students':c.students.all()}
    if request.POST:
        action = request.POST['action']
        if action == 'edit':
            cf = CourseForm(request.POST, instance=c)
            if cf.is_valid():
                cf.save()
                return redirect('members:courses')
            else:
                context['form'] = cf
                return render(request, 'members/edit_course.html', context)
        elif action == 'add':
            c.students.add(Member.objects.get(pk=request.POST['student']))
            c.save()
            context['form'] = CourseForm(request.POST, instance=c)
            return render(request, 'members/edit_course.html', context)
    else:
        context['form'] = CourseForm(instance=c)
        return render(request, 'members/edit_course.html', context)