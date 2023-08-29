from django.shortcuts import render, redirect
from .models import *
from .forms import *
from appauth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.images import ImageFile
from django.http import JsonResponse

# Create your views here.

@login_required(login_url='login')
def index(request):
    context = {}
    return render(request, 'index/index.html', context)

@login_required(login_url='login')
def electoraltable(request):
    query_candidates = Candidate.objects.all()
    context = {
        'candidates':query_candidates
    }
    return render(request, 'index/electoraltable.html', context)

def electoraltable_api(request):
    if request.method == 'POST':
        try:
            check = False
            createVote = VoteTable.objects.create(
                voted_by=request.user,
                role_name=Role.objects.get(role=request.POST.get('selected_role')),
                candidates=Candidate.objects.get(id=int(request.POST.get('candidate')))
            )
            # Add to user to the list to check if (s)he's voted already for a particular role 
            add_voter = VoteCheck.objects.get(
                role=Role.objects.get(role=request.POST.get('selected_role'))
            )
            if not request.user.id in add_voter.voters.all():
                add_voter.voters.add(request.user.id)
                check = True
            return JsonResponse({
                'check':check,
                'response':'Created successfully'
            }, safe=False)
        except:
            return JsonResponse('An error occurred', safe=False)

def get_votecheck(request):
    if request.method == 'GET':
        query_votecheck = VoteCheck.objects.get(role=Role.objects.get(role=request.GET.get('role_name')))
        if request.user in query_votecheck.voters.all():
            return JsonResponse('true', safe=False)
        else:
            return JsonResponse('false', safe=False)

@login_required(login_url='login')
def adminDashboard(request):
    query_candidates = Candidate.objects.all()
    form = CandidateForm
    if request.method == 'POST':
        if not 'remove-candidate' in request.POST:
            form = CandidateForm(request.POST or None, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.bio = UserBio.objects.get(user_id=form.cleaned_data["candidate_name"])

                instance.save()
                return redirect('dashboard')
        else:
            candidate_id = request.POST.get('remove-candidate')
            print(candidate_id)
            candidate = Candidate.objects.get(id=candidate_id)
            candidate.delete()
            return redirect('dashboard')
    context = {
        'dataset':query_candidates,
        'form':form
    }
    return render(request, 'index/dashboard.html', context)

# Remove Candidate
# def remove_all(request):
#     if request.method == "POST":
        # candidate_id = request.POST.get('candidate_id')
        # candidate = Candidate.objects.get(id=candidate_id)
        # candidate.delete()
#         data = {
#             'mssg': 'Removed!'
#         }
#         return JsonResponse(data, safe=False)
#     return redirect(f'dashboard')

def createUser(request, *args, **kwargs):
    if request.method == "POST":
        data = request.POST
        try:
            user = User(
                email=data['email'],
                reg_no=data['registration_number'],
                first_name=data['firstname'],
                last_name=data['lastname']
            )
            user.set_password(data['password'])
            user.save()
            return JsonResponse({'response':f'Account created successfully for {data["registration_number"]}'}, safe=False)
        except:
            return JsonResponse({'negative':'An error occured while trying to create user'}, safe=False)

# @csrf_exempt
def addrole(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        try:
            add_role = Role(
                role=data["role"],
            )
            add_role.save()
            return JsonResponse({'response':'created successfully!'}, safe=False)
        except:
            return JsonResponse({'negative':f'Failed to create role!'}, safe=False)