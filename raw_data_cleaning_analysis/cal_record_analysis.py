import numpy as np
import pickle

def cal_record_analysis(record_file,output_dir):

    cal_record = dict()
    cal_record['in_cal'] = list()
    cal_record['out_cal'] = list()
    cal_record['diff_cal'] = list()
    cal_record['usr'] = dict()

    with open(record_file,'r') as recf:
        for line in recf:
            line = line.rstrip("\n").split(",")
            if line[0] != "record_id":
                usr = line[1]
                try:
                    in_cal = float(line[2])
                    out_cal = float(line[3])
                    diff_cal = in_cal-out_cal
                    #if in_cal>100000:
                    #    print('test')
                except:
                    continue

                cal_record['in_cal'].append(in_cal)
                cal_record['out_cal'].append(out_cal)
                cal_record['diff_cal'].append(diff_cal)

                if usr not in cal_record['usr']: #initialize user data
                    cal_record['usr'][usr] = [diff_cal]
                else: #update user data
                    cal_record['usr'][usr].append(diff_cal)

    for key, value in cal_record['usr'].items():
        record_num = len(value)
        value = np.array(value)
        diff_ratio = len(value[value<0])/len(value)
        cal_record['usr'][key] = [record_num, diff_ratio]

    with open(output_dir+"/cal_record.pkl",'wb') as outf:
        pickle.dump(cal_record,outf)

