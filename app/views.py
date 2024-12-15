from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .forms import AnketaForm 
from django.contrib.auth.forms import UserCreationForm

from django.db import models
from .models import Blog

from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария
from .forms import BlogForm # использование формы ввода статьи блога

from .models import Category, Event, Order, OrderItem
from .forms import OrderForm
from django.contrib.auth.decorators import login_required, user_passes_test
from decimal import Decimal
from django.http import JsonResponse

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    categories = Category.objects.all()
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'year':datetime.now().year,
            'categories': categories,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    categories = Category.objects.all()
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'year':datetime.now().year,
            'categories': categories,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    categories = Category.objects.all()
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'year':datetime.now().year,
            'categories': categories,
        }
    )

def links(request):
    """Рендерит страницу с полезными ресурсами."""
    assert isinstance(request, HttpRequest)
    categories = Category.objects.all()
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'year':datetime.now().year,
            'categories': categories,
        }
    )

def pool(request):
    """Рендерит страницу обратной связи."""
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    vopros = {'1': 'Не посещаю вообще', '2': '1-2 раза в год', '3': 'Раз в пару месяцев', '4': 'Раз в месяц', '5': 'Больше одного раза в месяц'}
    categories = Category.objects.all()
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['age'] = form.cleaned_data['age']
            data['gender'] = form.cleaned_data['gender']
            data['city'] = form.cleaned_data['city']
            data['vopros'] = form.cleaned_data['vopros']
            data['message'] = form.cleaned_data['message']
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            form = None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/pool.html',
        {
            'form':form,
            'data':data,
            'title':'Обратная связь',
            'year':datetime.now().year,
            'categories': categories,
        }
    )

def registration(request):
    """Renders the registration page."""
    categories = Category.objects.all()
    if request.method == "POST": # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False # запрещён вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации

            regform.save() # сохраняем изменения после добавления полей

            return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm()  # создание объекта формы для ввода данных

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform, # передача формы в шаблон веб-страницы
            "year" :datetime.now().year,
            'categories': categories,
        }
    )

def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели
    categories = Category.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
        'title':'Блог',
        'posts': posts, # передача списка статей в шаблон веб-страницы
        'year' :datetime.now().year,
        'categories': categories,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)
    categories = Category.objects.all()
    
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
            comment_f.save() # сохраняем изменения после добавления полей

            return redirect('blogpost', parametr=post_1.id)  # переадресация
    else:
        form = CommentForm()
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'title': post_1.title,
            'year': datetime.now().year,
            'categories': categories,
        }
    )

def newpost(request):
    """Renders the newpost page."""
    categories = Category.objects.all()
    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.author = request.user
            blog_f.posted = datetime.now()
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью',
            'year': datetime.now().year,
            'categories': categories,
        }
    )

def videopost(request):
    """Renders the videopost page."""
    categories = Category.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title': 'Видео',
            'year': datetime.now().year,
            'categories': categories,
        }
    )

def category_detail(request, slug):
    """Renders the category detail page."""
    category = get_object_or_404(Category, slug=slug)
    events = Event.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'events/category_detail.html', {'category': category, 'events': events, 'categories': categories})

def event_detail(request, slug):
    """Renders the event detail page."""
    event = get_object_or_404(Event, slug=slug)
    categories = Category.objects.all()
    return render(request, 'events/event_detail.html', {'event': event, 'categories': categories})

def event_detail(request, slug):
    """Renders the event detail page."""
    event = get_object_or_404(Event, slug=slug)
    categories = Category.objects.all()
    return render(request, 'events/event_detail.html', {'event': event, 'categories': categories})

def is_not_admin(user):
    """Проверяет, является ли пользователь обычным пользователем (не администратором)."""
    return not user.is_staff and not user.is_superuser

@login_required
@user_passes_test(is_not_admin)
def add_to_cart(request, event_id):
    """Adds an event to the cart."""
    event = get_object_or_404(Event, id=event_id)
    cart = request.session.get('cart', {})
    if event_id in cart:
        cart[event_id] += 1
    else:
        cart[event_id] = 1
    request.session['cart'] = cart
    return redirect('cart')


