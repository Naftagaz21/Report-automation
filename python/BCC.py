import pandas as pd
from datetime import date, timedelta, datetime
from data_extract import P_Time_BusinessCC
from RCC import get_prev_date
import numpy as np
import os


def append_bcc(app_arr, bcc_script, bcc_out, delta):
    BCC = P_Time_BusinessCC(bcc_script, bcc_out, delta)
    app_arr += BCC.get_data()
    del BCC
    return app_arr


def add_bcc_full(output, delta, bcc_script, bcc_out):
    out_arr = []
    row_names = ['BCC Offered calls',
                'BCC Answered calls',
                'BCC Accessibility rate (%)',
                'BCC Service Level (20 sec) (%)']

    out_arr = append_bcc(out_arr, bcc_script, bcc_out, delta)
    df = pd.DataFrame(out_arr, row_names)
    df_nu = df.rename(columns={0: get_prev_date(delta)})
    df_nu.to_csv(output + '_' + str(get_prev_date(delta)) + '.csv')
    return df_nu


def append_bcc_full(file, output, delta, bcc_script, bcc_out):
    out_arr = []
    df = pd.read_csv(file, index_col=[0])

    col = df.columns
    date_time_obj = datetime.strptime(col[-1], '%m_%d_%Y')
    dif = date_time_obj - datetime.strptime(get_prev_date(delta), '%m_%d_%Y')
    dif = abs(dif.days)
    print(dif)

    while dif != 0:
        df_nu = add_bcc_full(output, dif, bcc_script, bcc_out)
        df = df.join(df_nu)
        dif = dif - 1

    df.to_csv(file)


def run_bcc(bcc_script, bcc_out, archive_output, daily_output, delta, delta_arch):
    if not os.path.exists(daily_output):
        print("NO PREVIOUS DAILY")
        add_bcc_full(archive_output, delta_arch, bcc_script, bcc_out)
        arch = archive_output + '_' + get_prev_date(delta_arch) + '.csv'
        assert(os.path.exists(arch))
        copy_file = open(arch, 'r')
        copy_file = copy_file.read()
        nu = open(daily_output, 'w')
        nu.write(copy_file)
        nu.close()
        append_bcc_full(daily_output, archive_output, delta, bcc_script, bcc_out)
    else:
        append_bcc_full(daily_output, archive_output, delta, bcc_script, bcc_out)
