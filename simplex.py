import numpy as np
import re
import random as rand

def valid_input(mensaje: str, caso: int) -> float | str:
    patron = r'[+-]?([0-9]*\.)?[0-9]+'
    patron2 = r"(^(?=.)(?:(?:[+-]?([+-]?([0-9]*\.)?[0-9]+)(?:\w)*)+)[<>]?=(?=.)(?:(?:[+-]?(([0-9]*\.)?[0-9]+)(?:\w)*)+)$)"
    
    while True:
        msj_temp = input(f'{mensaje}')
        if caso == 1:
            if re.fullmatch(patron, msj_temp):
                return float(msj_temp)
            else:
                print("Escriba un número correcto, o no negativo.")
        elif caso == 2:
            if re.match(patron2, msj_temp):
                return msj_temp
            else:
                print("Escriba una desigualdad correcta.")
        else:
            if len(separar_coefs(msj_temp)) == 2:
                return msj_temp
            else:
                print("Escriba una función objetivo correcta (con dos variables).")

def separar_coefs(eq: str) -> list:
    coefs = re.findall(r'[\d\.\-\+]+', eq)
    return [float(x) for x in coefs]

def simplex_solver(c, A, b, maximizar=True, max_iter=100):
    if not maximizar:
        c = -c
    matriz = creador_matriz(c, A, b)
    m, n = np.shape(A)
    base = list(range(n+1, n+m+1))
    print(f"Matriz generada:\n{matriz}\n")

    for i in range(max_iter):
        if np.all(matriz[0, 1:] >= 0):
            sol = np.zeros(n+m)
            for j, b_idx in enumerate(base):
                if b_idx - 1 < len(sol):
                    sol[b_idx-1] = matriz[j+1, 0]
            return matriz[0,0], matriz, sol
        
        col = np.argmin(matriz[0, 1:]) + 1        

        # No acotado
        if np.all(matriz[1:, col] <= 0):
            return None

        matriz, fila_piv = pivoteo(matriz, col, m-1)
        base[fila_piv-1] = col
        if matriz is None:
            return None

        matriz = np.round(matriz, 2)
        print(f"Iteración {i+1}:\n{matriz}\n")

    return None

def pivoteo(D: np.array, col_piv: int, m: int):
    limite = 1e-10
    candidatos = []
    
    for i in range(1, m+1):
        if D[i, col_piv] > limite:
            cociente = D[i, 0] / D[i, col_piv]
            candidatos.append((cociente, i))
    
    if not candidatos:
        return None
    
    _, fila_piv = min(candidatos)
    pivote = D[fila_piv, col_piv]
    
    if abs(pivote) < limite:
        return None
    
    D[fila_piv, :] = D[fila_piv, :] / pivote
    
    for fila in range(np.shape(D)[0]):
        if fila != fila_piv:
            factor = D[fila, col_piv]
            D[fila, :] = D[fila, :] - factor * D[fila_piv, :]
    
    return D, fila_piv

def creador_matriz(c: np.array, A: np.array, b: np.array):
    m, n = np.shape(A)
    matriz = np.zeros((m+1, n+m+1))
    
    matriz[0, 1:n+1] = -c
    matriz[1:, 0] = b
    matriz[1:, 1:n+1] = A
    matriz[1:, n+1:] = np.eye(m)
    return matriz

def generar_multiple(n, m):
    a = [rand.uniform(1, 10) for _ in range (n)]
    b = rand.uniform(10, 50)
    k = rand.uniform(1,5)

    z = np.array([k*i for i in a])
    restricciones = []
    restricciones.append(a + [b])

    for _ in range(m-1):
        fila = [rand.uniform(1, 10) for _ in range(n)]
        desig = rand.uniform(4,40)
        restricciones.append(fila + [desig])

    restricciones = np.array(restricciones)
    A = restricciones[:, :-1]
    b_vec = restricciones[:, -1]
    return z, A, b_vec

def generar_acotada(n, m):
   ... 

if __name__ == '__main__':
    print("===================================SIMPLEX===================================")
    while True:
        opc = input("¿Desea generar automáticamente la función objetivo y sus restricciones? S/n: ")
        if opc.upper() != 'S' and opc.upper() != 'N':
            print("Escriba una de las opciones indicadas.")
        else:
            break
    
    if opc.upper() == 'N':
        obj = valid_input("Escriba la función objetivo: ", 3)
        coefs_z = separar_coefs(obj)
        n_res = int(valid_input("Escriba el número de restricciones: ", 1))

        res = [valid_input(f"Escriba la restricción {i+1}: ", 2) for i in range(n_res)]
        coefs_res = np.array([separar_coefs(i) for i in res])
    else:
        n_vars  = rand.uniform(1,4)
        coefs_z = [rand.uniform(1, 10) for _ in range(n_vars)]
        n_res = int(valid_input("Escriba el número de restricciones: ", 1))
        coefs_res = np.array([[rand.uniform(1, 10) for _ in range(n_vars)] for _ in range(n_res)])

    z = np.array(coefs_z)
    A = coefs_res[:, :-1]
    b = coefs_res[:, -1]

    while True: 
        try:
            opc2 = int(input("\nElija una opción:\n1. Maximizar\n2. Minimizar\n"))
        except TypeError:
            print("Escriba un número correcto.")
        else:
            if opc2 != 1 and opc2 != 2:
                print("Escriba un número dentro de las opciones.")
            else:
                break
    
    if opc2 == 1:
        maximizar = True
    else:
        maximizar = False
    
    res, matriz, vars = simplex_solver(z, A, b, maximizar)
    print("\nRESULTADO:")
    if res is not None:
        print(f"Resultado óptimo: {res}\nMatriz resultante:\n{matriz}\nVariables resultantes: {vars}")
    else:
        print(res)