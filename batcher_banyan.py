#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Batcher-Banyan network

import numpy as np

class Batcher:
    def __init__(self, x):
        self.x = x
        self.n = int(len(x))
        
    # 2*2 bitnic sorter
    # ２つを比べて大きい方を下にする
    def sorter_base(self, x):
        if x[0] >= x[1]:
            return x[::-1]
        else:
            return x

    # n*n bitnic sorter
    # n*n bitnic sorterは一回り小さいbitnic sorterの組み合わせで表現できる
    # 任意の大きさのbitnic sorterは再帰的に表現することができる．
    def sorter(self, x):
        n = int(len(x))
        n2 = int(n/2)
        if n == 2:
            return self.sorter_base(x)  # 2*2が最小単位
        else:
            x1 = np.zeros(n)

            # まず2*2でsort
            for i in range(n2): 
                x1[2*i:2*i+2] = self.sorter_base(x[2*i:2*i+2]) 
            
            x2 = np.zeros(n)

            # 一回り小さいsorterに入力するために並び替える
            for i in range(n):
                if i<n2 and i%2 == 1:
                    x2[i] = x1[n2+i-1]
                elif i>=n2 and i%2 == 0:
                    x2[i] = x1[i-n2+1]
                else:
                    x2[i] = x1[i]
            
            x3 = np.zeros(n)

            # 上半分と下半分をそれぞれ一回り小さいbitnic sorterに入力する(再帰)
            x3[:n2] = self.sorter(x2[:n2])
            x3[n2:] = self.sorter(x2[n2:])
            return x3

    # n batcher network
    # batcher networkは2*2 bitnic sorterから初めて徐々に大きいsorterへ入力することを繰り返して実現される．
    # よって入力数に等しいbitnic sorterがくるまで，　sorterに入力→並び替え→より大きいsorterに入力．．．を繰り返す．
    # 任意のn*n bitnic sorterは上で定義されているのでそれを利用する．
    # k: sorterの入力次元数
    # p: sorterの数=n/k
    def run(self):
        data = self.x
        k = 2 

        # bitnic sorterの大きさが入力と一致するまで繰り返す．
        while k <= self.n:
            p = int(self.n/k) 
            
            data1 = np.zeros(self.n)

            # まず入力を適切に並び替える．
            for i in range(p): 
                for j in range(k):
                    if j<k/2:
                        data1[2*j+i*k] = data[j+i*k]
                    else:
                        data1[2*j-k+1+i*k] = data[j+i*k]                
            
            data2 = np.zeros(self.n)

            # 並び替えたものをそれぞれsorterに入力する．
            for i in range(p):
                s = self.sorter(data1[k*i:k*i+k])
                if i%2 == 1:
                    s = s[::-1]  # 奇数番目のものは出力を反転させる
                data2[k*i:k*i+k] = s
                
            k = k*2
            data = data2
            
        return data


class Banyan:
    def __init__(self, x):
        self.x = x

    # 2bit banyan sorter
    # Noneがきたらスルー
    # n_time: 判定に使うビットが先頭から何番目であるかを指定
    # n_time番目のbitが0なら上，　1なら下に出力
    def banyan_base(self, x, n_time):
        if x[0] is not None:
            if x[0][n_time] == '1':
                return x[::-1]
        elif x[1] is not None:
            if x[1][n_time] == '0':
                return x[::-1]
        
        return x

    # n入力 banyan network
    # 2bit banyan sorterを組み合わせることで実現
    # 内部の結び方はn*n bitnic sorterと同様になるのでこちらも再帰的に表現できる．
    def banyan(self, x, n_time):
        n = int(len(x))
        n2 = int(n/2)
        
        if n == 2:  # 2*2が最小単位
            return self.banyan_base(x,n_time)
        else:
            # まず2*2でsort
            x1 = [''] * n
            for i in range(n2): 
                x1[2*i:2*i+2] = self.banyan_base(x[2*i:2*i+2],n_time)
            
            # 一回り小さいsorterに入力するために並び替える
            x2 = [''] * n
            for i in range(n): 
                if i<n2 and i%2 == 1:
                    x2[i] = x1[n2+i-1]
                elif i>=n2 and i%2 == 0:
                    x2[i] = x1[i-n2+1]
                else:
                    x2[i] = x1[i]
            
            # 上半分と下半分をそれぞれ一回り小さいbitnic sorterに入力する(再帰)
            x3 = [''] * n
            x3[:n2] = self.banyan(x2[:n2],n_time+1)  # 判定に使うbitを何番目にするかについて，値を1増やす(n_time+1)
            x3[n2:] = self.banyan(x2[n2:],n_time+1)

            return x3

    def run(self):
        return self.banyan(self.x, 0)

def main():
    # 入力数列
    # x = np.array([1,1000,4,6,1000,0,1000,7])  # 8要素
    x = np.array([13,1000,4,6,1000,11,1000,8,1,1000,15,1000,7,3,9,1000])  # 16要素
    # x = np.array([13,1000,29,6,1000,11,1000,8,25,1000,15,1000,7,28,19,1000,
    #             1000,31,1000,1000,27,18,4,1,1000,1000,3,21,16,1000,9,1000])  # 32要素

    print('---input--- \n', x)

    n = int(len(x))
    n_time = int(np.log2(n))
    print('---x size--- \n', n)

    # batcher network
    batcher = Batcher(x)
    x1 = batcher.run()
    print('---batcher output--- \n', x1)

    # batcher networkの出力を banyan network　に入力するために並び替える
    x2 = np.zeros(n)
    for i in range(n):
        if i<n/2:
            x2[2*i] = x1[i]
        else:
            x2[2*i-n+1] = x1[i]

    # 10進数から2進数表現に変更
    x3 = [None]*n
    for i in range(n):
        if x2[i] < n:
            x3[i] = format(int(x2[i]), '0{}b'.format(n_time))  # n bitの2進数表現
    print('---banyan input--- \n', x3)

    # banyan network
    banyan = Banyan(x3)
    x4 = banyan.run()
    print('---banyan output--- \n', x4)

    # 確認のためbanyan networkの出力を10進数に変更
    x5 = [None] * n
    for i in range(n):
        if x4[i] != None:
            x5[i] = int(x4[i], 2)
    print('---final output--- \n', x5)


if __name__ == '__main__':
    main()

