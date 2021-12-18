import numpy as np

def spreading_pattern_analysis(usr_label_file,follow_edg_file,comment_edg_file,mention_edg_file1,mention_edg_file2,):

    usr_label = list()
    
    with open(usr_label_file,'r') as ulf:
        for line in ulf:
            if line[0]!="y":
                usr_label.append(int(float(line.rstrip('\n'))))

    follow_dict = dict()
    with open(follow_edg_file,'r') as fllf:
        for line in fllf:
            line = line.rstrip('\n').split(',')
            if line[3] == '1':
                usr_followed = int(float(line[0]))
                follower = int(float(line[1]))
                if usr_followed not in follow_dict:
                    follow_dict[usr_followed] = [follower,]
                else:
                    follow_dict[usr_followed].append(follower)

    comment_dict = dict()
    with open(comment_edg_file,'r') as comf:
        for line in comf:
            line = line.rstrip('\n').split(',')
            if line[2] == '1':
                usr_commented = int(float(line[0]))
                comment_by = int(float(line[1]))
                if usr_commented not in comment_dict:
                    comment_dict[usr_commented] = [comment_by,]
                else:
                    comment_dict[usr_commented].append(comment_by)

    mention_dict = dict()
    with open(mention_edg_file1,'r') as menf1:
        for line in menf1:
            line = line.rstrip('\n').split(',')
            if line[4] == '1':
                usr_mentioned = int(float(line[0]))
                mentioned_by = int(float(line[1]))
                if usr_mentioned not in mention_dict:
                    mention_dict[usr_mentioned] = [mentioned_by,]
                else:
                    mention_dict[usr_mentioned].append(mentioned_by)

    with open(mention_edg_file2,'r') as menf2:
        for line in menf2:
            line = line.rstrip('\n').split(',')
            if line[4] == '1':
                usr_mentioned = int(float(line[0]))
                mentioned_by = int(float(line[1]))
                if usr_mentioned not in mention_dict:
                    mention_dict[usr_mentioned] = [mentioned_by,]
                else:
                    mention_dict[usr_mentioned].append(mentioned_by)

    for edg_dict in [follow_dict,comment_dict,mention_dict]:
        for key,value in edg_dict.items():
            edg_dict[key] = list(set(value))

    follow_spreading_pattern = dict()
    comment_spreading_pattern = dict()
    mention_spreading_pattern = dict()
    for pattern_dict in [follow_spreading_pattern,comment_spreading_pattern,mention_spreading_pattern]:
        for i in range(4):
            pattern_dict[i] = list()

    for key,value in follow_dict.items():
        for i in value:
            follow_spreading_pattern[usr_label[key]].append(usr_label[i])

    for key,value in comment_dict.items():
        for i in value:
            comment_spreading_pattern[usr_label[key]].append(usr_label[i])

    for key,value in mention_dict.items():
        for i in value:
            mention_spreading_pattern[usr_label[key]].append(usr_label[i])

    for pattern_dict in [follow_spreading_pattern,comment_spreading_pattern,mention_spreading_pattern]:
        for key,value in pattern_dict.items():
            value = np.array(value)
            pattern_dict[key] = dict()
            for i in range(4):
                pattern_dict[key][i] = len(value[value==i])/len(value)

    print("spreading pattern for follow-edge:")
    for i in range(4):
        print("category "+str(i)+":")
        print(follow_spreading_pattern[i])

    print("spreading pattern for commentedge:")
    for i in range(4):
        print("category "+str(i)+":")
        print(comment_spreading_pattern[i])

    print("spreading pattern for mention-edge:")
    for i in range(4):
        print("category "+str(i)+":")
        print(mention_spreading_pattern[i])

if __name__ == '__main__':

    usr_label_file='../WeightLoss/label_slide.csv'
    follow_edg_file='../WeightLoss/follow_edge_final.csv'
    comment_edg_file='../WeightLoss/comment_edge_final.csv'
    mention_edg_file1='../WeightLoss/mention_edge1_final.csv'
    mention_edg_file2='../WeightLoss/mention_edge2_final.csv'
    
    spreading_pattern_analysis(usr_label_file,follow_edg_file,comment_edg_file,mention_edg_file1,mention_edg_file2,)