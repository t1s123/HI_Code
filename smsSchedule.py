from datetime import date, datetime
import gspread
from google.oauth2.service_account import Credentials
import re
import Text
import FILEOP
import Sheets
import Check
import time
import os
from zoneinfo import ZoneInfo


messenger=Text.SMS()
reader=FILEOP.FILE()
check=Check.Check()


today = date.today()
now= datetime.now(ZoneInfo("America/New_York"))
key = os.getenv("TEXTBEEKEY")
#key=reader.read('TextBeeKey.txt')

has="3477401544"
nhu="2403149462"
ryan="4437937273"

spreadsheet='https://docs.google.com/spreadsheets/d/1TNfQEpC2mWLuSg0wZZLcKmlKocfoemsnc4eREBVhg2Y/edit?gid=0#gid=0'

prov_ma_sheet = Sheets.Sheets(spreadsheet).get_sheet_by_name('Provider and MA Calendar')
info = Sheets.Sheets(spreadsheet).get_sheet_by_name('Scheduler and MA Contact')

schedule_start_dates = prov_ma_sheet.col_values(prov_ma_sheet.row_values(1).index(" ") + 1)[1:]

for each_date in schedule_start_dates:
    try:
        start_date = datetime.strptime(each_date, "%m/%d/%Y").date()
    except:
        print("INVALID DATE: "+start_date)
        continue
    if(today<start_date):
        start_str=start_date.strftime("%m/%d/%Y")
        delta=(start_date-today).days
        break

start_str=start_str.replace("/0", "/")
ma_1_name=prov_ma_sheet.row_values(prov_ma_sheet.find(start_str).row)[2]
ma_2_name=prov_ma_sheet.row_values(prov_ma_sheet.find(start_str).row)[3]

try:
    ma_1_number=re.sub(r'\D', '', info.row_values(info.find(ma_1_name).row)[2]).strip()
except:
    ma_1_number="none"

try:
    ma_2_number=re.sub(r'\D', '', info.row_values(info.find(ma_2_name).row)[2]).strip()
except:
    ma_2_number="none"

ma_1_name=ma_1_name.strip()
ma_2_name=ma_2_name.strip()

if(delta==0):
    schedule="today!"
elif(delta>0):
    schedule="tomorrow!"
if(delta>1):
    schedule="in "+str(delta)+" days."

if((now.hour==11 and now.minute>=45) or (now.hour==12 and now.minute<=15)):
#if(True):
    if(check.check(ma_1_name)):
        ma_1_message = f"Hello "+ma_1_name+"!"+" This is a reminder that you are scheduled for "+start_str+", which is "+schedule+" Please remember to come in."

        messenger.text(ma_1_number,ma_1_message,key)

        messenger.text(has,ma_1_message,key)

        messenger.text(nhu,ma_1_message,key)

        messenger.text(ryan,ma_1_message,key)

    if(check.check(ma_2_name)):
        ma_2_message = f"Hello "+ma_2_name+"!"+" This is a reminder that you are scheduled for "+start_str+", which is "+schedule+" Please remember to come in."

        messenger.text(ma_2_number,ma_2_message,key)

        messenger.text(has,ma_2_message,key)

        messenger.text(nhu,ma_2_message,key)

        messenger.text(ryan,ma_2_message,key)

if(not check.check(ma_1_name)):
    prev_ma_1=reader.readlines('info.txt')[0].strip()
    prev_ma_1_number=reader.readlines('info.txt')[1]

    message_current = f"Hello "+ma_1_name+"!"+" This is a reminder that you have been switched out for "+prev_ma_1+" and are scheduled for "+start_str+", which is "+schedule+" Please remember to come in."
    message_prev = f"Hello "+prev_ma_1+"!"+" This is a you have been switched out with "+ma_1_name+" for the shift "+schedule+" you don't need to come in."

    messenger.text(ma_1_number,message_current,key)
    messenger.text(prev_ma_1_number,message_prev,key)

    messenger.text(has,message_current,key)
    messenger.text(has,message_prev,key)

    messenger.text(nhu,message_current,key)
    messenger.text(nhu,message_prev,key)

    messenger.text(ryan,message_current,key)
    messenger.text(ryan,message_prev,key)

if(delta==7):
    with open('info.txt','w') as f:
        f.writelines([ma_1_name+'\n',ma_1_number+'\n',ma_2_name+'\n',ma_2_number+'\n',start_str+'\n'])

elif(not check.check(ma_2_name)):
    prev_ma_2=reader.readlines('info.txt')[2].strip()
    prev_ma_2_number=reader.readlines('info.txt')[3]

    message_current = f"Hello "+ma_2_name+"!"+" This is a reminder that you have been switched out for "+prev_ma_2+" and are scheduled for "+start_str+", which is "+schedule+" Please remember to come in."
    message_prev = f"Hello "+prev_ma_2+"!"+" This is a you have been switched out with "+ma_2_name+" for the shift "+schedule+" You don't need to come in."

    messenger.text(ma_2_number,message_current,key)
    messenger.text(prev_ma_2_number,message_prev,key)

    messenger.text(has,message_current,key)
    messenger.text(has,message_prev,key)

    messenger.text(nhu,message_current,key)
    messenger.text(nhu,message_prev,key)

    messenger.text(ryan,message_current,key)
    messenger.text(ryan,message_prev,key)

with open('info.txt','w') as f:
    f.writelines([ma_1_name+'\n',ma_1_number+'\n',ma_2_name+'\n',ma_2_number+'\n',start_str+'\n'])










