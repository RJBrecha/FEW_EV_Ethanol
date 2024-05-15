#!/usr/bin/env python
# coding: utf-8


import numpy as np
from scipy.ndimage import shift
import pandas as pd
import matplotlib.ticker as ticker
from matplotlib import pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)


import streamlit as st

#from importlib.metadata import version
#version('numpy')


#Read in the data on starting vintages "years old, from 0-30", your survival rate function, initial distribution of vehicle vintages
df = pd.read_excel("US_LDV_stock_and_turnover.xlsx",sheet_name = ['Python_input_data'])
df3 = pd.read_excel("US_LDV_stock_and_turnover.xlsx",sheet_name = ['SSP_pop_data'])
df.keys()

population_projected = np.array(df3['SSP_pop_data'].pop)
#vintage = np.array(df['Python_input_data'].Vintage)
vintage = np.linspace(0, 30, 31).astype(int)

#survival = np.array(df['Python_input_data'].survival_rate)
survival = np.array([1.    , 0.994 , 0.988 , 0.982 , 0.972 , 0.9575, 0.94  , 0.9165,
       0.8895, 0.858 , 0.823 , 0.7835, 0.7425, 0.6845, 0.609 , 0.5315,
       0.4585, 0.3925, 0.334 , 0.2835, 0.2405, 0.204 , 0.1735, 0.1475,
       0.1255, 0.107 , 0.0915, 0.078 , 0.065 , 0.056 , 0.048 ])
#scrappage = np.array(df['Python_input_data'].survival_rate_delta)
scrappage = np.array([0.        , 0.006     , 0.00603622, 0.00607287, 0.0101833 ,
       0.0149177 , 0.01827676, 0.025     , 0.0294599 , 0.03541315,
       0.04079254, 0.04799514, 0.05232929, 0.07811448, 0.11029949,
       0.1272578 , 0.13734713, 0.14394766, 0.14904459, 0.1511976 ,
       0.15167549, 0.15176715, 0.1495098 , 0.14985591, 0.14915254,
       0.14741036, 0.14485981, 0.14754098, 0.16666667, 0.13846154,
       0.14285714])

#vehicle_distribution = np.array(df['Python_input_data'].initial_distribution)
vehicle_distribution = np.array([16.45287982, 12.90918263, 13.16230386, 10.12484912,  8.0998793 ,
       14.17478877, 15.44039491, 15.44039491, 15.44039491, 16.19975859,
       14.68103122, 13.92166754, 12.40294017, 11.64357649, 10.63109158,
        9.87172789,  8.09481687,  6.63774983,  5.44295486,  4.46322299,
        3.65984285,  3.00107114,  2.46087833,  2.01792023,  1.65469459,
        1.35684956,  1.11261664,  0.91234565,  0.74812343,  0.61346121,
        0.50303819])

EV_distribution = np.array(df['Python_input_data'].initial_EV_distribution)
EV_distribution = np.array([0.8  , 0.47 , 0.23 , 0.24 , 0.24 , 0.1  , 0.087, 0.071, 0.063,
       0.048, 0.015, 0.01 , 0.   , 0.   , 0.   , 0.   , 0.   , 0.   ,
       0.   , 0.   , 0.   , 0.   , 0.   , 0.   , 0.   , 0.   , 0.   ,
       0.   , 0.   , 0.   , 0.   ])

#print("Total number of vehicles",vehicle_distribution.sum())
#plt.plot(vintage,vehicle_distribution)
#plt.xlabel('Years old', size=12)
#plt.ylabel('Stock of vehicles', size=12)

scen = 'SSP2'+'_pop'
df1 = pd.read_excel("US_LDV_stock_and_turnover.xlsx",sheet_name = ['SSP_pop_data'])
population_projected = np.array(df1['SSP_pop_data'].SSP2_pop)
year = np.array(df1['SSP_pop_data'].Year)   
df2 = pd.DataFrame({'Years':year,'pop':population_projected})
df2 = df2.interpolate()
population_projected = df2['pop']
#df1.keys()
#vehicles_per_1000_people = df1['AB'].Vehicles_per_1000_people
#GDP_per_capita = df1['AB'].GDP_per_capita
vehicles_per_1000_people = np.linspace(750,800,31)

#df2 = pd.read_excel("US_LDV_stock_and_turnover.xlsx",sheet_name = ['Pop_scen_data'])
#df2.keys()
#GDP_per_capita_projected = (df2['AB_projected'].GDP_per_capita)*1000
#population_projected = (df2['Pop_scen_data'].scen)

projected_vehicle_stocks = vehicles_per_1000_people*population_projected/1000

