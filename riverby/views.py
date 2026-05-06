import csv

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from home.dwaclasses import DwaCommon
from .forms import RiverbyCreateForm, RiverbyUpdateForm
from .models import Address


@login_required
def start_page(request):
    return render(request, 'riverby/start_page.html')


def export_rhha_addresses(request):
    print(f"\n*** export_donations ***")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rhha-addr.csv"'

    writer = csv.writer(response)
    columns = ['rd_section', 'fire_num', 'addr_name1', 'addr_name2', 'addr_line1', 'addr_line2', 'city', 'state', 'zip']
    writer.writerow(columns)
    addresses = Address.objects.all().values_list(*columns).order_by('rd_section', 'fire_num').filter(rhha=True,
                                                                                                      archive=False)
    for address in addresses:
        print(f"address: {address}")
        writer.writerow(address)
    return response


class AddrList(DwaCommon, generic.ListView):

    #    def get(self, request, *args, **kwargs):
    #        return self.dwa_get_limited(request, *args, **kwargs)

    def get_queryset(self):
        """Return the address objects."""
        print(f"\n***AddrList:get_queryset ")
        objects = Address.objects.all().order_by('rd_section', 'fire_num').filter(archive=False)
        #        for object in objects:
        #            print (f"object: '{object}'; {vars(object)}")
        return objects


class RhhaList(AddrList):
    def get_queryset(self):
        """Return the address objects."""
        print(f"\nRhhaList:get_queryset")
        objects = Address.objects.all().order_by('rd_section', 'fire_num').filter(rhha=True, archive=False)
        return objects


class AddrDetailView(generic.DetailView):
    model = Address


class AddrCreate(DwaCommon, CreateView):
    model = Address
    template_name = 'riverby/address_form.html'
    form_class = RiverbyCreateForm

    def form_valid(self, form):
        print("*** AddrCreate:form_valid enter\n")
        return self.dwa_form_valid_save(form)


class AddrUpdate(DwaCommon, UpdateView):
    model = Address
    template_name = 'riverby/address_form.html'
    form_class = RiverbyUpdateForm

    def form_valid(self, form):
        print("\n*** AddrUpdate:form_valid enter\n")
        return self.dwa_form_valid_save(form)


class AddrDelete(DeleteView):
    model = Address
    success_url = reverse_lazy('riverby:address_list')


class AddrNewOwner(DwaCommon, UpdateView):
    model = Address
    template_name = 'riverby/address_form.html'
    form_class = RiverbyUpdateForm

    def form_valid(self, form):
        original_owner = Address.objects.all().filter(pk=self.object.pk)[0]
        print(f"={original_owner.pk}")
        clone = original_owner
        print(f"={clone}")
        clone.pk = None
        clone._state.adding = True
#       original_model.archive = True
        clone.billable = False
        clone  .lastupdate = datetime.now()
        clone.save()
        print("\n*** AddrUpdate:form_valid enter\n")
        return self.dwa_form_valid_save(form)