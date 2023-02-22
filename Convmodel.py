from scipy.optimize import minimize
import numpy as np

bound_freqency = (1, 2.6) # GHz

def generate_obj_fun(x, time_slot_num, coff_obj):
    fun = coff_obj[0] * x[0]
    for i in range(1, time_slot_num):
        fun += coff_obj[i] * x[i] * x[i] * x[i]
    return fun

def generate_con_fun(x, time_slot_num, coff_cons, right_side_value):
    fun = coff_cons[0] * x[0]
    for i in range(1, time_slot_num):
        fun += coff_cons[i] * x[i]
    fun -= right_side_value
    return fun

def get_fun_string(coff, time_slot_num):
    fun = ''
    for i in range(time_slot_num):
        fun += '{}*x[{}]'.format(coff[i], i)
        if i != time_slot_num - 1:
            fun += '+'
        if i%3 == 0:
            fun += '\n'
    return fun

def output_model(coff_obj, coff_con, time_slot_num, right_hand_side, solution, obj_value):
    fw = open('modelconv.lp', 'w')
    fw.write('min:{}\n'.format(get_fun_string(coff_obj, time_slot_num)))
    fw.write('st:{}={}\n'.format(get_fun_string(coff_con, time_slot_num), right_hand_side))
    fw.write('solution:\n')
    for i in range(len(solution)):
        fw.write('x[{}]={}\n'.format(i, solution[i]))
    fw.write('Obj_value:{}\n'.format(obj_value))
    fw.close()

def check(solution, obj_value, coff_obj, coff_cons, time_slot_num, total_required_circle):
    temp_total = 0
    temp_total_2 = 0
    for t in range(time_slot_num):
        temp_total += coff_cons[t] * solution[t]
        temp_total_2 += coff_cons[t] * 1.5
    assert abs(temp_total_2 - total_required_circle) <= 1
    assert abs(temp_total-total_required_circle) <= 1
    
    temp_total = 0
    for t in range(time_slot_num):
        temp_total += coff_obj[t] * (solution[t]**3)
    
    assert abs(obj_value - temp_total) <= 1


def build_and_solve(total_required_circle, coff_obj, coff_cons):
    # initial_solution
    time_slot_num = coff_obj.shape[0]

    x0 = [1.5]*time_slot_num
    bnds = [bound_freqency for i in range(time_slot_num)]

    cons = ({'type':'eq', 'fun': lambda x: generate_con_fun(x, time_slot_num, coff_obj, total_required_circle)})

            # - 'Nelder-Mead' :ref:`(see here) <optimize.minimize-neldermead>`
            # - 'Powell'      :ref:`(see here) <optimize.minimize-powell>`
            # - 'CG'          :ref:`(see here) <optimize.minimize-cg>`
            # - 'BFGS'        :ref:`(see here) <optimize.minimize-bfgs>`
            # - 'Newton-CG'   :ref:`(see here) <optimize.minimize-newtoncg>`
            # - 'L-BFGS-B'    :ref:`(see here) <optimize.minimize-lbfgsb>`
            # - 'TNC'         :ref:`(see here) <optimize.minimize-tnc>`
            # - 'COBYLA'      :ref:`(see here) <optimize.minimize-cobyla>`
            # - 'SLSQP'       :ref:`(see here) <optimize.minimize-slsqp>`
            # - 'trust-constr':ref:`(see here) <optimize.minimize-trustconstr>`
            # - 'dogleg'      :ref:`(see here) <optimize.minimize-dogleg>`
            # - 'trust-ncg'   :ref:`(see here) <optimize.minimize-trustncg>`
            # - 'trust-exact' :ref:`(see here) <optimize.minimize-trustexact>`
            # - 'trust-krylov' :ref:`(see here) <optimize.minimize-trustkrylov>`


    # model = minimize(generate_obj_fun, x0, method='SLSQP', constraints=cons, bounds=bnds)
    model = minimize(generate_obj_fun, x0, args=(time_slot_num, coff_obj), method='SLSQP', constraints=cons, bounds=bnds, options={'disp': True, 'ftol': 1**(-5)})
    
    print(model)
    print('cost:{}'.format(model.fun))
    print('message:', model.message)
    print(model.success)
    print('solution:', model.x)
    output_model(coff_obj, coff_cons, time_slot_num, total_required_circle, model.x, model.fun)
    check(model.x, model.fun, coff_obj, coff_cons, time_slot_num, total_required_circle)
    return model.fun