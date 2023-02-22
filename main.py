import numpy as np
import IPmodel

piC = 10
time_slot_num = 24
price = np.zeros((time_slot_num), dtype=np.float32)
r = 0.9
normal_freq = 2

for i in range(time_slot_num):
    if i <= 9 or i >= 23:
        price[i] = 0.312
    else:
        price[i] = 0.728 


def solve(job_start_time, job_end_time, job_execuse_days):

    job_at_each_time_slot_num = np.zeros((time_slot_num), dtype=np.float32)
    job_at_each_time_slot_num += job_execuse_days
    for time_index in range(job_start_time, 24):
        job_at_each_time_slot_num[time_index] += 1
    for time_index in range(job_end_time):
        job_at_each_time_slot_num[time_index] += 1

    # print('job number at each time:', job_at_each_time_slot_num)
    print("sum of time:"+str(sum(job_at_each_time_slot_num)))
    
    coff_obj = job_at_each_time_slot_num * price * piC
    coff_con = job_at_each_time_slot_num * r

    # print('coff obj:', coff_obj)
    # print('coff con:', coff_con)

    # 1.5GHZ
    total_required_circle = job_at_each_time_slot_num.sum() * r * normal_freq #C
    cal_num = 0
    for i in range(time_slot_num):
        cal_num += coff_con[i] * normal_freq
    assert abs(cal_num - total_required_circle) <= 1

    cost_ip, solution = IPmodel.build_and_solve(coff_obj=coff_obj, coff_cons=coff_con, right_hand_side=total_required_circle)

    origin_cost = 0
    for i in range(time_slot_num):
        origin_cost += coff_obj[i] * (normal_freq**3)
    
    return origin_cost, cost_ip, solution


    # print('origin cost:', origin_cost)
    # print('diff ip and origin:', cost_ip - origin_cost)


start_times = np.arange(1, 24, 2)
end_times = np.arange(24, 1, -2)
execuse_days = [1,2,3,3,2,1,1,2,3,3,2,1]

cases_num = len(execuse_days)

fw_diff = open('diff.txt','w')
fw_freq = open('frequency.txt','w')

for i in range(cases_num):
    print("------------------------------------solving case of {}----------------------------------".format(i))
    origincost, newcost, solution = solve(start_times[i], end_times[i], execuse_days[i])
    fw_diff.write('{},{},{}\n'.format(i, origincost, newcost))
    solution = map(str, solution)
    fw_freq.write('{},{}\n'.format(i, ','.join(solution)))

fw_diff.close()
fw_freq.close()











    