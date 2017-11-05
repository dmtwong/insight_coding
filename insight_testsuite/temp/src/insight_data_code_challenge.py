# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 20:49:51 2017

@author: dmtwong
"""
#!/usr/bin/python

import os
import numpy
import datetime
import collections 


os.getcwd()
#os.chdir( os.getcwd()+ '/Desktop')
#os.chdir("..")
#input_file = open(os.getcwd() + '/insight_testsuite/temp/input/itcont.txt')
input_file = open(os.getcwd() + '/input/itcont.txt')
#os.chdir("..")
#os.chdir( os.getcwd()+ '/output)
#specify each row as a class with the five attributes needed:
stream_data = collections.namedtuple('stream_data', 'CMTE_ID ZIP_CODE TRANSACTION_DT TRANSACTION_AMT OTHER_ID')

consolidate_tmp = []
date_pair = dict()
date_roll = dict()
zip_pair = collections.OrderedDict()
zip_roll = collections.OrderedDict()

def update_by_date(inc, date_bool):
    if date_bool == True:
        if (inc.CMTE_ID, inc.TRANSACTION_DT) not in date_pair.keys():
            date_pair[(inc.CMTE_ID, inc.TRANSACTION_DT)] = [inc.TRANSACTION_AMT]
        else:
            date_pair[(inc.CMTE_ID, inc.TRANSACTION_DT)].extend([inc.TRANSACTION_AMT])
        int_txn_lst = map(int, date_pair[(inc.CMTE_ID, inc.TRANSACTION_DT)])
        med = int(round( numpy.median( int_txn_lst ) ))
        num_txn = len( int_txn_lst )
        tot_txn = sum( int_txn_lst )
        #date_roll[(inc.CMTE_ID, inc.TRANSACTION_DT)] = [inc.CMTE_ID + '|' + inc.TRANSACTION_DT + '|' + str(med) + '|' + str(num_txn) + '|' + str(tot_txn) + '\n']
        date_roll[(inc.CMTE_ID, inc.TRANSACTION_DT)] = [inc.CMTE_ID + '|' + inc.TRANSACTION_DT + '|' + str(med) + '|' + str(num_txn) + '|' + str(tot_txn) + '\n']
    else:
        pass

def update_by_zip(inc, zip_bool):
    if zip_bool == True:
        if (inc.CMTE_ID, inc.ZIP_CODE[:5]) not in zip_pair.keys():
            zip_pair[(inc.CMTE_ID, inc.ZIP_CODE[:5])] = [inc.TRANSACTION_AMT]
        else:
            zip_pair[(inc.CMTE_ID, inc.ZIP_CODE[:5])].extend([inc.TRANSACTION_AMT])
        int_txn_lst = map(int, zip_pair[(inc.CMTE_ID, inc.ZIP_CODE[:5])])
        med = int(round( numpy.median( int_txn_lst ) ))
        num_txn = len( int_txn_lst )
        tot_txn = sum( int_txn_lst )
        if os.path.exists(os.getcwd()+ '/output/medianvals_by_zip.txt'):
            param = 'a'
        else:
            param = 'w'
        #by_zip  = open(os.getcwd()+ '/insight_testsuite/temp/output/medianvals_by_zip.txt',param)
        #by_zip.write(inc.CMTE_ID + '|' + inc.ZIP_CODE[:5] + '|' + str(med) + '|' + str(num_txn) + '|' + str(tot_txn) + '\n')
        by_zip  = open(os.getcwd()+ '/output/medianvals_by_zip.txt',param)
        by_zip.write(inc.CMTE_ID + '|' + inc.ZIP_CODE[:5] + '|' + str(med) + '|' + str(num_txn) + '|' + str(tot_txn)+ '\n')
    else:
        pass

def is_validate(date_suppose):
    try:
        if datetime.datetime.strptime(date_suppose, '%m%d%Y'):
            return True
    except:
        return False

#def zip_rebalance():
 #   by_zip  = open('medianvals_by_zip.txt','w+')
  #  for pair in zip_roll.keys():
   #     by_zip.write(zip_roll[pair][0])
    #by_zip.close()
    
def date_rebalance():
    date_pair.keys()
    #by_date  = open(os.getcwd()+ '/insight_testsuite/temp/output/medianvals_by_date.txt','w+')
    by_date  = open(os.getcwd()+ '/output/medianvals_by_date.txt','w+')
    sorted_key = sorted(date_pair.keys())
    for pair in sorted_key:
        #print pair
        by_date.write(date_roll[pair][0])
    by_date.close()
    
for line in input_file:
    tmp = line.split('|')
    #print tmp
    tmp_2 = stream_data(tmp[0], tmp[10], tmp[13], tmp[14], tmp[15])
    if (tmp_2.OTHER_ID != '') | (tmp_2.CMTE_ID == '') | (tmp_2.TRANSACTION_AMT == ''):        
        pass
    else:
        zip_bool =  (len(tmp_2.ZIP_CODE) >=5) #| (tmp_2.ZIP_CODE == '')
        date_bool = is_validate(tmp_2.TRANSACTION_DT)
        #print str(zip_bool) + str(date_bool)
        if zip_bool | date_bool:
            consolidate_tmp.append(tmp_2)
            update_by_date(tmp_2, date_bool)
            update_by_zip(tmp_2, zip_bool)
        else:
            pass
      #  if zip_bool == True:
       #     zip_rebalance()
        if date_bool == True:
            date_rebalance()