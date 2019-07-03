from datetime import date
import datetime
import time
import discord


def calcAge(born):
    today = date.today()
    try:
        birthday = born.replace(year = today.year)

    # raised when birth date is February 29
    # and the current year is not a leap year
    except ValueError:
        birthday = born.replace(year = today.year,
                  month = born.month + 1, day = 1)

    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year

def parsedate(stringdate):
    month_lst = {'January':1, 'Feburary':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7,'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
    year = 0
    month = 0
    day = 0
    year1, month1, day1, hour1, minute1 = time.strftime("%Y,%m,%d,%H,%M").split(',')
    date = []
    #today1 = date.now()
    #today = today1.year

    for i in month_lst.keys():
        if stringdate.lower().find(i.lower()) != -1:
            month = month_lst[i]
    date.append(month)

    for i in range(1,32):
       # print(i)
        if stringdate[:-5].lower().find(str(i)) !=-1:
            day = i
    date.append(day)

    for i in range(1920,int(year1)+1):
        if stringdate.lower().find(str(i)) != -1:
            year = i
    date.append(year)
    return date
def main():
    date='October 31st 2001'
    b = parsedate(date)
    print(datetime.date(b[-1],b[-3],b[-2]))
    print(calcAge(datetime.date(b[-1],b[-3],b[-2])))
main()
