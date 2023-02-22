import os
import time
from ortools.linear_solver import pywraplp
import numpy as np

freq_set = np.arange(1, 2.7, 0.1)

def get_fun_string(coff, nb_time, nb_freq):
    fun = ''
    for s in range(nb_time):
        for f in range(nb_freq):
            fun += '{}*x[{}, {}]'.format(coff[s][f], s, f)
            if not (s == nb_time - 1 and f == nb_freq -1):
                fun += '+'
            if f%3 == 0:
                fun += '\n'
    return fun

def output_model(coff_obj, coff_con, right_hand_side, solution, obj_value):
    nb_time = len(solution)
    nb_freq = len(solution[0])
    freq_solution = []
    fw = open('modelip2.lp', 'w')
    fw.write('min:{}\n'.format(get_fun_string(coff_obj, nb_time, nb_freq)))
    fw.write('st:{}>={}\n'.format(get_fun_string(coff_con, nb_time, nb_freq), right_hand_side))
    fw.write('solution:\n')
    for s in range(nb_time):
        for f in range(nb_freq):
            if solution[s][f].solution_value() >= 0.9:
                fw.write('time {} freq is {}\n'.format(s, freq_set[f]))
                freq_solution.append(freq_set[f])
    fw.write('Obj_value:{}\n'.format(obj_value))
    fw.close()
    return freq_solution

def deal_coff(coff_obj, coff_cons):
    nb_freq = len(freq_set)
    list_temp = [None]*nb_freq
    for f in range(nb_freq):
        list_temp[f] = coff_obj * (freq_set[f]**3) 
    coff_obj_new = np.array(list_temp).T
    
    list_temp = [None]*nb_freq
    for f in range(nb_freq):
        list_temp[f] = coff_cons * freq_set[f]
    coff_cons_new = np.array(list_temp).T
    return coff_obj_new, coff_cons_new

def build_and_solve(coff_obj, coff_cons, right_hand_side):
    model = pywraplp.Solver.CreateSolver('SCIP')
    coff_obj_ip, coff_cons_ip = deal_coff(coff_obj, coff_cons)
    nb_time = coff_obj_ip.shape[0]
    nb_freq = coff_obj_ip.shape[1]

    x = [[None]* nb_freq for i in range(nb_time)]
  
    # 定义变量
    for s in range(nb_time):
        for f in range(nb_freq):
            x[s][f] = model.IntVar(0.0, 1.0, 'x['+ str(s)+','+ str(f)+']')

    # 添加约束
    expression = 0
    for s in range(nb_time):
        for f in range(nb_freq):
            expression += coff_cons_ip[s][f] * x[s][f]
    model.Add(expression >= right_hand_side)

    for s in range(nb_time):
        expression = 0
        for f in range(nb_freq):
            expression += x[s][f]
        model.Add(expression == 1)

    expression = 0
    for s in range(nb_time):
        for f in range(nb_freq):
            expression += coff_obj_ip[s][f] * x[s][f]
    model.Minimize(expression)

    f1 = open("modelip.lp",'r+', encoding='UTF-8') # 用r打开，会有not writable的问题
    f1.write(model.ExportModelAsLpFormat(False))
    f1.close()
    
    status = model.Solve()
    # 结果输出
    if status == model.OPTIMAL or status == model.FEASIBLE:
        pass
        # print('objective=', model.Objective().Value())
        # print('problem solved in %f ms' % model.wall_time())
        # print('problem solved in %d iterations' % model.iterations())
        # print('problem solved in %d branch-and-bound node' % model.nodes())
    else:
        print('problem have no optimal solution')
    freq_solution = output_model(coff_obj_ip, coff_cons_ip, right_hand_side, solution = x, obj_value=model.Objective().Value())
    return model.Objective().Value(), freq_solution
