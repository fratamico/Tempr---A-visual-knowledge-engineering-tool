

learner_dict = {"High": [], "Low": []}

f_learner = open('learners.csv', 'r')
lines = f_learner.readlines()
for line in lines:
    split_lines = line.split("\t")
    if "High" in split_lines[1]:
        learner_dict["High"].append(split_lines[0])
    else:
        learner_dict["Low"].append(split_lines[0])

f_learner.close()


f = open("log_files/parser_log_user.txt", 'r')

lines = f.readlines()

a1_f = open("a1_log.txt", 'w')
a2_high_f = open("a2_high_log.txt", 'w')
a2_low_f = open("a2_low_log.txt", 'w')
a2_med_f = open("a2_med_log.txt", 'w')
a3_f = open("a3_log.txt", 'w')

current_activity = 0


user = ""

for index, line in enumerate(lines):
    if "pause <" in line or "<<pause ENDED" in line:
        continue
    if "current_file" in line:
        
        user = line.split("parsedData\\")[1].split("_")[0]
        print user
        if "a1" in line:
            a1_f.write("========================================\n")
            current_activity = 1
            continue
        if "a2" in line:
            if user in learner_dict["High"]:
                a2_high_f.write("========================================\n")
            elif user in learner_dict["Low"]:
                a2_low_f.write("========================================\n")
            else:
                a2_med_f.write("========================================\n")
            current_activity = 2
            continue
        if "a3" in line:
            a3_f.write("========================================\n")
            current_activity = 3
            continue



    actor = line.split("\n")[0].split(",")[1].replace("'", "").strip()
    component = line.split("\n")[0].split(",")[2].replace("'", "").split(".")[0].strip()
    action = line.split("\n")[0].split(",")[4].replace("'", "").strip()

    if actor == "system":
        continue
    

    if current_activity == 1:
        a1_f.write(actor + "." + component + "." + action + "\n")
    elif current_activity == 2:
        if user in learner_dict["High"]:
            a2_high_f.write(actor + "." + component + "." + action + "\n")
        elif user in learner_dict["Low"]:
            a2_low_f.write(actor + "." + component + "." + action + "\n")
        else:
            a2_med_f.write(actor + "." + component + "." + action + "\n")
    elif current_activity == 3:
        a3_f.write(actor + "." + component + "." + action + "\n")
    else:
        raise "no activity???"

