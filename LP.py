from ortools.linear_solver import pywraplp
import numpy as np

bound_freqency = (1, 2.6)
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
    fw = open('modelip2.lp', 'w')
    fw.write('min:{}\n'.format(get_fun_string(coff_obj, nb_time, nb_freq)))
    fw.write('st:{}>={}\n'.format(get_fun_string(coff_con, nb_time, nb_freq), right_hand_side))
    fw.write('solution:\n')
    for s in range(nb_time):
        for f in range(nb_freq):
            if solution[s][f].solution_value() >= 0.9:
                fw.write('time {} freq is {}\n'.format(s, freq_set[f]))
    fw.write('Obj_value:{}\n'.format(obj_value))
    fw.close()

def build_and_solve(coff_obj, coff_cons, right_hand_side):
    model = pywraplp.Solver.CreateSolver('SCIP')
    nb_time = len(coff_obj)

    x = [None]* nb_time
  
    # 定义变量
    for s in range(nb_time):
        x[s] = model.NumVar(bound_freqency[0], bound_freqency[1], 'x['+ str(s)+']')

    # 添加约束
    expression = 0
    for s in range(nb_time):
        expression += coff_cons[s] * x[s]
    model.Add(expression == right_hand_side)

    expression = 0
    for s in range(nb_time):
        expression += coff_obj[s] * x[s]
    model.Minimize(expression)

    f1 = open("modellp.lp",'r+', encoding='UTF-8') # 用r打开，会有not writable的问题
    f1.write(model.ExportModelAsLpFormat(False))
    f1.close()
    
    status = model.Solve()
    # 结果输出
    if status == model.OPTIMAL or status == model.FEASIBLE:
        print('objective=', model.Objective().Value())
        print('problem solved in %f ms' % model.wall_time())
        print('problem solved in %d iterations' % model.iterations())
        print('problem solved in %d branch-and-bound node' % model.nodes())
        for s in range(nb_time):
            print('x[{}]=', x[s].solution_value())          
    else:
        print('problem have no optimal solution')
    # output_model(coff_obj, coff_cons_ip, right_hand_side, solution = x, obj_value=model.Objective().Value())
    return model.Objective().Value()
