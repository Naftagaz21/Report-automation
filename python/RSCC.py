import pandas as pd
from datetime import date, timedelta, datetime
from data_extract import Residental_All_Res_VDNs
from RCC import get_prev_date
import numpy as np
import os


def append_rscc(app_arr, rscc_script, rscc_out, delta):
    RSCC = Residental_All_Res_VDNs(rscc_script, rscc_out, delta)
    app_arr += RSCC.get_data()
    del RSCC
    return app_arr


def add_rscc_full(output, delta, rscc_script, rscc_out):
    out_arr = []
    row_names = ['Residential Offered calls',
                'Residential Answered calls',
                'Residential Accessibility rate (%)',
                'Residential Service Level (30 sec) (%)']

    out_arr = append_rscc(out_arr, rscc_script, rscc_out, delta)
    df = pd.DataFrame(out_arr, row_names)
    df_nu = df.rename(columns={0: get_prev_date(delta)})
    df_nu.to_csv(output + '_' + str(get_prev_date(delta)) + '.csv')
    return df_nu


def append_rscc_full(file, output, delta, rscc_script, rscc_out):
    out_arr = []
    df = pd.read_csv(file, index_col=[0])

    col = df.columns
    date_time_obj = datetime.strptime(col[-1], '%m_%d_%Y')
    dif = date_time_obj - datetime.strptime(get_prev_date(delta), '%m_%d_%Y')
    dif = abs(dif.days)
    print(dif)

    while dif != 0:
        df_nu = add_rscc_full(output, dif, rscc_script, rscc_out)
        df = df.join(df_nu)
        dif = dif - 1

    df.to_csv(file)


def run_rscc(rscc_script, rscc_out, archive_output, daily_output, delta, delta_arch):
    if not os.path.exists(daily_output):
        print("NO PREVIOUS DAILY")
        add_rscc_full(archive_output, delta_arch, rscc_script, rscc_out)
        arch = archive_output + '_' + get_prev_date(delta_arch) + '.csv'
        assert(os.path.exists(arch))
        copy_file = open(arch, 'r')
        copy_file = copy_file.read()
        nu = open(daily_output, 'w')
        nu.write(copy_file)
        nu.close()
        append_rscc_full(daily_output, archive_output, delta, rscc_script, rscc_out)
    else:
        append_rscc_full(daily_output, archive_output, delta, rscc_script, rscc_out)
