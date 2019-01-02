from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

def home_page(request):
    '''home page'''
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/unique_list_in_the_world/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

def view_list(request):
    """list view"""
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
