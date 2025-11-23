from datetime import date, datetime
import gspread
from google.oauth2.service_account import Credentials
import re
import Text
import FILEOP
import Sheets
import Check
import time

messenger=Text.SMS()
reader=FILEOP.FILE()
check=Check.Check()

today = date.today()
now=datetime.now()
key=reader.read('TextBeeKey.txt')

spreadsheet='https://docs.google.com/spreadsheets/d/1TNfQEpC2mWLuSg0wZZLcKmlKocfoemsnc4eREBVhg2Y/edit?gid=0#gid=0'

schedule_sheet = Sheets.Sheets(spreadsheet).get_sheet_by_name('Scheduler')
info = Sheets.Sheets(spreadsheet).get_sheet_by_name('Scheduler Info')

headers = schedule_sheet.row_values(1)
schedule_start_dates = schedule_sheet.col_values(headers.index("Start date") + 1)[1:]

for each_date in schedule_start_dates:
    start_date = datetime.strptime(each_date, "%m/%d/%Y").date()
    if(today<start_date):
        start_str=start_date.strftime("%m/%d/%Y")
        delta=(start_date-today).days
        break

scheduler_name=schedule_sheet.row_values(schedule_sheet.find(start_str).row)[2]
scheduler_phone_number=info.row_values(info.find(scheduler_name).row)[2]

scheduler_number=re.sub(r'\D', '', scheduler_phone_number)  

if(delta==0):
    schedule="today!"
elif(delta>0):
    schedule="tomorrow!"
if(delta>1):
    schedule="in "+str(delta)+" days."

if(check.check(scheduler_name)):
    if((now.hour==21 and now.minute>=45) or (now.hour==22 and now.minute<=20)):
        message = f"Hello "+scheduler_name+"!"+" This is a reminder that you are scheduled for "+start_str+", which is "+schedule+" Please remember to come in."
        #scheduler_number="4437937273"
        messenger.text(scheduler_number,message,key)
        #input("NUMBER: "+scheduler_number+"\nMESSAGE: "+message+"\nKEY: "+key)
        #time.sleep(300)

else:
    prev_name=reader.readlines('info.txt')[0]
    prev_number=reader.readlines('info.txt')[1]

    message_current = f"Hello "+scheduler_name+"!"+" This is a reminder that you have been switched out for "+prev_name+" and are scheduled for "+start_str+", which is "+schedule+" Please remember to come in."
    #prev_number="4437937273"
    messenger.text(prev_number,message_current,key)
    #input("NUMBER: "+scheduler_number+"\nMESSAGE: "+message_current+"\nKEY: "+key)
    message_prev = f"Hello "+prev_name+"!"+" This is a you have been switched out with "+scheduler_name+" for "+schedule+", you do NOT need to come in."
    #scheduler_number="4437937273"
    messenger.text(scheduler_number,message_prev,key)
    #input("NUMBER: "+scheduler_number+"\nMESSAGE: "+message_prev+"\nKEY: "+key)


with open('info.txt','w') as f:
    f.writelines([scheduler_name+'\n',scheduler_number+'\n',start_str+'\n'])





