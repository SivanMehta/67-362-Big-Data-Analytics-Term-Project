from __future__ import print_function
import os
import json
import csv

'''
    The Basic ERD for bills (at least for our purposes) is as follows

    Bill: ID*, sponsor, status
    Subject_bill: subject*, bill_id*
'''

def process_states_simple(status):
    return str(1 if "ENACTED" in status else 0)

def distill_3NF():
    bill_csv =  open('data_distilled/distilled_bills.csv', 'w')
    bill_csv_writer = csv.writer(bill_csv, delimiter='\t', quoting=csv.QUOTE_MINIMAL)

    bill_subject_csv =  open('data_distilled/distilled_bills_subjects.csv', 'w')
    bill_subject_csv_writer = csv.writer(bill_subject_csv, delimiter='\t', quoting=csv.QUOTE_MINIMAL)

    for path, dirs, files in os.walk("data"):
        for data_file in files:
            bill_path = path + "/" + data_file

            data_file = open(bill_path)
            data = json.load(data_file)

            try:
                
                bill_csv_row = [data["bill_id"], data["sponsor"]["name"], process_states_simple(data["status"])]
                # print(bill_csv_row)
                bill_csv_writer.writerow(bill_csv_row)

                for subject in data["subjects"]:
                    bill_subject_csv_row = [data["bill_id"], subject]
                    bill_subject_csv_writer.writerow(bill_subject_csv_row)

            except:
                # this is the case of malformed JSON
                pass

def distill_1NF():
    bill_csv =  open('data_distilled/distilled_bills_1NF.csv', 'w')

    for path, dirs, files in os.walk("data"):
        for data_file in files:
            bill_path = path + "/" + data_file

            data_file = open(bill_path)
            data = json.load(data_file)

            try:

                row_buffer = data["sponsor"]["name"] + "\t" + process_states_simple(data["status"]) + "\t"
                
                # bill_csv_row = [data["bill_id"], data["sponsor"]["name"], process_states_simple(data["status"])]
                # print(bill_csv_row)

                for subject in data["subjects"]:
                    row_buffer += subject + "|"

                row_buffer = row_buffer[:-1]

                # print(row_buffer)
                bill_csv.write(row_buffer + "\n")
            except:
                # this is the case of malformed JSON
                pass

    bill_csv.close()

distill_1NF()
