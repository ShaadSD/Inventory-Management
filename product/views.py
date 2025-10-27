
from django.shortcuts import render, redirect,get_object_or_404
from .models import Product, Category,SalesRecord
from .forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import SalesRecord, Product, Customer,StockMovement
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SalesRecordForm ,StockMovementForm
from django.utils import timezone 
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from datetime import datetime
from django.db.models import Sum
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



@login_required
def download_product_report(request):

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

 
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Product List Report")


    p.setFont("Helvetica-Bold", 12)
    y = height - 80
    p.drawString(50, y, "SKU")
    p.drawString(150, y, "Name")
    p.drawString(300, y, "Category")
    p.drawString(450, y, "Stock")


    p.setFont("Helvetica", 10)
    y -= 20
    for product in Product.objects.all():
        p.drawString(50, y, str(product.sku))
        p.drawString(150, y, product.name)
        p.drawString(300, y, product.category.name if product.category else "N/A")
        p.drawString(450, y, str(product.quantity))
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


@login_required
def download_sales_report(request):

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

 
    sales = SalesRecord.objects.all().order_by('-date')


    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            sales = sales.filter(date__range=[start_date, end_date])
        except ValueError:
            pass 

  
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter


    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Sales Report")

  
    if start_date_str and end_date_str:
        p.setFont("Helvetica", 10)
        p.drawString(50, height - 70, f"Date Range: {start_date_str} to {end_date_str}")


    p.setFont("Helvetica-Bold", 12)
    y = height - 100
    p.drawString(50, y, "Date")
    p.drawString(150, y, "Product")
    p.drawString(300, y, "Customer")
    p.drawString(450, y, "Qty")


    p.setFont("Helvetica", 10)
    y -= 20
    for sale in sales:
        p.drawString(50, y, sale.date.strftime('%Y-%m-%d'))
        p.drawString(150, y, sale.product.name)
        p.drawString(300, y, sale.customer.name if sale.customer else "N/A")
        p.drawString(450, y, str(sale.quantity_sold))
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


@login_required
def reports(request):
    return render(request,'reports.html')



@login_required
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    search = request.GET.get('search', '')        
    category = request.GET.get('category', '')    
    supplier = request.GET.get('supplier', '')    

    if search:
        products = products.filter(name__icontains=search)  

    if category:
        products = products.filter(category__id=category)   

    if supplier:
        products = products.filter(supplier__icontains=supplier)  
    context = {
        'products': products,
        'categories': categories,
        'search': search,
        'selected_category': str(category),   
        'selected_supplier': supplier
    }

    return render(request, 'product.html', context)




@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    return redirect('product_list') 

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
    return redirect('product_list')


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
    return redirect('product_list')



def sales_list(request):
    sales = SalesRecord.objects.all().order_by('-date')
    products = Product.objects.all()
    customers = Customer.objects.all()


    selected_date = request.GET.get('date')
    customer_name_query = request.GET.get('customer_name')

    if selected_date:
        sales = sales.filter(date=selected_date)

    if customer_name_query:
        sales = sales.filter(customer__name__icontains=customer_name_query)

    return render(request, 'sales.html', {
        'sales': sales,
        'products': products,
        'customers': customers,
    })


@login_required
def add_sale(request):
    if request.method == 'POST':
        form = SalesRecordForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            product = sale.product

            if product.quantity >= sale.quantity_sold:
                product.quantity -= sale.quantity_sold
                product.save()
                sale.save()
                messages.success(request, 'Sale recorded successfully.')
                return redirect('sales_list')
            else:
                messages.error(request, 'Not enough stock available.')

        products = Product.objects.all()
        customers = Customer.objects.all()
        return render(request, 'sales.html', {
            'form': form,
            'products': products,
            'customers': customers,
        })

  
    return redirect('sales_list')


@login_required
def edit_sale(request, sale_id):
    sale = get_object_or_404(SalesRecord, id=sale_id)
    old_quantity = sale.quantity_sold

    if request.method == 'POST':
        form = SalesRecordForm(request.POST, instance=sale)

        product_id = request.POST.get('product')
        product = get_object_or_404(Product, id=product_id)

        if form.is_valid():
            updated_sale = form.save(commit=False)
            new_quantity = updated_sale.quantity_sold

            quantity_difference = new_quantity - old_quantity           
            if product.quantity >= quantity_difference:
                product.quantity -= quantity_difference
                product.save()

                updated_sale.save()
                messages.success(request, 'Sale updated successfully.')
            else:
                messages.error(request, 'Not enough stock to update sale.')

        else:
            messages.error(request, 'Invalid form submission.')

    return redirect('sales_list')


@login_required
def delete_sale(request, sale_id):
    sale = get_object_or_404(SalesRecord, id=sale_id)
    product = sale.product
    if request.method == 'POST':

        product.quantity += sale.quantity_sold
        product.save()
        sale.delete()
        messages.success(request, 'Sale deleted and stock restored.')
        return redirect('sales_list')
    return render(request, 'sales.html', {'sale': sale})


@login_required
def stock_list(request):
    stock = StockMovement.objects.all().order_by('-date')
    products = Product.objects.all()


    return render(request, 'stock_movement.html', {
        'stock': stock,
        'products': products,
    })



@login_required
def stock_in(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            product = stock.product

         
            product.quantity += stock.quantity
            product.save()

          
            stock.movement_type = 'In'
            stock.date = timezone.now().date()
            stock.actioned_by = request.user
            stock.save()

            messages.success(request, 'Stock successfully added.')
            return redirect('stock_list')
        else:
            messages.error(request, 'Failed to add stock.')

    return redirect('stock_list')


@login_required
def stock_out(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            product = stock.product


            if product.quantity >= stock.quantity:
                product.quantity -= stock.quantity
                product.save()

               
                stock.movement_type = 'Out'
                stock.date = timezone.now().date()
                stock.actioned_by = request.user
                stock.save()

                messages.success(request, 'Stock successfully removed.')
                return redirect('stock_list')
            else:
                messages.error(request, 'Not enough stock to remove.')

    return redirect('stock_list')



@login_required
def dashboard(request):
  
    total_products = Product.objects.count()
    total_sales = SalesRecord.objects.aggregate(total=Sum('product__price'))['total'] or 0
    current_stock = Product.objects.aggregate(total=Sum('quantity'))['total'] or 0
    low_stock = Product.objects.filter(quantity__lt=10).count()


    today = date.today()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    sales_data = []
    for day in last_7_days:
        total = SalesRecord.objects.filter(date=day).aggregate(Sum('quantity_sold'))['quantity_sold__sum'] or 0
        sales_data.append({'date': day.strftime("%b %d"), 'total': total})

    recent_sales = SalesRecord.objects.select_related('product').order_by('-date')[:3]
    recent_customers = Customer.objects.order_by('-id')[:3]
    low_stock_products = Product.objects.filter(quantity__lt=10)[:3]

    context = {
        'total_products': total_products,
        'total_sales': total_sales,
        'current_stock': current_stock,
        'low_stock': low_stock,
        'sales_data': sales_data,
        'recent_sales': recent_sales,
        'recent_customers': recent_customers,
        'low_stock_products': low_stock_products,
    }

    return render(request, 'dashboard.html', context)





    
