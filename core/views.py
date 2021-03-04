from django.shortcuts import render
# Create your views here.


def profile_core(request):
    return render(request, 'core/profile.html')