#parameters for fuels, economics
veh_km_trav = 18500
ICEV_eff = 13.5/100 #liters of fuel (gasoline +ethanol) per km
ICEV_eff_improve = 0.01
EV_eff = 5.0 #km/kWh or million vkm per TWh
EV_eff_improve = 0.01 # improvement per year
etoh_fraction = 0.09
etoh_prod_eff = 10.5 #liters of ethanol per bushel of corn
corn_yield = 170.0 #bushels of corn per acre 2020
corn_yield_improve = 0.007 #yield improvement rate per year
solar_pv_fraction = 0.1 #fraction of reduced corn acreage used for PV
solar_pv_spec_acres = 5.0 #acres of land per MW of PV capacity
solar_pv_yield = 1.0 # TWh of output electricity per GW of capacity
etoh_earn_per_liter = 0.01 #average dollars per liter average over time 
corn_earn_per_acre = 250.0 #average dollars per acre earned over time
solar_pv_ppa = 30.0 #average dollars per MWh
ethanol_ef_agric = 300.0 #employment factor per billion liters
ethanol_ef_other = 360.0 # employment factor per billion liters
solar_ef_CI = 3000.0 #employment factor per GW capacity
solar_ef_OM = 100.0 # employment factor per GW capacity
max_corn_irrig = 10.0 #million acres
spec_irrig = 0.67 # irrigation amount, acre-feet per acre

#projected_vehicle_stocks.round(decimals=0)


# Interactive Streamlit elements, like these sliders, return their value.
# This gives you an extremely simple interaction model.
EV_sales_fraction_2030 = st.sidebar.slider("EV sales fraction in 2030", 0.0, 1.0, .25)
EV_sales_fraction_2040 = st.sidebar.slider("EV sales fraction in 2040", 0.0, 1.0, .5)
EV_sales_fraction_2050 = st.sidebar.slider("EV sales fraction in 2050", 0.0, 1.0, 0.75)
solar_pv_fraction = st.sidebar.slider("Fraction of corn cropland used for PV", 0.0,1.0,0.1)
solar_pv_income = st.sidebar.slider("Solar PV net income [$/MWh]", 0.0,100.0,30.0)
etoh_earn_per_liter = st.sidebar.slider("Ethanol net income [$/liter]", 0.0,0.2,0.02)
corn_earn_per_acre = st.sidebar.slider("Corn net income [$/acre]", 0.0, 500.0, 250.0)

#sales_oldest_vintage=1

#def plot(EV_sales_fraction_2030,EV_sales_fraction_2040, EV_sales_fraction_2050, sales_oldest_vintage):
    #Define the function that represents the progression of sales of EVs over time; here it is a three-part function
    #with three input values for 2030, 2040 and 2050 taken from above (again, ideally with sliders)
sales1 = np.linspace(0.05,EV_sales_fraction_2030,10)
sales2 = np.linspace(EV_sales_fraction_2030+(EV_sales_fraction_2040-EV_sales_fraction_2030)/10,EV_sales_fraction_2040,10)
sales3 = np.linspace(EV_sales_fraction_2040+(EV_sales_fraction_2050-EV_sales_fraction_2040)/10,EV_sales_fraction_2050,10)
EV_sales_fraction = np.concatenate((sales1,sales2,sales3))
    #Define a vector of years for use later
years = np.linspace(2020, 2050, 31).astype(int)
    #Initialize the arrays (will be added to by concatenation later)
EV_sales=[0.2]
ICEV_sales=[13.8]
EV_eff_t = [EV_eff]
ICEV_eff_t = [ICEV_eff] 
corn_yield_t = [corn_yield]
    #Define a loop variable to count through the years over which we are interested in running the program.
x = range(len(years)-1)
    #Assume above initial distributions for all vehicles; initialized the array of EV distribution with zeros
