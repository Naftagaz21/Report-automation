import os
import subprocess
from datetime import date
from datetime import timedelta
import re

def same_dates(date_list):
    check = date_list[0]
    for date in date_list:
        if check != date:
            return False
    return True


def execute_script(script_location):
    os.startfile(script_location)


def daily_script_date_update(script_location, delta):
    # Find the previous day in the same format as the CMS script
    today = date.today()
    yesterday = today - timedelta(days=delta)
    yesterday_2 = yesterday.strftime("%m_%d_%Y")
    yesterday = yesterday.strftime("%m/%d/%Y")

    script_1 = open(script_location, "r+")
    script_1_text = script_1.read()

    # bara bilo kakva forma na 2digit/2digit/4digit
    x = re.findall("(\d{2}\/\d{2}\/\d{4})", script_1_text)

    # if dates are the same replace both with correct date
    if same_dates(x):
        date_to_replace = x[0]
        print("Date to replace: ", date_to_replace)
        print("Replace with: ", yesterday)
        script_1_text = script_1_text.replace(date_to_replace, yesterday)
        script_1.seek(0)
        script_1.write(script_1_text)
        script_1.truncate()
        script_1.close()

    return yesterday_2


def daily_script_output_update(script_location, output, append_date):
    script = open(script_location, "r+")
    script_text = script.read()
    x = re.findall('Rep.ExportData\(\"(.*)\"', script_text)
    out_file_old = x[0]
    out_file_new = output + '_' + append_date + '.csv'
    #out_file_new = os.path.abspath(out_file_new)
    script_text = script_text.replace(out_file_old, out_file_new)
    script.seek(0)
    script.write(script_text)
    script.truncate()
    script.close()
    print("OUT FILE NEW:  ", out_file_new)
    return out_file_new

def call_script(script_location, output_name, delta):
    append_date = daily_script_date_update(script_location, delta)
    output = daily_script_output_update(script_location, output_name, append_date)
    print("Executing script: ", script_location, " FOR DATE ", append_date)
    execute_script(script_location)
    print("OUTPUT: ", output)
    return output


'''
def daily_script_output_update(script_location, new_out_name, append_date):
    #TODO da se dodade avtomatski datum na output name
    #TODO moznost da se zameni output path dokolku toa e potrebno
    script = open(script_location, "r+")
    script_text = script.read()
    x = re.findall('Rep.ExportData\(\"(.*)\"', script_text)
    out_file_old = x[0]
    out_file_split = out_file_old.split("\\")
    print(out_file_split[-1])
    out_file_new = out_file_old.replace(out_file_split[-1], new_out_name) + "_" + append_date + ".csv"
    print(out_file_old)
    print(out_file_new)
    script_text = script_text.replace(out_file_old, out_file_new)
    script.seek(0)
    script.write(script_text)
    script.truncate()
    script.close()
'''
