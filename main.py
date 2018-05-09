import functools
import scipy.sparse
import numpy as np
from flask import Flask
from flask import request
from flask import render_template
import random
app = Flask(__name__)


# x_stare_urmatoare(i) = (vectorulB(i) - suma(linia i din matrice * x_din stare_precendenta)(j)) / linia i din matrice(i)

def sparse_matrix(fisier):
    f = open(fisier, "r")
    n = int(f.readline());
    matrix = [[]] * n;
    lines = f.readlines()[n + 2:];
    nr = 0;
    for line in lines:
        vals = line.split(',');
        # vals[0]-valoarea vals[1]-linia vals[2]-coloana
        m = list(matrix[int(vals[1])]);
        ok = 0;
        for t in range(len(m)):
            if m[t][1] == vals[2]:
                x = float(m[t][0]) + float(vals[0])
                new_t = (float(x), int(m[t][1]))
                m[t] = new_t;
                ok = 1;
        matrix[int(vals[1])] = list(m);
        if (ok == 0):
            t = (float(vals[0]), int(vals[2]));
            new_line = list(matrix[int(vals[1])])
            new_line.append(t)
            matrix[int(vals[1])] = list(new_line);
            # matrix[int(vals[1])].append(t);
            nr += 1;
        mn = sorted(matrix[int(vals[1])], key=functools.cmp_to_key(compare));
        matrix[int(vals[1])] = list(mn);
    return matrix


def dot(v1, v2):
    s = 0
    k = 0
    p = 0
    while (k < len(v1) and p < len(v2)):
        if (v1[k][1] == v2[p][1]):
            s += v1[k][0] * v2[p][0]
            k += 1
            p += 1
        else:
            if (v1[k][1] > v2[p][1]):
                p += 1
            else:
                k += 1
    return s


def transpune(m1):
    matrix = [[]] * len(m1);
    for i in range(len(m1)):
        for t in m1[i]:
            ctuplu = (t[0], i);
            new_line = list(matrix[int(t[1])])
            new_line.append(ctuplu)
            matrix[int(t[1])] = list(new_line);
    return matrix;


def multiply(m1, m2):
    matrix = [[]] * len(m1)
    for i in range(len(m1)):
        for j in range(len(m2)):
            x = dot(m1[i], m2[j])
            if (x != 0):
                t = (x, j)
                new_line = list(matrix[i])
                new_line.append(t)
                matrix[i] = list(new_line);
    return matrix;


def diferenta(m1, m2):
    matrix = [[]] * len(m1);
    for i in range(len(m2)):
        k = 0
        l = 0

        while (k < len(m1[i]) and l < len(m2[i])):
            if (m1[i][k][1] == m2[i][l][1]):
                x = float(m1[i][k][0]) - float(m2[i][l][0]);
                t = (x, m1[i][k][1]);
                new_line = list(matrix[i])
                new_line.append(t)
                matrix[i] = list(new_line);
                k += 1;
                l += 1;
            else:
                if (int(m1[i][k][1]) < int(m2[i][l][1])):
                    # matrix[i].append(m1[i][k]);
                    new_line = list(matrix[i])
                    new_line.append(m1[i][k])
                    matrix[i] = list(new_line);
                    k += 1;
                else:
                    new_line = list(matrix[i])
                    new_line.append(m2[i][l])
                    matrix[i] = list(new_line);
                    # matrix[i].append(m2[i][l])
                    l += 1;
        # print(k,l)
        while (k < len(m1[i])):
            new_line = list(matrix[i])
            new_line.append(m1[i][k])
            matrix[i] = list(new_line);
            k += 1;
        while (l < len(m2[i])):
            new_line = list(matrix[i])
            new_line.append(m2[i][l])
            matrix[i] = list(new_line);
            l += 1;
    return matrix;


def compare(t1, t2):
    return (int(t1[1]) > int(t2[1])) - (int(t1[1]) < int(t2[1]))


def get_b(fisier):
    f = open(fisier, "r")
    n = int(f.readline());
    matrix = [[]] * n
    lines = f.readlines()[1:n + 1]
    res = []
    for i in range(len(lines)):
        t = (float(lines[i]), 0)
        new_line = list(matrix[i])
        new_line.append(t)
        matrix[i] = list(new_line);
    return matrix


def checkDiagonal(matrix, n):
    hasValue = True
    for i in range(n):
        line = [x[1] for x in matrix[i]]
        if i not in line:
            hasValue = False
    if (hasValue == True):
        return True
    else:
        return False


def nextValues(matrix, vectorB, xValues, n):
    for i in range(n):
        line = matrix[i]
        bi = vectorB[i]
        divisor = 1
        for j in range(len(line)):
            if (line[j][1] != i):
                bi = bi - line[j][0] * xValues[j]
            if (line[j][1] == i):
                divisor = line[j][0]
        bi = bi / divisor
        xValues[i] = bi
    return xValues


def checkFinalState(xValues, newxValues, precision):
    ok = True
    for i in range(len(xValues)):
        if (abs(xValues[i] - newxValues[i]) >= precision):
            ok = False
    return ok


def norma(matrix, xValues, vectorB):
    print(xValues)
    m = multiply(matrix, transpune(xValues))
    #bAsMatrix = [[tuple([x, 0])] for x in vectorB]
    print(m)
    print(vectorB)
    norma = diferenta(m, vectorB)
    max = norma[0][0][0]
    for line in norma:
        for column in line:
            if abs(column[0]) > max:
                max = column[0]
    return max


def functie():
    f = open("m_rar_2018_4.txt", "r")
    n = int(f.readline())
    v = get_b("m_rar_2018_4.txt")
    precision = 10 ** -7
    vectorB = [x[0][0] for x in v]
    matrix = sparse_matrix("m_rar_2018_4.txt")
    xValues = [0] * (n)
    finished = False
    nrOfIteration = 0
    results = []
    if (checkDiagonal(matrix, n) == True):
        while finished == False and nrOfIteration < 10000:
            prevIteration = xValues[:]
            newxValues = nextValues(matrix, vectorB, xValues, n)
            # asta trebuie afisata in html
            print("xvalues la iteratia ", nrOfIteration, " : ", xValues)
            results.append(list(xValues))

            finished = checkFinalState(prevIteration, newxValues, precision)
            nrOfIteration = nrOfIteration + 1
            print("nrOfIteration", nrOfIteration)
    else:
        print("Diagonala are valori nule")
        return
    xValuesTransformed = [[tuple([x, 0])] for x in xValues]

    bAsMatrix = list(map(lambda x: [(x, 0)], vectorB))

    norma2 = norma(matrix, xValuesTransformed, bAsMatrix)
    # asta trebuie afisata in html
    print(norma2)
    for l in results:
        print('\n')
        print(l)
    return results, norma2


@app.route('/')
def my_form():
   res, norma = functie()
   return render_template("Tema1.html", res=res, norma=norma)


app.debug=True
@app.route('/', methods=['POST'])
def my_form_post():
    f = functie()
    return render_template("Tema1.html", res=res, norma=norma)

if __name__ == '__main__':
    app.run()
