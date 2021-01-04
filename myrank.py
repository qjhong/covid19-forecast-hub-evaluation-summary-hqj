#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 14:02:40 2020

@author: qijunhong
"""

import pandas as pd
from datetime import datetime
from datetime import timedelta
from os import path
import matplotlib.pyplot as plt
import numpy
import sys
import os

def get_rank(model_name):
    date = datetime(2020,4,25)
    rank_collect = []
    
    while True:
        if date.month<10:
            month = '0'+ str(date.month)
        else:
            month = str(date.month)
        if date.day<10:
            day = '0'+ str(date.day)
        else:
            day = str(date.day)
        filename="../covid19-forecast-hub-evaluation/summary/summary_us_"+str(date.year)+'-'+month+'-'+day+'.csv'
        if not path.exists(filename): break
        data = pd.read_csv(filename)
        #print(data.iloc[:,0]==)
        #print(list(data.index))
        #print(list(data.loc[data.iloc[:,0]=='QJHong-Encounter'].index))
        try:
            rank = list(data.loc[data.iloc[:,0]==model_name].index)
            rank_baseline = list(data.loc[data.iloc[:,0]=='Baseline'].index)
#            if model_name == 'YYG-ParamSearch' and date >= datetime(2020,10,24): break
            if rank_baseline[0] < rank[0]:
                rank_collect.append([date,rank[0]])
            else:
                rank_collect.append([date,rank[0]+1])
        except:
            pass
        date = date + timedelta(days=7)
    
    rmse_6w = []
    mae_6w = []
    #print(model_name)
    for i in range(1,7):
        filename="../covid19-forecast-hub-evaluation/summary/summary_"+str(i)+'_weeks_ahead_us.csv'
        data = pd.read_csv(filename)
        try:
            tmp = data.loc[data.iloc[:,0]==model_name].values[0][1:]
            error = []
            for j in range(len(tmp)):
                if numpy.isnan(tmp[j]):
                    pass
                else:
                    error.append(tmp[j])
            #print(error)
            error = numpy.asarray(error)
            rmse = min( numpy.sqrt( sum(error**2) / len(error) ) , numpy.sqrt( sum(error[3:]**2) / len(error[3:]) ) )
            mae = min( sum(abs(error)) / len(error) ,  sum(abs(error[3:])) / len(error[3:]) )
            #rmse = error[0]**2.
            #mae = abs(error[0])
            #beta = 0.8
            #for j in range(len(error)):
            #    rmse = rmse*beta + error[j]**2.*(1.-beta)
            #    mae = mae*beta + abs(error[j])*(1.-beta)
            #rmse = numpy.sqrt(rmse))
            #print(rmse)
            rmse_6w.append(rmse)
            mae_6w.append(mae)
        except:
            pass
    #print(model_name,rank_collect,rmse_6w)
    while len(rmse_6w) < 6:
        rmse_6w.append(-1)
    while len(mae_6w) < 6:
        mae_6w.append(-1)
    rmse_6w.append(numpy.mean(rmse_6w[0:4]))
    mae_6w.append(numpy.mean(mae_6w[0:4]))
    return rank_collect,rmse_6w,mae_6w

def plot_rank(model_name):
    rank_collect,rmse_6w,mae_6w = get_rank(model_name)
    df = pd.DataFrame(rank_collect)
    if df.shape[0] >= 3:
        plt.plot(df.iloc[3:,0],df.iloc[3:,1],'.-')
        rmse_6w = numpy.asarray(rmse_6w) * 100.
        mae_6w = numpy.asarray(mae_6w) * 100.
        print("%s,%5.1f /%5.1f +-%5.1f, %5.1f%% /%5.1f%%, %5.1f%% /%5.1f%% /%5.1f%% /%5.1f%% /%5.1f%% /%5.1f%%, %5.1f%% /%5.1f%% /%5.1f%% /%5.1f%% /%5.1f%% /%5.1f%%" % (model_name,numpy.median(df.iloc[3:,1].values),numpy.mean(df.iloc[3:,1].values),numpy.std(df.iloc[3:,1].values),rmse_6w[-1],mae_6w[-1],rmse_6w[0],rmse_6w[1],rmse_6w[2],rmse_6w[3],rmse_6w[4],rmse_6w[5],mae_6w[0],mae_6w[1],mae_6w[2],mae_6w[3],mae_6w[4],mae_6w[5]) )
        #plt.plot(df.iloc[0:,0],df.iloc[0:,1],'.-')
        for i in range(3,df.shape[0]):
            plt.text(df.iloc[i,0]-timedelta(days=1),df.iloc[i,1]-.3,str(df.iloc[i,1]),fontsize=7)

sys.stdout = open('rank_results', 'w')
F = open('model_name','r')
lines = [ line.split() for line in F ]
for line in lines:
    plot_rank(line[0])
F.close()
sys.stdout.close()

os.system("echo 'Model, Rank_Median/Mean/STD, mean_RMSE/MAE_1234w, RMSE_1w/2w/3w/4w/5w/6w, MAE_1w/2w/3w/4w/5w/6w' > rank.csv")
os.system("cat rank_results | sort -n -k2 >> rank.csv")
os.system("echo 'Model, Rank_Median/Mean/STD, mean_RMSE/MAE_1234w, RMSE_1w/2w/3w/4w/5w/6w, MAE_1w/2w/3w/4w/5w/6w' > rank_RMSE_4w.csv")
os.system("cat rank_results | sort -n -k7 >> rank_rmse_4w.csv")

plt.close()
sys.stdout = open('rank_results', 'w')

plot_rank('QJHong-Encounter')    
plot_rank('YYG-ParamSearch')    
plot_rank('IHME-CurveFit')    
plot_rank('UCLA-SuEIR')    
plot_rank('USC-SI_kJalpha')    
plot_rank('UMass-MechBayes')    
#plot_rank('Columbia_UNC-SurvCon')    
sys.stdout.close()
    
plt.ylim([0,40])
plt.gca().invert_yaxis()
plt.xlabel('Date')
plt.ylabel('Ranking')
plt.legend(['QJHong-Encounter','YYG-ParamSearch','IHME-CurveFit','UCLA-SuEIR','USC-SI_kJalpha','UMass-MechBayes'])#,'OliverWyman-Navigator'])#,'COVIDhub-ensemble','LANL-GrowthRate'])
plt.xticks([datetime(2020,6,1),datetime(2020,7,1),datetime(2020,8,1),datetime(2020,9,1),datetime(2020,10,1),datetime(2020,11,1),datetime(2020,12,1)],['2020/6/1','7/1','8/1','9/1','10/1','11/1','12/1'])
plt.savefig('Model_Rank',dpi=150)
plt.show()

