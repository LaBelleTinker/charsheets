from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import View
from django import forms
from django.http import HttpResponse
from django.conf import settings
from .models import Sheet, Skill


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ResetForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


class NewSheetForm(forms.Form):
    name = forms.CharField()
    type = forms.ChoiceField(choices=[['0','D&D 3.5e']])


class LoginView(View):
    
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'error': False, 'form': form})
        
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if password == '1234':
                    return redirect('/password_reset/')
                else:
                    return redirect('/profile/')
            else:
                form = LoginForm()
                return render(request, 'login.html', {'error': True, 
                                                      'form': form})


class NewUserView(View):
    
    def get(self, request):
        form = LoginForm()
        context = {'permission_error': False,
                   'duplicate_error': False,
                   'form': form}
        return render(request, 'register.html', context)
        
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if username not in settings.USER_WHITELIST:
                context = {'permission_error': True,
                           'duplicate_error': False,
                           'form': form}
            elif len(User.objects.filter(username=username)) > 0:
                context = {'permission_error': False,
                           'duplicate_error': True,
                           'form': form}
            else:
                print("creating new user " + username)
                new_user = User.objects.create_user(username, password=password)
                return redirect('/login/')
            return render(request, 'register.html', context)                                                 


class PasswordResetView(View):
    
    def get(self, request):
        form = ResetForm()
        return render(request, 'pwdreset.html', {'pwderror': False, 
                                                 'matcherror': False,
                                                 'form': form})
        
    def post(self, request):
        form = ResetForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if request.user.check_password(old_password):
                if new_password == confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    return redirect('/login/')
                else:
                    context = {'pwderror': False, 
                               'matcherror': True,
                               'form': ResetForm()}
            else:
                context = {'pwderror': True, 
                           'matcherror': False,
                           'form': ResetForm()}
            return render(request, 'pwdreset.html', context)


class ProfileView(View):
    
    def get(self, request):
        form = NewSheetForm()
        context = {'user': request.user,
                   'sheet_list': Sheet.objects.filter(owner=request.user),
                   'form': form}
        return render(request, 'profile.html', context)
        
    def post(self, request):
        form = NewSheetForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            type = form.cleaned_data['type']
            sheet = Sheet(name=name, owner=request.user)
            sheet.initialize()
            sheet.save()
        form = NewSheetForm()
        context = {'user': request.user,
                   'sheet_list': Sheet.objects.filter(owner=request.user),
                   'form': form}
        return render(request, 'profile.html', context)


def home_view(request):
    skills = list([s for s in Skill.objects.all() if s.super_skill == None])
    print(type(skills))
    skills.sort(key=lambda x: x.name)
    skill_subskill_list = []
    for s in skills:
        subskills = list(Skill.objects.filter(super_skill=s))
        if subskills:
            subskills.sort(key=lambda ss: ss.name)
            skill_subskill_list.append((s, tuple(subskills)))
        else:
            skill_subskill_list.append((s, tuple()))
    context = {'skills': skill_subskill_list}
    return render(request, 'home.html', context)
