import pandas as pd
from datetime import date, timedelta, datetime
from data_extract import BusinessCC_ALL_BUS_VDNs
from RCC import get_prev_date
import numpy as np
import os


def append_bscc(app_arr, bscc_script, bscc_out, delta):
    BSCC = BusinessCC_ALL_BUS_VDNs(bscc_script, bscc_out, delta)
    app_arr += BSCC.get_data()
    del BSCC
    return app_arr


def add_bscc_full(output, delta, bscc_script, bscc_out):
    out_arr = []
    row_names = ['Business Offered calls',
                'Business Answered calls',
                'Business Accessibility rate (%)',
                'Business Service Level (20 sec) (%)'
                ]

    out_arr = append_bscc(out_arr, bscc_script, bscc_out, delta)
    df = pd.DataFrame(out_arr, row_names)
    df_nu = df.rename(columns={0: get_prev_date(delta)})
    df_nu.to_csv(output + '_' + str(get_prev_date(delta)) + '.csv')
    return df_nu


def append_bscc_full(file, output, delta, bscc_script, bscc_out):
    out_arr = []
    df = pd.read_csv(file, index_col=[0])

    col = df.columns
    date_time_obj = datetime.strptime(col[-1], '%m_%d_%Y')
    dif = date_time_obj - datetime.strptime(get_prev_date(delta), '%m_%d_%Y')
    dif = abs(dif.days)
    print(dif)

    while dif != 0:
        df_nu = add_bscc_full(output, dif, bscc_script, bscc_out)
        df = df.join(df_nu)
        dif = dif - 1

    df.to_csv(file)


def run_bscc(bscc_script, bscc_out, archive_output, daily_output, delta, delta_arch):
    if not os.path.exists(daily_output):
        print("NO PREVIOUS DAILY")
        add_bscc_full(archive_output, delta_arch, bscc_script, bscc_out)
        arch = archive_output + '_' + get_prev_date(delta_arch) + '.csv'
        assert(os.path.exists(arch))
        copy_file = open(arch, 'r')
        copy_file = copy_file.read()
        nu = open(daily_output, 'w')
        nu.write(copy_file)
        nu.close()
        append_bscc_full(daily_output, archive_output, delta, bscc_script, bscc_out)
    else:
        append_bscc_full(daily_output, archive_output, delta, bscc_script, bscc_out)
