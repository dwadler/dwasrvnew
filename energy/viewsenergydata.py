import calendar
import sqlite3
from datetime import datetime, timedelta, date

from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView

from home.dwamethods import prev_month, next_month, get_date
from .forms import FileFieldForm


def mdy2iso(inDate):
    tokens = inDate.split('/')
    mm = tokens[0]
    if len(mm) == 1: mm = '0' + mm
    dd = tokens[1]
    if len(dd) == 1: dd = '0' + dd
    isoDate = f'{tokens[2]}-{mm}-{dd}'
    return isoDate


def process_main_energy(contents):
    dailyData = dict()
    idx = 0
    for row in contents:
        idx += 1
        if idx == 1: continue
        #        print(f'idx: {idx}; row: {row}')
        tokens = row.split()
        if len(tokens) < 2: break
        isoDate = mdy2iso(tokens[0])
        tokens = row.split(",")
        mainA = round(float(tokens[1]), 2)
        mainB = round(float(tokens[2]), 2)
        total = round(mainA + mainB, 2)
        miniSplitPanel = round(float(tokens[4]), 2)
        #        print(isoDate, date, mainA, mainB, total, miniSplitPanel)
        dailyData[isoDate] = (mainA, mainB, total, miniSplitPanel)
        if idx == 4000:
            break
    return dailyData


def process_garage_energy(contents):
    dailyData = dict()
    idx = 0
    for row in contents:
        idx += 1
        if idx == 1: continue
        #        print(f'idx: {idx}; row: {row}')
        tokens = row.split()
        if len(tokens) < 2:
            break
        isoDate = mdy2iso(tokens[0])
        tokens = row.split(",")
        mainA = round(float(tokens[1]), 2)
        mainB = round(float(tokens[2]), 2)
        total = round(mainA + mainB, 2)
        solarA = round(-float(tokens[4]), 2)
        solarB = round(-float(tokens[5]), 2)
        solarTotal = round((solarA + solarB), 2)
        ev = round(float(tokens[6]), 2)
        #        print(isoDate, date, mainA, mainB, total, solarTotal, ev)
        dailyData[isoDate] = (mainA, mainB, total, solarTotal, ev)
        if idx == 4000:
            break
    return dailyData


def process_enphase_solar(contents):
    allData = []
    dailyData = dict()
    idx = 0
    lastDate = ""
    startTime = ""
    endTime = ""
    kwh = 0
    maxkwh = 0
    for row in contents:
        idx += 1
        if idx == 1: continue
        #    print(f'idx: {idx}; row: {row}')
        tokens = row.split(',')
        if len(tokens) < 2: break
        date = tokens[0]
        if lastDate != date:
            if lastDate != "":
                kwh = round(kwh / 1000.0, 2)
                dailyData[lastDate] = (kwh, maxkwh, startTime, endTime)
            #            print(f"{lastDate} - kWh: {kwh}; {maxkwh}; startTime: {startTime}; endTime: {endTime}")
            lastDate = date
            kwh = 0
            maxkwh = 0
            startTime = ""
            endTime = ""
        times = tokens[1].split(':')
        hh = times[0]
        mm = times[1]
        kw = float(tokens[3])
        if kw > 0:
            time = f"{hh}:{mm}"
            if startTime == "":
                startTime = time
            endTime = time
            allData.append((f"'{date} {hh}:{mm}'", kw))
            kwh = kwh + kw
            if kw > maxkwh:
                maxkwh = kw
    #           print(f'date: {date}; time: {times}; kw: {kw}; kwh {kwh}')
    kwh = round(kwh / 1000, 2)
    dailyData[lastDate] = (kwh, maxkwh, startTime, endTime)
    return (allData, dailyData)


