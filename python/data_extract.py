from daily_export import call_script
import os.path
import time
import csv
from datetime import date
from datetime import timedelta
from timeit import default_timer as timer

# returns yesterdays date
def get_yesterday(delta):
    today = date.today()
    yesterday = today - timedelta(days = delta)
    yesterday = yesterday.strftime("%m_%d_%Y")
    return yesterday

# checks if the report from the previous day exists
# and returns boolean
def report_check(output, delta):
    output = output + "_" + get_yesterday(delta) + ".csv"
    if not os.path.exists(output):
        return False
    else:
        return True

class PTime_Res:
    def __init__(self, script_location, out_file_location, delta):
        self.script = script_location
        self.output = out_file_location
        self.delta = delta

        report_exists = report_check(self.output, self.delta)

        if not report_exists:
            out = call_script(self.script, self.output, self.delta)
            start = timer()
            while not os.path.exists(out):
                time.sleep(5)
                if (timer() - start > 85):
                    print("Time Limit of 85s exceeded, exiting!")
                    exit()


        else:
            out = self.output + "_" + get_yesterday(delta) + ".csv"

        if os.path.isfile(out):
            with open(out, 'r') as csvfile:
                 csvreader = csv.reader(csvfile)
                 fields = next(csvreader)
                 fields = next(csvreader)
                 row_names = next(csvreader)
                 row_totals = next(csvreader)

                 self.offered_calls_net = row_totals[6]
                 self.performance = row_totals[39]
                 self.sla_20 = row_totals[42]
                 self.answered_calls = row_totals[7]

    def get_data(self):
        print(self.offered_calls_net, self.performance, self.sla_20, self.answered_calls)
        return  [int(self.offered_calls_net), int(self.answered_calls), float(self.performance), float(self.sla_20)]

class Pop_Prospect_and_Transfers:
    def __init__(self, script_location, out_file_location, delta):
        self.script = script_location
        self.output = out_file_location
        self.delta = delta

        report_exists = report_check(self.output, self.delta)


        if not report_exists:
            out = call_script(self.script, self.output, self.delta)
            start = timer()
            while not os.path.exists(out):
                time.sleep(5)
                if (timer() - start > 85):
                    print("Time Limit of 85s exceeded, exiting!")
                    exit()

        else:
            out = self.output + "_" + get_yesterday(delta) + ".csv"

        if os.path.isfile(out):
            with open(out, 'r') as csvfile:
                 csvreader = csv.reader(csvfile)
                 fields = next(csvreader)
                 row_totals = next(csvreader)

                 self.offered_calls_net = row_totals[4]
                 self.performance = row_totals[37]
                 self.sla_20 = row_totals[40]
                 self.answered = row_totals[5]

    def get_data(self):
        print(self.offered_calls_net, self.performance, self.sla_20, self.answered)
        return [int(self.offered_calls_net), int(self.answered), float(self.performance), float(self.sla_20)]


class Prepaid:
    def __init__(self, script_location, out_file_location, delta):
        self.script = script_location
        self.output = out_file_location
        self.delta = delta

        report_exists = report_check(self.output, self.delta)


        if not report_exists:
            out = call_script(self.script, self.output, self.delta)
            start = timer()
            while not os.path.exists(out):
                time.sleep(5)
                if (timer() - start > 85):
                    print("Time Limit of 85s exceeded, exiting!")
                    exit()

        else:
            out = self.output + "_" + get_yesterday(delta) + ".csv"

        if os.path.isfile(out):
            with open(out, 'r') as csvfile:
                 csvreader = csv.reader(csvfile)
                 fields = next(csvreader)
                 row_totals = next(csvreader)

                 self.offered_calls_net = row_totals[4]
                 self.performance = row_totals[37]
                 self.sla_20 = row_totals[40]
                 self.answered = row_totals[5]

    def get_data(self):
        print(self.offered_calls_net, self.performance, self.sla_20, self.answered)
        return [int(self.offered_calls_net), int(self.answered), float(self.performance), float(self.sla_20)]

class P_TimeTCC:
    def __init__(self, script_location, out_file_location, delta):
        self.script = script_location
        self.output = out_file_location
        self.delta = delta

        report_exists = report_check(self.output, self.delta)


        if not report_exists:
            out = call_script(self.script, self.output, self.delta)
            start = timer()
            while not os.path.exists(out):
                time.sleep(5)
                if (timer() - start > 85):
                    print("Time Limit of 85s exceeded, exiting!")
                    exit()
        else:
            out = self.output + "_" + get_yesterday(delta) + ".csv"

        if os.path.isfile(out):
            with open(out, 'r') as csvfile:
                 csvreader = csv.reader(csvfile)
                 fields = next(csvreader)
                 fields = next(csvreader)
                 row_names = next(csvreader)
                 row_totals = next(csvreader)

                 self.offered_calls_net = row_totals[6]
                 self.performance = row_totals[39]
                 self.sla_30 = row_totals[44]
                 self.answered_calls = row_totals[7]

    def get_data(self):
        print(self.offered_calls_net, self.performance, self.sla_30, self.answered_calls)
        return [int(self.offered_calls_net), int(self.answered_calls), float(self.performance), float(self.sla_30)]

