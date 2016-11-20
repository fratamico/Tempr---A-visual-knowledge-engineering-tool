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


for NUM_SPLITS in range(1,21): #precalculate for all potential NUM_SPLITS

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



d_file = open("heatmap_data.tsv", 'w')
d_file_2 = open("heatmap_data_labels.tsv", 'w')
d_file.write("row_idx\tcol_idx\tlog2ratio\n")
col = 0
if "MOOC" in LL_FILE:
    rowLabel = ['graded_problem5.module5.problem_check', 'video3.module1.play_video', 'graded_problem9.module5.problem_check', 'video2.module2.play_video', 'graded_problem2.module5.problem_check', 'video1.module4.play_video', 'graded_problem11.module5.problem_check', 'graded_problem6.module2.problem_check', 'graded_problem4.module5.problem_check', 'video3.module2.pause_video', 'self_test24.module2.problem_check', 'graded_problem4.module6.problem_check', 'graded_problem4.module2.problem_check', 'video3.module5.play_video', 'graded_problem8.module2.problem_check', 'video2.module2.pause_video', 'video1.module4.pause_video', 'graded_problem3.module5.problem_check', 'video11.module2.play_video', 'graded_problem7.module5.problem_check', 'self_test23.module2.problem_check', 'self_test17.module2.problem_check', 'video19.module2.play_video', 'video4.module2.play_video', 'video4.module6.play_video', 'video4.module6.pause_video', 'video5.module2.play_video', 'graded_problem10.module4.problem_check', 'graded_problem5.module2.problem_check', 'video4.module5.play_video', 'video12.module2.play_video', 'video3.module5.pause_video', 'self_test20.module2.problem_check', 'graded_problem8.module5.problem_check', 'video1.module5.play_video', 'forum.read', 'graded_problem1.module6.problem_check', 'video11.module2.pause_video', 'video19.module2.pause_video', 'video2.module6.play_video', 'self_test16.module2.problem_check', 'graded_problem3.module2.problem_check', 'self_test22.module2.problem_check', 'graded_problem6.module5.problem_check', 'video3.module1.pause_video', 'video1.module6.play_video', 'video2.module6.pause_video', 'graded_problem2.module6.problem_check', 'video1.module2.play_video', 'video2.module1.pause_video', 'graded_problem10.module5.problem_check']
if "PHET" in LL_FILE:
    rowLabel = ['user.showReadoutCheckBox.pressed', 'user.blackProbe.drag', 'user.bulbResistorEditor.activated', 'user.batteryResistanceEditor.changed', 'user.mediumRadioButton.pressed', 'user.blackProbe.startDrag', 'model.nonContactAmmeterModel.measuredCurrentChanged', 'user.battery.addedComponent', 'user.voltmeterCheckBox.pressed', 'user.nonContactAmmeter.startDrag', 'model.voltmeterRedLeadModel.connectionFormed', 'user.resetAllConfirmationDialogYesButton.pressed', 'user.smallRadioButton.pressed', 'user.resistor.movedComponent', 'model.nonContactAmmeterModel.connectionFormed', 'user.resistorEditor.changed', 'user.grabBagItemButton.pressed', 'user.redProbe.startDrag', 'user.resistorEditor.deactivated', 'model.junction.junctionSplit', 'user.resetAllButton.pressed', 'user.nonContactAmmeter.drag', 'user.redProbe.drag', 'user.blackProbe.endDrag', 'user.junction.movedJunction', 'user.resetAllConfirmationDialogNoButton.pressed', 'user.resistorEditor.activated', 'user.battery.removedComponent', 'model.voltmeterModel.measuredVoltageChanged', 'user.resistorEditor.endDrag', 'model.voltmeterBlackLeadModel.connectionBroken', 'user.lightBulb.removedComponent', 'user.wire.addedComponent', 'user.resistor.removedComponent', 'parser.break.merge', 'user.voltageEditor.endDrag', 'model.voltmeterRedLeadModel.connectionBroken', 'user.resistor.addedComponent', 'user.resistorEditor.startDrag', 'model.junction.junctionFormed', 'user.nonContactAmmeter.endDrag', 'user.wire.removedComponent', 'model.resistor.fireStarted', 'user.redProbe.endDrag', 'model.voltmeterBlackLeadModel.connectionFormed', 'user.nonContactAmmeterCheckBox.pressed', 'model.nonContactAmmeterModel.connectionBroken', 'user.wire.movedComponent', 'model.battery.currentChanged', 'user.voltageEditor.windowClosing']
else:
    print "need to fix heatmap"
for aca in rowLabel:
    col += 1
    d_file_2.write('"' + aca + '",')
    if col == 51:
        break
    for i in range(NUM_SPLITS):
        d_file.write(str(col) + "\t" + str(i+1) + "\t" + str(final_med_dict[aca][i]) + "\n")

min_num = 100000
max_num = -10000
for aca in final_med_dict:
    for i in range(NUM_SPLITS):
        if final_med_dict[aca][i] < min_num:
            min_num = final_med_dict[aca][i]
        if final_med_dict[aca][i] > max_num:
            max_num = final_med_dict[aca][i]

print min_num
print max_num


top_events = []
for aca in final_med_dict:
    for i in range(NUM_SPLITS):
        if final_med_dict[aca][i] < -.0000001:
            top_events.append(aca)
        if final_med_dict[aca][i] > .0000001:
            top_events.append(aca)

top_events = set(top_events)
print len(top_events)
for aca in final_med_dict:
    if aca not in top_events:
        top_events.add(aca)
    if len(top_events) == 50:
        break
print len(top_events)
print top_events



THREEPLACES = Decimal(10) ** -2
d_file_3 = open("heatmap_data_labels2.tsv", 'w')
for i in range(61):
    val = str(Decimal(str(i*100/float(60))).quantize(THREEPLACES))
    d_file_3.write("'" + val + "%',")