def process_files(files):
    for f in files:
        name = f.name
        data = f.read()
        datastring = data.decode("utf-8")
        lines = datastring.split('\r\n')
        num_lines = len(lines)
        if num_lines == 1:
            lines = datastring.split('\n')
            num_lines = len(lines)
        print(f"{name=}; lines; {num_lines}")
        if name.find('enphase') > 0: allData, enphaseData = process_enphase_solar(lines)
        if name.find('garage') > 0: garageData = process_garage_energy(lines)
        if name.find('main') > 0: mainData = process_main_energy(lines)
        print("done getting data")
    try:
        dbFile = f'energy_data.sqlite3'
        conn = sqlite3.connect(dbFile)
        print("Connected to SQLite")
        init = False
        if init == True:
            conn.execute('DROP TABLE enphase_all')
            sqlite_create_table_query = '''CREATE TABLE enphase_all
                                           (
                                               datetime timestamp NOT NULL PRIMARY KEY UNIQUE,
                                               energy   float
                                           );'''

            conn.execute(sqlite_create_table_query)
            conn.commit()
            conn.execute('DROP TABLE energy_data')
            sqlite_create_table_query = '''CREATE TABLE energy_data
                                           (
                                               datetime       timestamp NOT NULL PRIMARY KEY UNIQUE,
                                               enphase        float,
                                               maxkwh         float,
                                               startTime      time,
                                               endTime        time,
                                               energyA        float,
                                               energyB        float,
                                               energyTotal,
                                               mainA          float,
                                               mainB          float,
                                               mainTotal      float,
                                               solar          float,
                                               EV             float,
                                               miniSplitPanel float
                                           );'''
            conn.execute(sqlite_create_table_query)
            conn.commit()
        # insert detailed enphase data - every 15 minutes that is non-zero
        insert_all_data = f"INSERT INTO enphase_all VALUES(?, ?);"
        #        print(insert_all_data)
        conn.executemany(insert_all_data, allData)

        allRecords = []
        for date, value in enphaseData.items():
            enphase, maxkwh, startTime, endTime = value
            if date in mainData:
                mainA, mainB, mainTotal, miniSplitPanel = mainData[date]
            else:
                mainA, mainB, mainTotal = (0, 0, 0)
            if date in garageData:
                garageA, garageB, garageTotal, solar, EV = garageData[date]
            else:
                garageA, garageB, garageTotal = (0, 0, 0)

            #            print(date, value, garageA, garageB, garageTotal, mainA, mainB, mainTotal)
            allRecords.append((date, enphase, maxkwh, startTime, endTime, garageA, garageB, garageTotal, mainA,
                               mainB, mainTotal, solar, EV, miniSplitPanel))
        #        print(allRecords)
        insert_all_data = f"INSERT INTO energy_data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        #        print(insert_all_data)
        conn.executemany(insert_all_data, allRecords)
        conn.commit()
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if conn:
            conn.close()
            print("sqlite connection is closed")
    return


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "energy/upload.html"  # Replace with your template.
    success_url = reverse_lazy('energy:index')  # Replace with your URL or reverse().

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        process_files(files)
        return super().form_valid(form)


class EnergyDisplay(ListView):
    template_name = 'energy/chart2.html'
#    template_name = 'energy/test1.html'

    # Have to implement this to use ListView - probably there is an easier solution
    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        month_parm = self.request.GET.get('month')
        if month_parm is None:
            d = date.today()
            first = d.replace(day=1)
            d = first - timedelta(days=1)
        else:
            d = get_date(month_parm)
        year = d.year
        month = d.month
        monthname = calendar.month_name[month]
        prevMonth = prev_month(d)
        nextMonth = next_month(d)
        context['prev_month'] = prevMonth
        context['next_month'] = nextMonth
        title = f"Energy Production for {monthname}, {year}"
        context['title'] = title
        curM = "{:02d}".format(month)
        nextM = nextMonth.split("=")[1]
        result = get_energy_data(f"{year}-{curM}", f"{nextM}")
        dates, values, values2 = result
        labels = list(range(1, len(dates) + 1))
        context['labels'] = labels
        context['values'] = values
        context['values2'] = values2
        return context

