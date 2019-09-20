#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Get history values for specific items in a time range:

# ./getitems.py -H BKP-FORTIGATE -I "Current connections" -f "26/6/2019 16:00" -t "27/6/2019 23:59"
ItemID: 77013 - Item: ICMP response time - Key: icmppingsec
1530021641 26/06/2018 16:00:41 Value: 0.1042
1530021701 26/06/2018 16:01:41 Value: 0.0993
1530021762 26/06/2018 16:02:42 Value: 0.1024
1530021822 26/06/2018 16:03:42 Value: 0.0966
[cut]
"""

from pyzabbix.api import ZabbixAPI
import sys, argparse
import time
import datetime
from datetime import date
import csv

zabbixServer    = 'http://10.23.2.250/zabbix/'
zabbixUser      = 'Admin'
zabbixPass      = 'zabbix'

today = date.today()
d     = today.strftime("%d-%m-%Y")
filename = "/csvdata/fortigate200d-{}.csv".format(d)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', required=True, metavar='Hostname')
    parser.add_argument('-I', required=True, metavar='Item Name')
    parser.add_argument('-f', required=True, metavar='From Timestamp')
    parser.add_argument('-t', required=True, metavar='Till Timestamp')

    args = parser.parse_args()


    zapi = ZabbixAPI(url=zabbixServer, user=zabbixUser, password=zabbixPass)

    fromTimestamp = int(time.mktime(datetime.datetime.strptime(args.f, "%d/%m/%Y %H:%M").timetuple()))
    tillTimestamp = int(time.mktime(datetime.datetime.strptime(args.t, "%d/%m/%Y %H:%M").timetuple()))
    

    f  = {  'name' : args.I  }
    items = zapi.item.get(filter=f, host=args.H, output='extend' )

    with open(filename,'w') as csvFile:
        csvHeader = ['date','current connections']
        writer = csv.writer(csvFile)
        writer.writerow(csvHeader)

        for item in items:
            #print("ItemID: {} - Item: {} - Key: {}".format(item['itemid'], item['name'], item['key_']))

            values = zapi.history.get(itemids=item['itemid'], time_from=fromTimestamp, time_till=tillTimestamp, history=item['value_type'])

            for historyValue in values:
                currentDate = datetime.datetime.fromtimestamp(int(historyValue['clock'])).strftime('%d/%m/%Y %H:%M:%S')

                #print("{} {} Value: {}".format(historyValue['clock'], currentDate, historyValue['value']))
                myData = [currentDate, historyValue['value']]
                writer.writerow(myData)
    csvFile.close()
    print("create csv finished")
if __name__ == "__main__":
   main(sys.argv[1:])