@login_required
@user_passes_test(is_not_admin)
def cart(request):
    """Renders the shopping cart page."""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal('0.00')
    for event_id, quantity in cart.items():
        event = get_object_or_404(Event, id=event_id)
        item_price = event.price * quantity
        total_price += item_price
        cart_items.append({
            'event': event,
            'quantity': quantity,
            'item_price': item_price
        })
    categories = Category.objects.all()
    return render(request, 'app/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'categories': categories})


@login_required
@user_passes_test(is_not_admin)
def update_cart(request):
    """Updates the quantity of an item in the cart."""
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', {})
        if event_id in cart:
            if quantity > 0:
                cart[event_id] = quantity
            else:
                del cart[event_id]
            request.session['cart'] = cart
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Item not in cart'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
@user_passes_test(is_not_admin)
def remove_from_cart(request, event_id):
    """Removes an item from the cart."""
    cart = request.session.get('cart', {})
    if event_id in cart:
        del cart[event_id]
        request.session['cart'] = cart
    return redirect('cart')


@login_required
@user_passes_test(is_not_admin)
def checkout(request):
    """Renders the checkout page and processes the order."""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal('0.00')
    for event_id, quantity in cart.items():
        event = get_object_or_404(Event, id=event_id)
        item_price = event.price * quantity
        total_price += item_price
        cart_items.append({
            'event': event,
            'quantity': quantity,
            'item_price': item_price
        })
    categories = Category.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()
            for item in cart_items:
                OrderItem.objects.create(order=order, event=item['event'], quantity=item['quantity'], price=item['event'].price)
            request.session['cart'] = {}  # Очищаем корзину после оформления заказа
            return redirect('my_orders')
    else:
        form = OrderForm()
    return render(request, 'app/checkout.html', {'form': form, 'cart_items': cart_items, 'total_price': total_price, 'categories': categories})


@login_required
@user_passes_test(is_not_admin)
def my_orders(request):
    """Renders the user's order history page."""
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    categories = Category.objects.all()
    return render(request, 'app/my_orders.html', {'orders': orders, 'categories': categories})

@login_required
def checkout(request):
    """Renders the checkout page and processes the order."""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal('0.00')
    for event_id, quantity in cart.items():
        event = get_object_or_404(Event, id=event_id)
        item_price = event.price * quantity
        total_price += item_price
        cart_items.append({
            'event': event,
            'quantity': quantity,
            'item_price': item_price
        })
    categories = Category.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()
            for item in cart_items:
                OrderItem.objects.create(order=order, event=item['event'], quantity=item['quantity'], price=item['event'].price)
            request.session['cart'] = {}  # Очищаем корзину после оформления заказа
            return redirect('my_orders')
    else:
        form = OrderForm()
    return render(request, 'app/checkout.html', {'form': form, 'cart_items': cart_items, 'total_price': total_price, 'categories': categories})


@login_required
def my_orders(request):
    """Renders the user's order history page."""
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    categories = Category.objects.all()
    return render(request, 'app/my_orders.html', {'orders': orders, 'categories': categories})

def is_staff_or_organizer(user):
    return user.groups.filter(name='Организатор').exists()  # Если есть группа "Organizer"

@user_passes_test(is_staff_or_organizer)
def manage_orders(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'app/manage_orders.html', {'orders': orders})

@user_passes_test(is_staff_or_organizer)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'app/order_detail.html', {'order': order})

@user_passes_test(is_staff_or_organizer)
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('manage_orders')

@user_passes_test(is_staff_or_organizer)
def update_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    quantity_change = int(request.POST.get('quantity_change', 0))

    if quantity_change > 0:
        item.quantity += quantity_change
    elif quantity_change < 0 and item.quantity > 1:
        item.quantity += quantity_change
    elif quantity_change < 0 and item.quantity == 1:
        item.delete()
        return JsonResponse({'success': True, 'order_total': item.order.total_price})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid quantity change'})

    item.save()
    item.order.total_price = item.order.get_total_price() # Пересчитываем общую стоимость заказа
    item.order.save()
    return JsonResponse({'success': True, 'order_total': item.order.total_price})

@user_passes_test(is_staff_or_organizer)
def add_order_item(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        quantity = int(request.POST.get('quantity', 1))

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Мероприятие не найдено.'})

        # Проверяем, есть ли уже такой товар в заказе
        existing_item = OrderItem.objects.filter(order=order, event=event).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            OrderItem.objects.create(order=order, event=event, quantity=quantity, price=event.price)

        order.total_price = order.get_total_price()
        order.save()
        return JsonResponse({'success': True, 'order_total': order.total_price})

    events = Event.objects.all()
    return render(request, 'app/add_order_item.html', {'order': order, 'events': events})