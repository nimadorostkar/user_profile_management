import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Profile, Notice
from . import models
from django.db import transaction
from .forms import ProfileForm, CreateUserForm





@login_required
def dashboard(request):
  profile = models.Profile.objects.filter(user=request.user)
  notices = models.Notice.objects.filter(user=request.user).order_by('-created_on')

  if request.method == 'POST':
      form = createUserForm(request.POST)
      profile_form = profileForm(request.POST)

      if form.is_valid() and profile_form.is_valid():
          user = form.save()

          #we don't save the profile_form here because we have to first get the value of profile_form, assign the user to the OneToOneField created in models before we now save the profile_form.

          profile = profile_form.save(commit=False)
          profile.user = user

          profile.save()

          messages.success(request,  'Your account has been successfully created')

          return redirect('login')


  context = {'profile': profile, 'notices':notices, 'form':form, 'profile_form': profile_form }
  return render(request, 'dashboard/dashboard.html', context)
