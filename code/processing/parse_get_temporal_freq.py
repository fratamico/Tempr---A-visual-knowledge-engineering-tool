from collections import Counter
from decimal import Decimal
import json
import numpy as np


################################################
# USER ENTERED SPECIFICATIONS
#
# Specify here the two files to be read in
# GROUP_A_FILE = "_MOOC_events_LL_formatted.csv"
# GROUP_B_FILE = "_MOOC_events_HL_formatted.csv"
GROUP_A_FILE = "_PHET_a2_low_log.txt"
GROUP_B_FILE = "_PHET_a2_high_log.txt"
# GROUP_A_FILE = "_test_low.txt"
# GROUP_B_FILE = "_test_high.txt"
#
# Specify here a name for the data
DATA_NAME = "PhET Sim"
# DATA_NAME = "MOOC Climate Change"
#
# Specify here a two letter name for group
GROUP_A_NAME = "LL" #brown color
GROUP_B_NAME = "HL" #blue/green color
#
################################################

##write user entered specifications to file
f = open("data/get_data_names.js", 'w')
f.write("function get_data_names() {\n")
f.write("   return {\n")
f.write('     "DATA_NAME": "' + str(DATA_NAME) + '",\n')
f.write('     "GROUP_A_NAME": "' + str(GROUP_A_NAME) + '",\n')
f.write('     "GROUP_B_NAME": "' + str(GROUP_B_NAME) + '",\n')
f.write("   }\n")
f.write("}")
f.close()


LL_FILE = GROUP_A_FILE
HL_FILE = GROUP_B_FILE

f_low = open(LL_FILE)
lines = f_low.readlines()
num_LL = 0
all_types = []
for line in lines:
    val = line.replace("\n", "")
    if "=====" in val:
        num_LL += 1
    all_types.append(val)
f_low.close()

f_high = open(HL_FILE)
lines = f_high.readlines()
num_HL = 0
for line in lines:
    val = line.replace("\n", "")
    if "=====" in val:
        num_HL += 1
    all_types.append(val)
f_high.close()

all_types = set(all_types)
all_types.remove("========================================")


##write number in each group to file
f = open("data/get_num_users.js", 'w')
f.write("function get_num_users() {\n")
f.write("   return {\n")
f.write('    "High": ' + str(num_HL) + ',\n')
f.write('    "Low": ' + str(num_LL) + ',\n')
f.write("   }\n")
f.write("}")
f.close()


## write all actions to file for use in dashboard
f = open("data/get_raw_log_events.js", 'w')
f.write("function get_raw_log_events() {\n")
f.write("   return ")
f.write(str(sorted(all_types)))
f.write(";\n")
f.write("}")
f.close()




def get_list_freq(l):
    ## Get frequency of each item in a list
    ## Return a dictionary of item:frequency
    freq_dict = Counter(l)
    for item in freq_dict:
        freq_dict[item] = freq_dict[item]/float(len(l))
    return freq_dict

def split_list(l):
    ## Split the list into NUM_SPLITS segments
    ## Return a list of lists
    num_items = len(l)/NUM_SPLITS
    s_list = {}
    for i in range(NUM_SPLITS):
        s_list[i] = l[i*num_items:((i+1)*num_items)]
    for i in range(len(l) % NUM_SPLITS):
        s_list[NUM_SPLITS-1].append(l[len(l)-1-i])
    return s_list




## Create dictionary of "High/Low":user:list of actions
d = {"High": {}, "Low": {}}
#read in, save to dict of dict:"high":user:actions

f_high = open(HL_FILE)

lines = f_high.readlines()
user = 0
for line in lines:
    val = line.replace("\n", "")
    if "======" in val:
        user += 1
        d["High"][user] = []
    else:
        d["High"][user].append(val)
f_high.close()

f_low = open(LL_FILE)
lines = f_low.readlines()
user = 0
for line in lines:
    val = line.replace("\n", "")
    if "======" in val:
        user += 1
        d["Low"][user] = []
    else:
        d["Low"][user].append(val)
f_low.close()


for NUM_SPLITS in range(1,21): #precalculate for all potential NUM_SPLITS

    ## Generate a dictionary of the frequency of items at eact of NUM_SPLITS time series
    f_dict = {}
    f_dict["High"] = {}
    f_dict["Low"] = {}

    for user in d["High"]:
        s_list = split_list(d["High"][user])
        f_dict["High"][user] = {}
        for i in range(NUM_SPLITS):
            f_dict["High"][user][i] = get_list_freq(s_list[i])

    for user in d["Low"]:
        s_list = split_list(d["Low"][user])
        f_dict["Low"][user] = {}
        for i in range(NUM_SPLITS):
            f_dict["Low"][user][i] = get_list_freq(s_list[i])


    ## Calculate the average frequency for the two groups at each timeslice and for each action
    ### This would be where to add the t-test
    avg_freq = {}
    avg_freq["High"] = {}
    avg_freq["Low"] = {}
    num_high_users = len(f_dict["High"].keys())
    num_low_users = len(f_dict["Low"].keys())

    #get list of frequencies for each user
    users_action_dict = {}
    users_action_dict["High"] = {}
    users_action_dict["Low"] = {}

    for i in range(NUM_SPLITS):
        avg_freq["High"][i] = {}
        users_action_dict["High"][i] = {}
        for aca in all_types:
            users_action_dict["High"][i][aca] = []
            total = 0
            for user in d["High"]:
                total += f_dict["High"][user][i][aca]
                users_action_dict["High"][i][aca].append(f_dict["High"][user][i][aca])
            avg_freq["High"][i][aca] = total/float(num_high_users)


    for i in range(NUM_SPLITS):
        avg_freq["Low"][i] = {}
        users_action_dict["Low"][i] = {}
        for aca in all_types:
            users_action_dict["Low"][i][aca] = []
            total = 0
            for user in d["Low"]:
                total += f_dict["Low"][user][i][aca]
                users_action_dict["Low"][i][aca].append(f_dict["Low"][user][i][aca])
            avg_freq["Low"][i][aca] = total/float(num_low_users)


    with open('json_files/ALL_ACTIONS_' + str(NUM_SPLITS) + '.json', 'w') as fp:
        json.dump(users_action_dict, fp)






