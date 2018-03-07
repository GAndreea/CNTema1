from flask import Flask
from flask import request
from flask import render_template
import numpy as np
import math
import random
import time
import sys
app = Flask(__name__)

def ex_1():
    i=1;
    while True:
        if (1+pow(10, -i)==1):
            break;
        x=i;
        i = i + 1;
    return -x-1;

def ex_2():
    x=1.0;
    u=pow(10, ex_1());
    y=u;
    z=u;
    return (((x+y)+z)==(x+(y+z)))

def ex_2_b():
    x=1.0;
    y=0.4;
    z=1.2;
    while ((x*y)*z==x*(y*z)):
        y += 0.01
        z += 0.1
    print (x,y,z)


#inmultire normala
def multipl(X,Y):
    result = [[0 for x in range(len(X))] for y in range(len(Y))]
    for i in range(len(X)):
        # iterate through columns of Y
        for j in range(len(Y)):
            # iterate through rows of Y
            for k in range(len(Y)):
                result[i][j] += X[i][k] * Y[k][j]
    return result;

#inmultire strassen - matrici 2*2
def inmultire(M1, M2):
    w = 2;
    M3 = [[0 for x in range(w)] for y in range(w)]

    p1 = (M1[0][0] + M1[1][1])*(M2[0][0]+M2[1][1])
    p2 = (M1[1][0]+M1[1][1])*M2[0][0]
    p3 = M1[0][0]*(M2[0][1]-M2[1][1])
    p4 = M1[1][1]*(M2[1][0]-M2[0][0])
    p5=(M1[0][0]+M1[0][1])*M2[1][1]
    p6=(M1[1][0]-M1[0][0])*(M2[0][0]+M2[0][1])
    p7=(M1[0][1]-M1[1][1])*(M2[1][0]+M2[1][1])

    M3[0][0] = p1+p4-p5+p7;
    M3[0][1] = p3+p5;
    M3[1][0] = p2+p4
    M3[1][1] = p1+p3-p2+p6;

    return M3;

def suma(M1, M2):
    M3 = [[0 for x in range(len(M1))] for y in range(len(M1))]
    for i in range (0,len(M1)):
        for j in range (0,len(M1)):
            M3[i][j] = M1[i][j] + M2[i][j];
    return M3

def dif(M1, M2):
    M3 = [[0 for x in range(len(M1))] for y in range(len(M1))]
    for i in range (0,len(M1)):
        for j in range (0,len(M1)):
            M3[i][j] = M1[i][j] - M2[i][j];
    return M3

#redimensioneaza matricea la o dimensiune n
def redim(M,n):
    R = [[0 for x in range(n)] for y in range(n)]
    m = min(len(M),n)
    for i in range(m):
        for j in range(m):
            R[i][j] = M[i][j]
    return R;

#generare matrice random de dim n
def gen_mat(n):
    R = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            R[i][j] =  random.randint(0, 30)
    return R;

one_time_only = 1;

#algoritm Strassen
def algo(M1, M2, d):
    temp = math.log(len(M1),2)
    temp = int(temp)
    if (pow(2, temp)!=len(M1)):
        temp = temp + 1;
        new_n = pow(2,temp);
        M1 = redim(M1, new_n);
        M2 = redim(M2, new_n);
    n = math.log(len(M1), 2) - 1
    if (n+1<=d):
        return multipl(M1, M2)
    if (n==0):
        return inmultire(M1,M2);
    else:
        n = math.log(len(M1), 2) - 1
        n=int(n)
        n=pow(2,n)
        m = math.log(len(M2), 2) - 1
        m = int(m)
        m = pow(2, m)
        A = np.array(M1)[0:n,0:n]
        B = np.array(M1)[0:n, n:len(M1)]
        C = np.array(M1)[n:len(M1), 0:n]
        D = np.array(M1) [n:len(M1), n:len(M1)]
        E = np.array(M2)[0:m, 0:m]
        F = np.array(M2)[0:m, m:len(M2)]
        G = np.array(M2)[m:len(M2), 0:m]
        H = np.array(M2)[m:len(M2), m:len(M2)]

        p1 = algo(suma(A, D), suma(E, H), d)
        p2 = algo(suma(C, D), E,  d)
        p3 = algo(A, dif(F, H), d)
        p4 = algo(D, dif(G, E),  d)
        p5 = algo(suma(A, B), H,  d)
        p6 = algo(dif(C, A), suma(E, F), d)
        p7 = algo(dif(B, D), suma(G, H), d)

        if (1==1):
            X = suma(dif(suma(p1 , p4), p5) , p7);
            Y = suma(p3 , p5);
            Z = suma(p2 , p4);
            W = suma(dif(suma(p1 , p3), p2) , p6);
            R = [[0 for x in range(len(X)+len(Y))] for y in range(len(X)+len(Y))]
            for i in range (len(X)):
                for j in range (len(X)):
                    R[i][j]=X[i][j]
            for i in range (len(Y)):
                for j in range (len(Y)):
                    R[i][j+len(Y)]=Y[i][j]
            for i in range (len(Z)):
                for j in range (len(Z)):
                    R[i+len(Z)][j] = Z[i][j]
            for i in range (len(W)):
                for j in range (len(W)):
                    R[i+len(W)][j+len(W)] = W[i][j]
            return R;

res1 = ex_1()
res2 = "(((x+y)+z)==(x+(y+z))): " + str(ex_2())

@app.route('/')
def my_form():
    global res1
    global res2
    return render_template("Tema1.html", res1 = res1, res2=res2, M1=[[]], M2=[[]], R=[[]])

app.debug=True
@app.route('/', methods=['POST'])
def my_form_post():
    global res1
    global res2
    d = request.form['dValue']
    n = request.form['nValue']
    d = int(d)
    n= int(n)
    M1 = gen_mat(n)
    M2 = gen_mat(n)
    start_time2 = time.time()
    R2 = multipl(M1, M2)
    print(time.time() - start_time2)
    start_time = time.time()
    R = algo(M1, M2, d)
    print(time.time()-start_time)

    R=redim(R,n)
    return render_template("Tema1.html", res1=res1,res2=res2, M1=M1, M2=M2, R=R)

if __name__ == '__main__':
    app.run()
