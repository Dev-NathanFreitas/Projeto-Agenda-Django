from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator
from django.db.models import Q
from contact.models import Contact
from django.contrib.auth.decorators import login_required


def contact(request,contact_id):
    #single_contact = Contact.objects.filter(id=contact_id).first()
    single_contact = get_object_or_404(Contact, id=contact_id,show=True)
    contact_name = f'{single_contact.first_name} {single_contact.last_name}'
    context = {
        'contact':single_contact,
        'site_title':f'Agenda: {contact_name}'
    }
    return render(request, 'contact/contact.html', context)


def index(request):
    user = request.user
    
    contacts = Contact.objects.filter(show=True).order_by('id')
    paginator = Paginator(contacts, 10)  

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj,
        'site_title':'Agenda'
    }
    return render(request, 'contact/index.html', context)
    


def search(request):
    search_value = request.GET.get('q','').strip()
    
    
    contacts = Contact.objects.filter(show=True).order_by('id').filter(\
        Q(first_name__icontains = search_value)|
        Q(last_name__icontains=search_value) |
        Q(phone__icontains=search_value)| 
        Q(email__icontains=search_value))
    
    paginator = Paginator(contacts, 10)  

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if search_value == '':
        return redirect('contact:index.html')
    
    context = {
        'page_obj':page_obj,
        'site_title':'Search - Agenda',
        'search_value':search_value
    }
    return render(request, 'contact/index.html', context)

@login_required(login_url='contact:login')
def user_my_contacts(request):
    contacts = Contact.objects.filter(show=True,owner=request.user).order_by('id')
    paginator = Paginator(contacts,10)  
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context ={
        'site_title':'Agenda - My Contacts',
        'page_obj':page_obj,

    }
    
    return render(request,'contact/mycontacts.html',context)