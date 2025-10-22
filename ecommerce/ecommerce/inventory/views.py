from django.shortcuts import render, redirect
from .forms import ProductForm, ProductFileForm
from .models import ProductFile, Product

def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        files = request.FILES.getlist('file')  # get multiple files
        if form.is_valid():
            product = form.save(commit=False)
            # ถ้าไม่ใช่ admin ให้บังคับ store เป็นของตัวเอง
            if not request.user.groups.filter(name='Administrator').exists():
                product.store = request.user.store_set.first()
            product = form.save()
            file_type = request.POST.get('file_type', 'image')
            for f in files:
                ProductFile.objects.create(product=product, file=f, file_type=file_type)
            return redirect('product_list')
    else:
        form = ProductForm(user=request.user)
        file_form = ProductFileForm()
    return render(request, 'product_form.html', {'form': form, 'file_form': file_form}) 

def product_edit(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        files = request.FILES.getlist('file')
        if form.is_valid():
            product = form.save()
            file_type = request.POST.get('file_type', 'image')
            for f in files:
                ProductFile.objects.create(product=product, file=f, file_type=file_type)
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
        file_form = ProductFileForm()
    return render(request, 'product_form.html', {'form': form, 'file_form': file_form, 'product': product})
def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
