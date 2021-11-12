import pandas as pd
from datetime import date, timedelta, datetime
from data_extract import PTime_Res, Pop_Prospect_and_Transfers, Prepaid
import numpy as np
import os


def get_prev_date(delta):
    today = date.today()
    prev_date = today - timedelta(days = delta)
    prev_date = prev_date.strftime("%m_%d_%Y")
    return prev_date


def append_RCC(append_arr, RCC_script, RCC_output, delta):
    RCC = PTime_Res(RCC_script, RCC_output, delta)
    append_arr += RCC.get_data()
    del RCC
    return append_arr


def append_POP(app_arr, POP_script, POP_out, delta):
    POP = Pop_Prospect_and_Transfers(POP_script, POP_out, delta)
    app_arr += POP.get_data()
    del POP
    return app_arr


def append_PRE(app_arr, PRE_script, PRE_out, delta):
    PRE = Prepaid(PRE_script, PRE_out, delta)
    app_arr += PRE.get_data()
    del PRE
    return app_arr


def app_NA(app_arr):
    app_arr += [None] * 6
    return app_arr


def add_rcc_full(output, delta, RCC_script, RCC_output, postpaid_script, postpaid_output, prepaid_script, prepaid_output):
    # IF RCC exists skip
    out_arr = []
    row_names = ['RCC Offered calls',
                'RCC Answered calls',
                'RCC Accessibility rate (%)',
                'RCC Service Level  (20 sec) (%)',
                'Postpaid Offered calls',
                'Postpaid Answered calls',
                'Postpaid Accessibility rate (%)',
                'Postpaid Service Level  (20 sec) (%)',
                'Prepaid Offered calls',
                'Prepaid Answered calls',
                'Prepaid Accessibility rate (%)',
                'Prepaid Service Level  (20 sec) (%)'
                ]

    out_arr = append_RCC(out_arr, RCC_script, RCC_output, delta)
    out_arr = append_POP(out_arr, postpaid_script, postpaid_output, delta)
    out_arr = append_PRE(out_arr, prepaid_script, prepaid_output, delta)
    #out_arr = app_NA(out_arr)
    df = pd.DataFrame(out_arr, row_names)
    df_nu = df.rename(columns={0: get_prev_date(delta)})
    df_nu.to_csv(output + '_' + str(get_prev_date(delta)) + '.csv')
    return df_nu

def append_rcc_full(file, output, delta, RCC_script, RCC_output, postpaid_script, postpaid_output, prepaid_script, prepaid_output):
    out_arr = []
    df = pd.read_csv(file, index_col=[0])

    col = df.columns
    date_time_obj = datetime.strptime(col[-1], '%m_%d_%Y')
    dif = date_time_obj - datetime.strptime(get_prev_date(delta), '%m_%d_%Y')
    dif = abs(dif.days)
    print(dif)

    while dif != 0:
        df_nu = add_rcc_full(output, dif, RCC_script, RCC_output, postpaid_script, postpaid_output, prepaid_script, prepaid_output)
        df = df.join(df_nu)
        dif = dif - 1

    df.to_csv(file)

def run_rcc(RCC_script, RCC_output, postpaid_script, postpaid_output, prepaid_script, prepaid_output, archive_output, daily_output, delta, delta_arch):
    if not os.path.exists(daily_output):
        print("NO PREVIOUS DAILY")
        add_rcc_full(archive_output, delta_arch, RCC_script, RCC_output, postpaid_script, postpaid_output, prepaid_script, prepaid_output)
        arch = archive_output + '_' + get_prev_date(delta_arch) + '.csv'
        assert(os.path.exists(arch))
        copy_file = open(arch, 'r')
        copy_file = copy_file.read()
        nu = open(daily_output, 'w')
        nu.write(copy_file)
        nu.close()
        append_rcc_full(daily_output, archive_output, delta, RCC_script, RCC_output, postpaid_script, postpaid_output, prepaid_script, prepaid_output)
    else:
        append_rcc_full(daily_output, archive_output, delta, RCC_script, RCC_output, postpaid_script, postpaid_output, prepaid_script, prepaid_output)
