import numpy as np
import tkinter
from tkinter import ttk
from tkinter import messagebox
import os
import openpyxl as xl

def compute_pattern_divisor(n_el, n_distr):
    return n_el / n_distr

def display_result(results_frame,patt_div_r,n_decimal, result_display):
    pd2_label = tkinter.Label(results_frame, text="Divisor Padrão Final:")
    pd2_label.grid(row=0, column=2)
    pd2_value_label = tkinter.Label(results_frame, text=str(round(patt_div_r,n_decimal)))
    pd2_value_label.grid(row=1, column=2)

    df_label = tkinter.Label(results_frame, text="Distribuição Final:")
    df_label.grid(row=0, column=3)
    result2_value_label = tkinter.Label(results_frame, text=str(result_display))
    result2_value_label.grid(row=1, column=3)

def jefferson(votes, result , n_distr, patt_div_r, n_decimal, inc, results_frame, n_el):
    soma = sum(np.floor(result))
    n_decimal_it = n_decimal
  
    it = 1
    if (soma > n_distr):
        while (soma != n_distr):
            
            patt_div_r -= inc
            patt_div_r = round(patt_div_r,n_decimal_it)
            result = votes / patt_div_r
            result = [round(elem, n_decimal_it) for elem in result ]
            result_display = [np.floor(elem) for elem in result ]
            soma = sum(np.floor(result))
            it+=1

            if (soma < n_distr):
                patt_div_r = patt_div_r - 3 * inc
                inc = inc / 100
                n_decimal_it += 1
                if (it>=10000000):
                    messagebox.showwarning(title="Atenção!",message="Limite de interações atingido!")
                    break
                messagebox.showwarning(title="Atenção!",message="Olha o incremento: " + str(inc))

    elif (soma < n_distr):
        while (soma != n_distr):
            
            patt_div_r -= inc
            patt_div_r = round(patt_div_r,n_decimal_it)
            result = votes / patt_div_r
            result = [round(elem, n_decimal_it) for elem in result ]
            result_display = [np.floor(elem) for elem in result ]
            soma = sum(np.floor(result))
            it+=1

            if (soma > n_distr):
                patt_div_r = patt_div_r + 3 * inc
                inc = inc / 100
                n_decimal_it += 1
                if (it>=10000000):
                    messagebox.showwarning(title="Atenção!",message="Limite de interações atingido!")
                    break
                messagebox.showwarning(title="Atenção!",message="Olha o incremento: " + str(inc))

    else:
        result_display = [round(elem, 0) for elem in result ]

    if (soma == n_distr):
        display_result(results_frame,patt_div_r,n_decimal, result_display)

def compute():
    votes = []
    
    if ((str(n_elements_entry.get()) == "") | (str(n_decimal_entry.get()) == "") | (str(metodo_combobox.get()) == "") | (str(el1_entry.get()) == "")):
                messagebox.showwarning(title="Atenção!",message="Valores em falta!")
                return

    for widget in elements_frame.winfo_children():
        if isinstance(widget, tkinter.Entry):
            if (widget.get().isnumeric() & (widget.get() != "")):
                votes.append(int(widget.get()))

    n_el = np.sum(votes) # Number of elements
    n_distr = int(n_elements_entry.get()) # Number of elements to distribute

    std_div = compute_pattern_divisor(n_el, n_distr) # Standard divisor
    n_decimal = int(n_decimal_entry.get()) # get n. decimal    

    inc = round(std_div, n_decimal) / 1000 # value to in(de)crement on each iteration

    result = votes / round(std_div, n_decimal) # Standard quote for each member
    result_display = [np.floor(elem) for elem in result ] # Standard quote for each member (inferior quote)
    result = [round(elem, n_decimal) for elem in result ] # Standard quote for each member (rounded)

    # RESULTS' FRAME (Display the first iteration)
    results_frame = tkinter.LabelFrame(frame, text="Resultados:")
    results_frame.grid(row=4,column=0, padx=20 ,pady=10)

    pd1_label = tkinter.Label(results_frame, text="Divisor Padrão inicial:")
    pd1_label.grid(row=0, column=0)
    pd1_value_label = tkinter.Label(results_frame, text=str(round(n_el/n_distr,n_decimal)))
    pd1_value_label.grid(row=1, column=0)

    di_label = tkinter.Label(results_frame, text="Distribuição Inicial:")
    di_label.grid(row=0, column=1)
    result1_value_label = tkinter.Label(results_frame, text=str(result_display))
    result1_value_label.grid(row=1, column=1)

    method = str(metodo_combobox.get()) # Check the method

    if method=="Jefferson":
        jefferson(votes, result, n_distr, round(std_div, n_decimal), n_decimal, inc, results_frame, n_el)

### WINDOW ###

window = tkinter.Tk()

window.title("TEORIA DAS ELEIÇÕES")
frame = tkinter.Frame(window)
frame.pack()

# TOP FRAME
metodo_frame = tkinter.LabelFrame(frame, text="Informação principal:")
metodo_frame.grid(row=0,column=0, padx=20 ,pady=10)

metodo_label = tkinter.Label(metodo_frame, text="Nationality")
metodo_combobox = ttk.Combobox(metodo_frame, values=["Jefferson"])
metodo_label.grid(row=0,column=0)
metodo_combobox.grid(row=1,column=0)

# TOP FRAME
top_frame = tkinter.LabelFrame(frame, text="Informação principal:")
top_frame.grid(row=1,column=0, padx=20 ,pady=10)

n_elements_label = tkinter.Label(top_frame, text="Números de elementos a distribuir:")
n_elements_label.grid(row=0, column=0)
n_elements_entry = tkinter.Entry(top_frame)
n_elements_entry.grid(row=1, column=0)

n_decimal_label = tkinter.Label(top_frame, text="Número de casas decimais:")
n_decimal_label.grid(row=0, column=1)
n_decimal_entry = tkinter.Entry(top_frame)
n_decimal_entry.grid(row=1, column=1)

for widget in top_frame.winfo_children():
    widget.grid_configure(padx=10,pady=5)

# ELEMENTS FRAME
elements_frame = tkinter.LabelFrame(frame, text="Dados dos elementos:")
elements_frame.grid(row=2,column=0, padx=20 ,pady=10)

el1_label = tkinter.Label(elements_frame, text="Nome A:")
el1_label.grid(row=0, column=0)
el1_entry = tkinter.Entry(elements_frame)
el1_entry.grid(row=1, column=0)

el2_label = tkinter.Label(elements_frame, text="Nome B:")
el2_label.grid(row=0, column=1)
el2_entry = tkinter.Entry(elements_frame)
el2_entry.grid(row=1, column=1)

el3_label = tkinter.Label(elements_frame, text="Nome C:")
el3_label.grid(row=0, column=2)
el3_entry = tkinter.Entry(elements_frame)
el3_entry.grid(row=1, column=2)

el4_label = tkinter.Label(elements_frame, text="Nome D:")
el4_label.grid(row=0, column=3)
el4_entry = tkinter.Entry(elements_frame)
el4_entry.grid(row=1, column=3)

el5_label = tkinter.Label(elements_frame, text="Nome E:")
el5_label.grid(row=0, column=4)
el5_entry = tkinter.Entry(elements_frame)
el5_entry.grid(row=1, column=4)

for widget in elements_frame.winfo_children():
    widget.grid_configure(padx=10,pady=5)

# BUTTON FRAME
button = tkinter.Button(frame, command = compute, text="Calcular!")
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

window.mainloop()