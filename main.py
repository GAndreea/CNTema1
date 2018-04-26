import numpy as np
from flask import Flask
from flask import request
from flask import render_template
import random
app = Flask(__name__)

import functools

epsilon = pow(10,-6);

def compare(t1,t2):
    return (int(t1[1])>int(t2[1])) - (int(t1[1])<int(t2[1]))

def sparse_matrix(fisier):
    f = open(fisier, "r")
    n = int(f.readline());
    matrix = [[]] * n;
    lines = f.readlines()[n + 2:];
    nr=0;
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
            #matrix[int(vals[1])].append(t);
            nr+=1;
        mn=sorted(matrix[int(vals[1])], key=functools.cmp_to_key(compare));
        matrix[int(vals[1])]=list(mn);
    return matrix

def get_b(fisier):
    f = open(fisier, "r")
    n = int(f.readline());
    matrix=[[]]*n
    lines = f.readlines()[1:n+1]
    res = []
    for i in range(len(lines)):
        t=(float(lines[i]), 0)
        new_line = list(matrix[i])
        new_line.append(t)
        matrix[i] = list(new_line);
    return matrix

def suma(m1, m2):
    matrix = [[]] * len(m1);
    for i in range(len(m2)):
        k=0
        l=0
        #print(k,l)
        while (k<len(m1[i]) and l<len(m2[i])):
            if (m1[i][k][1] == m2[i][l][1]):
                x = float(m1[i][k][0]) + float(m2[i][l][0]);
                t=(x,m1[i][k][1]);
                new_line = list(matrix[i])
                new_line.append(t)
                matrix[i]=list(new_line);
                k+=1;
                l+=1;
            else:
                if (int(m1[i][k][1]) < int(m2[i][l][1])):
                    new_line = list(matrix[i])
                    new_line.append(m1[i][k])
                    matrix[i] = list(new_line);
                    k+=1;
                else:
                    new_line = list(matrix[i])
                    new_line.append(m2[i][l])
                    matrix[i] = list(new_line);
                    l += 1;
        while (k<len(m1[i])):
            new_line = list(matrix[i])
            new_line.append(m1[i][k])
            matrix[i] = list(new_line);
            k += 1;
        while (l<len(m2[i])):
            new_line = list(matrix[i])
            new_line.append(m2[i][l])
            matrix[i] = list(new_line);
            l += 1;
    return matrix;

def compara(m1,m2):
    if (len(m1)!=len(m2)):
        return -1;
    for i in range(len(m1)):
        if (len(m1[i])!=len(m2[i])):
            return -1
        for j in range(len(m1[i])):
            if (m1[i][j][1]!=m2[i][j][1]):
                return -1
            if (abs(m1[i][j][0]-m2[i][j][0])>epsilon):
                return -1
    return 0

def transpune(m1):
    matrix = [[]] * len(m1);
    for i in range(len(m1)):
        for t in m1[i]:
            ctuplu = (t[0], i);
            new_line = list(matrix[int(t[1])])
            new_line.append(ctuplu)
            matrix[int(t[1])] = list(new_line);
    return matrix;

def dot(v1,v2):
    s=0
    k=0
    p=0
    while (k<len(v1) and p<len(v2)):
        if (v1[k][1]==v2[p][1]):
            s += v1[k][0] * v2[p][0]
            k+=1
            p+=1
        else:
            if (v1[k][1]>v2[p][1]):
                p+=1
            else:
                k+=1
    return s


def multiply(m1,m2):
    matrix=[[]]*len(m1)
    for i in range(len(m1)):
        for j in range(len(m2)):
            x = dot(m1[i], m2[j])
            if (x!=0):
                t = (x, j)
                new_line = list(matrix[i])
                new_line.append(t)
                matrix[i] = list(new_line);
    return matrix;

def creeaza_x(n):
    matrix=[[]]*n;
    for i in range(n):
        t=(n-i,0);
        new_line = list(matrix[i])
        new_line.append(t)
        matrix[i] = list(new_line);
    return matrix

def functie():
    m1 = sparse_matrix("a.txt");
    m2 = sparse_matrix("b.txt");
    m3 = sparse_matrix("aplusb.txt")
    m4 = sparse_matrix("aorib.txt")
    s = suma(m1, m2)

    f = open("res2.txt", "w+");
    f1 = open("m3.txt", "w+")
    f2 = open("s.txt", "w+")

    print("COMPARA SUMA: " + str(compara(s,m3)));
    i = multiply(m1,transpune(m2));
    print("COMPARA INMULTIRE: " + str(compara(i, m4)));
    x=creeaza_x(2018)
    b=get_b("a.txt")
    m = multiply(m1, transpune(x));
    print("COMPARA B (A): " + str(compara(m,b)))

    b2=get_b("b.txt")
    i0=multiply(m2,transpune(x));
    print("COMPARA B (B): " + str(compara(i0, b2)))
    k1=str(compara(s,m3))
    k2=str(compara(i, m4))
    k3=str(compara(m,b))
    k4=str(compara(i0, b2))
    return (k1,k2,k3,k4)


@app.route('/')
def my_form():
   f = functie()
   return render_template("Tema1.html", k1=f[0], k2=f[1], k3=f[2],k4=f[3])


app.debug=True
@app.route('/', methods=['POST'])
def my_form_post():
    f = functie()
    return render_template("Tema1.html", k1=f[0], k2=f[1], k3=f[2], k4=f[3])

if __name__ == '__main__':
    app.run()

