from collections import Counter
from decimal import Decimal
import json
import numpy as np

NUM_SPLITS = 10
THREEPLACES = Decimal(10) ** -2


f_low = open("a2_low_log.txt")

lines = f_low.readlines()

all_types = []
for line in lines:
    val = line.replace("\n", "")
    all_types.append(val)
f_low.close()

f_high = open("a2_high_log.txt")
lines = f_high.readlines()
for line in lines:
    val = line.replace("\n", "")
    all_types.append(val)
f_high.close()

all_types = set(all_types)
all_types.remove("========================================")


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

f_low = open("a2_high_log.txt")

lines = f_low.readlines()
user = 0
for line in lines:
    val = line.replace("\n", "")
    if "======" in val:
        user += 1
        d["High"][user] = []
    else:
        d["High"][user].append(val)
f_low.close()

f_high = open("a2_low_log.txt")
lines = f_high.readlines()
user = 0
for line in lines:
    val = line.replace("\n", "")
    if "======" in val:
        user += 1
        d["Low"][user] = []
    else:
        d["Low"][user].append(val)
f_high.close()


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




final_dict = {}

for aca in all_types:
    final_dict[aca] = {}
    for i in range(NUM_SPLITS):
        final_dict[aca][i] = str(avg_freq["High"][i][aca] - avg_freq["Low"][i][aca])
    # write to file
    #outfile = open("json_files/horizon-" + aca + ".json", 'w')
    #outfile.write('{"timeslice":' + str(range(1,NUM_SPLITS + 1)) + ',\n"freq_difference":[')
    #outfile.write(",".join(final_dict[aca].values()))
    #outfile.write("]}")

# Save frequencies to json file
# This is read back into javascript when merging actions
with open('json_files/ALL_ACTIONS_FREQUENCY.json', 'w') as fp:
    json.dump(final_dict, fp)


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

# Save frequencies to json file
# This is read back into javascript when merging actions
with open('json_files/ALL_ACTIONS_PERCENTILES.json', 'w') as fp:
    json.dump(final_percentile_dict, fp)

with open('json_files/ALL_ACTIONS.json', 'w') as fp:
    json.dump(users_action_dict, fp)


"""
print "user.bulbResistorEditor.changed: ", ",".join(final_dict["user.bulbResistorEditor.changed"].values())
print "user.nonContactAmmeter.drag: ", ",".join(final_dict["user.nonContactAmmeter.drag"].values())

print "model.nonContactAmmeterModel.measuredCurrentChanged: ", ",".join(final_dict["model.nonContactAmmeterModel.measuredCurrentChanged"].values())
print "model.junction.junctionFormed: ", ",".join(final_dict["model.junction.junctionFormed"].values())
#print "user.nonContactAmmeter.drag: ", ",".join(final_dict["user.nonContactAmmeter.drag"].values())
"""

"""
## Create json files for initially defined merged events

# Voltmeter Testing
voltmeter_test_list = ["model.voltmeterBlackLeadModel.connectionBroken", "model.voltmeterBlackLeadModel.connectionFormed", "model.voltmeterModel.measuredVoltageChanged", "model.voltmeterRedLeadModel.connectionBroken", "model.voltmeterRedLeadModel.connectionFormed", "user.blackProbe.drag", "user.blackProbe.endDrag", "user.blackProbe.startDrag", "user.redProbe.drag", "user.redProbe.endDrag", "user.redProbe.startDrag", "user.voltmeterCheckBox.pressed"]

test_final_dict = {}
for i in range(NUM_SPLITS):
    test_final_dict[i] = {}
    total = 0
    for aca in voltmeter_test_list:
        total += float(final_dict[aca][i])
    test_final_dict[i] = str(total)

print "voltmeter_test_final_dict: ", ",".join(test_final_dict.values())
outfile = open("json_files/horizon-Voltmeter Testing.json", 'w')
outfile.write('{"timeslice":' + str(range(1,NUM_SPLITS + 1)) + ',\n"freq_difference":[')
outfile.write(",".join(test_final_dict.values()))
outfile.write("]}")


# Ammeter Testing
ammeter_test_list = ["model.nonContactAmmeterModel.connectionBroken","model.nonContactAmmeterModel.connectionFormed","model.nonContactAmmeterModel.measuredCurrentChanged","model.seriesAmmeter.fireEnded","model.seriesAmmeter.fireStarted","model.seriesAmmeter.measuredCurrentChanged","user.nonContactAmmeter.drag","user.nonContactAmmeter.endDrag","user.nonContactAmmeter.startDrag","user.nonContactAmmeterCheckBox.pressed","user.seriesAmmeter.addedComponent","user.seriesAmmeter.movedComponent","user.seriesAmmeter.removedComponent","user.seriesAmmeterCheckBox.pressed"]

test_final_dict = {}
for i in range(NUM_SPLITS):
    test_final_dict[i] = {}
    total = 0
    for aca in ammeter_test_list:
        total += float(final_dict[aca][i])
    test_final_dict[i] = str(total)

print "ammeter_test_final_dict: ", ",".join(test_final_dict.values())
outfile = open("json_files/horizon-Ammeter Testing.json", 'w')
outfile.write('{"timeslice":' + str(range(1,NUM_SPLITS + 1)) + ',\n"freq_difference":[')
outfile.write(",".join(test_final_dict.values()))
outfile.write("]}")


# All Testing
all_test_list = voltmeter_test_list + ammeter_test_list

test_final_dict = {}
for i in range(NUM_SPLITS):
    test_final_dict[i] = {}
    total = 0
    for aca in all_test_list:
        total += float(final_dict[aca][i])
    test_final_dict[i] = str(total)

print "all_test_final_dict: ", ",".join(test_final_dict.values())
outfile = open("json_files/horizon-All Testing.json", 'w')
outfile.write('{"timeslice":' + str(range(1,NUM_SPLITS + 1)) + ',\n"freq_difference":[')
outfile.write(",".join(test_final_dict.values()))
outfile.write("]}")


# Initial Building
build_list = ["user.battery.addedComponent","user.circuitSwitch.addedComponent","user.grabBagResistor.addedComponent","user.lightBulb.addedComponent","user.resistor.addedComponent","user.seriesAmmeter.addedComponent","user.wire.addedComponent"]

basic_build_final_dict = {}
for i in range(NUM_SPLITS):
    basic_build_final_dict[i] = {}
    total = 0
    for aca in build_list:
        total += float(final_dict[aca][i])
    basic_build_final_dict[i] = str(total)


print "basic_build_final_dict: ", ",".join(basic_build_final_dict.values())
outfile = open("json_files/horizon-Initial Building.json", 'w')
outfile.write('{"timeslice":' + str(range(1,NUM_SPLITS + 1)) + ',\n"freq_difference":[')
outfile.write(",".join(basic_build_final_dict.values()))
outfile.write("]}")

"""



d_file = open("heatmap_data.tsv", 'w')
d_file_2 = open("heatmap_data_labels.tsv", 'w')
d_file.write("row_idx\tcol_idx\tlog2ratio\n")
col = 0
for aca in final_dict:
    col += 1
    d_file_2.write('"' + aca + '",')
    if col == 51:
        break
    for i in range(NUM_SPLITS):
        d_file.write(str(col) + "\t" + str(i+1) + "\t" + str(final_dict[aca][i]) + "\n")



d_file_3 = open("heatmap_data_labels2.tsv", 'w')
for i in range(61):
    val = str(Decimal(str(i*100/float(60))).quantize(THREEPLACES))
    d_file_3.write("'" + val + "%',")





