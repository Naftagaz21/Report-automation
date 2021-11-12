import pandas as pd
from datetime import datetime
import csv
from collections import defaultdict
from L2.get_report import download_report
from datetime import date
from datetime import timedelta
from datetime import datetime
from datetime import time
import os

def remove_files(file):
    folder = os.path.dirname(file)
    for x in os.listdir(folder):
        os.remove(os.path.join(folder, x))

def transform_date(date):
    date = datetime.strftime(date, "%m_%d_%Y")
    return date

def get_prev_date(delta):
    today = date.today()
    prev_date = today - timedelta(days = delta)
    prev_date = prev_date.strftime("%m_%d_%Y")
    return prev_date


def add_date(dif, file_loc, user_file):
    date_to_look = get_prev_date(dif)

    useri = []

    with open(user_file) as inputfile:
        for row in csv.reader(inputfile):
            useri.append(row[0])

    df = pd.read_excel(file_loc)
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header

    date_closed = df['TICKET_DATE_CLOSED_']
    closed_by = df['TICKED_CLOSED_BY']
    ticket_type = df['TICKET_TYPE']

    date_closed_si, date_closed_tc = [], []
    for idx in range(1, len(closed_by) + 1):
        if closed_by[idx] in useri:
            if ticket_type[idx] == "Technical complaint":
                date_closed_tc.append(date_closed[idx])
            if ticket_type[idx] == "System incident":
                date_closed_si.append(date_closed[idx])

    date_closed_tc = sorted(date_closed_tc)
    date_closed_si = sorted(date_closed_si)

    dateCounter_tc = defaultdict(int)
    dateCounter_si = defaultdict(int)
    for x in date_closed_tc:
        date = transform_date(x)
        dateCounter_tc[date] += 1
    for x in date_closed_si:
        date = transform_date(x)
        dateCounter_si[date] += 1

    value_tc = dateCounter_tc[date_to_look]
    value_si = dateCounter_si[date_to_look]

    df = pd.DataFrame({"Technical complaints closed":[value_tc], "System incidents closed":[value_si]})
    df = df.T
    df.columns = [date_to_look]

    return df


def append_date_closed(delta, daily_loc, url, user_file, gecko):
    df = pd.read_csv(daily_loc, index_col=[0])

    last_date = datetime.strptime(df.columns[-1], '%m_%d_%Y')
    dif = last_date - datetime.strptime(get_prev_date(delta), '%m_%d_%Y')
    dif = abs(dif.days)
    print(dif)

    if dif == 0:
        return

    file_loc = download_report(url, gecko)

    while dif != 0:
        # From downloaded file here
        df_nu = add_date(dif, file_loc, user_file)
        print(df_nu)

        df = df.join(df_nu)
        print(df)
        dif = dif - 1

    remove_files(file_loc)
    df.to_csv(daily_loc)

def run_L2_closed(daily_loc, user_file, delta, gecko):
    url = 'https://vmdwhwp001.austria.local/ReportPortal/frmreport.aspx?reportid=8234'
    append_date_closed(delta, daily_loc, url, user_file, gecko)
