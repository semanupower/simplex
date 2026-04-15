from subprocess import DEVNULL, STDOUT, check_call
import numpy as np
import random as rand
import os

def generar_unica(n, m, intentos=100):
    for _ in range(intentos):
        A = np.random.randint(1, 10, (m, n))
        b = np.random.randint(10, 50, m)
        z = np.random.randint(1, 10, n)
        res1 = simplex_solver(z, A, b)
        if res1 is None: continue
        val1, _, _ = res1
        z2 = z + np.random.uniform(0.1, 0.5, n)
        res2 = simplex_solver(z2, A, b)
        if res2 is not None:
            val2, _, _ = res2
            if abs(val1 - val2) > 1e-5:
                return z, A, b
    return None, None, None

def generar_sin_solucion(n, m):
    A = np.zeros((m, n))
    b = np.zeros(m)
    A[0, 0], b[0] = 1, 5
    A[1, 0], b[1] = -1, -10
    for i in range(2, m):
        A[i] = np.random.randint(1, 10, n)
        b[i] = np.random.randint(5, 20)
    z = np.random.randint(1, 10, n)
    return z, A, b

def generar_acotada(n, m):
    A = np.random.randint(1, 15, (m, n))
    b = np.random.randint(20, 100, m)
    z = np.random.randint(1, 10, n)
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
    for i in range(1, m+1):
        if D[i, col_piv] > limite:
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

def simplex_solver(c, A, b, maximizar=True, max_iter=50):
    if not maximizar: c = -c
    matriz = creador_matriz(c, A, b)
    m, n = A.shape
    base = list(range(n+1, n+m+1))
    for i in range(max_iter):
        if np.all(matriz[0, 1:] >= -1e-10):
            sol = np.zeros(n + m)
            for j, b_idx in enumerate(base):
                if b_idx - 1 < len(sol):
                    sol[b_idx-1] = matriz[j+1, 0]
            return matriz[0, 0], matriz, sol[:n]
        col = np.argmin(matriz[0, 1:]) + 1
        matriz, fila_piv = pivoteo(matriz, col, m)
        if matriz is None: return None
        base[fila_piv-1] = col
    return None

def iniciar_latex(nombre_archivo):
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(r"\documentclass{article}" + "\n")
        f.write(r"\usepackage[utf8]{inputenc}" + "\n")
        f.write(r"\usepackage{amsmath}" + "\n")
        f.write(r"\begin{document}" + "\n")
        f.write(r"\title{Lista de Problemas de Simplex}" + "\n")
        f.write(r"\maketitle" + "\n")

def añadir_problema_latex(z, A, b, contador, desc, nombre_archivo):
    n, m = len(z), len(b)
    with open(nombre_archivo, "a", encoding="utf-8") as f:
        f.write(f"\\section*{{Problema {contador}: Tipo: {desc}}}\n")
        obj = " + ".join([f"{z[i]}x_{i+1}" for i in range(n)])
        f.write(f"Maximizar: $Z = {obj}$\n\n")
        f.write(r"Sujeto a:" + "\n")
        f.write(r"\begin{align*}" + "\n")
        
        for i in range(m):
            rest = " + ".join([f"{A[i,j]}x_{j+1}" for j in range(n)])
            f.write(f"{rest} &\\leq {b[i]} \\\\\n")
        
        vars = ", ".join([f"x_{i+1}" for i in range(n)])
        f.write(f"{vars} &\geq 0" + "\n")
        f.write(r"\end{align*}" + "\n")
        f.write(r"\vspace{1cm}" + "\n") 

def finalizar_latex(nombre_archivo):
    with open(nombre_archivo, "a", encoding="utf-8") as f:
        f.write(r"\end{document}")

if __name__ == '__main__':
    archivo_pdf = "./Problemas_simplex.tex"
    iniciar_latex(archivo_pdf)
    contador_problemas = 1
    
    while True:
        print("\nMENU GENERADOR SIMPLEX")
        print("1. Generar problema con solucion unica")
        print("2. Generar problema sin solucion")
        print("3. Generar problema acotado")
        print("4. SALIR")
        
        tipo = input("\nElije una opcion: ")
        
        if tipo == '4':
            finalizar_latex(archivo_pdf)
            print(f"\nSe ha generado '{archivo_pdf}'.")
            #os.system(f'pdflatex {archivo_pdf}')
            check_call(['pdflatex', f'{archivo_pdf}'], stdout=DEVNULL, stderr=STDOUT)
            break
        
        if tipo not in ['1', '2', '3']:
            print("Opcion no valida")
            continue

        n, m = 2, 3 
        
        if tipo == '1':
            z, A, b = generar_unica(n, m)
            desc = "unica"
        elif tipo == '2':
            z, A, b = generar_sin_solucion(n, m)
            desc = "sin solucion"
        else:
            z, A, b = generar_acotada(n, m)
            desc = "acotada"

        if z is not None:
            print(f"\n[Problema #{contador_problemas} Generado y añadido]")
            añadir_problema_latex(z, A, b, contador_problemas, desc, archivo_pdf)
            
            res = simplex_solver(z, A, b)
            if res:
                val, _, vars = res
                print(f"optimo encontrado: {val:.2f}")
            
            contador_problemas += 1
        else:
            print("Error: No se pudo generar el problema.")