import csv
from datetime import date

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from home.dwaclasses import DwaCommon
from .forms import AddressCreateForm, AddressUpdateForm, MovieCreateForm, MovieUpdateForm
from .models import DwaAddr, Movie


@login_required
def start_page(request):
    return render(request, 'myaddr/start_page.html')


def login(request):
    return render(request, 'myaddr/start_page.html')


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out")
    print(f"*** logout **** request: {request}")
    return render(request, 'myaddr/start_page.html')


class MovieList(ListView):
    model = Movie
    template_name = 'myaddr/movie_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        """Return the address objects."""
        print(f"\nMovieList::get_queryset")
        objects = Movie.objects.all().order_by('-date')
        return objects


class MovieCreate(DwaCommon, CreateView):
    model = Movie
    template_name = 'myaddr/movie_form.html'
    form_class = MovieCreateForm

    def form_valid(self, form):
        print("*** MovieCreate:form_valid enter\n")
        model = form.save(commit=False)
        model.date = date.today()
        return self.dwa_form_valid_save(form)


class MovieUpdate(DwaCommon, UpdateView):
    model = Movie
    template_name = 'myaddr/movie_form.html'
    form_class = MovieUpdateForm

    def get(self, request, *args, **kwargs):
        print(f"{request=}; {args=}; {kwargs=}")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        print("*** MovieUpdate:form_valid enter\n")
        return self.dwa_form_valid_save(form)


class MovieDelete(DeleteView):
    model = Movie
    success_url = reverse_lazy('myaddr:movie_list')


def export_all_addresses(request):
    print(f"\n*** export_donations ***")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="myaddr.csv"'

    writer = csv.writer(response)
    columns = ['lastname', 'xmas', 'status', 'addr_name', 'addrline1', 'addrline2', 'city', 'state', 'postalcode',
               'email', 'phone1', 'phone2']
    writer.writerow(columns)
    addresses = DwaAddr.objects.all().values_list(*columns).order_by('lastname').filter(archive='N')
    for address in addresses:
        print(f"address: {address}")
        writer.writerow(address)
    return response


def export_xmas(request):
    print(f"\n*** export_xmas ***")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="myaddr.csv"'

    writer = csv.writer(response)
    columns = ['lastname', 'addr_name', 'addrline1', 'addrline2', 'city', 'state', 'postalcode']
    writer.writerow(columns)
    addresses = DwaAddr.objects.all().values_list(*columns).order_by('lastname').filter(archive='N', xmas='Y')
    for address in addresses:
        print(f"address: {address}")
        writer.writerow(address)
    return response


def export_status_addresses(request):
    print(f"\n*** export_status_addresses ***")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="myaddr.csv"'

    writer = csv.writer(response)
    columns = ['addr_name', 'addrline1', 'addrline2', 'city', 'state', 'postalcode', 'email', 'phone1', 'phone2']
    writer.writerow(columns)
    addresses = DwaAddr.objects.all().values_list(*columns).order_by('lastname').filter(archive='N', status='Y')
    for address in addresses:
        print(f"address: {address}")
        writer.writerow(address)
    return response


def load_addresses(request):
    prefix = request.GET.get('prefix')

    print(f"load_addresses::request.GET: {request.GET}")
    print(f"load_addresses::prefix: {prefix}")
    if prefix == '*':
        addresses = DwaAddr.objects.all().order_by('lastname')
    else:
        addresses = DwaAddr.objects.filter(lastname__istartswith=prefix, archive='N').order_by('lastname')[:10]
    print(f"load_addresses::addresses: {addresses}")
    return render(request, 'myaddr/address_list_options.html', {'addresses': addresses})


class CreateAddressList(ListView):
    model = DwaAddr
    template_name = 'myaddr/address_list.html'
    context_object_name = 'object_list'


class AddrDetailView(DetailView):
    model = DwaAddr


class AddrCreate(DwaCommon, CreateView):
    model = DwaAddr
    template_name = 'myaddr/movie_form.html'
    form_class = AddressCreateForm

    def form_valid(self, form):
        print("*** AddrCreate:form_valid enter\n")
        return self.dwa_form_valid_save(form)


class AddrUpdate(DwaCommon, UpdateView):
    model = DwaAddr
    template_name = 'myaddr/movie_form.html'
    form_class = AddressUpdateForm

    def get(self, request, *args, **kwargs):
        print(f"{request=}; {args=}; {kwargs=}")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        print("*** AddrUpdate:form_valid enter\n")
        return self.dwa_form_valid_save(form)


class AddrDelete(DeleteView):
    model = DwaAddr
    success_url = reverse_lazy('myaddr:myaddr_list')
