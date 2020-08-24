import numpy as np

#L1  = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
L1  = [0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
L2  = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
#L3  = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
L3  = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
L4  = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
L5  = [0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
L6  = [0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
L7  = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
L8  = [0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
L9  = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
L10 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

L = np.array([L1, L2, L3, L4, L5, L6, L7, L8, L9, L10])

ITERATIONS = 100
SIZE = 10


def getM(L):
    M = np.zeros([10, 10], dtype=float)
    # number of outgoing links
    c = np.zeros([10], dtype=int)
    
    ## TODO 1 compute the stochastic matrix M
    for i in range(0, 10):
        c[i] = sum(L[i])
    
    for i in range(0, 10):
        for j in range(0, 10):
            if L[j][i] == 0: 
                M[i][j] = 0
            else:
                M[i][j] = 1.0/c[j]
    return M

def getRank(M, v, q, iter, d = np.ones([SIZE], dtype=float)):
    for t in range(iter):
        tempV = v.copy()
        for i in range(SIZE):
            tempSum = 0
            for j in range(SIZE):
                tempSum += M[i][j] * tempV[j]
            v[i] = q * d[i] + (1 - q) * tempSum
    return v

print("Matrix L (indices)")
print(L)    

M = getM(L)



### TODO 2: compute pagerank with damping factor q = 0.15
### Then, sort and print: (page index (first index = 1 add +1) : pagerank)
### (use regular array + sort method + lambda function)
print("PAGERANK")

q = 0.15

pr = np.zeros([10], dtype=float)
pr[:] = 1/10
pr = getRank(M, pr, q, ITERATIONS)
pr = pr/sum(pr)
pSort = lambda x: [print(np.where(x==i)[0] + 1, '\t: ', i) for i in sorted(np.unique(x), reverse = True)]

print("Page Rank")
pSort(pr)
# Najlepszy wynik uzyskała strona 7, ponieważ zgodnie z algorytmem posiadała najwięcej
# dojść od zewnętrznych stron

### TODO 3: compute trustrank with damping factor q = 0.15
### Documents that are good = 1, 2 (indexes = 0, 1)
### Then, sort and print: (page index (first index = 1, add +1) : trustrank)
### (use regular array + sort method + lambda function)
print("TRUSTRANK (DOCUMENTS 1 AND 2 ARE GOOD)")

q = 0.15

d = np.zeros([10], dtype=float)
d[0:2] = 1
d = d / sum(d)
tr = [v for v in d]

tr = getRank(M, tr, q, ITERATIONS, d)
pSort(tr)

# Patrząc na graf połączeń można stwierdzić, że strona 7 należy do farmy linków
# Algorytm Trustrank pozwala nam określić, które strony są dobre, a które złe.
# W porównaniu z algorytmem Pagerank pozwoliło nam to osłabić strony należące do farmy linków,
# oraz wzmocnić strony, które oznaczyliśmy jako dobre. Aktualnie najlepsza okazała się strona 2.
# Strona 1 jest na drugim miejscu, a wcześniej plasowała się na ostatniej pozycji.
# Strona 7 znalazła się na trzecim miejscu.


### TODO 4: Repeat TODO 3 but remove the connections 3->7 and 1->5 (indexes: 2->6, 0->4) 
### before computing trustrank
print("TRUSTRANK (DOCUMENTS 1 AND 2 ARE GOOD) - changed L1 and L3")

L1  = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
L3  = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
L = np.array([L1, L2, L3, L4, L5, L6, L7, L8, L9, L10])
M = getM(L)


q = 0.15

d = np.zeros([10], dtype=float)
d[0:2] = 1
d = d / sum(d)
tr = [v for v in d]

tr = getRank(M, tr, q, ITERATIONS, d)
pSort(tr)

# Usunięcie połączeń do stron 5 i 7 spowodowało dużą zmiane wyników. Nadal najlepsze okazały się strony
# 2 i 1, za nimi uplasowały się strony 3 i 4. Strony 5, 6, 7, 8, 9, 10 zajeły ostatnie miejsce.
# Spowodowane jest to sztucznym promowaniem strony 7 i brakiem odnośników do innych stron z poza tej grupy.