def plot_cal_record_distribution(record_pkl_file):
    import matplotlib.pyplot as plt

    with open(record_pkl_file,'rb') as infile:
        cal_record = pickle.load(infile)

    record_num = list()
    diff_ratio = list()

    for value in cal_record['usr'].values():
        record_num.append(value[0])
        diff_ratio.append(value[1])

    #fig,axes = plt.subplots(2,3,figsize=(18,12))
    fig,axes = plt.subplots(2,2,figsize=(14,12))
    fig.suptitle("User cal record distribution analysis")

    #bins1 = np.array([0,]+list(np.logspace(0,np.log10(2000))))
    axes[0][0].hist(record_num, histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[0][0].axvline(x=np.mean(record_num),color='r')
    axes[0][0].set_title("record number distribution (user)")
    #axes[0][0].set_xscale('log', basex=10)

    #bins2 = np.array([0,]+list(np.logspace(0,np.log10(3000))))
    axes[0][1].hist(cal_record['in_cal'], histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[0][1].ticklabel_format(style='sci', scilimits=(-1,2), axis='x')
    axes[0][1].axvline(x=np.mean(cal_record['in_cal']),color='r')
    axes[0][1].set_title("eating cal distribution (record)")
    #axes[0][1].set_xscale('log', basex=10)

    axes[1][0].hist(cal_record['out_cal'], histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[1][0].ticklabel_format(style='sci', scilimits=(-1,2), axis='x')
    axes[1][0].axvline(x=np.mean(cal_record['out_cal']),color='r')
    axes[1][0].set_title("exercise cal distribution (record)")

    axes[1][1].hist(cal_record['diff_cal'], histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[1][1].ticklabel_format(style='sci', scilimits=(-1,2), axis='x')
    axes[1][1].axvline(x=np.mean(cal_record['diff_cal']),color='r')
    axes[1][1].set_title("eating cal - exercise cal distribution (record)")

    #axes[1][1].hist(diff_ratio, histtype="stepfilled",alpha=0.8,log=True,bins=30)
    #axes[1][1].set_title("user's ratio of eating cal - exercise < 0 cal record distribution (user)")

    plt.savefig('cal_record_distribution',bbox_inches='tight')

    plt.close()

def plot_filtered_cal_record_distribution(record_pkl_file,filtered_usr_file,weight_loss_label):
    import matplotlib.pyplot as plt

    with open(record_pkl_file,'rb') as infile:
        cal_record = pickle.load(infile)

    filtered_usr=list()
    with open(filtered_usr_file,'r') as usrf:
        for line in usrf:
            line = line.rstrip("\n").split(",")
            if line[0] != "id":
                filtered_usr.append(str(int(float(line[0]))))

    wl_label = list()
    with open(weight_loss_label,'r') as wlf:
        for line in wlf:
            line = line.rstrip("\n")
            wl_label.append(line)

    record_num = dict()
    record_num['all_usr'] = list()
    diff_ratio = dict()
    diff_ratio['all_usr'] = list()

    for usr,label in zip(filtered_usr,wl_label):
        try:
            if label not in record_num:
                record_num[label] = [cal_record['usr'][usr][0],]
            else:
                record_num[label].append(cal_record['usr'][usr][0])
            record_num['all_usr'].append(cal_record['usr'][usr][0])
        except:
            #print(usr)
            pass

        try:
            if label not in diff_ratio:
                diff_ratio[label] = [cal_record['usr'][usr][1],]
            else:
                diff_ratio[label].append(cal_record['usr'][usr][1])
            diff_ratio['all_usr'].append(cal_record['usr'][usr][1])
        except:
            pass

    fig,axes = plt.subplots(2,5,figsize=(24,12),sharex='row',sharey='row')
    fig.suptitle("User cal record distribution analysis")

    axes[0][0].hist(record_num['all_usr'], histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[0][0].axvline(x=np.mean(record_num['all_usr']),color='r')
    axes[0][0].set_title("all usrs' record \n number distribution (user)")

    axes[0][1].hist(record_num['0'], histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[0][1].axvline(x=np.mean(record_num['0']),color='r')
    #axes[0][1].ticklabel_format(style='sci', scilimits=(-1,2), axis='x')
    axes[0][1].set_title("0%~25% progress usrs' record \n number distribution (user)")

    axes[0][2].hist(record_num['1'], histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[0][2].axvline(x=np.mean(record_num['1']),color='r')
    #axes[0][2].ticklabel_format(style='sci', scilimits=(-1,2), axis='x')
    axes[0][2].set_title("25%~50% progress usrs' record \n number distribution (user)")
    
    axes[0][3].hist(record_num['2'], histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[0][3].axvline(x=np.mean(record_num['2']),color='r')
    #axes[0][3].ticklabel_format(style='sci', scilimits=(-1,2), axis='x')
    axes[0][3].set_title("50%~75% progress usrs' record \n number distribution (user)")

    axes[0][4].hist(record_num['3'], histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[0][4].axvline(x=np.mean(record_num['3']),color='r')
    axes[0][4].set_title("75%~100% progress usrs' record \n number distribution (user)")

    axes[1][0].hist(diff_ratio['all_usr'], histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[1][0].axvline(x=np.mean(diff_ratio['all_usr']),color='r')
    axes[1][0].set_title("all users' negative \n net cal intake ratio record distribution (user)")

    axes[1][1].hist(diff_ratio['0'], histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[1][1].axvline(x=np.mean(diff_ratio['0']),color='r')
    axes[1][1].set_title("0%~25% progress usrs' negative \n net cal intake ratio record distribution(user)")

    axes[1][2].hist(diff_ratio['1'], histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[1][2].axvline(x=np.mean(diff_ratio['1']),color='r')
    axes[1][2].set_title("25%~50% progress usrs' negative \n net cal intake ratio record distribution(user)")

    axes[1][3].hist(diff_ratio['2'], histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[1][3].axvline(x=np.mean(diff_ratio['2']),color='r')
    axes[1][3].set_title("50%~75% progress usrs' negative \n net cal intake ratio record distribution(user)")

    axes[1][4].hist(diff_ratio['3'], histtype="stepfilled",alpha=0.8,log=True,bins=30)
    axes[1][4].axvline(x=np.mean(diff_ratio['3']),color='r')
    axes[1][4].set_title("75%~100% progress usrs' negative \n net cal intake ratio record distribution(user)")

    plt.savefig('cal_record_distribution_filtered',bbox_inches='tight')

    plt.close()


if __name__ == '__main__':

    #cal_record_analysis('../WeightLoss/can_record_consolidated.csv','../WeightLoss/')
    plot_cal_record_distribution('../WeightLoss/cal_record.pkl')
    plot_filtered_cal_record_distribution('../WeightLoss/cal_record.pkl','../WeightLoss/user_features_combine.csv','../WeightLoss/label_slide.csv')

