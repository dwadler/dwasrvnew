import csv
from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Inches

from home.dwaclasses import DwaCommon
from .forms import ScheduleForm, VolunteerCreateForm, VolunteerUpdateForm, ProviderUpdateForm, ProviderCreateForm
from .models import Volunteer, Schedule, Provider
from .utils import fix_phone_db
from .views_volunteer import recent_volunteers


def start_page(request):
    return render(request, 'dbsk/start_page.html')


@login_required
def login(request):
    return render(request, 'dbsk/start_page.html')


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out")
    print(f"*** logout **** request: {request}")
    return render(request, 'dbsk/start_page.html')


def fix_phone(request):
    fix_phone_db()
    return render(request, 'dbsk/start_page.html')


def get_email_message(v):
    message = f"Dear volunteer:"
    message += f"\nWe are trying new methods of communicating with our volunteers and "
    message += f"are sending this to all active or semi-active volunteers in our database."
    message += f"\nPlease reply indicating:"
    message += f"\n- That you received this and whether you are still an active volunteer."
    message += f"\n- Whether you would prefer reminders via phone, text or e-mail."
    message += f"\n- If the following information is correct. Please provide address if not specified."
    message += f"\n-- Name {v.firstname} {v.lastname}"
    message += f"\n-- Address: {v.addr1}, {v.city}, {v.state} {v.zip}"
    message += f"\n-- E-mail: {v.email}"
    message += f"\n-- Phone1: {v.phone1}"
    message += f"\n-- Phone2: {v.phone2}"
    message += f"\n\nThank you"
    message += f"\n\nDavid Adler - DBSK treasurer and IT guy"
    message += "f\n\nPlease ignore any duplicate messages - still testing."

    return message


class CantVolunteer(ListView):
    model = Volunteer
    template_name = 'dbsk/cantVolunteer.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        """Return the volunteer objects."""
        # order is set by Volunteer model
        volunteers = recent_volunteers()
        return volunteers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        volunteers = context['object_list']
        messages = []
        for v in volunteers:
            m = f"{v.firstname} {v.lastname} phone: {v.phone1}"
            messages.append(m)
        context['messages'] = messages
        timenow = datetime.now()
        context['timenow'] = timenow
        print(f"\n*** in AddrList::get_context_data; timenow: {timenow}; context: {context}")
        return context


class VolunteerEmail(ListView):
    model = Volunteer
    template_name = 'dbsk/volunteer_email.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        """Return the volunteer objects."""
        # order is set by Volunteer model
        volunteers = Volunteer.objects.all().order_by('lastname').filter(archive='N')
        return volunteers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        volunteers = context['object_list']
        messages = []
        for v in volunteers:
            if v.email is None or len(v.email) < 12:
                m = f"{v.firstname} {v.lastname} doesn't have e-mail"
            #            elif v.lastname != 'Adler':
            #                m = f"skipping {v.firstname} {v.lastname} e-mail: {v.email}"
            else:
                m = f"e-mail to {v.firstname} {v.lastname} e-mail: {v.email}"
                subject = "Message from Daily Bread Soup Kitchen"
                message = get_email_message(v)
                email_from = 'dbskclc@gmail.com'
                print(f'sending e-mail to {v.email}')
            #                send_mail(subject, message, email_from, [v.email])
            messages.append(m)
        context['messages'] = messages
        timenow = datetime.now()
        context['timenow'] = timenow
        print(f"\n*** in AddrList::get_context_data; timenow: {timenow}; context: {context}")
        return context


class VolunteerList(generic.ListView):
    model = Volunteer
    template_name = 'dbsk/volunteer_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        """Return the volunteer objects."""
        # order is set by Volunteer model
        volunteers = Volunteer.objects.all()
        return volunteers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timenow = datetime.now()
        context['timenow'] = timenow
        print(f"\n*** in AddrList::get_context_data; timenow: {timenow}; context: {context}")
        return context


class VolunteerUpdateView(DwaCommon, UpdateView):
    model = Volunteer
    form_class = VolunteerUpdateForm

    def form_valid(self, form):
        return self.dwa_form_valid_save(form)


class VolunteerCreateView(DwaCommon, CreateView):
    model = Volunteer
    form_class = VolunteerCreateForm

    def form_valid(self, form):
        print("*** ClcServerUpdateView:form_valid enter")
        return self.dwa_form_valid_save(form)


class VolunteerDeleteView(DeleteView):
    model = Volunteer
    success_url = reverse_lazy('dbsk:volunteer_list')


