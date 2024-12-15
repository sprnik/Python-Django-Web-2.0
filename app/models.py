from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name ="Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    image = models.FileField(default = 'temp.jpg', verbose_name="Путь к картинке")
    
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "статья блога"
        verbose_name_plural = "статьи блога"

admin.site.register(Blog)

class Comment(models.Model):
    text = models.TextField(verbose_name = "Текст комментария")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата комментария")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор комментария")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья комментария")

    def __str__(self):
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)

    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарии к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"

admin.site.register(Comment)

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    description = models.TextField(blank=True, verbose_name="Описание категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Event(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events', verbose_name="Категория")
    title = models.CharField(max_length=255, verbose_name="Название мероприятия")
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    description = models.TextField(verbose_name="Описание мероприятия")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время", default="00:00")
    location = models.CharField(max_length=255, verbose_name="Место проведения")
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="Изображение")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Электронная почта")
    
    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.price * item.quantity
        return total

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id} от {self.order_date.strftime('%d.%m.%Y %H:%M')}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Мероприятие")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.event.title} x {self.quantity}"