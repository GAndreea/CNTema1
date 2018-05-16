import numpy as np
import numpy
import math
from numpy import linalg as LA
from random import randint

epsilon = pow(10,-7);
kmax=100;
h=pow(10,-5)

def horner(coeficienti, v, n):
    if (n==0):
        return coeficienti[0];
    return coeficienti[n]+horner(coeficienti,v,n-1)*v;

def calculare_R(coeficienti):
    A=max(coeficienti)
    return (coeficienti[0]+A)/(coeficienti[0])

def get_Randoms(n):
    res=[]
    for i in range(n):
        a = randint(0,10)
        res.append(a)
    return res

def Muller2(coeficienti,x0,x1,x2):
    n1 = len(coeficienti)-1;
    deltax=5
    for loopCount in range(9000):
        Px = horner(coeficienti, x2, n1)
        Px1 = horner(coeficienti, x1, n1)
        Px2 = horner(coeficienti, x0, n1)
        h0=x1-x0
        h1=x2-x1
        delta0=(Px1-Px2)/h0
        delta1=(Px-Px1)/h1
        a=(delta1-delta0)/(h1+h0)
        b=a*h1+delta1
        c=Px
        if (b*b-4*a*c<0):
            break
        delta = math.sqrt(b*b-4*a*c)
        if (abs(max(b+delta,b-delta))<epsilon):
            break

        deltax = (2 * c) / max(b + delta, b - delta);

        x3=x2-deltax
        x0=x1;
        x1=x2;
        x2=x3
        if (deltax<epsilon or deltax>pow(10,8)):
            break;
    if (deltax<epsilon):
        return x3;
    return "div"


def main():
    # Declarare
    coeficienti=[1,4,-3,-18];
    #print(horner(coeficienti,-3,3))
    R=calculare_R(coeficienti)
    print("Interval: ", -R, R)
    for i in range(1000):
        sir = get_Randoms(3)
        try:
            x=Muller2(coeficienti, sir[0],sir[1],sir[2]);
            if (isinstance(x,float)):
                if (x!=0):
                    print(x)
        except ZeroDivisionError:
            # print("ZerDivErr")
            aq=2
        finally:
            # print("err2")
            aq=2

if __name__ == '__main__':
    main()