def export_volunteers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="volunteers.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['First name', 'Last name', 'phone1', 'availability', 'notes', 'addr1', 'addr2', 'city', 'state', 'zip',
         'phone2', 'email'])

    volunteers = Volunteer.objects.all().values_list('firstname', 'lastname', 'phone1', 'availability', 'notes',
                                                     'addr1', 'addr2', 'city', 'state', 'zip', 'phone2', 'email')
    for volunteer in volunteers:
        writer.writerow(volunteer)
    return response


def export_volunteers_docx(request):
    volunteers = Volunteer.objects.all().order_by('lastname')

    doc = Document()
    section = doc.sections[0]
    footer = section.footer
    doc.add_heading('Daily Bread Soup Kitchen - Volunteers', 0)
    today = date.today()
    documentDate = today.strftime('%B %d %Y')
    paragraph = footer.paragraphs[0]
    paragraph.text = f'Report generated on {documentDate}'

    style = doc.styles.add_style('Cell', WD_STYLE_TYPE.PARAGRAPH)
    paragraph_format = style.paragraph_format
    paragraph_format.space_before = Inches(0.25)
    paragraph_format.space_after = Inches(0.0)

    doc.add_paragraph('Values for Availability:', style='Cell')

    doc.add_paragraph('X - not available', style='List Bullet')
    doc.add_paragraph('W - available Wednesday', style='List Bullet')
    doc.add_paragraph('-W - not available Wednesday (precede with minus sign)', style='List Bullet')
    doc.add_paragraph('1W - available first Wednesday', style='List Bullet')
    doc.add_paragraph('1W, 3F - available first Wednesday, third Friday', style='List Bullet')
    doc.add_paragraph('Follow pattern above for other days and combinations', style='List Bullet')

    table = doc.add_table(rows=0, cols=2)
    doc.add_paragraph(' ')

    for v in volunteers:
        row_cells = table.add_row().cells

        cell1 = v.lastname + ', ' + v.firstname
        if v.addr1 is not None:
            cell1 += '\n' + v.addr1
        if v.addr2 is not None:
            cell1 += '\n' + v.addr2
        if v.city is not None:
            cell1 += '\n' + v.city + ', ' + v.state + ' ' + v.zip

        cell2 = v.phone1
        if v.phone2 is not None:
            cell2 += '\n' + v.phone2
        if v.email is not None:
            cell2 += '\n' + v.email
        if v.availability is not None:
            cell2 += f'\nAvailability: {v.availability}'
        if v.notes is not None:
            cell2 += f'\nNotes: {v.notes}'

        row_cells[0].text = cell1
        row_cells[1].text = cell2

    doc.save('volunteers.docx')
    with open('volunteers.docx', 'rb') as fh:
        response = HttpResponse(fh, content_type='application/docx')
    response['Content-Disposition'] = 'attachment; filename="volunteers.docx"'
    return response


class ScheduleList(generic.ListView):
    model = Schedule
    context_object_name = 'schedule_list'
    queryset = Schedule.objects.all().order_by("-schedule_date")


class ScheduleDetailView(DetailView):
    model = Schedule


class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'dbsk/schedule_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #  print (f" ******** in ScheduleUpdateView::get_context_data; context: {context}")
        schedule = context['schedule']
        #  print (f" ******** in ScheduleUpdateView::get_context_data; schedule: {schedule}")
        schedule_date = schedule.schedule_date
        date_string = schedule_date.strftime("%A %B %d %Y")
        #  print (f'*** ScheduleUpdateView:get_context_data date_string: {date_string}')
        context['date_string'] = date_string
        schedule_month = f"month={schedule_date.year}-{schedule_date.month}"
        context['schedule_month'] = schedule_month
        #  print (f'*** ScheduleUpdateView:get_context_data schedule_month: {schedule_month}')
        print(f"**** ScheduleUpdateView::get_context_data;context: {context}")
        return context

    def form_valid(self, form):
        print("*** ScheduleUpdateView:form_valid enter\n")
        model = form.save(commit=False)
        model.updateby = f"{self.request.user}"
        model.lastupdate = datetime.now()
        model.save()
        print(f"model: {model}")
        success_url = reverse('dbsk:schedule') + f'?month={model.schedule_date.year}-{model.schedule_date.month}'
        print(f"*****In ScheduleUpdateView::form_valid, success_url: {success_url}")
        return HttpResponseRedirect(success_url)


