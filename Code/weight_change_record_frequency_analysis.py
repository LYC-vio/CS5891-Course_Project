'''
user_id,weight,record_on,date
1,56.000,2013-02-28,2013-02-28
1,84.000,2013-03-17,2013-03-17
1,63.900,2013-03-18,2013-03-18
1,70.200,2013-10-01,2013-10-01
1,66.000,2013-10-31,2013-10-31
1,62.000,2014-01-11,2014-01-11
2,61.500,2013-06-16,2013-06-16
2,62.000,2013-06-17,2013-06-17
2,62.000,2013-07-07,2013-07-07
2,62.000,2013-08-04,2013-08-04
2,61.600,2013-08-26,2013-08-31
'''
from datetime import datetime
import numpy as np
import pickle

def weight_change_record_frequency_analysis(record_file,output_dir):

    record_frequency = dict()

    with open(record_file,'r') as recf:
        for line in recf:
            line = line.rstrip("\n").split(",")
            if line[0] != "user_id":
                usr = line[0]
                record_time_ = line[2].split("-")
                try:
                    record_time = datetime(int(record_time_[0]), int(record_time_[1]), int(record_time_[2]))
                except:
                    continue
                if usr not in record_frequency: #initialize user data
                    record_frequency[usr] = [1,[record_time,record_time]] #number of record, time intervals (earliest, latest)
                else: #update user data
                    if record_time < datetime(2008, 1, 1): #BOOHEE was found in 2008, any records before this date should be dropped
                        continue
                    if record_time > datetime(2015,12,31):
                        continue
                    if (record_time-record_frequency[usr][-1][0]).days < -30:
                        continue
                    record_frequency[usr][0] += 1
                    if (record_time-record_frequency[usr][-1][0]).days <= 0: #update earliest
                        record_frequency[usr][-1][0] = record_time
                    if record_time >= record_frequency[usr][-1][1]: #update latest
                        if (record_time-record_frequency[usr][-1][1]).days < 30:
                            record_frequency[usr][-1][1] = record_time
                        else:
                            record_frequency[usr].append([record_time,record_time])

    for key, value in record_frequency.items():
        interval_num = len(value)-1
        time_span = 0
        for intv in value[1:]:
            time_span += ((intv[1]-intv[0]).days+1)
        record_frequency[key] = [value[0],time_span,interval_num]
        #if value[0]/time_span > 200:
        #    print(key)

    with open(output_dir+"/weight_change_record_frequency.pkl",'wb') as outf:
        pickle.dump(record_frequency,outf)

def plot_frequency_distribution(record_pkl_file):
    import matplotlib.pyplot as plt

    with open(record_pkl_file,'rb') as infile:
        frequency_record = pickle.load(infile)

    record_number = list()
    record_time_span = list()
    record_interval = list()

    for value in frequency_record.values():
        record_number.append(value[0])
        record_time_span.append(value[1])
        record_interval.append(value[2])

    record_number = np.array(record_number)
    record_interval = np.array(record_interval)
    record_time_span = np.array(record_time_span).astype(float)
    record_density = record_number/record_time_span

    fig,axes = plt.subplots(2,2,figsize=(12,12))
    fig.suptitle("User weight record distribution analysis")

    bins1 = np.array([0,]+list(np.logspace(0,np.log10(2000))))
    axes[0][0].hist(record_number, histtype="stepfilled",alpha=0.6,log=True,bins=bins1)
    axes[0][0].set_title("record number distribution (number of records)")
    axes[0][0].set_xscale('log', basex=10)

    bins2 = np.array([0,]+list(np.logspace(0,np.log10(3000))))
    axes[0][1].hist(record_time_span, histtype="stepfilled",alpha=0.6,log=True,bins=bins2)
    axes[0][1].set_title("record time span (only count those with in intervals) distribution (days)")
    axes[0][1].set_xscale('log', basex=10)

    axes[1][0].hist(record_density, histtype="stepfilled",alpha=0.6,log=True,bins=50)
    axes[1][0].set_title("record density distribution (with in intervals) (record/day)")

    axes[1][1].hist(record_interval, histtype="stepfilled",alpha=0.6,log=True,bins=np.arange(0,35,1))
    axes[1][1].set_title("record interval distribution (number of intervals)")

    plt.savefig('record_frequency_distribution',bbox_inches='tight')

    plt.close()


if __name__ == '__main__':

    #weight_change_record_frequency_analysis('../WeightLoss/weight_record_consolidated(weight change history).csv','../WeightLoss/')
    plot_frequency_distribution('../WeightLoss/weight_change_record_frequency.pkl')

