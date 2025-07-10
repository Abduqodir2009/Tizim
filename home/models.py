from django.db import models

# Create your models here.

class References(models.Model):
    TYPE_CHOICES=[
         ('Kitob turi','Kitob turi'),
         ('Jinsi','Jinsi'),
         ('Chiqim','Chiqim')
    ]
    type = models.CharField(max_length=255,choices=TYPE_CHOICES,verbose_name="Turi")
    value = models.CharField(max_length=255,verbose_name="Qiymati")
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'Reference'
    
    def __str__(self):
        return self.value
    
class Author(models.Model):
    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    country = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'Author'

    def __str__(self):
        return self.full_name

class Book(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kitob nomi")
    image = models.ImageField(upload_to='media', verbose_name="Kitob rasmi") 
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name="book_author_author")
    category = models.ForeignKey(to=References, on_delete=models.CASCADE, related_name="book_category_reference")
    description = models.TextField(verbose_name="Ma'lumot")
    price = models.FloatField()
    quantity=models.IntegerField()
    created_at = models.DateField(verbose_name="Kitob yozilgan yil")
    is_deleted = models.BooleanField(default=False)


    class Meta:
        db_table = 'Book'

    def __str__(self):
        return self.name    

class Expence(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="expence_book_book")
    price = models.FloatField()
    quantity = models.IntegerField()
    total_price = models.FloatField()
    description = models.TextField(blank=True)
    creted_at = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

class Meta:
    db_table = "Expence"

    def __str__(self):
        return self.book
 
class Sell(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="sell_book_book")
    price = models.FloatField()
    quantity = models.IntegerField()
    total_price = models.FloatField()
    created_at = models.DateField()
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "Sell"

    def __str__(self):
            return self.book

class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    gender = models.ForeignKey(
        to=References,
        on_delete=models.CASCADE,
        related_name="staff_gender_references"
    )
    created_at = models.DateField()
    balance = models.FloatField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name  # ✔️ всегда возвращаем строку

        
class Staff_payment(models.Model):
    staff = models.ForeignKey(
        to=Staff,
        on_delete=models.CASCADE,
        related_name="staff_payment_set"
    )
    price = models.FloatField()
    created_at = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.staff.full_name} - {self.price} so'm"  # ✔️ читаемо и корректно
   
class Staff_work(models.Model):
    staff = models.ForeignKey(
        to=Staff,
        on_delete=models.CASCADE,
        related_name="staff_work_set"
    )
    price = models.FloatField()
    description = models.TextField()
    created_at = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.staff.full_name} - {self.price} so'm"  # ✔️ или просто str(self.staff)


class output(models.Model):
    type = models.ForeignKey(to=References, on_delete=models.CASCADE,related_name="output_type_references")
    price = models.FloatField()
    description = models.TextField()
    careated_at = models.DateField()
    is_deleted = models.BooleanField(default=False)
