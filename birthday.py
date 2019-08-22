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
    month_lst = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7,'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
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
        if stringdate[:-5].lower().find(str(i)) !=-1:
            day = i
    date.append(day)

    for i in range(1000,int(year1)+1):
        if stringdate.lower().find(str(i)) != -1:
            year = i
    date.append(year)
    return date

def birthAlert(date):
    year1, month1, day1, hour1, minute1 = time.strftime("%Y,%m,%d,%H,%M").split(',')
    b = parsedate((date))
    if month1[0] == '0' and day1[0] == '0':
        if b[-2] == int(day1[-1]) and b[-3] == int(month1[-1]):
            return True
    elif month1[0] == '0':
        print('entering...')
        if b[-2] == int(day1) and b[-3] == int(month1[-1]):
            return True
    elif day1[0] == '0':
        print('entering..')
        if b[-2] == int(day1) and b[-3] == int(month1[-1]):
            return True
    return False

def dateDiffer(date,date2):
    monthD = {'1':'January', '2':'February','3': 'March', '4':'April','5':'May', '6':'June', '7':'July','8':'August', '9':'September', '10':'October', '11':'November','12':'December'}
    month_lst = {'January':31, 'February':28, 'March':31, 'April':30, 'May':31, 'June':30, 'July':31,'August':31, 'September':30, 'October':31, 'November':30, 'December':31}
    d = parsedate(date)
    print(f'this it {d}')
    d2 = parsedate(date2)
    year = d[-1]
    year2 = d2[-1]
    month = d[-3]
    month2 = d2[-3]
    day = d[-2]
    day2 = d2[-2]

    # yearDif = min(year - year2, year2-year)
    yearDif = year - year2

    # monthDif = min(month - month2, month2 - month)
    monthDif = month - month2

    # dayDif = min(day - day2, day2 - day)
    dayDif = day - day2

    minu = min(month,month2)
    print(minu)
    print(monthDif*month_lst[monthD[str(minu)]])
    total = 365 * yearDif + monthDif*month_lst[monthD[str(minu)]]
    print(total)
    # if leap(year,year2):
    #     total += 1
    totalDays = total + dayDif
    return totalDays




def main():
    year1, month1, day1, hour1, minute1 = time.strftime("%Y,%m,%d,%H,%M").split(',')
    date='March 7, 1996'
    date2 = 'February 2, 1998'
    # d = parsedate(date)
    # d2 = parsedate(date2)


#     print(datetime.date(b[-1],b[-3],b[-2]))
#     print(calcAge(datetime.date(b[-1],b[-3],b[-2])))
#     print('exiting now....')
main()
