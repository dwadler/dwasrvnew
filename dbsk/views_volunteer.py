import calendar
import copy
from datetime import date, datetime, timedelta

from django.core.mail import send_mail
from django.shortcuts import render

from .forms import VolunteerReportForm, MessageInputForm, SMSAllowForm
from .models import Schedule
from .utils import send_sms


def get_schedules(startDate, endDate):
    schedules = Schedule.objects.all().order_by('id').filter(schedule_date__gte=startDate, schedule_date__lte=endDate)
    return schedules


def volunteers_for_period(startDate, endDate):
    schedules = get_schedules(startDate, endDate)
    volunteers = []
    for s in schedules:
        if s.volunteer1 not in volunteers:
            volunteers.append(s.volunteer1)
        if s.volunteer2 not in volunteers:
            volunteers.append(s.volunteer2)
    return volunteers


def recent_volunteers():
    # should target active volunteers
    # picking volunteers for last 4 months
    today = datetime.now()
    year = today.year
    month = today.month
    startDate = today + timedelta(days=-120)
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    #    startDate = date(year, month, 1)
    endDate = date(2030, 1, 1)  # everyone from this month on
    volunteers = volunteers_for_period(startDate, endDate)
    for v in volunteers:
        if v.phone1 is None or len(v.phone1) < 8:
            volunteers.remove(v)
    return volunteers


def send_reminders(request):
    messages = ["Reminders sent:"]
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    startDate = tomorrow
    endDate = tomorrow
    email_from = 'dbskclc@gmail.com'
    volunteers = volunteers_for_period(startDate, endDate)
    #    volunteers = Volunteer.objects.all().order_by('id').filter(lastname='Adler', firstname='David')
    print(f"send_reminders for {tomorrow}")
    for v in volunteers:
        if v.phone1 is None or len(v.phone1) < 8:
            continue
        subject = f"Friendly DBSK reminder for {v.firstname} on {tomorrow}."
        message = "Thank you for volunteering!\n"
        message = message + ("If you are unable to volunteer as scheduled, please check this link: "
                             "http://clc.dynalias.org:81/dbsk/cantvolunteer"
                             )
        if v.email is not None and len(v.email) > 10:
            try:
                send_mail(subject, message, email_from, [v.email])
                m = f"e-mail sent to {v.email}"
            except Exception as e:
                m = f"e-mail to {v.email} failed. {e}"
        else:
            m = f"No e-mail for {v.firstname} {v.lastname}"
        print(m)
        messages.append(m)
        if v.preferred_contact == 'T':
            try:
                message = f"{subject}\n{message}"
                send_sms(v.phone1, message)
                m = f"text sent to {v.phone1}"
            except Exception as e:
                m = f"SMS to {v.phone}, {v.firstname} {v.lastname} failed. {e}"
        else:
            m = f"No text to {v.firstname} {v.lastname}"
        print(m)
        messages.append(m)
    print(f"len(messages): {len(messages)}")
    if len(messages) > 2:
        messages2 = ""
        for m in messages:
            messages2 += f"{m}\n"
        print(f"sendreminder: {messages2}")
        cc_mail = ['dbskclc@gmail.com']
        subject = f"reminders sent {today}"
        try:
            send_mail(subject, messages2, email_from, cc_mail)
            m = f"e-mail sent to {cc_mail}"
        except Exception as e:
            m = f"e-mail to {cc_mail} failed. {e}"
        print(m)
        try:
            davidPhone = '(845)594-2721'
            message = f"{subject}\n{messages2}"
            send_sms(davidPhone, message)
            print(f"text sent to {davidPhone}")
        except Exception as e:
            print(f"SMS to {davidPhone} failed. {e}")

    print(f"messages: {messages}")
    context = dict(messages=messages, timenow=datetime.now())
    return render(request, 'dbsk/start_page.html', context)