class SolarMaxMonth(ListView):
    template_name = 'energy/chart1.html'

    # Have to implement this to use ListView - probably there is an easier solution
    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        d = date.today()
        d = d + timedelta(days=31)
        year = d.year
        month = d.month
        title = f"Max solar {year}"
        result = get_energy_data(f"2023-01", f"{year}-{month}")
        dates, v, v2 = result
        idx = 0
        idx2 = 5
        v_max = 0
        v2_max = 0
        labels = []
        values = []
        values2 = []
        year_month_last = ""
        d = None
        for d in dates:
            year_month = d[0:7]
            if year_month_last != year_month and len(year_month_last) > 1:
                idx2 += 1
                label = year_month_last
                #                label = datetime.fromisoformat(d).strftime("%b")
                labels.append(label)
                #                labels.append(idx2)
                values.append(int(v_max))
                values2.append(int(v2_max))
                v_max = 0
                v2_max = 0
            year_month_last = year_month
            v_max = v_max if v_max > v[idx] else v[idx]
            v2_max = v2_max if v2_max > v2[idx] else v2[idx]
            idx += 1
            print(f"{idx=}, {d=}, {v_max=}, {v2_max=}")
        label = datetime.fromisoformat(d).strftime("%b")
        label = year_month_last
        labels.append(label)
        #        labels.append(idx2 + 1)
        values.append(int(v_max))
        values2.append(int(v2_max))
        context['title'] = title
        context['labels'] = labels
        context['values'] = values
        context['values2'] = values2
        return context


class EnergyDisplayMonth(ListView):
    template_name = 'energy/chart2.html'

    # Have to implement this to use ListView - probably there is an easier solution
    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        d = date.today()
        d = d + timedelta(days=31)
        year = d.year
        month = d.month
        title = f"Energy Production for {year}"
        result = get_energy_data(f"2023-01", f"{year}-{month}")
        dates, v, v2 = result
        idx = 0
        idx2 = 5
        v_total = 0
        v2_total = 0
        labels = []
        values = []
        values2 = []
        year_month_last = ""
        d = None
        for d in dates:
            year_month = d[0:7]
            if year_month_last != year_month and len(year_month_last) > 1:
                idx2 += 1
                label = year_month_last
                #                label = datetime.fromisoformat(d).strftime("%b")
                labels.append(label)
                #                labels.append(idx2)
                values.append(int(v_total))
                values2.append(int(v2_total))
                v_total = 0
                v2_total = 0
            year_month_last = year_month
            v_total += v[idx]
            v2_total += v2[idx]
            idx += 1
            print(f"{idx=}, {d=}, {v_total=}, {v2_total=}")
        label = datetime.fromisoformat(d).strftime("%b")
        label = year_month_last
        labels.append(label)
        #        labels.append(idx2 + 1)
        values.append(int(v_total))
        values2.append(int(v2_total))
        context['title'] = title
        context['labels'] = labels
        context['values'] = values
        context['values2'] = values2
        return context


def get_energy_data(start_date, end_date):
    conn = ""
    dates = []
    values = []
    values2 = []
    try:
        conn = sqlite3.connect(f'energy_data.sqlite3')
        print("Connected to SQLite")
        cur = conn.cursor()
        qry = f"SELECT * FROM energy_data where datetime between '{start_date}' and '{end_date}' order by datetime"
        print(f"{qry=}")
        cur.execute(qry)
        rows = cur.fetchall()
        idx = 0
        for row in rows:
            idx = idx + 1
            date = row[0]
            dates.append(date)
            values.append(row[1])
            energyGarage = row[7]
            energyMain = row[10]
            energySolar = row[11]
            energyTotal = energyMain + energyGarage + energySolar
            #            print(f"{idx=}; {date=}; {energyTotal=}; {energyMain=}; {energyGarage=}; {energySolar=}")
            values2.append(energyTotal)
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if conn:
            conn.close()
            print("sqlite connection is closed")
    return (dates, values, values2)
