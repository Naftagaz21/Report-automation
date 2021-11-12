from configparser import ConfigParser
from pathlib import Path
import pandas as pd
import os
from BCC import run_bcc
from RCC import run_rcc, get_prev_date
from TSCC import run_tscc
from RSCC import run_rscc
from BSCC import run_bscc
from L2_closed import run_L2_closed
from freshdesk_calls import append_fresh


def check(loc, dir):
    assert(os.path.exists(loc))
    path = Path(dir)
    assert(os.path.exists(path.parent.absolute()))


def check_and_make(archive_output):
    print('CHECK AND MAKE: ', archive_output)
    archive_output = Path(archive_output)
    archive_output = archive_output.parent.absolute()
    print(archive_output)
    if not os.path.exists(archive_output):
        os.mkdir(archive_output)


def convert_backslash(path):
    path = os.path.abspath(path)
    return path

def get_delta(config):
    delta = int(config['DELTA']['delta'])
    delta_arch = int(config['DELTA']['delta_arch'])
    return delta, delta_arch

def bcc(config):
    BCC_loc = convert_backslash(config['BCC']['script_loc'])
    BCC_out = convert_backslash(config['BCC']['output_loc'])
    BCC_archive = convert_backslash(config['BCC']['archive'])
    BCC_daily = convert_backslash(config['BCC']['daily'])
    delta, delta_arch = get_delta(config)
    check(BCC_loc, BCC_out)
    check_and_make(BCC_archive)
    check_and_make(BCC_daily)
    print(BCC_loc, '\n',BCC_out,'\n', BCC_archive,'\n', BCC_daily, '\n', delta, '\n', delta_arch)
    print(BCC_out)

    run_bcc(BCC_loc, BCC_out, BCC_archive, BCC_daily, delta, delta_arch)


def rcc_full(config):
    rcc_loc = convert_backslash(config['RCC']['script_loc'])
    rcc_out = convert_backslash(config['RCC']['output_loc'])
    check(rcc_loc, rcc_out)

    pop_loc = convert_backslash(config['POP']['script_loc'])
    pop_out = convert_backslash(config['POP']['output_loc'])
    check(pop_loc, pop_out)

    pre_loc = convert_backslash(config['PRE']['script_loc'])
    pre_out = convert_backslash(config['PRE']['output_loc'])
    check(pre_loc, pre_out)

    delta, delta_arch = get_delta(config)

    rcc_archive = convert_backslash(config['RCC']['archive'])
    rcc_daily = convert_backslash(config['RCC']['daily'])

    check_and_make(rcc_archive)
    check_and_make(rcc_daily)

    run_rcc(rcc_loc, rcc_out, pop_loc, pop_out, pre_loc, pre_out, rcc_archive, rcc_daily, delta, delta_arch)


def tscc(config):
    tscc_loc = convert_backslash(config['TSCC']['script_loc'])
    tscc_out = convert_backslash(config['TSCC']['output_loc'])
    check(tscc_loc, tscc_out)

    delta, delta_arch = get_delta(config)

    tscc_arch = convert_backslash(config['TSCC']['archive'])
    tscc_daily = convert_backslash(config['TSCC']['daily'])

    check_and_make(tscc_arch)
    check_and_make(tscc_daily)

    run_tscc(tscc_loc, tscc_out, tscc_arch, tscc_daily, delta, delta_arch)


def rscc(config):
    rscc_loc = convert_backslash(config['RSCC']['script_loc'])
    rscc_out = convert_backslash(config['RSCC']['output_loc'])
    check(rscc_loc, rscc_out)

    delta, delta_arch = get_delta(config)

    rscc_arch = convert_backslash(config['RSCC']['archive'])
    rscc_daily = convert_backslash(config['RSCC']['daily'])
    check_and_make(rscc_arch)
    check_and_make(rscc_daily)

    run_rscc(rscc_loc, rscc_out, rscc_arch, rscc_daily, delta, delta_arch)

#TODO mozhebi check and make za output_loc
def bscc(config):
    bscc_loc = convert_backslash(config['BSCC']['script_loc'])
    bscc_out = convert_backslash(config['BSCC']['output_loc'])
    check(bscc_loc, bscc_out)

    delta, delta_arch = get_delta(config)

    bscc_arch = convert_backslash(config['BSCC']['archive'])
    bscc_daily = convert_backslash(config['BSCC']['daily'])
    check_and_make(bscc_arch)
    check_and_make(bscc_daily)

    run_bscc(bscc_loc, bscc_out, bscc_arch, bscc_daily, delta, delta_arch)

def run_fresh(config):
    daily = convert_backslash(config['ONLINE']['daily'])
    assert(os.path.exists(daily))
    delta, _ = get_delta(config)
    append_fresh(daily, delta)


def run_L2(config):
    daily = convert_backslash(config['L2']['closed_daily'])
    l2_useri = convert_backslash(config['L2']['user_file'])
    gecko = convert_backslash(config['L2']['gecko'])
    check(l2_useri, gecko)
    check_and_make(daily)
    delta, _ = get_delta(config)
    run_L2_closed(daily, l2_useri, delta, gecko)


def convert_to_xlsx(config):
    rcc = convert_backslash(config['RCC']['daily'])
    tcc = convert_backslash(config['TSCC']['daily'])
    bcc = convert_backslash(config['BCC']['daily'])
    bscc = convert_backslash(config['BSCC']['daily'])
    rscc = convert_backslash(config['RSCC']['daily'])
    fresh = convert_backslash(config['ONLINE']['daily'])
    l2_closed = convert_backslash(config['L2']['closed_daily'])

    rcc_df = pd.read_csv(rcc, index_col=[0])
    tcc_df = pd.read_csv(tcc, index_col=[0])
    bcc_df = pd.read_csv(bcc, index_col=[0])
    bscc_df = pd.read_csv(bscc, index_col=[0])
    rscc_df = pd.read_csv(rscc, index_col=[0])
    fresh_df = pd.read_csv(fresh, index_col=[0])
    l2_closed = pd.read_csv(l2_closed, index_col=[0])

    res = rcc_df.append(tcc_df)
    res = res.append(bcc_df)
    res = res.append(bscc_df)
    res = res.append(rscc_df)
    res = res.append(fresh_df)
    res = res.append(l2_closed)
    print(res)

    loc = convert_backslash(config['ALL']['daily'])
    check_and_make(loc)
    res.to_excel(loc)
    #print(rcc_df)
    #print(bcc_df)



config = ConfigParser()
config.read('../config.ini')
print(config.sections())
#print(config.sections())

run_fresh(config)
rcc_full(config)
bcc(config)
tscc(config)
rscc(config)
bscc(config)
run_L2(config)
convert_to_xlsx(config)
print("--- DONE ---")

#TODO add read_csv to files that dont have them
