from django.db.models import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from home.dwaclasses import DwaCommon
from .forms import EV6CreateForm
from .models import EV6, Electrical


def start_page(request):
    return render(request, 'energy/start_page.html')


class Reading(QuerySet):

    def __init__(self, id, date, meter_reading, kwh_net, kwh, solar_balance, ch_total, kwh_cost):
        super().__init__()
        self.id = id
        self.date = date
        self.meter_reading = meter_reading
        self.kwh_net = kwh_net
        self.kwh = kwh
        self.solar_balance = solar_balance
        self.ch_total = ch_total
        self.kwh_cost = kwh_cost

    def __str__(self):
        list_representation = (f"id: {self.id}; date: {self.date}; kwh: {self.kwh}; cost: {self.ch_total};"
                               f" kwh_net: {self.kwh_net}; solar_balance: {self.solar_balance};"
                               f" kwh_cost: {self.kwh_cost}")
        return list_representation

class ElectricalList(ListView):
    model = Electrical
    template_name = 'energy/electrical_list.html'

    def get_queryset(self):
        """Return the Electrical objects."""
        print(f"\nIn ElectricalList:get_queryset ")
        print("getting objects")
        objects = Electrical.objects.all().order_by('date')
        print(f"got objects; type {type(objects)}")
        object_list = []
        prev_meter = 0
        for object in objects:
            meter_reading = object.meter_reading
            if meter_reading > 90000 and prev_meter < 90000:
                meter_reading = meter_reading - 100000
            if meter_reading < 90000 and prev_meter > 90000:
                meter_reading = meter_reading + 100000
            object.kwh_net = meter_reading - prev_meter
            prev_meter = object.meter_reading
            object.kwh_cost = 0
            if object.kwh > 0:
                object.kwh_cost = round(object.ch_total / object.kwh, 2)
            print(f"object: {object}")
            reading = Reading(object.id, object.date, object.meter_reading, object.kwh_net, object.kwh
                              , object.solar_balance, object.ch_total, object.kwh_cost)
            object_list.append(reading)
        object_list.reverse()
        for object in object_list:
            print(f"object: {object}")
        return object_list


class ElectricalDetailView(DetailView):
    model = Electrical


class ElectricalCreate(DwaCommon, CreateView):
    model = Electrical
    fields = '__all__'

    def form_valid(self, form):
        print("*** ElectricalCreate:form_valid enter\n")
        return self.dwa_form_valid_save(form)


class ElectricalUpdate(DwaCommon, UpdateView):
    model = Electrical
    fields = '__all__'

    def form_valid(self, form):
        print("*** ElectricalUpdate:form_valid enter\n")
        return self.dwa_form_valid_save(form)


class ElectricalDelete(DeleteView):
    model = Electrical
    success_url = reverse_lazy('energy:electrical_list')


class EV6ListMPG(ListView):
    model = EV6
    template_name = 'energy/ev6_mpg.html'

    def get_queryset(self):
        obj_last = None
        objs = []
        object_list = EV6.objects.all().order_by('odometer')
        print(f"EV6ListMPG::get_queryset type {type(object_list)}")
        for obj in object_list:
            print(f"object: {obj}")
            if obj_last is not None:
                if obj.full_charge and obj_last.full_charge and obj.kwh > 0:
                    delta_miles = obj.odometer - obj_last.odometer
                    miles_kwh = round(delta_miles / obj.kwh, 1)
                    print(f"delta_miles: {delta_miles}, miles_kwh: {miles_kwh}")
                    obj.kwh = round(obj.kwh, 1)
                    obj.delta_miles = delta_miles
                    obj.miles_kwh = miles_kwh
                    obj.mpge = int(float(obj.miles_kwh) * 33.7)
                    objs.append(obj)
            obj_last = obj
        objs.reverse()
        print(objs)
        return objs


class EV6List(ListView):
    model = EV6

    def get_queryset(self):
        object_list = EV6.objects.all().order_by('-odometer')
        print(f"EV6List::get_queryset type {type(object_list)}")
        for obj in object_list:
            print(f"object: {obj}")
        return object_list


class EV6Create(CreateView):
    model = EV6
    form_class = EV6CreateForm


class EV6Update(UpdateView):
    model = EV6
    fields = '__all__'