class P_Time_BusinessCC:
    def __init__(self, script_location, out_file_location, delta):
        self.delta = delta
        self.script = script_location
        self.output = out_file_location

        report_exists = report_check(self.output, self.delta)


        if not report_exists:
            out = call_script(self.script, self.output, self.delta)
            start = timer()
            while not os.path.exists(out):
                time.sleep(5)
                if (timer() - start > 85):
                    print("Time Limit of 85s exceeded, exiting!")
                    exit()
        else:
            out = self.output + "_" + get_yesterday(delta) + ".csv"

        if os.path.isfile(out):
            with open(out, 'r') as csvfile:
                 csvreader = csv.reader(csvfile)
                 fields = next(csvreader)
                 fields = next(csvreader)
                 row_names = next(csvreader)
                 row_totals = next(csvreader)

                 self.offered_calls_net = row_totals[6]
                 self.performance = row_totals[39]
                 self.sla_20 = row_totals[42]
                 self.answered_calls = row_totals[7]

    def get_data(self):
        print(self.offered_calls_net, self.performance, self.sla_20, self.answered_calls)
        return [int(self.offered_calls_net), int(self.answered_calls), float(self.performance), float(self.sla_20)]

class Residental_All_Res_VDNs:
    def __init__(self, script_location, out_file_location, delta):
        self.delta = delta
        self.script = script_location
        self.output = out_file_location

        report_exists = report_check(self.output, self.delta)


        if not report_exists:
            out = call_script(self.script, self.output, self.delta)
            start = timer()
            while not os.path.exists(out):
                time.sleep(5)
                if (timer() - start > 85):
                    print("Time Limit of 85s exceeded, exiting!")
                    exit()
        else:
            out = self.output + "_" + get_yesterday(delta) + ".csv"

        if os.path.isfile(out):
            with open(out, 'r') as csvfile:
                 csvreader = csv.reader(csvfile)
                 fields = next(csvreader)
                 row_totals = next(csvreader)

                 self.offered_calls_net = row_totals[4]
                 self.performance = row_totals[37]
                 self.sla_30 = row_totals[42]
                 self.answered = row_totals[5]

    def get_data(self):
        print(self.offered_calls_net, self.performance, self.sla_30)
        return [int(self.offered_calls_net), int(self.answered), float(self.performance), float(self.sla_30)]

class BusinessCC_ALL_BUS_VDNs:
    def __init__(self, script_location, out_file_location, delta):
        self.delta = delta
        self.script = script_location
        self.output = out_file_location

        report_exists = report_check(self.output, self.delta)


        if not report_exists:
            out = call_script(self.script, self.output, self.delta)
            start = timer()
            while not os.path.exists(out):
                time.sleep(5)
                if (timer() - start > 85):
                    print("Time Limit of 85s exceeded, exiting!")
                    exit()
        else:
            out = self.output + "_" + get_yesterday(delta) + ".csv"

        if os.path.isfile(out):
            with open(out, 'r') as csvfile:
                 csvreader = csv.reader(csvfile)
                 fields = next(csvreader)
                 row_totals = next(csvreader)

                 self.offered_calls_net = row_totals[4]
                 self.performance = row_totals[37]
                 self.sla_20 = row_totals[40]
                 self.answered = row_totals[5]

    def get_data(self):
        print(self.offered_calls_net, self.performance, self.sla_20)
        return [int(self.offered_calls_net), int(self.answered), float(self.performance), float(self.sla_20)]


#*******************ANSWERED CALLS*******************
class RCC_ANSWERED_CALLS:
    def __init__(self, script_location, out_file_location):
        self.script = script_location
        self.output = out_file_location

        report_exists = report_check(self.output, self.delta)


        if not report_exists:
            out = call_script(self.script, self.output, self.delta)
            while not os.path.exists(out):
                time.sleep(5)
        else:
            out = self.output + "_" + get_yesterday(delta) + ".csv"

        if os.path.isfile(out):
            with open(out, 'r') as csvfile:
                 csvreader = csv.reader(csvfile)
                 fields = next(csvreader)
                 fields = next(csvreader)
                 row_names = next(csvreader)
                 row_totals = next(csvreader)

                 self.answered_calls = row_totals[7]

    def get_data(self):
        print(self.answered_calls)
        return self.answered_calls

class TSCC_ANSWERED_CALLS:
    def __init__(self, script_location, out_file_location):
        self.script = script_location
        self.output = out_file_location

        report_exists = report_check(self.output, self.delta)


        if not report_exists:
            out = call_script(self.script, self.output, self.delta)
            while not os.path.exists(out):
                time.sleep(5)
        else:
            out = self.output + "_" + get_yesterday(delta) + ".csv"

        if os.path.isfile(out):
            with open(out, 'r') as csvfile:
                 csvreader = csv.reader(csvfile)
                 fields = next(csvreader)
                 fields = next(csvreader)
                 row_names = next(csvreader)
                 row_totals = next(csvreader)

                 self.answered_calls = row_totals[7]

    def get_data(self):
        print(self.answered_calls)
        return self.answered_calls

class BCC_ANSWERED_CALLS:
    def __init__(self, script_location, out_file_location):
        self.script = script_location
        self.output = out_file_location

        report_exists = report_check(self.output, self.delta)


        if not report_exists:
            out = call_script(self.script, self.output, self.delta)
            while not os.path.exists(out):
                time.sleep(5)
        else:
            out = self.output + "_" + get_yesterday(delta) + ".csv"

        if os.path.isfile(out):
            with open(out, 'r') as csvfile:
                 csvreader = csv.reader(csvfile)
                 fields = next(csvreader)
                 fields = next(csvreader)
                 row_names = next(csvreader)
                 row_totals = next(csvreader)

                 self.answered_calls = row_totals[5]

    def get_data(self):
        print(self.answered_calls)
        return self.answered_calls
