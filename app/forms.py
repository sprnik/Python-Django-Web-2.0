"""
Definition of forms.
"""
from django.db import models
from .models import Comment
from .models import Blog

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Логин'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))
    
class AnketaForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    age_choices = [(i, str(i)) for i in range(18, 101)]  # Создаем список возможных значений от 18 до 100 лет
    age = forms.ChoiceField(choices=age_choices, label='Выберите ваш возраст')
    gender = forms.ChoiceField(label='Ваш пол', choices=[('Мужской', 'Мужской'),('Женский', 'Женский')], widget=forms.RadioSelect, initial=1)
    city = forms.CharField(label='Ваш город', min_length=2, max_length=100)
    vopros = forms.ChoiceField(label='Как часто вы посещаете различные культурные мероприятия?', 
                               choices=(('Не посещаю вообще', 'Не посещаю вообще'), ('1-2 раза в год', '1-2 раза в год'), ('Раз в пару месяцев', 'Раз в пару месяцев'), ('Раз в месяц', 'Раз в месяц'), ('Больше одного раза в месяц', 'Больше одного раза в месяц')))
    message = forms.CharField(label='Ваши пожелания по сайту', widget=forms.Textarea(attrs={'rows':12, 'cols':20}))
    notice = forms.BooleanField(label='Получать рассылку о новых мероприятиях на почту?', required=False)
    email = forms.EmailField(label='Ваш E-Mail', min_length=7)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text
# author будет автоматически выбран в зависимости от авторизованного пользователя
# date автоматически добавляется в момент создания записи
        
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog # используемая модель
        fields = ('title', 'description', 'content', 'image',) # заполняемые поля
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинка"}
        
from .models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'email']