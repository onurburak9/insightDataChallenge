#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 17:48:29 2018

@author: onurb

"""
import numpy as np
from collections import defaultdict

unique_donor_set = set()
a = lambda: defaultdict(a)
contributions = a()


def isNotEmpty(s):
    return bool(s and s.strip())


def percentile(N, P):
    """
    Find the percentile of a list of values

    @parameter N - A list of values.  N must be sorted.
    @parameter P - A float value from 0.0 to 1.0

    @return - The percentile of the values.
    """
    n = int(round(P * len(N) + 0.5))
    return N[n-1]

def extractDonor(data,perc,output):
    
    #extract values  
    id = data[0]
    name = data[7]
    zipcode = data[10][:5] if len(data[10]) >= 5 else ""
    transaction_dt = data[13] if len(data[10]) > 5 else ""
    transaction_year = data[13][-4:]
    transaction_amt = data[14]
    
    #validations
    if not id or not name or not zipcode or not transaction_dt or not transaction_amt:
        return
    
    if "min-year" in contributions[id+"-"+zipcode]:
        if int(transaction_year) >= contributions[id+"-"+zipcode]["min-year"]:
            if int(transaction_year) in contributions[id+"-"+zipcode]:
                contributions[id+"-"+zipcode][int(transaction_year)]["amt"].append(int(transaction_amt))
                contributions[id+"-"+zipcode][int(transaction_year)]["times"] += 1
            else:
                contributions[id+"-"+zipcode][int(transaction_year)] = {"amt":[int(transaction_amt)], "times":1}
    else:
        contributions[id+"-"+zipcode]={"min-year":int(transaction_year), int(transaction_year):{"amt":[int(transaction_amt)], "times":1}} 
    
    donor_tuple = (name,zipcode)
    #detect repeated donor
    if not (name,zipcode) in unique_donor_set:
        unique_donor_set.add(donor_tuple)
    else:
        if(int(transaction_year) >= contributions[id+"-"+zipcode]["min-year"]):
            array = contributions[id+"-"+zipcode][int(transaction_year)]["amt"]
            
            percentile_amt = str(percentile(array, perc))
            total_amt =str(np.sum(array))
            total_times =str(contributions[id+"-"+zipcode][int(transaction_year)]["times"])
            
            print("contributions: "+id+'|'+zipcode+'|'+transaction_year+'|'+percentile_amt+'|'+total_amt+'|'+total_times)
            output.write(id+'|'+zipcode+'|'+transaction_year+'|'+percentile_amt+'|'+total_amt+'|'+total_times+"\n")
    
    return

file_percentile = open("./input/percentile.txt", "r")
file_contributors = open("./input/itcont.txt", "r")
try:
    repeated_donors = open("./output/repeat_donors.txt","w")
except:
    print("This is an error message!")

p = file_percentile.read()
p = int(p)/100

for line in file_contributors:
    contribution = line.split("|")
    other_id = contribution[15]
    if not other_id:
        donor = extractDonor(contribution,p,repeated_donors )
        
repeated_donors.close()