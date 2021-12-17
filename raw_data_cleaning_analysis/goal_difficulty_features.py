import os
import pandas as pd


def get_goal_difficulty(user_profile='', user_consolidated=''):
    user_id_dict = dict()
    with open(user_consolidated, 'r') as f1:
        for line in f1:
            split_line = line.split(',')
            if split_line[0] == "id":
                continue
            user_id = split_line[0]
            target_weight = split_line[7]
            if target_weight == '' or target_weight == '$null$' or float(target_weight) < 30:
                # print("target weight")
                # print(split_line)
                continue
            weight = split_line[6]
            if weight == '' or weight == '$null$' or float(weight) < 30:
                # print("weight")
                # print(split_line)
                continue
            # print(split_line)
            if target_weight < weight:
                try:
                    user_id_dict[user_id] = [(float(weight) - float(target_weight))/float(weight)]
                except:
                    print("zero of weight")
                    print(split_line)

    with open(user_profile, 'r') as f2:
        for line in f2:
            # print(line)
            split_line = line.split(',')
            user_id = split_line[0]
            # weight = split_line[5]
            lastdays = split_line[5]
            if user_id in user_id_dict.keys() and lastdays != '' and int(lastdays) > 0:
                user_id_dict[user_id].append(lastdays)

    remove_waitlist = []
    for k in user_id_dict:
        if len(user_id_dict[k]) == 1:
            remove_waitlist.append(k)

    for e in remove_waitlist:
        user_id_dict.pop(e)


    print(len(user_id_dict.keys()))
    return user_id_dict


if __name__ == '__main__':
    uid_dict = get_goal_difficulty(user_profile='../data/WeightLoss/userprofile.csv', user_consolidated='../data/WeightLoss/users_consolidated.csv')
    output_dir = '../data/WeightLoss/clean/'
    df = pd.DataFrame.from_dict(uid_dict)
    print("write to file ...")
    df.to_csv(os.path.join(output_dir, 'goal_difficulty_features.csv'), index=False)
