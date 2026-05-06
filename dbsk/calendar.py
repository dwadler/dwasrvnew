from calendar import HTMLCalendar, monthrange
from datetime import date

from django.utils.safestring import mark_safe
from django.views import generic

from home.dwamethods import prev_month, next_month, get_date
from .models import Schedule


class CalendarView(generic.ListView):
    model = Schedule
    template_name = 'dbsk/calendar.html'

    def __init__(self):
        if not hasattr(self, 'restaurant'):
            self.restaurant = False
        print(f"***** initializing CalendarView *****; self.restaurant = {self.restaurant}")
        super().__init__()

    def get_context_data(self, **kwargs):
        print(f" ******** CalendarView::get_context_data")
        context = super().get_context_data(**kwargs)

        d = get_date(self.request.GET.get('month', None))
        print(f" ******** CalendarView::get_context_data; GET: {self.request.GET}; date: {d}")
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)
        cal.restaurants = self.restaurant
        cal.request = self.request
        print(f"***** CalendarView::get_context_data; self.restaurant = {self.restaurant}")

        cal.setfirstweekday(6)
        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        #        print (f" ******** CalendarView::get_context_data; context: {context}")
        return context


class RestaurantCalendarView(CalendarView):
    model = Schedule
    template_name = 'dbsk/restaurant_calendar.html'

    def __init__(self):
        self.restaurant = True
        print(f"***** initializing RestaurantCalendarView *****; self.restaurant = {self.restaurant}")
        super().__init__()


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        print(f"***** initializing Calendar *****; year = {year}; month = {month}")
        super().__init__()

    # formats a day as a td
    def formatday(self, day, weekday):
        #        print (f'** formatday: day: {day}; weekday: {weekday}')

        html = ''
        if (weekday == 1) or (weekday == 3) or (weekday == 5) or (weekday == 6):
            return ''

        if (weekday == 0) or (weekday == 2) or (weekday == 4):
            if day == 0:
                return '<td>&nbsp;\n</td>'
            current_date = date(self.year, self.month, day)
            date_string = f'{current_date}'
            schedules = Schedule.objects.filter(schedule_date=current_date)

            if (not self.restaurants and self.request.user.is_authenticated):
                html = f'<a href="schedule/create?schedule_date={date_string}">Create schedule</a>'

        for schedule in schedules:

            if (not self.restaurants and self.request.user.is_authenticated):
                html = f'<a href="schedule/{schedule.id}/update">'
            html += f'{schedule.provider}'
            if (schedule.provider.notes is not None) and (len(schedule.provider.notes) > 1):
                html += f'<br>{schedule.provider.notes}'
            if (not self.restaurants):
                html += f'<br>{schedule.volunteer1}'
                html += f'<br>{schedule.volunteer2}'
                if (schedule.notes is not None) and (len(schedule.notes) > 1):
                    html += f'<br>Note: {schedule.notes}'
            if (not self.restaurants):
                html += '</a>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><br>{html}&nbsp;</td\n>"
        return '<td>&nbsp;\n</td>'

    # formats a week as a tr 
    def formatweek(self, theweek):
        week = ''
        #        print (f'** formatweek; theweek: {theweek}')
        for d, weekday in theweek:

            # if first day of month and a saturday, skip this week
            if (d == 1 and weekday == 5):
                return ""

            mrange = monthrange(self.year, self.month)
            daysInMonth = mrange[1];
            #            print (f'day: {d}; weekday: {weekday}; monthrange: {mrange}; daysInMonth: {daysInMonth}')
            # if last day of month and a sunday, skip this week
            if (d == daysInMonth and weekday == 6):
                return ""

            week += self.formatday(d, weekday)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter schedules by year and month
    def formatmonth(self, withyear=True):
        cal = f'<table border="1" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        #        cal += f'{self.formatweekheader()}\n'
        cal += '<tr><th class="mon">Monday</th><th class="wed">Wednesday</th><th class="fri">Friday</th></tr>'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week)}\n'
        return cal
