import numpy as np
import random as rand
from subprocess import DEVNULL, STDOUT, check_call

def generar_datos_base(n, m):
    """Genera coeficientes aleatorios basicos."""
    A = np.random.randint(1, 15, (m, n))
    b = np.random.randint(10, 100, m)
    z = np.random.randint(1, 20, n)
    return z, A, b

def iniciar_latex(nombre_archivo):
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(r"\documentclass{article}" + "\n")
        f.write(r"\usepackage[utf8]{inputenc}" + "\n")
        f.write(r"\usepackage{amsmath}" + "\n")
        f.write(r"\begin{document}" + "\n")
        f.write(r"\title{Generador de Problemas de Programacion Lineal}" + "\n")
        f.write(r"\author{Simplex Generator}" + "\n")
        f.write(r"\maketitle" + "\n")

def añadir_problema_latex(z, A, b, contador, tipo_sol, metodo, objetivo, nombre_archivo):
    n, m = len(z), len(b)
    obj_str = "Max" if objetivo == "1" else "Min"
    with open(nombre_archivo, "a", encoding="utf-8") as f:
        f.write(f"\\section*{{Problema {contador}}}\n")
        f.write(f"\\textbf{{Tipo de solucion esperada:}} {tipo_sol} \\\\\n")
        f.write(f"\\textbf{{Metodo sugerido:}} {metodo} \\\\\n")
        obj_tex = " + ".join([f"{z[j]}x_{{{j+1}}}" for j in range(n)])
        f.write(f"\\textbf{{{obj_str}:}} $Z = {obj_tex}$\n\n")
        f.write(r"\textbf{Sujeto a:}" + "\n")
        f.write(r"\begin{align*}" + "\n")
        for i in range(m):
            rest = " + ".join([f"{A[i,j]}x_{{{j+1}}}" for j in range(n)])
            f.write(f"{rest} &\\leq {b[i]} \\\\\n")  
        vars_tex = ", ".join([f"x_{{{j+1}}}" for j in range(n)])
        f.write(f"{vars_tex} &\geq 0\n")
        f.write(r"\end{align*}" + "\n")
        f.write(r"\hrule" + "\n")
        f.write(r"\vspace{0.5cm}" + "\n")

def finalizar_latex(nombre_archivo):
    with open(nombre_archivo, "a", encoding="utf-8") as f:
        f.write(r"\end{document}")

if __name__ == '__main__':
    archivo_tex = "./Problemas_Generados.tex"
    iniciar_latex(archivo_tex)
    contador = 1

    #pruebas = [[o, s, m] for o in [1, 2] for s in [1, 2, 3, 4] for m in [1, 2, 3]]
    tipos_dict = {1: "Unica", 2: "Multiples soluciones", 3: "No acotada", 4: "Infactible"}
    metodos_dict = {1: "Simplex Estandar", 2: "Gran M", 3: "Dos Fases"}

    while True:
        print(f"\nMENU PRINCIPAL problema {contador-1})")
        print("1 Agregar problema manual y continuar\n2 Finalizar y generar PDF\n3 Generar automatico (24 problemas)")
        op = input("Seleccione una opcion: ")

        if op == '2':
            finalizar_latex(archivo_tex)
            try:
                check_call(['pdflatex', '-interaction=nonstopmode', archivo_tex], stdout=DEVNULL, stderr=STDOUT)
                print(f"\nArchivo '{archivo_tex}' y PDF creados exitosamente.")
            except:
                print("\nNo se pudo ejecutar pdflatex")
            break
                   
        #elif op == '3':
            for obj, sol, met in pruebas:
                n_v, m_r = np.random.randint(2, 5), np.random.randint(2, 5)
                z, A, b = generar_datos_base(n_v, m_r)
                añadir_problema_latex(z, A, b, contador, tipos_dict[sol], metodos_dict[met], str(obj), archivo_tex)
                contador += 1
            print("Los 24 problemas se añadieron al archivo .tex")
            continue 
            
        elif op == '1':
            try:
                n = int(input("Cantidad de variables: "))
                m = int(input("Cantidad de restricciones: "))
                
                print("\nObjetivo:\n1 Maximizar\n2 Minimizar")
                obj = input("Opcion: ")
                
                print("\nTipo de solucion:\n1 Unica\n2 Multiples soluciones\n3 No acotada\n4 Sin solucion")
                t_sel = input("Opcion: ")
                tipo_sol = tipos_dict.get(int(t_sel), "Unica")

                print("\nMetodo de resolucion:\n1 Simplex Estandar\n2 Gran M\n3 Dos Fases")
                m_sel = input("Opcion: ")
                metodo = metodos_dict.get(int(m_sel), "Simplex Estandar")

                z, A, b = generar_datos_base(n, m)
                añadir_problema_latex(z, A, b, contador, tipo_sol, metodo, obj, archivo_tex)
                
                print(f"\nProblema #{contador} añadido")
                contador += 1
            except ValueError:
                print("\nesa opcion no existe")