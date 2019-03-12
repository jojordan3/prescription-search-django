from tabula import read_pdf
import sys
import os
import pandas as pd

l = ['https://www.caremark.com/portal/asset/HCA90DayProviders.pdf',
     'http://aidsnet.org/wp-content/uploads/2016/03/Expanded-Network-now-in-place-\
for-ADAP-Premium-Plus-Clients.pdf',
     'https://www.molinahealthcare.com/members/ny/en-US/PDF/EP/\
MNY_Pharmacy_Network_2018.pdf',
      'http://www.uhh.org/hubfs/Hospitality_Rx/_files/Welldyne-Network-Pharmacy-List.pdf']

# Molina - start at 2nd page
