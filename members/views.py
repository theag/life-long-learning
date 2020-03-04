from django.shortcuts import render, redirect
from .models import Member, MemberForm

def index(request):
    context = {}
    try:
        action = request.POST['action']
        if action == 'delete':
            Member.objects.get(pk=request.POST['member_id']).delete()
    except KeyError:
        pass
    context['members'] = Member.objects.all()
    return render(request, 'members/index.html', context)

def add(request):
    if request.POST:
        m = MemberForm(request.POST)
        m.save()
        return redirect('members:index')
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