ICEV_distribution = vehicle_distribution - EV_distribution
#EV_distribution = [0]*len(vehicle_distribution)
EV_total = [EV_distribution.sum()]
ICEV_total = [ICEV_distribution.sum()]
for i in x:
        #Use the survival profile to "scrap" cars of different vintages with a given probability, both ICEVs and EVs
        ICEV_scrap_by_vintage = (ICEV_distribution*(scrappage))
        EV_scrap_by_vintage = (EV_distribution*(scrappage))
        
        #ICEV_scrap_by_vintage = (ICEV_distribution*(1-survival))
        #EV_scrap_by_vintage = (EV_distribution*(1-survival))
        
        #Here's what's left of each vintage after the scrapping is done each year
        ICEV_remaining_by_vintage = (ICEV_distribution - ICEV_scrap_by_vintage) 
        EV_remaining_by_vintage = (EV_distribution - EV_scrap_by_vintage) 
        
        #Total scrappage distribution by vintage
        scrap_by_vintage = ICEV_scrap_by_vintage + EV_scrap_by_vintage 
        scrap_by_vintage.sum() 
        ##Total sales is just equal to total scrappage plus change in expected stock
        
        vehicle_sales_total = projected_vehicle_stocks[i+1] - projected_vehicle_stocks[i] + scrap_by_vintage.sum()
            
            
        #Count the total sales for EVs and ICEVs each time through the loop
        EV_sales.append(((vehicle_sales_total*EV_sales_fraction[i])).sum()) 
        ICEV_sales.append(((vehicle_sales_total*(1-EV_sales_fraction[i]))).sum())
        
        #Assume a uniform distribution of sales over different vintages; this could be changed, but we don't have
        #particularly good reason to know how the vintage distribution of sold vehicles will look
        #sales_by_vintage = vehicle_sales_total/(sales_oldest_vintage)
        
        #Divide sales between EVs and ICEVs, and by vintage; 
        #Create an array of sales by vintage for EVs and ICEVs vehicle_sales_total/(sales_oldest_vintage+1)
        #EV_sales = (vehicle_sales_total*EV_sales_fraction[i]).round(decimals=0)
        #ICEV_sales = (vehicle_sales_total*(1-EV_sales_fraction[i])).round(decimals=0)
        #EV_sales_vintage_distribution = [EV_sales_by_vintage.round(decimals=0)]*(sales_oldest_vintage+1)+[0]*(len(vehicle_distribution)-(sales_oldest_vintage+1))
        #ICEV_sales_vintage_distribution = [ICEV_sales_by_vintage.round(decimals=0)]*(sales_oldest_vintage+1)+[0]*(len(vehicle_distribution)-(sales_oldest_vintage+1))
        
        # Create the new distribution array before going through the loop again
        # Now the cars that were 0 years old will be 1 year old, etc.  The zero-year-old cars in the stock for the next 
        #are that fraction of the sales that were of new cars
        EV_distribution = shift(EV_remaining_by_vintage, 1, cval=(vehicle_sales_total*EV_sales_fraction[i]).sum())
        ICEV_distribution = shift(ICEV_remaining_by_vintage, 1, cval=(vehicle_sales_total*(1-EV_sales_fraction[i])).sum())
        
        
        #Continue building the array of EV stock and ICEV stock; will be used for plotting as a function of time.
        EV_total.append(EV_distribution.sum())
        ICEV_total.append(ICEV_distribution.sum())
        #print(population_projected[i])
        EV_eff = EV_eff*(1+EV_eff_improve)
        ICEV_eff = ICEV_eff*(1-ICEV_eff_improve)
        EV_eff_t.append(EV_eff)
        ICEV_eff_t.append(ICEV_eff)
        corn_yield = corn_yield*(1+ corn_yield_improve)
        corn_yield_t.append(corn_yield)
        


etoh_consump = veh_km_trav*etoh_fraction*np.multiply(ICEV_total,ICEV_eff_t)/1000 #billions of liters
EV_elec_consump = veh_km_trav*np.divide(EV_total,EV_eff_t)/1000 # TWh
acres_corn = (1/etoh_prod_eff)*np.divide(etoh_consump,corn_yield_t)*1000 #millions of acres of harvested corn
new_PV_capacity_total = (acres_corn[0] - acres_corn)*solar_pv_fraction/solar_pv_spec_acres*1000 #GW of capacity on a fraction of former corn cropland
added_PV_capacity = np.diff(new_PV_capacity_total)
added_PV_capacity = np.append(0,added_PV_capacity)
new_PV_production_total = new_PV_capacity_total*solar_pv_yield # production in TWh of electricity from "new" land
etoh_earnings = acres_corn*corn_earn_per_acre/1000 + etoh_earn_per_liter*etoh_consump #billion US$ from corn + ethanol
solar_pv_earnings = new_PV_production_total*solar_pv_ppa/1000 # billion US$ from solar
etoh_jobs_ag = etoh_consump*ethanol_ef_agric
etoh_jobs_other = etoh_consump*ethanol_ef_other  
solar_jobs_CI = added_PV_capacity*solar_ef_CI
solar_jobs_OM = new_PV_capacity_total*solar_ef_OM
irrig_water_saved = (acres_corn[0] - acres_corn)*spec_irrig

t = range(len(years))
for i in t:
    if irrig_water_saved[i] < spec_irrig * max_corn_irrig :
        irrig_water_saved[i] = irrig_water_saved[i]
    else:
        irrig_water_saved[i] = spec_irrig * max_corn_irrig
        


      
