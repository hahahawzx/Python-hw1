import numpy as np
T = eval(input())
for i in range(T):
    N,M = list(map(int,input().split()))
    sum = N*M
    b = np.arange(sum).reshape(N,M)
    for i in range(N):
        b[i] = list(map(int,input().split()))
    w = b[0].copy()
    b[0] = b[N-1]
    b[N-1] = w
    for i in range(N):
        t = b[i][0].copy()
        b[i][0] = b[i][M-1]
        b[i][M-1] = t
    middle = b.flatten()
    mask = middle > 0
    wask = middle == 0
    middle[mask] = 0
    middle[wask] = 1
    b = middle.reshape(N,M)
    for x in range(N):
        for y in range(M):
            if y!=M-1:
                print(b[x][y],end=" ")
            else:
                print(b[x][y])
             
        
        
            
    