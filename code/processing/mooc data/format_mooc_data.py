import sys

f_a = open("events_A.csv",'r')
g_h = open("events_HL_formatted.csv",'w')

f_b = open("events_B.csv",'r')
g_l = open("events_LL_formatted.csv",'w')

gains = open("climate_gains_tertiarysplit.csv",'r')
anon_id = open("anon_id.csv",'r')


learning = {}
for line in gains.readlines():
	l =line.split(',')
	learning[l[0]]=l[5]

id_to_anon = {}
for line in anon_id.readlines():
	l =line.split(',')
	id_to_anon[l[0]]=l[1]

LLcount = 0
HLcount = 0
MLcount = 0

lines = f_a.readlines()[1:]
lines.extend(f_b.readlines()[1:])
current_student = ''
for line in lines:
	sid,action,time,oldgroup = line.split(',')
	anonid = id_to_anon[sid]
	# print anonid
	if anonid not in learning.keys():
		continue

	# print sid,action,time,oldgroup
	# print learning[anonid]
	if sid != current_student:
		if sid != '':
			if 'HL' in learning[anonid]:
				g_h.write("========================================\n")
				HLcount += 1
			elif 'LL' in learning[anonid]:
				g_l.write("========================================\n")
				LLcount += 1
			else:
				MLcount += 1
		current_student = sid

	if 'HL' in learning[anonid]:
		g_h.write(action+'\n')
	elif 'LL' in learning[anonid]:
		g_l.write(action+'\n')

print HLcount, LLcount, MLcount


f_a.close()
f_b.close()
g_h.close()
g_l.close()
gains.close()
anon_id.close()