class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleForm

    def get(self, request, *args, **kwargs):
        test_form = ScheduleForm(data=request.GET)
        print(f'*** ScheduleCreateView:get test_form.data: {test_form.data}')
        schedule_date = datetime.strptime(test_form.data['schedule_date'], '%Y-%m-%d')
        date_string = schedule_date.strftime("%A %B %d %Y")
        print(f'*** ScheduleCreateView:get date_string: {date_string}')
        schedule_month = f"month={schedule_date.year}-{schedule_date.month}"
        test_form.is_valid()
        form = ScheduleForm(initial=test_form.cleaned_data)
        return render(request, 'dbsk/schedule_form.html', {'form': form,
                                                           'schedule_month': schedule_month,
                                                           'date_string': date_string})

    def form_valid(self, form):
        print("*** ScheduleCreateView:form_valid enter")
        model = form.save(commit=False)
        print(f"model: {model}")
        model.s_year = model.schedule_date.year
        model.s_month = model.schedule_date.month
        model.s_day = model.schedule_date.day
        model.updateby = f"{self.request.user}"
        model.lastupdate = datetime.now()
        model.save()
        success_url = reverse('dbsk:schedule') + f'?month={model.schedule_date.year}-{model.schedule_date.month}'
        print(f"*****In ScheduleCreateView::form_valid, success_url: {success_url}")
        return HttpResponseRedirect(success_url)


class ScheduleDeleteView(DeleteView):
    model = Schedule
    success_url = reverse_lazy('dbsk:schedule_list')


class ProviderList(generic.ListView):
    model = Provider
    context_object_name = 'object_list'

    def get_queryset(self):
        """Return the providers - ordering specified in model"""
        return Provider.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timenow = datetime.now()
        context['timenow'] = timenow
        print(f"\n*** in AddrList::get_context_data; timenow: {timenow}; context: {context}")
        return context


class ProviderDetailView(DetailView):
    model = Provider


class ProviderUpdateView(DwaCommon, UpdateView):
    model = Provider
    form_class = ProviderUpdateForm

    def form_valid(self, form):
        print("*** ProviderUpdateView:form_valid enter")
        return self.dwa_form_valid_save(form)


class ProviderCreateView(DwaCommon, CreateView):
    model = Provider
    form_class = ProviderCreateForm

    def form_valid(self, form):
        print("*** ProviderCreateView:form_valid enter")
        return self.dwa_form_valid_save(form)


class ProviderDeleteView(DeleteView):
    model = Provider
    success_url = reverse_lazy('dbsk:provider')

    def delete(self, request, *args, **kwargs):
        pk = kwargs['pk']
        print(f"Deleting provider with key: {pk}")
        response = super(ProviderDeleteView, self).delete(request, *args, **kwargs)
        return response


def export_providers_csv(request):
    print(f"\n*** export_providers_csv ***")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="providers.csv"'

    writer = csv.writer(response)
    columns = ['id', 'provider_name', 'contact_name', 'preferred_day', 'addr1', 'addr2', 'city', 'state', 'zip',
               'phone1', 'phone2', 'email', 'notes', 'status', 'archive']
    writer.writerow(columns)

    providers = Provider.objects.all().values_list(*columns).order_by('provider_name').filter(archive='N')
    #    providers = Provider.objects.all().order_by('provider_name').filter(archive='N')
    #    print(f"*** export_providers_csv; providers: {providers} ***")
    #    providers = providers.values_list(*columns)
    #    print(f"*** export_providers_csv; providers: {providers} ***")
    idx = 1
    for provider in providers:
        print(f"*** export_providers_csv; idx: {idx}; provider: {provider[0:2]} ***")
        idx += 1
        writer.writerow(provider)
    return response


def provider_schedule_labels(request):
    print(f"\n*** provider_schedule_labels ***")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="provider_schedule.csv"'

    writer = csv.writer(response)
    columns = ['id', 'provider_name', 'contact_name', 'preferred_day', 'addr1', 'addr2', 'city', 'state', 'zip',
               'status']
    writer.writerow(columns)
    monthSchedule = Schedule.objects.all().filter(s_month=11)
    for item in monthSchedule:
        print(f"*** provider_schedule_labels: item")

    providers = Provider.objects.all().values_list(*columns).order_by('provider_name').filter(archive='N', status='A')
    idx = 1
    for provider in providers:
        print(f"*** export_providers_csv; idx: {idx}; provider: {provider[0:2]} ***")
        idx += 1
        writer.writerow(provider)
    return response
