import numpy as np
import IPmodel
import Convmodel
import ipopt
import LP

seed = 0
np.random.seed(seed)

piC = 3
time_slot_num = 24
price = np.zeros((time_slot_num), dtype=np.float32)

for i in range(time_slot_num):
    if i <= 9 or i >= 23:
        price[i] = 0.312
    else:
        price[i] = 0.728
print('price:', price)        

job_start_time = 9
job_end_time = 12
job_execuse_days = 4

job_at_each_time_slot_num = np.zeros((time_slot_num), dtype=np.float32)
job_at_each_time_slot_num += job_execuse_days
for time_index in range(job_start_time, 24):
    job_at_each_time_slot_num[time_index] += 1
for time_index in range(job_end_time):
    job_at_each_time_slot_num[time_index] += 1

print('job number at each time:', job_at_each_time_slot_num)

r = 0.9
coff_obj = job_at_each_time_slot_num * price * piC
coff_con = job_at_each_time_slot_num * r

print('coff obj:', coff_obj)
print('coff con:', coff_con)

# 1.5GHZ
total_required_circle = job_at_each_time_slot_num.sum() * r * 1.5 #C
cal_num = 0
for i in range(time_slot_num):
    cal_num += coff_con[i] * 1.5
assert abs(cal_num - total_required_circle) <= 1

print('Solving IP model...')
cost_ip, solution = IPmodel.build_and_solve(coff_obj=coff_obj, coff_cons=coff_con, right_hand_side=total_required_circle)

print('Solving Conv model...')
# cost_conv = Convmodel.build_and_solve(total_required_circle=total_required_circle, coff_obj=coff_obj, coff_cons=coff_con)
# cost_conv = ipopt.build_and_solve(total_required_circle=total_required_circle, coff_obj=coff_obj, coff_cons=coff_con)

# print("Solving LP model...")
# cost_lp = LP.build_and_solve(coff_obj, coff_con, total_required_circle)

origin_cost = 0
for i in range(time_slot_num):
    origin_cost += coff_obj[i] * (1.5**3)


print('origin cost:', origin_cost)
print('diff ip and origin:', cost_ip - origin_cost)
# print('diff cov and origin', cost_conv - origin_cost)




    