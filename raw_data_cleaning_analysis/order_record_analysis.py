'''
order_id,user_id,good_id,quantity,created_at,price_each_goods
2,203198,1,1,2013-10-23 21:32:11,80.000
3,203714,2,1,2013-10-24 09:09:28,38.000
4,203803,2,1,2013-10-24 10:39:59,38.000
5,203803,3,1,2013-10-24 10:39:59,72.000
6,203825,1,1,2013-10-24 10:48:46,80.000
10,203871,2,1,2013-10-24 11:17:18,38.000
11,203891,2,1,2013-10-24 11:43:58,38.000
14,205476,1,1,2013-10-25 14:47:53,80.000
15,205476,3,1,2013-10-25 14:47:53,72.000
16,205476,2,1,2013-10-25 14:47:53,40.000
17,205479,1,1,2013-10-25 14:55:30,80.000
18,205483,3,1,2013-10-25 14:58:54,72.000
'''
import numpy as np
import pickle

def order_record_analysis(record_file,output_dir):

    record_order = dict()

    with open(record_file,'r') as recf:
        for line in recf:
            line = line.rstrip("\n").split(",")
            if line[0] != "order_id":
                usr = line[1]
                price = int(line[3])*float(line[5])
                if usr not in record_order: #initialize user data
                    record_order[usr] = [int(line[3]),price] 
                else: #update user data
                    record_order[usr][0] += int(line[3])
                    record_order[usr][1] += price

    with open(output_dir+"/order_record.pkl",'wb') as outf:
        pickle.dump(record_order,outf)

def plot_order_distribution(record_pkl_file):
    import matplotlib.pyplot as plt

    with open(record_pkl_file,'rb') as infile:
        order_record = pickle.load(infile)

    good_number_record = list()
    price_record = list()

    for value in order_record.values():
        good_number_record.append(value[0])
        price_record.append(value[1])

    fig,axes = plt.subplots(1,2,figsize=(12,8))
    fig.suptitle("User order record distribution analysis")

    #bins1 = np.array([0,]+list(np.logspace(0,np.log10(2000))))
    axes[0].hist(good_number_record, histtype="stepfilled",alpha=0.6,log=True,bins=50)
    axes[0].set_title("distribution of the number of goods purchased by user")
    #axes[0].set_xscale('log', basex=10)

    #bins2 = np.array([0,]+list(np.logspace(0,np.log10(3000))))
    axes[1].hist(price_record, histtype="stepfilled",alpha=0.6,log=True,bins=50)
    axes[1].set_title("distribution of the amount of money spent by user")
    #axes[1].set_xscale('log', basex=10)

    plt.savefig('record_order_distribution',bbox_inches='tight')

    plt.close()


if __name__ == '__main__':

    order_record_analysis('../WeightLoss/order_detail_record_consolidated.csv','../WeightLoss/')
    plot_order_distribution('../WeightLoss/order_record.pkl')

