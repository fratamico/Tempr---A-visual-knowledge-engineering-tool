from collections import Counter
import numpy
import scipy.stats
from decimal import Decimal


THREEPLACES = Decimal(10) ** -3
FIVEPLACES = Decimal(10) ** -5

f_low = open("a2_low_log.txt")

lines = f_low.readlines()

all_types = []
for line in lines:
    val = line.replace("\n", "")
    all_types.append(val)
f_low.close()

list_file = open("list_file.csv", 'w')
for x in sorted(set(all_types)):
    list_file.write('<li><input type="checkbox" name="aca" value="' + x + '"> ' + x + '</li>\n')

list_file = open("list_file_test.csv", 'w')
for x in sorted(set(all_types)):
    list_file.write('<li>' + x + '</li>\n')

f_high = open("a2_high_log.txt")
lines = f_high.readlines()
for line in lines:
    val = line.replace("\n", "")
    all_types.append(val)
f_high.close()

all_types = set(all_types)
all_types.remove("========================================")



counts_dict = {}
counts_dict["High"] = {}
counts_dict["Low"] = {}

#for t in all_types:
#    counts_dict["High"][t] = Counter()
#    counts_dict["Low"][t] = Counter()

#print counts_dict
#print len(counts_dict["High"])
#print len(counts_dict["Low"])

#raise "Wewweew"


f_low = open("a2_low_log.txt")
lines = f_low.readlines()

user = 0
for line in lines:
    if "==========" in line:
        user += 1
        counts_dict["Low"][user] = {}
        for t in all_types:
            counts_dict["Low"][user] = Counter()
    else:
        aca = line.replace("\n", "")
        counts_dict["Low"][user][aca] += 1

f_low.close()


f_high = open("a2_high_log.txt")
lines = f_high.readlines()

user = 0
for line in lines:
    if "==========" in line:
        user += 1
        counts_dict["High"][user] = {}
        for t in all_types:
            counts_dict["High"][user] = Counter()
    else:
        aca = line.replace("\n", "")
        counts_dict["High"][user][aca] += 1

f_low.close()




frequency_dict = {}
frequency_dict["High"] = {}
frequency_dict["Low"] = {}

for t in all_types:
    frequency_dict["High"][t] = []
    frequency_dict["Low"][t] = []




for user in counts_dict["High"]:
    total = sum(counts_dict["High"][user].values())
    for aca in counts_dict["High"][user]:
        frequency = counts_dict["High"][user][aca]/float(total)
        frequency_dict["High"][aca].append(frequency)

for user in counts_dict["Low"]:
    total = sum(counts_dict["Low"][user].values())
    for aca in counts_dict["Low"][user]:
        frequency = counts_dict["Low"][user][aca]/float(total)
        frequency_dict["Low"][aca].append(frequency)

action_counts_f = open("action_counts.csv", 'w')
action_counts_f.write("High,Low,High,Low\n")
for user in counts_dict["Low"]:
    total_low = sum(counts_dict["Low"][user].values())
    total_high = sum(counts_dict["High"][user].values())
    action_counts_f.write(str(total_high) + "," + str(total_low) + "," + str(total_high) + "," + str(total_low) + "\n")

counts_dict_4 = {"High": {"user": [], "model": []}, "Low": {"user": [], "model": []}}
for user in counts_dict["High"]:
    model_count = 0
    user_count = 0
    for aca in counts_dict["High"][user]:
        if "model" in aca:
            model_count += counts_dict["High"][user][aca]
        if "user" in aca:
            user_count += counts_dict["High"][user][aca]
    counts_dict_4["High"]["model"].append(model_count)
    counts_dict_4["High"]["user"].append(user_count)

for user in counts_dict["Low"]:
    model_count = 0
    user_count = 0
    for aca in counts_dict["Low"][user]:
        if "model" in aca:
            model_count += counts_dict["Low"][user][aca]
        if "user" in aca:
            user_count += counts_dict["Low"][user][aca]
    counts_dict_4["Low"]["model"].append(model_count)
    counts_dict_4["Low"]["user"].append(user_count)
