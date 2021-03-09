from django.shortcuts import render
# Create your views here.


def profile_view_base(request):
    return render(request, 'core/profile.html')
