import numpy as np
from scipy.spatial import distance
from flask import Flask
from flask import request
from flask import render_template
import random
app = Flask(__name__)


class GEPP():
    def __init__(self, A, b, doPricing=True, isMatrixSingular = False, pivotElementZero = False, invalidArguments = False):
        self.A = A                      # input: A is an n x n numpy matrix
        self.b = b                      # b is an n x 1 numpy array
        self.doPricing = doPricing
        self.isMatrixSingular = isMatrixSingular
        self.pivotElementZero = pivotElementZero
        self.invalidArguments = invalidArguments
        self.n = None                   # n is the length of A
        self.x = None                   # x is the solution of Ax=b

        if(self._validate_input() == 1):
            if(self._elimination() == 2):
                self._backsub()
            elif self._elimination() == 0:
                self.isMatrixSingular = True
            else: self.pivotElementZero = True
        else: self.invalidArguments = True


    def _validate_input(self):
        self.n = len(self.A)
        if self.b.size != self.n:
            return 0
        return 1

    def _elimination(self):
        # Elimination
        for k in range(self.n - 1):
            if self.doPricing:
                # Pivot
                maxindex = abs(self.A[k:, k]).argmax() + k
                if self.A[maxindex, k] == 0:
                   return 0
                # Swap
                if maxindex != k:
                    self.A[[k, maxindex]] = self.A[[maxindex, k]]
                    self.b[[k, maxindex]] = self.b[[maxindex, k]]
            else:
                if self.A[k, k] == 0:
                    return 1
            # Eliminate
            for row in range(k + 1, self.n):
                multiplier = self.A[row, k] / self.A[k, k]
                self.A[row, k:] = self.A[row, k:] - multiplier * self.A[k, k:]
                self.b[row] = self.b[row] - multiplier * self.b[k]
        return 2
    def _backsub(self):
        # Back Substitution
        self.x = np.zeros(self.n)
        for k in range(self.n - 1, -1, -1):
            self.x[k] = (self.b[k] - np.dot(self.A[k, k + 1:], self.x[k + 1:])) / self.A[k, k]

    def inversaMatricii(A):
        return np.linalg.inv(A)

    def normaEuclidiana(A,b):
        return distance.euclidean(A, b);


#generare matrice random de dim n
def gen_mat(n):
    R = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            R[i][j] = random.randint(0, 30)
    return R;

def gen_array(n):
    R = [[0 for x in range(1)] for y in range(n)]
    for i in range(n):
        for j in range(1):
            R[i][j] = random.randint(0, 30)
    return R;

def main():
    A = np.array([[0.02, 0.01, 0., 0.],
                  [1., 2., 1., 0.],
                  [0., 1., 2., 1.],
                  [0., 0., 100., 200.]])
    # A = np.array([[0, 0,],
    #               [0., 1.]])
    b = np.array([[0.02],
                  [1.],
                  [4.],
                  [800.]])
    # b = np.array([[2.],
    #               [1.]])

    GaussElimPiv = GEPP(np.copy(A), np.copy(b), doPricing=True)
    #print(GaussElimPiv.x)
    #print(GaussElimPiv.A)
    # print(GaussElimPiv.b)
    GaussElimPiv = GEPP(A, b)
    print(GaussElimPiv.x)

    #norma
    x= GaussElimPiv.A.dot(GaussElimPiv.x)
    norma = GEPP.normaEuclidiana(x,b)
    print(norma)

    #inversa matricii
    print(GEPP.inversaMatricii(A))

@app.route('/')
def my_form():
    return render_template("Tema1.html", M1=[[]], M2=[[]], R=[[]], x=[[]], N=0);

app.debug=True
@app.route('/', methods=['POST'])
def my_form_post():
    global res1
    global res2
    n = request.form['nValue']
    n= int(n)
    M1 = gen_mat(n)
    M2 = gen_array(n)
    A = np.array(M1)
    # A = np.array([[0, 0,],
    #               [0., 1.]])
    b = np.array(M2)
    # b = np.array([[2.],
    #               [1.]])

    GaussElimPiv = GEPP(np.copy(A), np.copy(b), doPricing=True)
    # print(GaussElimPiv.x)
    # print(GaussElimPiv.A)
    # print(GaussElimPiv.b)
    GaussElimPiv = GEPP(A, b)
    print(GaussElimPiv.x)

    # norma
    x = GaussElimPiv.A.dot(GaussElimPiv.x)
    norma = GEPP.normaEuclidiana(x, b)
    print(norma)

    # inversa matricii
    R=GEPP.inversaMatricii(A);
    print(R)
    return render_template("Tema1.html", M1=M1, M2=M2, R=R, x=GaussElimPiv.x, N=norma)

if __name__ == '__main__':
    app.run()