  # app/context_processors.py
from .models import Category
from django.contrib.auth.models import Group
from datetime import datetime

def categories(request):
    return {'categories': Category.objects.all()}

def is_organizer(request):
    if request.user.is_authenticated:
        return {'is_organizer': request.user.groups.filter(name='Организатор').exists()}
    return {'is_organizer': False}


def year(request):
    """Добавляет текущий год в контекст каждого шаблона."""
    return {'year': datetime.now().year}