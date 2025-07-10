from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Expence, Book, Sell, Staff, Staff_payment, Staff_work

@receiver([post_save, post_delete], sender=Expence)
@receiver([post_save, post_delete], sender=Sell)
def book_quantity_sifnal( sender, instance, **kvargs):
    book =Book.objects.get(name=instance.book)
    expences=Expence.objects.filter(book=book, is_deleted=False)
    sells=Sell.objects.filter(book=book, is_deleted=False)
    
    total_quantity = 0
    for i in expences:
        total_quantity += i.quantity
        
    for j in sells:
        total_quantity -= j.quantity      
        
    book.quantity =total_quantity
    book.save()
    
@receiver([post_save, post_delete], sender=Staff_payment)
@receiver([post_save, post_delete], sender=Staff_work)
def staff_balance_signal(sender, instance, **kwargs):
    staff=Staff.objects.get(id=instance.staff.id)
    staff_payment=Staff_payment.objects.filter(staff=staff, is_deleted=False)
    staff_work=Staff_work.objects.filter(staff=staff, is_deleted=False)
    
    
    staff_payment_total=sum(payment.price for payment in staff_payment)
    staff_work_total=sum(work.price for work in staff_work)
    
    staff_balance=staff_work_total-staff_payment_total
    staff.balance=staff_balance
    staff.save()