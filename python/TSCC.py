import pandas as pd
from datetime import date, timedelta, datetime
from data_extract import P_TimeTCC
from RCC import get_prev_date
import numpy as np
import os


def append_tscc(app_arr, tscc_script, tscc_out, delta):
    TSCC = P_TimeTCC(tscc_script, tscc_out, delta)
    app_arr += TSCC.get_data()
    del TSCC
    return app_arr


def add_tscc_full(output, delta, tscc_script, tscc_out):
    out_arr = []
    row_names = ['TSCC Offered calls',
                 'TSCC Answered calls',
                 'TSCC Accessibility rate (%)',
                 'TSCC Service Level  (30 sec) (%)']

    out_arr = append_tscc(out_arr, tscc_script, tscc_out, delta)
    df = pd.DataFrame(out_arr, row_names)
    df_nu = df.rename(columns={0: get_prev_date(delta)})
    df_nu.to_csv(output + '_' + str(get_prev_date(delta)) + '.csv')
    return df_nu


def append_tscc_full(file, output, delta, tscc_script, tscc_out):
    out_arr = []
    df = pd.read_csv(file, index_col=[0])

    col = df.columns
    date_time_obj = datetime.strptime(col[-1], '%m_%d_%Y')
    dif = date_time_obj - datetime.strptime(get_prev_date(delta), '%m_%d_%Y')
    dif = abs(dif.days)
    print(dif)

    while dif != 0:
        df_nu = add_tscc_full(output, dif, tscc_script, tscc_out)
        df = df.join(df_nu)
        dif = dif - 1

    df.to_csv(file)


def run_tscc(tscc_script, tscc_out, archive_output, daily_output, delta, delta_arch):
    if not os.path.exists(daily_output):
        print("NO PREVIOUS DAILY")
        add_tscc_full(archive_output, delta_arch, tscc_script, tscc_out)
        arch = archive_output + '_' + get_prev_date(delta_arch) + '.csv'
        assert(os.path.exists(arch))
        copy_file = open(arch, 'r')
        copy_file = copy_file.read()
        nu = open(daily_output, 'w')
        nu.write(copy_file)
        nu.close()
        append_tscc_full(daily_output, archive_output, delta, tscc_script, tscc_out)
    else:
        append_tscc_full(daily_output, archive_output, delta, tscc_script, tscc_out)
