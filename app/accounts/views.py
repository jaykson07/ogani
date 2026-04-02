from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Profile

# Create your views here.


@login_required
def profile(request):
    prof, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name = request.POST.get('last_name', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        request.user.save()

        prof.bio = request.POST.get('bio', '').strip()
        avatar = request.FILES.get('avatar')
        if avatar:
            prof.avatar = avatar
        prof.save()

        messages.success(request, 'Your profile has been updated.')
        return redirect('accounts:profile')

    ctx = {
        'profile': prof
    }
    return render(request, 'profile.html', ctx)