fig1 = plt.figure()
ax = fig1.add_axes([0,0,1,1])
ax.stackplot(years, [ICEV_total, EV_total]) 
ax.legend(labels = ('ICEV Stock', 'EV Stock'),loc=2)
ax.set_title("Vehicle stocks")
ax.set_xlabel('Year', size=12)
ax.set_ylabel('Stock of vehicles [millions]', size=12)
plt.show()
#chart_data = pd.DataFrame(years,[EV_total, ICEV_total])    
st.pyplot(fig1)   
#st.area_chart(chart_data)
# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
#st.button("Re-run")

fig2 = plt.figure()
ax = fig2.add_axes([0,0,1,1])
ax.stackplot(years, [ICEV_sales, EV_sales]) 
ax.legend(labels = ('ICEV sales', 'EV sales'),loc=2, fontsize='small')
ax.set_title("Vehicle sales")
ax.set_xlabel('Year', size=12)
ax.set_ylabel('Sales of vehicles [millions]', size=12)
plt.show()
st.pyplot(fig2) 

fig, axs = plt.subplots(ncols=2, nrows=2,layout="constrained")
#axs.tick_params(axis='both', which='major', labelsize=10)
axs[0,0].plot(years, etoh_consump)
axs[0,0].set_title("Ethanol consumption", size=9)
axs[0,0].tick_params(axis='x', color='m', length=4, direction='in', labelsize = 'small')
axs[0,0].set_ylabel('Ethanol consumption [billion liters]', size=7)
axs[0,0].tick_params(axis='y', color='m', length=4, direction='in', labelsize = 'small')

axs[0,1].plot(years, EV_elec_consump)
axs[0,1].plot(years,new_PV_production_total) 
axs[0,1].legend(labels = ('EV electricity consumption', 'New PV production'),loc=2,fontsize='xx-small')
axs[0,1].set_title("EV electricity consumption and new PV production", size=7)
axs[0,1].tick_params(axis='x', color='m', length=4, direction='in', labelsize = 'small')
axs[0,1].tick_params(axis='y', color='m', length=4, direction='in', labelsize = 'small')
axs[0,1].set_ylabel('Electricity  [TWh]', size=8)

axs[1,0].plot(years, acres_corn) 
axs[1,0].set_title("Harvested acres of corn for ethanol", size=9)
axs[1,0].set_xlabel('Year', size=6)
axs[1,0].tick_params(axis='x', color='m', length=4, direction='in', labelsize = 'small')
axs[1,0].tick_params(axis='y', color='m', length=4, direction='in', labelsize = 'small')
axs[1,0].set_ylabel('Corn acres [millions]', size=8)

axs[1,1].plot(years, irrig_water_saved) 
axs[1,1].set_title("Decreased irrigation water demand", size=9)
axs[1,1].set_xlabel('Year', size=6)
axs[1,1].tick_params(axis='x', color='m', length=4, direction='in', labelsize = 'small')
axs[1,1].tick_params(axis='y', color='m', length=4, direction='in', labelsize = 'small')
axs[1,1].set_ylabel('Irrigation water saved [million acre-ft]', size=7)

plt.show()
#chart_data = pd.DataFrame(years,[EV_total, ICEV_total])    
st.pyplot(fig) 

#fig4 = plt.figure()
#ax = fig4.add_axes([0,0,1,1])

#plt.show()
#chart_data = pd.DataFrame(years,[EV_total, ICEV_total])    
#st.pyplot(fig4) 

fig5 = plt.figure()
ax = fig5.add_axes([0,0,1,1])
ax.stackplot(years, [etoh_earnings, solar_pv_earnings]) 
ax.legend(labels = ('Corn + ethanol net income', 'Solar PV net income'),loc=2)
ax.set_title("Corn + ethanol and Solar PV income")
ax.set_xlabel('Year', size=12)
ax.set_ylabel('Net income [billions]', size=12)
plt.show()
#chart_data = pd.DataFrame(years,[EV_total, ICEV_total])    
st.pyplot(fig5)   

fig6 = plt.figure()
ax = fig6.add_axes([0,0,1,1])
ax.stackplot(years, [etoh_jobs_ag, etoh_jobs_other, solar_jobs_CI,solar_jobs_OM]) 
ax.legend(labels = ('Ethanol agriculture', 'Ethanol other','Solar PV C&I', 'Solar PV O&M'),loc=2, fontsize='small')
ax.set_title("Corn + ethanol and Solar PV jobs")
ax.set_xlabel('Year', size=12)
ax.set_ylabel('Total employment [thousands]', size=12)
plt.show()
#chart_data = pd.DataFrame(years,[EV_total, ICEV_total])    
st.pyplot(fig6)  

#fig7 = plt.figure()
#ax = fig7.add_axes([0,0,1,1])
#plt.show()
#chart_data = pd.DataFrame(years,[EV_total, ICEV_total])    
#st.pyplot(fig7)