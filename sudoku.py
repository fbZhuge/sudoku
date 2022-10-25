#!/usr/bin/python3
import numpy as np
import subprocess

def check_row(M, i, j):
    k=0
    while(k<=8):
        if(M[i,k]==M[i,j] and k != j):
            return True
        k+=1
    return False

def check_column(M,i,j):
    k=0
    while(k<=8):
        if(M[k,j]==M[i,j] and k != i):
            return True
        k+=1
    return False

def top_box(M,i,j):
    i0=i//3*3
    j0=j//3*3
    return i0,j0

def check_box(M,i,j):
    i0,j0=top_box(M,i,j)
    for k in range(3):
        for l in range(3):
            if(M[i0+k,j0+l]==M[i,j] and i != i0+k and j != j0+l):
                return True
    return False

def check_sodoku(M,i,j):
    if(check_row(M,i,j) or check_column(M,i,j) or check_box(M,i,j)):
        return True
    else:
        return False

def get_zero_indices(M):
    zero_indices=[]
    for i in range(9):
        for j in range(9):
            if M[i,j]==0:
                zero_indices.append((i,j))
    return zero_indices

def get_non_zero_indices(M):
    zero_indices=[]
    for i in range(9):
        for j in range(9):
            if(M[i,j] != 0):
                zero_indices.append((i,j))
    return zero_indices

def solve_sodoku(M):
    zero_indices=get_zero_indices(M)
    n=len(zero_indices)
    index=0
    while index<n:
        i,j = zero_indices[index]
        if M[i,j] > 9:
            print("algorithm failed!")
            return M
        M[i,j]+=1
        while True:
            if(M[i,j]<=9 and check_sodoku(M,i,j)):
                M[i,j]+=1
                continue
            elif(M[i,j]==10):
                M[i,j]=0
                index-=1
                break
            else:
                index+=1
                break
    return M

def color_string(text, c="red"):
    s="{\\bf\\color{"+c+"}"+text+"}"
    return s

def create_tex_string(my_array):
    s="\\begin{sudoku}\n"
    for i in range(9):
        for j in range(9):
            if(my_array[i,j]==0): 
                s+="| "
            else: 
                s+=f"|{my_array[i,j]}"
        s+="|.\n"
    s+="\\end{sudoku}\n"
    return s

def create_colored_tex_string(my_array, nz, c="red"):
    #non_zero_indices=get_non_zero_indices(pb_array)
    non_zero_indices=nz
    print(f"non_zero_indices={non_zero_indices}")
    s="\\begin{sudoku}\n"
    for i in range(9):
        for j in range(9):
            if(my_array[i,j]==0): 
                s+="| "
            elif((i,j) not in non_zero_indices): 
                cs = color_string(f"{my_array[i,j]}", c)
                s+=f"|{cs}"
            else:
                s+=f"|{my_array[i,j]}"
        s+="|.\n"
    s+="\\end{sudoku}\n"
    return s

def main():
    O=np.array(([0,0,0, 0,0,0, 0,0,0],
                [0,0,0, 0,0,0, 0,0,0],
                [0,0,0, 0,0,0, 0,0,0],

                [0,0,0, 0,0,0, 0,0,0],
                [0,0,0, 0,0,0, 0,0,0],
                [0,0,0, 0,0,0, 0,0,0],

                [0,0,0, 0,0,0, 0,0,0],
                [0,0,0, 0,0,0, 0,0,0],
                [0,0,0, 0,0,0, 0,0,0]))

    A=np.array(([0,0,0, 0,0,0, 0,0,0],
                [0,1,0, 0,2,0, 0,3,0],
                [0,0,0, 0,0,0, 0,0,0],

                [0,0,0, 0,0,0, 0,0,0],
                [0,3,0, 0,1,0, 0,2,0],
                [0,0,0, 0,0,0, 0,0,0],

                [0,0,0, 0,0,0, 0,0,0],
                [0,2,0, 0,3,0, 0,1,0],
                [0,0,0, 0,0,0, 0,0,0]))

    # N easy puzzle
    N=np.array(([0,0,0, 2,6,0, 7,0,1],
                [6,8,0, 0,7,0, 0,9,0],
                [1,9,0, 0,0,4, 5,0,0],

                [8,2,0, 1,0,0, 0,4,0],
                [0,0,4, 6,0,2, 9,0,0],
                [0,5,0, 0,0,3, 0,2,8],

                [0,0,9, 3,0,0, 0,7,4],
                [0,4,0, 0,5,0, 0,3,6],
                [7,0,3, 0,1,8, 0,0,0]))

    # M very hard puzzle
    M=np.array(([0,0,0, 6,0,0, 4,0,0],
                [7,0,0, 0,0,3, 6,0,0],
                [0,0,0, 0,9,1, 0,8,0],

                [0,0,0, 0,0,0, 0,0,0],
                [0,5,0, 1,8,0, 0,0,3],
                [0,0,0, 3,0,6, 0,4,5],

                [0,4,0, 2,0,0, 0,6,0],
                [9,0,3, 0,0,0, 0,0,0],
                [0,2,0, 0,0,0, 1,0,0]))

    pb=N
    nz=get_non_zero_indices(pb)
    tex_file_path="my_sudoku.tex"
    pdf_file_path="my_sudoku.pdf"
    sudoku_pb_string=create_tex_string(pb)
    #print(f"sodoku=\n{pb}")
    solved_sodoku=solve_sodoku(pb)
    sudoku_solved_colored_string=create_colored_tex_string(solved_sodoku, nz, c="Orange")
    sudoku_solved_string=create_tex_string(solved_sodoku)

    tex_preambule_text="\\documentclass[10pt,a4paper]{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage[T1]{fontenc}\n\\usepackage{amsmath}\n\\usepackage{amssymb}\n\\usepackage{graphicx}\n\\usepackage[english]{babel}\n\\usepackage[dvipsnames]{xcolor}\n\\usepackage{sudoku}\n\\pagenumbering{gobble}\n\\begin{document}\n"

    with open(tex_file_path, 'w') as tex_file:
        tex_file.write(tex_preambule_text)
        tex_file.write(sudoku_pb_string)
        tex_file.write(sudoku_solved_colored_string)
        #tex_file.write(sudoku_solved_string)
        tex_file.write("\\end{document}\n")

    #print(f"solved sodoku=\n{solved_sodoku}")
    subprocess.run(["pdflatex", tex_file_path], capture_output=False)
    subprocess.run(["zathura", pdf_file_path], capture_output=False)

if(__name__ == "__main__"):
    main()
