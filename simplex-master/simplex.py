import numpy as np
import re
import random as rand
import os


def valid_input(mensaje: str, caso: int) -> float | str:
    patron = r'[+-]?([0-9]*\.)?[0-9]+'
    patron2 = r"(^(?=.)(?:(?:[+-]?([+-]?([0-9]*\.)?[0-9]+)(?:\w)*)+)[<>]?=(?=.)(?:(?:[+-]?(([0-9]*\.)?[0-9]+)(?:\w)*)+)$)"
    
    while True:
        msj_temp = input(f'{mensaje}')
        if caso == 1:
            if re.fullmatch(patron, msj_temp):
                return float(msj_temp)
            else:
                print("Escriba un número correcto.")
        elif caso == 2:
            if re.match(patron2, msj_temp):
                return msj_temp
            else:
                print("Escriba una desigualdad correcta.")
        else:
            if len(separar_coefs(msj_temp)) >= 2:
                return msj_temp
            else:
                print("Escriba una función objetivo correcta.")

def separar_coefs(eq: str) -> list:
    coefs = re.findall(r'[\d\.\-\+]+', eq)
    return [float(x) for x in coefs]



def generar_pdf_latex(c, A, b, maximizar=True, nombre="problema_simplex"):
    tipo = "Maximizar" if maximizar else "Minimizar"
    obj_str = " + ".join([f"{c[i]}x_{i+1}" for i in range(len(c))])
    res_str = ""
    for i in range(len(A)):
        fila = " + ".join([f"{A[i][j]}x_{j+1}" for j in range(len(A[i]))])
        res_str += f"        {fila} & \\le {b[i]} \\\\\n"

    contenido_latex = r"""\documentclass{article}\usepackage[utf8]{inputenc}\usepackage{amsmath}\begin{document}\section*{Problema de Programacion Lineal Generado}
    \textbf{Objetivo:} %s $Z = %s$ \\\\\textbf{Sujeto a:}\begin{align*}%sx_i & \ge 0\end{align*}\end{document}""" % (tipo, obj_str, res_str)

    with open(f"{nombre}.tex", "w") as f:
        f.write(contenido_latex)
    
    try:
        os.system(f"pdflatex -interaction=nonstopmode {nombre}.tex")
        print(f"\n[INFO] PDF generado: {nombre}.pdf")
    except:
        print("\nNo se pudo compilar el PDF. no esta latex instalado.")

def generar_unica(n, m):
    z = np.array([round(rand.uniform(1, 10), 1) for _ in range(n)])
    A = np.array([[round(rand.uniform(1, 10), 1) for _ in range(n)] for _ in range(m)])
    b = np.array([round(rand.uniform(20, 100), 1) for _ in range(m)])
    return z, A, b

def generar_sin_solucion(n, m):
    z = np.array([round(rand.uniform(1, 10), 1) for _ in range(n)])
    A = np.array([[round(rand.uniform(1, 5), 1) for _ in range(n)] for _ in range(m)])
    b = np.array([round(rand.uniform(10, 20), 1) for _ in range(m)])

    b[0] = -50.0 
    return z, A, b



def creador_matriz(c, A, b):
    m, n = np.shape(A)
    matriz = np.zeros((m+1, n+m+1))
    matriz[0, 1:n+1] = -c
    matriz[1:, 0] = b
    matriz[1:, 1:n+1] = A
    matriz[1:, n+1:] = np.eye(m)
    return matriz

def pivoteo(D, col_piv, m):
    limite = 1e-10
    candidatos = []
    for i in range(1, m + 2):
        if i < D.shape[0] and D[i, col_piv] > limite:
            cociente = D[i, 0] / D[i, col_piv]
            candidatos.append((cociente, i))
    if not candidatos: return None, None
    _, fila_piv = min(candidatos)
    pivote = D[fila_piv, col_piv]
    D[fila_piv, :] /= pivote
    for fila in range(D.shape[0]):
        if fila != fila_piv:
            D[fila, :] -= D[fila, col_piv] * D[fila_piv, :]
    return D, fila_piv

def simplex_solver(c, A, b, maximizar=True, max_iter=100):
    if not maximizar: c = -c
    matriz = creador_matriz(c, A, b)
    m, n = np.shape(A)
    base = list(range(n+1, n+m+1))
    
    for i in range(max_iter):
        if np.all(matriz[0, 1:n+1] >= 0): 
            sol = np.zeros(n+m)
            for j, b_idx in enumerate(base):
                if b_idx - 1 < len(sol): sol[b_idx-1] = matriz[j+1, 0]
            return matriz[0,0], matriz, sol
        
        col = np.argmin(matriz[0, 1:n+1]) + 1
        matriz, fila_piv = pivoteo(matriz, col, m-1)
        if matriz is None: return None, None, None
        base[fila_piv-1] = col
    return None, None, None


if __name__ == '__main__':
    print("=================================== SIMPLEX ===================================")
    opc = input("¿Desea generar automaticamente el problema? S/n: ").upper()
    
    if opc == 'N':
        obj = valid_input("Escriba la funcion objetivo (ej: 3x1 + 2x2): ", 3)
        coefs_z = separar_coefs(obj)
        n_res = int(valid_input("Escriba el numero de restricciones: ", 1))
        res = [valid_input(f"Escriba la restriccion {i+1}: ", 2) for i in range(n_res)]
        coefs_res = np.array([separar_coefs(i) for i in res])
        z = np.array(coefs_z)
        A = coefs_res[:, :-1]
        b = coefs_res[:, -1]
    else:
        print("\n1. Unica solucion\n2. Sin solucion\n3. Multiples soluciones")
        tipo_gen = int(input("Elija tipo de problema: "))
        n_vars = rand.randint(2, 3)
        n_res = int(input("Numero de restricciones: "))
        
        if tipo_gen == 1:
            z, A, b = generar_unica(n_vars, n_res)
        elif tipo_gen == 2:
            z, A, b = generar_sin_solucion(n_vars, n_res)
        else:
            z = np.array([round(rand.uniform(1, 5),1) for _ in range(n_vars)])
            A = np.array([[round(rand.uniform(1, 5),1) for _ in range(n_vars)] for _ in range(n_res)])
            b = np.array([round(rand.uniform(10, 30),1) for _ in range(n_res)])

    opc2 = int(input("\n1. Maximizar\n2. Minimizar\nOpcion: "))
    maximizar = True if opc2 == 1 else False
    
    generar_pdf_latex(z, A, b, maximizar)
    

    res, matriz, variables = simplex_solver(z, A, b, maximizar)
    
    print("\n" + "="*20 + " RESULTADO " + "="*20)
    if res is not None:
        print(f"Z Optimo: {res}")
        print(f"Variables (incluyendo holgura): {variables}")
    else:
        print("El problema no tiene solucion optima (Infactible o No acotado).")