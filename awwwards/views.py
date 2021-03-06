from django.http import HttpResponse,Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import SignupForm,ProfileForm,ProjectForm
from django.contrib.auth.models import User
from .models import Profile, Project
from django.core.mail import EmailMessage


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile=Profile(user=user)
            profile.save()             
            current_site = get_current_site(request)
            mail_subject = 'Activate your awwwwwwwwwwww account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you. Now you can login your account.' '<a href="/accounts/login">Click here</a>')
    else:
        return HttpResponse('Activation link is invalid!')

def home(request):
    projects = Project.objects.all()

    return render(request, 'awwards/index.html',{"projects": projects})

@login_required(login_url="/accounts/login/")
def profile(request):
    current_user = request.user
    profile=Profile.objects.filter(user=request.user)
    # images=Image.objects.filter(user=request.user)
    return render (request,'awwards/profile.html',{'profile':profile})

@login_required
def edit_profile(request):
    # images = Image.objects.all()
    profile = Profile.objects.filter(user=request.user)
    current_user = request.user
    # photos = Image.objects.filter(user=current_user)
    prof_form = ProfileForm()
    if request.method == 'POST':
        prof_form =ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if prof_form.is_valid:
            prof_form.save()
        else:
            prof_form = ProfileForm()
            return render(request, 'awwards/edit-profile.html', {"prof_form": prof_form,"profile":profile})
    return render(request, 'awwards/edit-profile.html', {"prof_form":prof_form,"profile":profile})

@login_required
def add_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect('/')

    else:
        form = ProjectForm()
        return render(request, 'awwards/add-project.html', {"form": form})



@login_required
def single_project(request,project_id):
    project = Project.objects.get(id=project_id)
    return render(request,'awwards/single-project.html',{"project":project})

@login_required
def search_project(request):

    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_projects = Project.search_by_project_title(search_term)
        # searched_projects = Project.objects.filter(project=search_term)
        message = f"{search_term}"

        return render(request, 'awwards/search.html',{"message":message,"searched_projects": searched_projects})

    else:
        message = "Project not found"
        return render(request, 'awwards/search.html',{"message":message})