print counts_dict_4
print len(counts_dict_4["Low"]["model"])
print len(counts_dict_4["Low"]["user"])
print len(counts_dict_4["High"]["model"])
print len(counts_dict_4["High"]["user"])

action_counts_4_f = open("action_counts_4.csv", 'w')
action_counts_4_f.write("Q1,Q2,Q3,Q4\n")
for user in range(32):
    print user
    total_low_user = counts_dict_4["Low"]["user"][user]
    total_low_model = counts_dict_4["Low"]["model"][user]
    total_high_user = counts_dict_4["High"]["user"][user]
    total_high_model = counts_dict_4["High"]["model"][user]
    action_counts_4_f.write(str(total_high_user) + "," + str(total_low_user) + "," + str(total_high_model) + "," + str(total_low_model) + "\n")



def average(l):
    return sum(l)/float(len(l))


f_out = open("frequency.csv", 'w')
f_out_table = open("frequency_table.txt", 'w')
for aca in all_types:
    actor = aca.split(".")[0]
    component = aca.split(".")[1]
    action = aca.split(".")[2]



    high_val_mean = str(Decimal(str(numpy.mean(frequency_dict["High"][aca]))).quantize(FIVEPLACES))
    high_val_std = str(Decimal(str(numpy.std(frequency_dict["High"][aca]))).quantize(THREEPLACES))

    low_val_mean = str(Decimal(str(numpy.mean(frequency_dict["Low"][aca]))).quantize(FIVEPLACES))
    low_val_std = str(Decimal(str(numpy.std(frequency_dict["Low"][aca]))).quantize(THREEPLACES))

    try:
        t_test = str(Decimal(str(scipy.stats.ttest_ind(frequency_dict["High"][aca], frequency_dict["Low"][aca])[1])).quantize(THREEPLACES))
    except:
        t_test = "-"

    minus = str(Decimal(str(numpy.mean(frequency_dict["High"][aca]) - numpy.mean(frequency_dict["Low"][aca]))).quantize(FIVEPLACES))

    if minus == "NaN":
        if high_val_mean == "NaN":
            minus = "-" + low_val_mean
        if low_val_mean == "NaN":
            minus = high_val_mean


    if high_val_mean == "NaN":
        high_val_mean = "-"
    if high_val_std == "NaN":
        high_val_std = "-"
    if low_val_mean == "NaN":
        low_val_mean = "-"
    if low_val_std == "NaN":
        low_val_std = "-"
    if t_test == "NaN":
        t_test = "-"
    if minus == "NaN":
        minus = "-"

    f_out.write(actor + "," + component + "," + action + "," + high_val_mean + " (" + high_val_std + ")," + low_val_mean + " (" + low_val_std + ")," + str(t_test) + "\n")

    f_out_table.write("<tr>\n")
    f_out_table.write("\t<td>" + actor + "</td>\n")
    f_out_table.write("\t<td>" + component + "</td>\n")
    f_out_table.write("\t<td>" + action + "</td>\n")
    if high_val_mean > low_val_mean:
        f_out_table.write("\t<td><b>" + high_val_mean + " (" + high_val_std + ")" + "</b></td>\n")
        f_out_table.write("\t<td>" + low_val_mean + " (" + low_val_std + ")" + "</td>\n")
    else:
        f_out_table.write("\t<td>" + high_val_mean + " (" + high_val_std + ")" + "</td>\n")
        f_out_table.write("\t<td><b>" + low_val_mean + " (" + low_val_std + ")" + "</b></td>\n")
    
    f_out_table.write("\t<td>" + str(minus) + "</td>\n")
    f_out_table.write("\t<td>" + str(t_test) + "</td>\n")
    f_out_table.write("</tr>\n")


#print all_types


"""

<tr>
                <td>Tiger Nixon</td>
                <td>System Architect</td>
                <td>Edinburgh</td>
                <td>61</td>
                <td>2011/04/25</td>
                <td>$320,800</td>
            </tr>
"""
