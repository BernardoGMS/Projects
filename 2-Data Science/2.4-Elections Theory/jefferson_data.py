import numpy as np
import os
import csv
import pandas as pd
import random as rd

def compute_pattern_divisor(n_el, n_distr):
    return n_el / n_distr

def jefferson(votes, result , n_distr, patt_div_r, n_decimal, inc, n_el, mean_dev):
    soma = sum(np.floor(result))
    n_decimal_it = n_decimal
    
    it = 1
    if (soma > n_distr):
        while (soma != n_distr):
            
            patt_div_r -= inc
            patt_div_r = round(patt_div_r,n_decimal_it)
            result = votes / patt_div_r
            result = [round(elem, n_decimal_it) for elem in result ]
            soma = sum(np.floor(result))
            it+=1

            if (soma < n_distr):
                patt_div_r = patt_div_r - 3 * inc
                inc = inc / 100
                n_decimal_it += 1

            if (it>=100000):
                break

    elif (soma < n_distr):
        while (soma != n_distr):
            
            patt_div_r -= inc
            patt_div_r = round(patt_div_r,n_decimal_it)
            result = votes / patt_div_r
            result = [round(elem, n_decimal_it) for elem in result ]
            soma = sum(np.floor(result))
            it+=1

            if (soma > n_distr):
                patt_div_r = patt_div_r + 3 * inc
                inc = inc / 100
                n_decimal_it += 1

            if (it>=100000):
                break
                
    filepath = "jef_data.csv"           
    if not os.path.exists(filepath):
        heading = pd.DataFrame(columns=["id","total","to_distribute","n_elements","std_div_mod","len_votes","mean_dev"]) 
        heading.to_csv('jef_data.csv', index=False)
        max_idx = 0
    else:
        df = pd.read_csv('jef_data.csv')
        max_idx = df["id"].max()
    max_idx = max_idx+1

    data_save = [max_idx,soma,n_distr,n_el,patt_div_r, len(votes), round(mean_dev,4)]
    file = open(filepath,'a')
    file.write(f'\n{str(data_save).replace("[","").replace("]","")}')
    file.close()

for i in [156]:
    max_ = i
    min_ = max_ - 6
    for k in [35]:
        for j in range(10000):
        
            votes = [np.floor(min_+(max_-min_)*round(rd.randint(0,100)/100,1)), 
                     np.floor(min_+(max_-min_)*round(rd.randint(0,100)/100,1)), 
                     np.floor(min_+(max_-min_)*round(rd.randint(0,100)/100,1)), 
                     np.floor(min_+(max_-min_)*round(rd.randint(0,100)/100,1))]
            
            n_el = np.sum(votes) # Number of elements
            mean_dev = np.mean(np.abs(votes - np.mean(votes))) / n_el
            n_distr = k # Number of elements to distribute

            std_div = compute_pattern_divisor(n_el, n_distr) # Standard divisor
            n_decimal = 4 # get n. decimal    

            inc = round(std_div, n_decimal) / 1000 # value to in(de)crement on each iteration

            result = votes / round(std_div, n_decimal) # Standard quote for each member
            result = [round(elem, n_decimal) for elem in result ] # Standard quote for each member (rounded)

            method = "Jefferson" # Check the method

            if method=="Jefferson":
                jefferson(votes, result, n_distr, round(std_div, n_decimal), n_decimal, inc, n_el, mean_dev)