##heatmap
NUM_SPLITS = 5

## Generate a dictionary of the frequency of items at eact of NUM_SPLITS time series
f_dict = {}
f_dict["High"] = {}
f_dict["Low"] = {}

for user in d["High"]:
    s_list = split_list(d["High"][user])
    f_dict["High"][user] = {}
    for i in range(NUM_SPLITS):
        f_dict["High"][user][i] = get_list_freq(s_list[i])

for user in d["Low"]:
    s_list = split_list(d["Low"][user])
    f_dict["Low"][user] = {}
    for i in range(NUM_SPLITS):
        f_dict["Low"][user][i] = get_list_freq(s_list[i])


## Calculate the average frequency for the two groups at each timeslice and for each action
### This would be where to add the t-test
avg_freq = {}
avg_freq["High"] = {}
avg_freq["Low"] = {}
num_high_users = len(f_dict["High"].keys())
num_low_users = len(f_dict["Low"].keys())

#get list of frequencies for each user
users_action_dict = {}
users_action_dict["High"] = {}
users_action_dict["Low"] = {}

for i in range(NUM_SPLITS):
    avg_freq["High"][i] = {}
    users_action_dict["High"][i] = {}
    for aca in all_types:
        users_action_dict["High"][i][aca] = []
        total = 0
        for user in d["High"]:
            total += f_dict["High"][user][i][aca]
            users_action_dict["High"][i][aca].append(f_dict["High"][user][i][aca])
        avg_freq["High"][i][aca] = total/float(num_high_users)


for i in range(NUM_SPLITS):
    avg_freq["Low"][i] = {}
    users_action_dict["Low"][i] = {}
    for aca in all_types:
        users_action_dict["Low"][i][aca] = []
        total = 0
        for user in d["Low"]:
            total += f_dict["Low"][user][i][aca]
            users_action_dict["Low"][i][aca].append(f_dict["Low"][user][i][aca])
        avg_freq["Low"][i][aca] = total/float(num_low_users)

#save the median, 25%, and 75% values
final_percentile_dict = {}

for aca in all_types:
    final_percentile_dict[aca] = {}
    for t in ["low_25", "low_med", "low_75", "high_25", "high_med", "high_75"]:
        final_percentile_dict[aca][t] = {}
    for i in range(NUM_SPLITS):
        final_percentile_dict[aca]["low_25"][i] = np.percentile(users_action_dict["Low"][i][aca], 25)
        final_percentile_dict[aca]["low_med"][i] = np.percentile(users_action_dict["Low"][i][aca], 50)
        final_percentile_dict[aca]["low_75"][i] = np.percentile(users_action_dict["Low"][i][aca], 75)
        
        final_percentile_dict[aca]["high_25"][i] = np.percentile(users_action_dict["High"][i][aca], 25)
        final_percentile_dict[aca]["high_med"][i] = np.percentile(users_action_dict["High"][i][aca], 50)
        final_percentile_dict[aca]["high_75"][i] = np.percentile(users_action_dict["High"][i][aca], 75)


final_med_dict = {}

for aca in all_types:
    final_med_dict[aca] = {}
    for i in range(NUM_SPLITS):
        final_med_dict[aca][i] = final_percentile_dict[aca]["high_med"][i] - final_percentile_dict[aca]["low_med"][i]


# determine top 50 that should be in heatmap
top_events_dict = {}
for aca in final_med_dict:
    for i in range(NUM_SPLITS):
        if not aca in top_events_dict:
            top_events_dict[aca] = abs(final_med_dict[aca][i])
        else:
            if abs(final_med_dict[aca][i]) > top_events_dict[aca]:
                top_events_dict[aca] = abs(final_med_dict[aca][i])

top_events = []
top_event_values = []
for k,v in sorted(top_events_dict.iteritems(), key=lambda x:-x[1])[:50]:
    top_events.append(k)
    top_event_values.append(v)
rowLabel = list(set(top_events))



d_file = open("heatmap_data.tsv", 'w')
d_file.write("row_idx\tcol_idx\tlog2ratio\n")
col = 0
for aca in rowLabel:
    col += 1
    for i in range(NUM_SPLITS):
        d_file.write(str(col) + "\t" + str(i+1) + "\t" + str(final_med_dict[aca][i]) + "\n")


# get domain of heatmap
domain_max = np.percentile(top_event_values, 90) #90th percentile, so that we can better see the smaller changes
domain =  [round(val, 3) for val in np.linspace(-1*domain_max,domain_max,11)]

##write number in each group to file
f = open("data/get_heatmap_data.js", 'w')
f.write("function get_heatmap_data() {\n")
f.write("   return {\n")
f.write('     "ROW_LABELS": ' + str(rowLabel) + ',\n')
f.write('     "DOMAIN": ' + str(domain) + '\n')
f.write("   }\n")
f.write("}")
f.close()





