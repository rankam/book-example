from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html')


def new_list(request):
    list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list)
    return redirect('/lists/%d/' % (list.id,))


def view_list(request, list_id):
    list = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list})


def add_item(request, list_id):
    list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list)
    return redirect('/lists/%d/' % (list.id,))