def email_blast(request):
    messages = []
    debug = False
    email_from = 'dbskclc@gmail.com'
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = MessageInputForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            data = form.cleaned_data
            messageText = data['messageText']
            subject = data['subject']
            volunteers = recent_volunteers()
            for v in volunteers:
                if v.email is None or len(v.email) < 12:
                    m = f"{v.firstname} {v.lastname} doesn't have e-mail"
                elif v.email != 'dadler@christwoodstock.org' and debug == True:
                    m = f"skipping {v.firstname} {v.lastname} e-mail: {v.email}"
                else:
                    m = f"e-mail to {v.firstname} {v.lastname} e-mail: {v.email}"
                    print(f'sending e-mail to {v.email}')
                    send_mail(subject, messageText, email_from, [v.email])
                if v.preferred_contact == 'T':
                    text_phone = v.phone1
                    try:
                        if v.email == 'dadler@christwoodstock.org':
                            rc = send_sms(text_phone, messageText)
                            print(rc)
                    except Exception as e:
                        print(e, e.args)
                messages.append(m)
            context = dict(form=form, messages=messages, timenow=datetime.now())
            return render(request, 'dbsk/start_page.html', context)

    # If this is a GET (or any other method) create the default form.
    else:  # GET
        volunteers = recent_volunteers()
        for v in volunteers:
            textPhone = ''
            if v.preferred_contact == 'T':
                textPhone = v.phone1
            message = [f'{v.lastname}, {v.firstname}', v.phone1, v.email, textPhone]
            messages.append(message)
        messages = sorted(messages, key=lambda x: str(x[0]))
        header = ['Name', 'Phone', 'E-mail', 'Text Phone']
        messages.insert(0, header)
        form = MessageInputForm()
        context = dict(form=form, messages=messages, timenow=datetime.now())
        return render(request, 'dbsk/volunteer_email_message.html', context)


def volunteer_report_generate(schedules):
    messages = []
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    served0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #        monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
    for idx in range(12):
        months[idx] = calendar.month_name[idx + 1]
    vReport = {' Volunteer': months}
    for s in schedules:
        v1 = s.volunteer1
        v2 = s.volunteer2
        name1 = f'{v1.lastname}, {v1.firstname}'
        name2 = f'{v2.lastname}, {v2.firstname}'
        if name1 not in vReport:
            vReport[name1] = copy.copy(served0)
        served = vReport[name1]
        month = s.s_month
        served[month - 1] += 1
        vReport[name1] = served
        #            print(name1, served)
        if name2 not in vReport:
            vReport[name2] = copy.copy(served0)
        served = vReport[name2]
        month = s.s_month
        served[month - 1] += 1
        vReport[name2] = served
    #            print(name2, served)
    for key in vReport:
        columns = [key]
        values = vReport[key]
        for idx in range(12):
            columns.append(values[idx])
        message = columns
        messages.append(message)
    #       print(message)
    messages = sorted(messages, key=lambda x: str(x[0]))
    #    print(messages)
    return messages


def volunteer_report(request):
    # If this is a POST request then process the Form data
    context = None
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = VolunteerReportForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            data = form.cleaned_data
            startDate = data['startDate']
            endDate = data['endDate']
            schedules = get_schedules(startDate, endDate)
            messages = volunteer_report_generate(schedules)
            context = {
                'form': form,
                'messages': messages,
                'timenow': datetime.now()
            }
    # If this is a GET (or any other method) create the default form.
    else:
        startDate = date(2023, 10, 1)
        endDate = date(2023, 10, 31)
        schedules = get_schedules(startDate, endDate)
        form = VolunteerReportForm()
        context = {
            'form': form,
            'timenow': datetime.now()
        }

    return render(request, 'dbsk/volunteer_report.html', context)


def volunteers_in_month(request):
    # If this is a POST request then process the Form data
    context = None
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = VolunteerReportForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            data = form.cleaned_data
            startDate = data['startDate']
            endDate = data['endDate']
            schedules = get_schedules(startDate, endDate)
            messages = volunteer_report_generate(schedules)
            context = {
                'form': form,
                'messages': messages,
                'timenow': datetime.now()
            }
    # If this is a GET (or any other method) create the default form.
    else:
        startDate = datetime.date(2023, 10, 1)
        endDate = datetime.date(2023, 10, 31)
        form = VolunteerReportForm()
        context = {
            'form': form,
            'timenow': datetime.now()
        }

    return render(request, 'dbsk/volunteer_report.html', context)


def sms_allow(request):
    # If this is a POST request then process the Form data
    context = None
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SMSAllowForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            data = form.cleaned_data
            name = data['name']
            phoneNumber = data['phoneNumber']
            allowSMS = data['smsAllow']
            screenJPG = 'https://ibb.co/RDjs1qp'
            return render(request, 'dbsk/start_page.html', context)
    # If this is a GET (or any other method) create the default form.
    else:

        form = SMSAllowForm()
        context = {
            'form': form,
            'name': 'David Adler',
            'phone': '845-594-2721'
        }

    return render(request, 'dbsk/sms_allow.html', context)
