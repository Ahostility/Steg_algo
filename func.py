import imageio
import random
import numpy as np


def encode_LSBR(in_f, out_f, text, R):
    if R <= 0 or R > 3:
        print('Неверный рейт внедрения')
        return
    bits = []
    f = open(text, 'r')
    blist = [ord(b) for b in f.read()]
    for b in blist:
        for i in range(8):
            bits.append((b >> i) & 1)
    I = imageio.imread(in_f)
    idx = 0
    for i in range(int(float(I.shape[0]) * R)):
        for j in range(int(float(I.shape[1]) * R)):
            for k in range(3):
                if idx < len(bits):
                    I[i][j][k] &= 0xFE
                    I[i][j][k] += bits[idx]
                    idx += 1
    imageio.imsave(out_f, I)
    f.close()
    print("Секретное сообщение запаковано в контейнер ", out_f)


def decode_LSBR(in_sf, out_text):
    I = imageio.imread(in_sf)
    f = open(out_text, 'w', encoding='utf8')
    bitidx, bitval = 0, 0
    for i in range(I.shape[0]):
        for j in range(I.shape[1]):
            for k in range(3):
                if bitidx == 8:
                    f.write(chr(bitval))
                    bitidx = 0
                    bitval = 0
                bitval |= (I[i, j, k] % 2) << bitidx
                bitidx += 1
    f.close()
    print("Контейнер бьш распакован секретное сообщение записано в файл ", out_text)


def encode_LSBM(in_f, out_f, text, R):
    bits = []
    f = open(text, 'r')
    blist = [ord(b) for b in f.read()]
    for b in blist:
        for i in range(8):
            bits.append((b >> i) & 1)
    I = imageio.imread(in_f)
    sign = [1, -1]
    idx = 0
    for i in range(int(float(I.shape[0])*R)):
        for j in range(int(float(I.shape[1])*R)):
            for k in range(3):
                if idx < len(bits):
                    if I[i][j][k] % 2 != bits[idx]:
                        s=sign[random.randint(0, 1)]
                        if I[i][j][k] == 0:
                            s = 1
                        if I[i][j][k] == 255:
                            s = -1
                        I[i][j][k] += s
                    idx += 1
    imageio.imwrite(out_f, I)
    f.close()
    print("Секретное сообщение запаковано в контейнер ", out_f)


def decode_LSBM(in_sf, out_text):
    I = imageio.imread(in_sf)
    f = open(out_text, 'w', encoding='utf8')
    bitidx = bitval = 0
    for i in range(I.shape[0]):
        for j in range(I.shape[1]):
            for k in range(3):
                if bitidx == 8:
                    f.write(chr(bitval))
                    bitidx = bitval = 0
                bitval |= (I[i, j, k] % 2) << bitidx
                bitidx += 1
    f.close()
    print("Контейнер был распакован секретное сообщение записано в файл ", out_text)


def encode_HAM(in_f, out_f, text):
    bits, minim, all = [], [], []
    H = [[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1], [0,1,1,0,0,1,1,0,0,1,1,0,0,1,1], [0,0,0,1,1,1,1,0,0,0,0,1,1,1,1],
         [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1]]
    f = open(text, 'r')
    blist = [ord(b) for b in f.read()]
    f.close()
    for b in blist:
        for i in range(8):
            bits.append((b >> i) & 1)
    I = imageio.imread(in_f)
    idx = 0
    new = [bits[d:d+4] for d in range(0, len(bits), 4)]
    print(I.shape[0], I.shape[1])
    for i in range(I.shape[0]):
        for j in range(I.shape[1]):
            for k in range(3):
                minim.append((I[i][j][k] >> 0) & 1)
    newb = [minim[d:d + 15] for d in range(0, len(minim), 15)]
    for i in range(len(new)):
        c = np.array(newb[i])
        m = np.array(new[i])
        B = (np.dot(H, c.transpose())) % 2
        N = (B+m.transpose()) % 2
        index = 8*N[3]+4*N[2]+2*N[1]+N[0]
        if index != 0:
            if newb[i][index-1] == 0:
                newb[i].pop(index - 1)
                newb[i].insert(index-1, 1)
            else:
                newb[i].pop(index - 1)
                newb[i].insert(index - 1, 0)
    for i in range(len(newb)):
        for j in range(len(newb[i])):
            all.append(newb[i][j])
    for i in range(I.shape[0]):
        for j in range(I.shape[1]):
            for k in range(3):
                if idx < len(all):
                    if ((I[i][j][k] >> 0) & 1) != all[idx]:
                        I[i][j][k] &= 0xFE
                        I[i][j][k] += all[idx]
                    idx += 1
    imageio.imsave(out_f, I)
    f.close()
    print("Секретное сообщение запаковано в контейнер ", out_f)


def decode_HAM (in_sf, out_text):
    # minim = tx = all = []
    minim = tx = all = [],[],[]
    H = [[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1], [0,1,1,0,0,1,1,0,0,1,1,0,0,1,1], [0,0,0,1,1,1,1,0,0,0,0,1,1,1,1],
         [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1]]
    I = imageio.imread(in_sf)
    f = open(out_text, 'w', encoding='utf8')
    for i in range(I.shape[0]):
        for j in range(I.shape[1]):
            for k in range(3):
                minim.append((I[i][j][k] >> 0) & 1)
    newb = [minim[d:d + 15] for d in range(0, len(minim), 15)]
    for i in range(len(newb)):
        c = np.array(newb[i])
        if len(newb[i]) == 15:
            mt = (np.dot(H, c.transpose())) % 2
        tx.append(list(mt))
    for i in range(len(tx)):
        for j in range(len(tx[i])):
            all.append(tx[i][j])
    for k in range(0, len(all), 8):
        st = str(all[k+7]) + str(all[k+6]) + str(all[k+5]) + str(all[k+4]) + str(all[k+3]) + str(all[k+2]) + str(all[k+1]) + str(all[k])
        bitval=int(st, base=2)
        f.write(chr(bitval))
    f.close()
    print("Контейнер был распакован секретное сообщение записано в файл ", out_text)
