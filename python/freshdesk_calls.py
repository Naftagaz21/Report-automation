import requests
import json
from datetime import date
from datetime import timedelta
from datetime import datetime
from datetime import time
import pandas as pd
from freshdesk.change_network import run_cisco, connect_guest, connect_wired

def get_prev_date(delta):
    today = date.today()
    prev_date = today - timedelta(days = delta)
    prev_date = prev_date.strftime("%Y-%m-%d")
    return prev_date

def get_emails(delta, rq):
    kontakt_id = '25000027656'
    bcc_id = '25000028619'
    api_key = '2jT5oCNvKzmeQNyrpKF'
    page = 1
    print("Requested date: ", get_prev_date(delta))
    params = (
        ('query', '"(group_id: {0} OR group_id:{1}) AND created_at:\'{2}\'"'.format(bcc_id, kontakt_id, get_prev_date(delta))),
        ('page', '{0}'.format(page)),
    )
    response = rq.get('https://onevip.freshdesk.com/api/v2/search/tickets', params=params, auth=(api_key, 'X'))
    if response.status_code != 200:
        print("Request failed!")
    data = response.json()
    total = data['total']
    return total

def get_sm(delta, rq):
    fb_message = "'Fb message'"
    fb_post = "'Fb public post'"
    twitter = "'Twitter'"
    api_key = '2jT5oCNvKzmeQNyrpKF'
    page = 1
    print("Requested date: ", get_prev_date(delta))
    params = (
        ('query', '"(cf_channel:{0} OR cf_channel:{1} OR cf_channel:{2}) AND created_at:\'{3}\'"'.format(fb_message, fb_post, twitter, get_prev_date(delta))),
        ('page', '{0}'.format(page)),
    )
    response = rq.get('https://onevip.freshdesk.com/api/v2/search/tickets', params=params, auth=(api_key, 'X'))
    if response.status_code != 200:
        print("Request failed!")
        print(response.json())
    data = response.json()
    total = data['total']
    return total

def get_chatbot(delta, rq):
    fb_transfer = '25000030360'
    viber = "'Viber'"
    help_ = "'Help and Support'"
    api_key = '2jT5oCNvKzmeQNyrpKF'
    page = 1
    print("Requested date: ", get_prev_date(delta))
    params = (
        ('query', '"(group_id:{0} OR cf_channel:{1} OR cf_channel:{2}) AND created_at:\'{3}\'"'.format(fb_transfer, viber, help_, get_prev_date(delta))),
        ('page', '{0}'.format(page)),
    )
    response = rq.get('https://onevip.freshdesk.com/api/v2/search/tickets', params=params, auth=(api_key, 'X'))
    if response.status_code != 200:
        print("Request failed!")
        print(response.json())
    data = response.json()
    total = data['total']
    return total

def convert_to_proper_date(date):
    date_time_obj = datetime.strptime(date, '%m_%d_%Y')
    date = date_time_obj.strftime("%Y-%m-%d")
    return date

def convert_date(date):
    date_time_obj = datetime.strptime(date, '%m_%d_%Y')
    #date = date_time_obj.strftime("%Y-%m-%d")
    return date_time_obj

def convert_date_2(date):
    date_time = datetime.strptime(date, "%Y-%m-%d")
    return date_time

def convert_date_3(date):
    date_time = datetime.strptime(date, "%Y-%m-%d")
    date_time = date_time.strftime('%m_%d_%Y')
    return str(date_time)

def add_fresh(delta, rq):
    out_arr = []
    row_names = ['E-mails',
                'Chatbot interactions',
                'Social Media Contacts']
    out_arr.append(get_emails(delta, rq))
    out_arr.append(get_chatbot(delta, rq))
    out_arr.append(get_sm(delta, rq))
    df = pd.DataFrame(out_arr, row_names)
    df_nu = df.rename(columns={0: convert_date_3(get_prev_date(delta))})
    return df_nu

def append_fresh(file, delta):
    check = False

    rq = requests.Session()
    rq.trust_env = False
    out_arr = []
    df = pd.read_csv(file, index_col=[0])

    col = df.columns
    print(col[-1])
    date_time_obj = datetime.strptime(col[-1], '%m_%d_%Y')
    dif = date_time_obj - datetime.strptime(convert_date_3(get_prev_date(delta)), '%m_%d_%Y')
    dif = abs(dif.days)
    print(dif)

    if dif != 0:
        child = run_cisco()
        connect_guest(child)
        check = True

    while dif != 0:
        df_nu = add_fresh(dif, rq)
        df = df.join(df_nu)
        dif = dif - 1
        print(df)

    if check:
        connect_wired(child)

    df.to_csv(file)
