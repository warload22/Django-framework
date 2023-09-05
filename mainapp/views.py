from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    context = {
        'title': 'Home',
        'player': request.user
    }
    return render(request, 'mainapp/index.html', context=context)
