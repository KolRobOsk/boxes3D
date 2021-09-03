import os, sys
sys.path.insert(0, os.path.abspath('.'))
from signatures_setup import *
from split_intervals import *
from cut_box import *

try:
    os.remove('3d_index.idx')
    os.remove('3d_index.dat')
except:
    pass
'''
Usuwanie poprzednich plików drzewa,
inaczej błąd kompilacji, bo python
próbuje zapisać coś co już jest
'''

#główna klasa całego programu
class algorithm:
    '''
    Główna klasa programu.
    '''
    def rotate_and_execute(self, box1, box2):
        '''
        Funkcja obraca pudełka zmieniając kolejność interwałów \n
        :param box1: pudełko ze stosu \n
        :param box2: pudełko z drzewa \n
        :return: lista table, która zawiera pudełka po rozbiciach \n
        :rtype: list
        '''
        sign = signatures()
        spl = split()
        idx_sign = sign.get_signatures_triple(box1, box2)
        sort, in2sorted, sorted2in = sign.my_sort(idx_sign)
        tri_sign = sign.permute([box1.interval_x, box1.interval_y, box1.interval_z], in2sorted)
        tri_sign_i = sign.permute([box2.interval_x, box2.interval_y, box2.interval_z], in2sorted)
        tri_sign, tri_sign_i = box3D(tri_sign[0], tri_sign[1], tri_sign[2]), box3D(tri_sign_i[0], tri_sign_i[1], tri_sign_i[2])
        split_sign = spl.split(tuple(sort), tri_sign, tri_sign_i)
        table = sign.ret_original_order(split_sign, sorted2in)
        return table

    @staticmethod
    def execute(box_list):
        '''
        Funkcja statyczna, która przyjmuje listę pudełek i zwraca listę rozbitych pudełek\n
        :param box_list: lista pudełek do rozbicia\n
        :return: lista pudełek po rozbiciu\n
        :rtype: list
        '''
        Q, drzewo = boxStack(), tree()
        Q.extend(box_list)
        algorithm().algorytm(Q, drzewo)
        return drzewo.ret_boxes()
		
		
    @staticmethod
    def algorytm(Q, tree):
        '''
        Funkcja statyczna, w wyniku której wszystkie przecinające się pudełka ze stosu zostają rozbite i wstawione do drzewa\n

        :param Q: stos pudełek\n
        :param tree: puste drzewo z indeksowaniem w trzech wymiarach\n
        :return: drzewo rtree zawierające pudełka\n
        :rtype: tree.tree
        '''

        #obiekt klasy myInterval
        my_int = myInterval()
        #zmienna potrzebna do wprowadzania pudełka w unikalne miejsce do drzewa
        iD = 0
        #pętla działa dopóki stos nie zostanie pusty
        while not Q.empty():
            #zdjęcie ostatniego pudełka ze stosu i przycięcie go
            q = Q.pop()
            if tree.tree.count((q.interval_x.lower,  q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper,  q.interval_z.upper)) > 0:
                '''
                Sprawdzenie czy pudełko q przecina się z którymkolwiek elementem z drzewa.
                Jeśli tak, pudełko przecinające się zostaje pobrane z drzewa i usunięte,
                zaś wynik rozbicia zostaje wstawiony ponownie na stos pudełek
                '''
                i = list(tree.tree.intersection((q.interval_x.lower,  q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper,  q.interval_z.upper), objects=True))[0]
                inter = [i.object.interval_x, i.object.interval_y, i.object.interval_z]
                j = box3D(inter[0], inter[1], inter[2])
                q = my_int.box_uncut(q)
                j = my_int.box_uncut(j)
                #cofnięcie przycięcia dla pudełek które mają być rozbite
                q = [my_int.box_cut(i) for i in algorithm().rotate_and_execute(q, j)]
                for box in q:
                    if box.interval_x.empty or box.interval_y.empty or box.interval_z.empty:
                        tree.tree.add(iD, (
                        box.interval_x.lower, box.interval_y.lower, box.interval_z.lower, box.interval_x.upper,
                        box.interval_y.upper, box.interval_z.upper), box)
                        iD += 1
                    else:
                        Q.extend([box])
                #wprowadzenie wyniku rozbicia na stos
                tree.tree.delete(i.id, (i.bbox[0], i.bbox[1], i.bbox[2], i.bbox[3], i.bbox[4], i.bbox[5]))
                #usunięcie starego pudełka z drzewa
            else:
                tree.tree.add(iD, (q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper, q.interval_z.upper), q)
                #dodanie nowego pudełka do drzewa i zwiększenie zmiennej iD o 1
                iD += 1

