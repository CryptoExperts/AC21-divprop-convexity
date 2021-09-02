import sys
f = open(sys.argv[1])

# 00:00:01.333.010 INFO root: Constraints: 110100111
# 32
# 00:23:03.086.762 INFO root: final SAT_times: 12.9 - 83.2, avg 36.3 med 36.0
#

data = []
while True:
    line = f.readline().strip()
    if not line:
        break

    *rest, marker, scons = line.split()
    assert marker == "Constraints:"

    cons = list(map(int, scons))[::-1]

    row = {}
    row['SSB_card'] = cons.pop()
    row['SSB_box_lb'] = cons.pop()
    row['SSB_box_ub'] = cons.pop()
    row['SSB_lb'] = cons.pop()
    row['SSB_ub'] = cons.pop()

    row['MC_card'] = cons.pop()
    row['MC_matching'] = cons.pop()
    row['MC_lb'] = cons.pop()
    row['MC_ub2'] = cons.pop()

    num_solves = int(f.readline())

    # 00:23:03.086.762 INFO root: final SAT_times: 12.9 - 83.2, avg 36.3 med 36.0
    *rest, marker, vmin, _, vmax, _, avg, _, med = f.readline().replace(",", "").split()
    assert marker == "SAT_times:"
    vmin, vmax, avg, med = map(float, [vmin, vmax, avg, med])

    assert not f.readline().strip()

    # turn on to remove SSB_ub from consideration
    if 0:
        if row["SSB_ub"] != 0:
            continue
        # if row["SSB_card"] != 1:
        #     continue
        # if row["SSB_box_lb"] != 0:
        #     continue
        # if row["SSB_box_ub"] != 0:
        #     continue
        # if row["MC_matching"] != 0:
        #     continue
        # if row["MC_ub2"] != 0:
        #     continue
        # if row["MC_card"] != 1:
        #     continue
    data.append((row, vmin, vmax, avg, med, num_solves))

print("=========================")

datas = sorted(data, key=lambda dat: dat[3])
print("Legend:")
print("{constraints}, time_min, time_max, time_average, time_median, num_solves_recorded")
print()

print("Best 10")
for dat in datas[:10]:
    print(dat)
print()

print("Worst 10")
for dat in datas[-10:]:
    print(dat)

'''
Conclusions:
SSB_ub: very bad effect
'''
