from django.shortcuts import render, redirect
from .forms import ProductForm, ProductFileForm
from .models import ProductFile, Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages

def product_create_or_edit(request, pk=None):
    product = get_object_or_404(Product, pk=pk) if pk else None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        delete_files = request.POST.getlist('delete_files')  # IDs of existing files to delete
        if form.is_valid():
            product = form.save()

            # delete old files
            for file_id in delete_files:
                f = ProductFile.objects.filter(id=file_id, product=product).first()
                if f:
                    f.file.delete(save=False)
                    f.delete()

            # save new files
            for f in request.FILES.getlist('file'):
                ProductFile.objects.create(product=product, file=f)

            return redirect('product_list')
    else:
        form = ProductForm(instance=product, user=request.user)

    # ไฟล์เก่า สำหรับ preview
    existing_files = product.files.all() if product else []

    return render(request, 'product_form.html', {
        'form': form,
        'existing_files': existing_files,
        'product': product,
    })

def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

@login_required
def product_add_file(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        files = request.FILES.getlist('files')
        if not files:
            messages.warning(request, "Please select at least one file.")
            return redirect('product_add_file', pk=pk)

        for f in files:
            ProductFile.objects.create(product=product, file=f)

        messages.success(request, f"Added {len(files)} file(s) to {product.name}.")
        return redirect('product_list')

    return render(request, 'product_add_file.html', {'product': product})

def product_list_view(request):
    products = Product.objects.prefetch_related('files').all()
    return render(request, 'product_list.html', {'products': products})

    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_view')