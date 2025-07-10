from django.shortcuts import render, redirect, get_object_or_404
from .models import Author , References, Book, Expence, Sell, Staff, Staff_payment, Staff_work, output
from .forms import AuthorForms, ReferenceForms, BookForms, ExpenceForm, SellForm, StaffForm, Staff_paymentForms, Staff_workForms, OutputForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def author_view(request):
    authors = Author.objects.filter(is_deleted=False)

    search = request.GET.get('q', None)  
    if search:
        authors = authors.filter(full_name__icontains=search)

    context = {
        "authors": authors
    }
    return render(request, 'author.html', context=context)

@login_required(login_url='login')
def authors_create(request):
    if request.method=="POST":
        forms=AuthorForms(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('author_view')
    else:
        forms=AuthorForms()
    context={
        "forms":forms
    }
    return render(request, 'author_create.html', context=context)

@login_required(login_url='login')
def authors_read(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'author_read.html', {'author': author})

@login_required(login_url='login')
def authors_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForms(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_view')
    else:
        form = AuthorForms(instance=author)

    return render(request, 'author_create.html', {'forms': form})

@login_required(login_url='login')
def authors_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    author.is_deleted = True  
    author.save()
    return redirect('author_view')

@login_required(login_url='login')
def reference_view(request):
    book_category = References.objects.filter(type="Kitob turi", is_deleted=False)
    gender= References.objects.filter(type="Jinsi", is_deleted=False)
    Chiqim= References.objects.filter(type="Chiqim", is_deleted=False)
    context = {
        "book_category": book_category,
        "gender":gender,
        "Chiqim":Chiqim
    }

    return render(request, 'reference.html', context=context)

@login_required(login_url='login')
def reference_create(request):
    if request.method == "POST":
        form = ReferenceForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reference_view')  
    else:
        form = ReferenceForms()
    
    context = {
        'form': form
    }
    return render(request, 'reference_create.html', context=context)

@login_required(login_url='login')
def reference_update(request, pk):
    reference = get_object_or_404(References, pk=pk)

    if request.method == "POST":
        form = ReferenceForms(request.POST, instance=reference)
        if form.is_valid():
            form.save()
            return redirect('reference_view')  
    else:
        form = ReferenceForms(instance=reference)

    context = {
        'form': form
    }
    return render(request, 'reference_update.html', context)

@login_required(login_url='login')
def reference_delete(request, pk):
    reference = get_object_or_404(References, pk=pk)

    if request.method == "POST":
        reference.delete()
        return redirect('reference_view')  

    context = {
        'reference': reference
    }
    return render(request, 'reference_delete.html', context)


@login_required(login_url='login')
def home(request):
    all_books = Book.objects.filter(is_deleted=False)
    categories = References.objects.filter(type='Kitob turi', is_deleted=False)

    selected_category = request.GET.get('category', None)
    if selected_category:
        all_books = all_books.filter(category__id=selected_category)

    qidiruv = request.GET.get('q', None)
    if qidiruv:
        all_books = all_books.filter(name__icontains=qidiruv)

    context = {
        'all_books': all_books,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, "index.html", context=context)

@login_required(login_url='login')
def book_create(request):
    if request.method == "POST":
        form = BookForms(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = BookForms()  

    context = {
        'form': form
    }
    return render(request, "book_create.html", context=context)  

@login_required(login_url='login')
def read_book(request,pk):
    book = Book.objects.get(pk=pk)
    context ={
        'book':book
    }
    return render(request,"read_book.html",context=context)

@login_required(login_url='login')
def book_update(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        form = BookForms(request.POST, request.FILES, instance=book)  # <-- добавлен request.FILES
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForms(instance=book)

    context = {
        'form': form,
        'book': book
    }
    return render(request, "book_update.html", context=context)
def book_delet(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.is_deleted = True
        book.save()
        return redirect('home')

    return render(request, 'book_delete.html', {'book': book})

@login_required(login_url='login')
def expence_view(request):
    all_expenses = Expence.objects.filter(is_deleted=False)
    qidiruv = request.GET.get('q', None)
    show_category_field = request.GET.get('category_field', None)
    if qidiruv:
        all_expenses = all_expenses.filter(name__icontains=qidiruv)
    if show_category_field:
        all_expenses = all_expenses.filter(category__iexact=show_category_field)
        
    context = {
        'all_expenses': all_expenses,
        'show_category_field': show_category_field,
        'qidiruv': qidiruv,
    }
    return render(request, "expence.html", context=context)

@login_required(login_url='login')
def expence_create(request):
    if request.method == 'POST':
        form = ExpenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expence_view')
    else:
        form = ExpenceForm()
    return render(request, 'expence_create.html', {'form': form})

@login_required(login_url='login')
def expence_read(request, pk):
    expence=Expence.objects.get(pk=pk)
    context={
        'expence':expence
    }
    return render(request, 'expence_read.html', context=context)

@login_required(login_url='login')
def expence_update(request, pk):
    expence = get_object_or_404(Expence, pk=pk)
    if request.method == 'POST':
        form = ExpenceForm(request.POST, instance=expence)
        if form.is_valid():
            form.save()
            return redirect('expence_view')
    else:
        form = ExpenceForm(instance=expence)
    return render(request, 'expence_update.html', {'form': form})

@login_required(login_url='login')
def expence_delete(request, pk):
    expence = get_object_or_404(Expence, pk=pk)
    if request.method == 'POST':
        expence.is_deleted = True
        expence.save()
        return redirect('expence_view')
    return render(request, 'expence_delete.html', {'expence': expence})

@login_required(login_url='login')
def sell_view(request):
    all_sells = Sell.objects.filter(is_deleted=False)
    qidiruv = request.GET.get('q', None)  
    show_category_field = request.GET.get('category_field', None)
    if qidiruv:
        all_sells = all_sells.filter(name__icontains=qidiruv)
    if show_category_field:
        all_sells = all_sells.filter(category__iexact=show_category_field)
    context = {
        'all_sells': all_sells,
        'show_category_field': show_category_field,
        'qidiruv': qidiruv
    }

    return render(request, 'sell.html', context=context)

@login_required(login_url='login')
def sell_create(request):
    if request.method=="POST":
        form=SellForm(request.POST) 
        if form.is_valid():
           form.save()
           return redirect('sell_view')
    else:
        form=SellForm()
    return render(request, 'sell_create.html', {'form': form})

@login_required(login_url='login')
def sell_read(request, pk):
    sell=Sell.objects.get(pk=pk)
    context={
        'sell':sell
    }
    return render(request, 'sell_read.html', context=context)

@login_required(login_url='login')
def sell_update(request, pk):
    sell = get_object_or_404(Sell, pk=pk)
    if request.method == "POST":
        form = SellForm(request.POST, instance=sell)
        if form.is_valid():
            form.save()
            return redirect('sell_view')
    else:
        form = SellForm(instance=sell)
    
    return render(request, 'sell_update.html', {'form': form})

@login_required(login_url='login')
def sell_delete(request, pk):
    sell=get_object_or_404(Sell, pk=pk)
    if request.method == 'POST':
        sell.is_deleted=True
        sell.save()
        return redirect('sell_view')
    return render(request, 'sell_delete.html',{'sell':sell})
@login_required(login_url='login')
def staff_view(request):
    staff_search = request.GET.get('q_staff')
    category_filter = request.GET.get('category_field')

    all_staff = Staff.objects.filter(is_deleted=False)
    if staff_search:
        all_staff = all_staff.filter(full_name__icontains=staff_search)
    if category_filter:
        all_staff = all_staff.filter(gender__value__iexact=category_filter)

    payment_search = request.GET.get('q_payment')
    staff_payment = Staff_payment.objects.filter(is_deleted=False)
    if payment_search:
        staff_payment = staff_payment.filter(staff__full_name__icontains=payment_search)

    work_search = request.GET.get('q_work')
    staff_work = Staff_work.objects.filter(is_deleted=False)
    if work_search:
        staff_work = staff_work.filter(staff__full_name__icontains=work_search)

    context = {
        'all_staff': all_staff,
        'staff_payment': staff_payment,
        'staff_work': staff_work,
        'staff_search': staff_search,
        'payment_search': payment_search,
        'work_search': work_search,
        'category_filter': category_filter,
    }
    return render(request, 'staff.html', context)

@login_required(login_url='login')
def staff_create(request):
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('staff_view')
    else:
        form = StaffForm()
    
    return render(request, 'staff_create.html', {'form': form})

@login_required(login_url='login')
def staff_read(request, pk):
    staff=Staff.objects.get(pk=pk)
    context={
        'staff':staff
    }
    return render(request, 'staff_read.html', context=context)

@login_required(login_url='login')
def staff_update(request, pk):
    staff = get_object_or_404(Staff, pk=pk)

    if request.method == "POST":
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff_view')
    else:
        form = StaffForm(instance=staff)
    
    return render(request, 'staff_update.html', {'form': form})

@login_required(login_url='login')
def staff_delete(request, pk):
    staff=get_object_or_404(Staff, pk=pk)
    if request.method=='POST':
        staff.is_deleted=True
        staff.save()
        return redirect('staff_view')
    return render(request, 'staff_delete.html', {'staff':staff})

@login_required(login_url='login')
def staff_payment_create(request):
    if request.method == 'POST':
        form = Staff_paymentForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_view')
    else:
        form = Staff_paymentForms()
    return render(request, 'staff_payment_create.html', {'form': form})

@login_required(login_url='login')
def staff_payment_read(request, pk):
    payment = get_object_or_404(Staff_payment, pk=pk)
    return render(request, 'staff_payment_read.html', {'payment': payment})

@login_required(login_url='login')
def staff_payment_update(request, pk):
    payment = get_object_or_404(Staff_payment, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = Staff_paymentForms(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('staff_view')  # или 'staff_payment_read', pk=payment.pk
    else:
        form = Staff_paymentForms(instance=payment)
    return render(request, 'staff_payment_update.html', {'form': form})

@login_required(login_url='login')
def staff_payment_delete(request, pk):
    payment = get_object_or_404(Staff_payment, pk=pk, is_deleted=False)
    if request.method == 'POST':
        payment.is_deleted = True
        payment.save()
        return redirect('staff_view')  # или на список выплат
    return render(request, 'staff_payment_delete.html', {'payment': payment})

@login_required(login_url='login')
def staff_work_create(request):
    if request.method == 'POST':
        form = Staff_workForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_view')  # или 'staff_work_list'
    else:
        form = Staff_workForms()
    return render(request, 'staff_work_create.html', {'form': form})

@login_required(login_url='login')
def staff_work_read(request, pk):
    work = get_object_or_404(Staff_work, pk=pk)
    return render(request, 'staff_work_read.html', {'work': work})

@login_required(login_url='login')
def staff_work_update(request, pk):
    work = get_object_or_404(Staff_work, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = Staff_workForms(request.POST, instance=work)
        if form.is_valid():
            form.save()
            return redirect('staff_view')  # или 'staff_work_read', pk=pk
    else:
        form = Staff_workForms(instance=work)
    return render(request, 'staff_work_update.html', {'form': form})

@login_required(login_url='login')
def staff_work_delete(request, pk):
    work = get_object_or_404(Staff_work, pk=pk, is_deleted=False)
    if request.method == 'POST':
        work.is_deleted = True
        work.save()
        return redirect('staff_view')  # или на список
    return render(request, 'staff_work_delete.html', {'work': work})

@login_required(login_url='login')
def income_calc_views(request):
    expence = Expence.objects.filter(is_deleted=False)
    sell = Sell.objects.filter(is_deleted=False)
    outputs = output.objects.filter(is_deleted=False)
    staff_payment = Staff_payment.objects.filter(is_deleted=False)

    # calculate sums
    sell_sum = sum(sell.total_price for sell in sell)
    expence_sum = sum(expence.total_price for expence in expence)
    outputs_sum = sum(outputs.price for outputs in outputs )
    staff_payment_sum = sum(staff_payment.price for staff_payment in staff_payment)
    context ={
        'sell_sum':sell_sum,
        'expence_sum':expence_sum,
        'outputs_sum':outputs_sum,
        'staff_payment_sum':staff_payment_sum,
        'profit':sell_sum - (expence_sum + outputs_sum + staff_payment_sum)
    }
    return render(request,"income_calc.html",context=context)

@login_required(login_url='login')
def output_view(request):
    all_outputs = output.objects.filter(is_deleted=False)

    qidiruv = request.GET.get('q', None)
    show_type_field = request.GET.get('type_field', None)

    if qidiruv:
        all_outputs = all_outputs.filter(description__icontains=qidiruv)

    if show_type_field:
        all_outputs = all_outputs.filter(type__value__iexact=show_type_field)

    context = {
        'all_outputs': all_outputs,
        'show_type_field': show_type_field,
        'qidiruv': qidiruv,
    }
    return render(request, 'output.html', context)

@login_required(login_url='login')
def output_create(request):
    if request.method == 'POST':
        form = OutputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('output_view')
    else:
        form = OutputForm()

    return render(request, 'output_create.html', {'form': form})

@login_required(login_url='login')
def output_read(request, pk):
    chiqim = get_object_or_404(output, pk=pk, is_deleted=False)
    return render(request, 'output_read.html', {'chiqim': chiqim})

@login_required(login_url='login')
def output_update(request, pk):
    chiqim = get_object_or_404(output, pk=pk, is_deleted=False)
    form = OutputForm(request.POST or None, instance=chiqim)
    if form.is_valid():
        form.save()
        return redirect('output_view')
    return render(request, 'output_update.html', {'form': form, 'chiqim': chiqim})

@login_required(login_url='login')
def output_delete(request, pk):
    chiqim = get_object_or_404(output, pk=pk, is_deleted=False)
    if request.method == 'POST':
        chiqim.is_deleted = True
        chiqim.save()
        return redirect('output_view')
    return render(request, 'output_delete.html', {'chiqim': chiqim})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Если уже вошел, отправляем домой

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # или куда нужно
        else:
            messages.error(request, 'Login yoki parol noto‘g‘ri')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

