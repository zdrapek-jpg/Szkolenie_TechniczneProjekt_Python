import math
import numpy as np
import matplotlib
import pandas as pd
import random

data = [2,41,61,72,2,1,12,45,23,21,14,34]
data = ["snieg",1, "slonce",56]
data = [0,1, 9.8,   1,0 , 63.6]
def _find_min_max(data_row)-> list:
    if len(data_row)<=1:
        return None
    minimum = data_row[0]
    maximum = data_row[0]
    for data in data_row:
        if data> maximum:
            maximum= data
        if data<minimum:
            minimum= data
    return minimum,maximum

#print(_find_min_max(data))
def   conf( data,k):
    mn,mx = _find_min_max(data)
    difference = (mx-mn)/k

    granice = [mn+x*difference for x in range(k+1)]
    i = 1
    while i < len(data) :
        if granice[0] <= data[i] <= granice[1]:
            srednia = (granice[1] - granice[0]) / 2
            print(f"{srednia + granice[0]} : range <{granice[0]} {granice[1]}>")
        for j in range(2, len(granice)):
            srednia =(granice[j]- granice[j-1])/2
            if granice[j-1]<data[i]<=granice[j]:
                print(f"{srednia+ granice[j-1]} : range ({granice[j-1]} {granice[j]}>")
                break
        i += 1



    return granice



print(conf(data,4))

def sorting(data):
    for x in range():
        pass

def most_efficient_cutting(bom):
    x = 6000
    cutting = x
    rest = 0
    for cut in bom:
        if x >= cut:
            x -= cut
            print(cut, rest)
        if x < cut:
            rest = x - cut
            x = 6000
            print(cut, rest)


print(most_efficient_cutting([3000, 2200, 2000, 1800, 1600, 1300]))
print(most_efficient_cutting([4000, 4000, 4000]))
print(most_efficient_cutting([1]))
print(most_efficient_cutting([3001, 3001]))
print(most_efficient_cutting([3000, 2200, 1900, 1800, 1600, 1300]))
print(most_efficient_cutting([3000]))
print(most_efficient_cutting([3000, 2200, 2000, 1800, 1600, 1400]))

