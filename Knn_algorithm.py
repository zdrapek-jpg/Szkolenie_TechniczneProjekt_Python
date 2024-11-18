# Python  3.10!
# algorytm knn - k nearest neighbours
from typing import List

# porównywanie odległości między punktami

                 # k najbliższych punków#
#               #metoda: sum odwrotności#
#                #metryka: city block#
Data = [("A",24,17),
        ("B",14,19),
        ("B",-140,8),
        ("B",43,63),
        ("A",19,1),
        ("C",25,21),
        ("C",14,13),
        ("D",1,1)
        ]
#Data.sort(key= lambda x : x[0])

from math import sqrt
def sumy_odwrotnosci(added_point, distance_data):
    if len(added_point)!= len(distance_data):
        raise  Exception(f"nieodpowiednie dystane dla punktów miedzy sobą {len(added_point)}, {len(distance_data)} ")
    suma = [(e1-e2)**2 for e1,e2 in zip(added_point,distance_data)]
    #return sum(suma)
    return round(sqrt(sum(suma)),4)

sumy_odwrotnosci((3,5),(6,7))
def sum_of_current_point(data,added_point):
    for i in range(len(data)):
        point = data[i][0]
        distance_data = data[i][1:]
        data[i] = (point, sumy_odwrotnosci(added_point, distance_data))
    return data

Data =sum_of_current_point(Data,(14,15))

print(Data)

def classify_point_at_k_neightbours(Distances_to_klasses, k):
    Distances_to_klasses = sorted(Distances_to_klasses,key= lambda x : x[1])
    print(Distances_to_klasses)
    classes = {}
    distance = 0
    i =0
    while i<len(Distances_to_klasses) and i <=k:
        distance = Distances_to_klasses[i][1]
        if Distances_to_klasses[i][0] in classes.keys():
            classes[Distances_to_klasses[i][0]] += 1/(distance**2)
        elif Distances_to_klasses[i][0] not in classes.keys():
            classes[Distances_to_klasses[i][0]] =1/(distance**2)
        i+=1
    print("by closest to object is :")
    return classes



print(classify_point_at_k_neightbours(Data,7))