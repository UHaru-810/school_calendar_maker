import csv
from datetime import datetime, timedelta

def to_circled_number(n):
    circled_numbers = { '1': '❶', '2': '❷', '3': '❸', '4': '❹', '5': '❺', '6': '❻', '7': '❼' }
    return circled_numbers[n]

def to_start_time(n):
    start_times = { '1': '084500', '2': '094000', '3': '103500', '4': '113000', '5': '130000', '6': '135500', '7': '145000' }
    return start_times[n]

def to_end_time(n):
    end_times = { '1': '093000', '2': '102500', '3': '112000', '4': '121500', '5': '134500', '6': '144000', '7': '153500' }
    return end_times[n] 

def convert_scv_toical(csv_path, ics_path): 
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        events = list(reader)

    with open(ics_path, 'w', encoding='utf-8') as f:
        f.write("BEGIN:VCALENDAR\n")
        f.write("VERSION:2.0\n")

        for event in events:
            is_all_day = event['startPeriod'] == '' and event['endPeriod'] == ''

            f.write("BEGIN:VEVENT\n")
            if is_all_day:
                f.write(f"SUMMARY:{event['title']}\n") # タイトル
                f.write(f"DTSTART;VALUE=DATE:{event['startDate']}\n") # 開始日
                end_date = datetime.strptime(event['endDate'], '%Y%m%d') + timedelta(days=1)
                f.write(f"DTEND;VALUE=DATE:{end_date.strftime('%Y%m%d')}\n") # 終了日
            else:
                title = ''
                duration = int(event['endPeriod']) - int(event['startPeriod'])
                if duration == 0: 
                    title = to_circled_number(event['startPeriod'])
                elif duration == 1:
                    title = to_circled_number(event['startPeriod']) + to_circled_number(event['endPeriod'])
                else:
                    title = to_circled_number(event['startPeriod']) + '〜' + to_circled_number(event['endPeriod'])
                title += ' ' + event['title']
                f.write(f"SUMMARY:{title}\n") # タイトル
                f.write(f"DTSTART:{event['startDate'] + 'T' + to_start_time(event['startPeriod'])}\n") # 開始時刻
                f.write(f"DTEND:{event['startDate'] + 'T' + to_start_time(event['endPeriod'])}\n") # 終了時刻
            f.write("END:VEVENT\n")
            
        f.write("END:VCALENDAR\n")

convert_scv_toical('events.csv', 'school_calendar.ics')
