import re
from calendar import HTMLCalendar
from datetime import datetime

from django.shortcuts import render
from twilio.rest import Client

from .models import Schedule, Volunteer


def sms_test(request):
    print(f"sms_test:: testing")
    messages = ["sms_test:: testing"]
    message = send_sms('(845)594-2721', "test message")
    messages.append(message)
    context = dict(messages=messages, timenow=datetime.now())
    return render(request, 'dbsk/start_page.html', context)


def send_sms(textPhone, messageText):
    # twilio code
    account_sid = 'AC08260cb8c35087ac00c7bfb2e528482f'
    auth_token = 'f6471f809d207ae4756116f717f01c53'
    client = Client(account_sid, auth_token)
    formattedPhone = format_phone(textPhone)
    print(f'formatted phone#: {formattedPhone}')
    #    formattedPhone = '+18455942721'
    message = client.messages.create(
        body=messageText,
        from_='+18557601617',
        to=formattedPhone
    )

    print(f"send_sms:: textphone#: {textPhone}, formatted phone#: {formattedPhone}, message: {message}")
    return message


def format_phone(inPhoneNumber):
    if inPhoneNumber is None:
        return inPhoneNumber
    formattedNumber = s = re.sub(r'\W+', '', inPhoneNumber)
    if (len(formattedNumber) == 7):
        formattedNumber = '845' + formattedNumber
    formattedNumber = '+1' + formattedNumber
    if (len(formattedNumber) != 12):
        formattedNumber = 'None'
    return formattedNumber


def format_phone2(inPhoneNumber):
    if inPhoneNumber is None:
        return 'None'
    fn = s = re.sub(r'\W+', '', inPhoneNumber)
    if (len(fn) == 7):
        fn = '845' + fn
    fn = '(' + fn[0:3] + ') ' + fn[3:6] + '-' + fn[6:10]

    if (len(fn) != 14):
        fn = 'None'
    return fn


def fix_phone(inPhoneNumber):
    if inPhoneNumber is None:
        return "None"
    if len(inPhoneNumber) <= 7:
        return "None"
    print(f"inPhoneNumber: '{inPhoneNumber}'")
    first = re.search(r'\d', inPhoneNumber).span()[0]
    print(f'first: {first}')
    last = len(inPhoneNumber) - re.search(r'\d', inPhoneNumber[::-1]).span()[0]
    print(f'last: {last}')
    prefix = inPhoneNumber[0:first]
    number = inPhoneNumber[first:last]
    number = format_phone2(number)
    suffix = inPhoneNumber[last:]
    print(f'{prefix}:{number}:{suffix}')
    return number


def fix_phone_db():
    volunteers = Volunteer.objects.all()
    for volunteer in volunteers:
        fixed_phone1 = fix_phone(volunteer.phone1)
        volunteer.phone1 = fixed_phone1
        fixed_phone2 = fix_phone(volunteer.phone2)
        volunteer.phone2 = fixed_phone2
        print(volunteer.lastname, volunteer.phone1, fixed_phone1, fixed_phone2)
        volunteer.save()


# fix_phone_db()


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        print("***** initializing Calendar *****")
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, weekday):
        #       junk = f'year: {self.year}; month: {self.month}; day: {day}; weekday: {weekday}'
        date = f'{self.year}-{self.month}-{day}'
        #       print (date)
        #       events_per_day = Schedule.objects.filter(s_year = self.year, s_month = self.month, s_day=day)
        events_per_day = Schedule.objects.filter(schedule_date__year=self.year, schedule_date__month=self.month,
                                                 schedule_date__day=day)

        d = ''
        if (weekday == 0) or (weekday == 2) or (weekday == 4):
            d = f'<a href="createschedule?schedule_date={date}">Create schedule</a>'

        for event in events_per_day:
            d = f'<a href="schedule/{event.id}/update">'
            d += f'{event.provider}'
            d += f'<br>{event.volunteer1}'
            d += f'<br>{event.volunteer2}'
            if (event.notes is not None) and (len(event.notes) > 1):
                d += f'<br>Note: {event.notes}'
            d += '</a>'
        #           print (d)
        if day != 0:
            return f"<td><span class='date'>{day}</span><br>{d}&nbsp;</td\n>"
        return '<td>&nbsp;\n</td>'

    # formats a week as a tr 
    def formatweek(self, theweek):
        #       print ("******** in formatweek")
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, weekday)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        print("******** in formatmonth now")
        cal = f'<table border="1" cellpadding="0" cellspacing="0" class="calendar">\n'
        #       print (cal)
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        #       print (cal)
        cal += f'{self.formatweekheader()}\n'
        #       print (cal)

        for week in self.monthdays2calendar(self.year, self.month):
            #           print (f"week: {week}")
            cal += f'{self.formatweek(week)}\n'
        print("leaving formatmonth")
        return cal
