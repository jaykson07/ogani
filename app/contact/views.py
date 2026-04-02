from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from .forms import ContactForm
from .models import Subscribe
from app.products.models import Category


# Create your views here.

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contacts:contact')
    else:
        form = ContactForm()

    email = request.GET.get('email', '').strip()
    if email:
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
        else:
            if Subscribe.objects.filter(email=email).exists():
                messages.info(request, 'This email is already subscribed.')
            else:
                Subscribe.objects.create(email=email)
                messages.success(request, 'You have successfully subscribed.')
        return redirect('contacts:contact')

    ctx = {
        'form': form,
        'categories': Category.objects.all(),
    }
    return render(request, 'contact.html', ctx)
