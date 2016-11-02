import sys

f_a = open("events_A.csv",'r')
g_h = open("events_A_formatted.csv",'w')

f_b = open("events_B.csv",'r')
g_l = open("events_B_formatted.csv",'w')

gains = open("climate_gains.csv",'r')
anon_id = open("anon_id.csv",'r')


lines = f_a.readlines()[1:]
lines.extend(f_b.readlines()[1:])

learning = {}
for line in gains.readlines():
	l =line.split(',')
	learning[l[0]]=l[5]

id_to_anon = {}
for line in anon_id.readlines():
	l =line.split(',')
	id_to_anon[l[0]]=l[1]

all_types = []
current_student = ''
for line in lines:
	sid,student,action,time,oldgroup = line.split(',')
	anonid = id_to_anon[sid]
	print sid,student,action,time,oldgroup
	print anonid, learning[str(anonid)]
	sys.exit()
	if anonid not in learning.keys():
		continue
	if student != current_student:
		if student != '':
			if learning[anonid] == "HL":
				g_h.write("========================================\n")
			else:
				g_l.write("========================================\n")
		current_student = student

	if learning[anonid] == "HL":
		g_h.write(action+'\n')
	else:
		g_l.write(action+'\n')



f_a.close()
f_b.close()
g_h.close()
g_l.close()
gains.close()
anon_id.close()