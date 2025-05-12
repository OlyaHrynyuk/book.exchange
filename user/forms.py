from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Offer

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'category', 'image', 'available']
        labels = {
            'title': 'Назва книги',
            'author': 'Автор',
            'description': 'Опис',
            'category': 'Категорія',
            'image': 'Зображення книги',
            'available': 'Доступна для обміну',
        }

class OfferForm(forms.ModelForm):
    offered_book = forms.ModelChoiceField(
        queryset=Book.objects.none(),
        label="Оберіть свою книгу для обміну",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Offer
        fields = ['offered_book']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['offered_book'].queryset = Book.objects.filter(owner=user, available=True)

class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="Пошук книги",
        widget=forms.TextInput(attrs={'placeholder': 'Введіть назву або автора'})
    )
