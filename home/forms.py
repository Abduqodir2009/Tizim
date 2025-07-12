from django import forms
from .models import Author, References, Book, Expence, Sell, Staff, Staff_payment,  Staff_work, output
import re
from django import forms
from datetime import date
from .models import Author
from django.core.exceptions import ValidationError

EXISTING_COUNTRIES = [
    'uzbekistan', 'russia', 'usa', 'uk', 'germany', 'france', 'china', 'japan',
  
]

class AuthorForms(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['full_name', 'birth_date', 'country']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'country': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')

        if not full_name:
            raise forms.ValidationError("F.I.Sh. kiritish majburiy")

        if len(full_name.split()) < 2:
            raise forms.ValidationError("F.I.Sh. kamida 3 ta so'zdan iborat bo'lishi kerak")

        for word in full_name.split():
            if len(word) < 3:
                raise forms.ValidationError("Har bir ism, familiya va otasining ismi kamida 3 harfdan iborat bo'lishi kerak")

        if not re.match(r'^[A-Za-zА-Яа-яЁёЎўҚқҲҳҒғҲҳ\s]+$', full_name):
            raise forms.ValidationError("F.I.Sh. faqat lotin yoki krill harflaridan tashkil topishi kerak")

        if any(char.isdigit() for char in full_name):
            raise forms.ValidationError("F.I.Sh. raqamlardan iborat bo'lmasligi kerak")

        return full_name

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        if not birth_date:
            raise forms.ValidationError("Tug'ilgan sanani kiriting")

        if birth_date > date.today():
            raise forms.ValidationError("Tug'ilgan sana kelajakdagi sana bo'lishi mumkin emas")

        return birth_date

    def clean_country(self):
        country = self.cleaned_data.get('country')

        if not country:
            raise forms.ValidationError("Davlat nomini kiriting")

        if len(country.strip()) < 3:
            raise forms.ValidationError("Davlat nomi kamida 3 ta harfdan iborat bo'lishi kerak")

        if not re.match(r'^[A-Za-zА-Яа-яЁёЎўҚқҲҳҒғҲҳ\s]+$', country):
            raise forms.ValidationError("Davlat nomi faqat lotin yoki krill harflaridan tashkil topishi kerak")

        if any(char.isdigit() for char in country):
            raise forms.ValidationError("Davlat nomi raqamlardan iborat bo'lmasligi kerak")

        # Проверка, существует ли такая страна
        normalized_country = country.lower().strip()
        if normalized_country not in EXISTING_COUNTRIES:
            raise forms.ValidationError("Bunday davlat mavjud emas")

        return country
class ReferenceForms(forms.ModelForm):
    class Meta:
        model = References
        fields = ['type', 'value']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_value(self):
        value = self.cleaned_data.get('value')

        if len(value) < 3:
            raise forms.ValidationError("Qiymat kamida 3 ta belgidan iborat bo'lishi kerak")

        if References.objects.filter(value__iexact=value).exists():
            raise forms.ValidationError("Bu qiymat allaqachon qo'shilgan!")

        return value
from django import forms
from .models import Book
from datetime import date


class BookForms(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'image', 'price',  'description', 'author', 'category', 'created_at']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'created_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Только те категории, где type='Kitob turi' и is_deleted=False
        self.fields['category'].queryset = References.objects.filter(type='Kitob turi', is_deleted=False)
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.split()) >= 3:
            raise forms.ValidationError("Kitob nomi 3 ta so'zdan ko'p bo'lishi kerak.")
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price >= 10000:
            raise forms.ValidationError("Kitob narxi $10 000 dan oshmasligi kerak.")
        return price

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description.split()) < 3:
            raise forms.ValidationError("Tavsif 3 ta so'zdan ortiq bo'lishi kerak.")
        return description

    def clean_created_at(self):
        created_at = self.cleaned_data.get('created_at')
        if created_at > date.today():
            raise forms.ValidationError("Qo'shish sanasi kelajak sana bo'lmasligi kerak.")
        return created_at

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        author = cleaned_data.get('author')

        if name and author:
            qs = Book.objects.filter(name__iexact=name.strip(), author=author)
            if self.instance.pk:  # exclude self when editing
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Bu nomdagi kitob ushbu muallif bilan allaqachon mavjud.")
class ExpenceForm(forms.ModelForm):
    class Meta:
        model = Expence
        fields = ['book', 'price', 'quantity', 'description', 'creted_at']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'creted_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        quantity = cleaned_data.get('quantity')

        if price is not None and quantity is not None:
            cleaned_data['total_price'] = price * quantity  # автоматический расчёт

        return cleaned_data

