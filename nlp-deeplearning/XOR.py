import numpy as np

X = np.array([[0, 0, 1, 1], [0, 1, 0, 1]])
Y = np.array([[0, 1, 1, 0]])

X_1 = X.shape[1]
Y_1 = Y.shape[1]

W_1=np.random.rand(2, 3)
B_1=np.random.rand(3, 1)
W_2=np.random.rand(3, 1)
B_2=np.random.rand(1, 1)


num_epoch = 10000
L_R = 0.03

# 시그모이드 함수 선언
def sigmoid(a):
    b = 1./(1+np.exp(- a))
    return b

for epoch in range(num_epoch):

    # 히든 노드
    H = np.dot(W_1.T, X) + B_1
    H = sigmoid(H)

    # output(Y_hat)
    H2 = np.dot(W_2.T, H) + B_2
    Y_hat = sigmoid(H2)

    # 로스 계산
    L =  -1 / X_1 * np.sum(Y[0] * np.log(Y_hat) + (1-Y[0]) * np.log(1-Y_hat))

    # Back-propagation 히든 레이어
    dW2 = np.dot(H, (Y_hat-Y).T)
    dB2 = 1. / Y_1 * np.sum(Y_hat-Y, axis=1, keepdims=True)
    dH  = np.dot(W_2, Y_hat-Y)

    # Back-propagation input layer
    dZ1 = dH * H * (1-H)
    dW1 = np.dot(X, dZ1.T)
    dB1 = 1. / Y_1 * np.sum(dZ1, axis=1, keepdims=True)
    
    # w
    W_2 += -L_R * dW2
    B_2 += -L_R * dB2
    W_1 += -L_R * dW1
    B_1 += -L_R * dB1


    pre = []

    for i in range(len(Y_hat[0])):
        if Y_hat[0][i] > 0.5:
            pre.append(1)
        else:
            pre.append(0)

accuracy=(pre==Y).mean()

print("loss: ", L)
print("예측: ", pre)
print("정확도: ", accuracy)