class SellForm(forms.ModelForm):
    class Meta:
        model = Sell
        fields = ['book', 'price', 'quantity', 'description', 'created_at']  # ⚠️ total_price удалён
        widgets = {
            'book': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'created_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        book = self.cleaned_data.get('book')

        if book and quantity:
            if quantity > book.quantity:
                raise ValidationError(
                    f"Siz {quantity} dona kitob sotmoqchisiz, lekin omborda faqat {book.quantity} dona bor."
                )
        return quantity

    def clean_price(self):
        price = self.cleaned_data.get('price')
        book = self.cleaned_data.get('book')

        if book and price:
            if price != book.price:
                raise ValidationError(
                    f"Bu kitob narxi aslida {book.price} so'm, siz {price} so'm deb noto‘g‘ri kiritdingiz."
                )
        return price

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.total_price = instance.price * instance.quantity
        if commit:
            instance.save()
        return instance

    def clean_price(self):
        price = self.cleaned_data.get('price')
        book = self.cleaned_data.get('book')

        if book and price:
            if price != book.price:
                raise ValidationError(
                    f"Bu kitob narxi aslida {book.price} so'm, siz {price} so'm deb noto‘g‘ri kiritdingiz."
                )
        return price
    

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['full_name', 'phone_number', 'gender', 'created_at', 'balance']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'To‘liq ism'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998901234567',
                'value': '+998'  # автоматически добавляется при открытии формы
            }),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'created_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Balans'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].queryset = References.objects.filter(type='Jinsi', is_deleted=False)

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        words = full_name.split()

        if len(words) != 2:
            raise forms.ValidationError("F.I.Sh 2 ta so‘zdan iborat bo‘lishi kerak.")

        for word in words:
            if not re.fullmatch(r'[A-Za-zА-Яа-яЎўҚқҒғҲҳЁё]+', word):
                raise forms.ValidationError("Ism va familiya faqat harflardan iborat bo‘lishi kerak.")

        return full_name

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()

        # Проверка: должен начинаться с +998 и далее 9 цифр
        if not re.fullmatch(r'\+998\d{9}', phone):
            raise forms.ValidationError("Telefon raqam +998 bilan boshlanishi va jami 13 ta belgidan iborat bo‘lishi kerak.")

        return phone

    def clean_balance(self):
        balance = self.cleaned_data.get('balance')
        if balance < 0:
            raise forms.ValidationError("Balans manfiy bo'lishi mumkin emas.")
        return balance
    
class Staff_paymentForms(forms.ModelForm):
    class Meta:
        model = Staff_payment
        fields = ['staff', 'price', 'created_at']
        widgets = {
            'staff': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Xodimni tanlang'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'To‘lov summasi'
            }),
            'created_at': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class Staff_workForms(forms.ModelForm):
    class Meta:
        model = Staff_work
        fields = ['staff', 'price', 'description', 'created_at']
        widgets = {
            'staff': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Xodimni tanlang'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'To‘lov summasi'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Batafsil ish tavsifi'
            }),
            'created_at': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class OutputForm(forms.ModelForm):
    class Meta:
        model = output
        fields = ['type', 'price', 'description', 'careated_at']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'careated_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].queryset = References.objects.filter(type='Chiqim', is_deleted=False)
