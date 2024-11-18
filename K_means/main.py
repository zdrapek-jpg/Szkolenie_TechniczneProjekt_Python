import K_means
import Tests_Kmeans
import string
import time
Data1 = [ ["cena",'zniżka'],
 [1, 13, 20, 41],
 [2, 12, 19, 72],
 [3, 12, 21, 7],
 [4, 12, 20, 37],
 [5, 10, 18, 8],
 [6, 10, 21, 22],
 [7, -11, 4, 84],
 [8, 1, 23, 9],
 [9, 5, 18, 63],
 [10, -5, 10, 13],
 [11, 0, 15, 11],
 [12, 11.3, 13.2, 66],
 [13, 22, 29, 22],
 [14, 25, 21, 20],
 [15, 20, 30, 59],
 [16, 24, 20, 61],
 [17, 20, 32, 37],
 [18, 20, 19, 13],
 [19, 16, 23, 83],
 [20, 16, 24, 89],
 [21, 14, 29, 63],
 [22, 17, 29, 17],
 [23, 15, 28, 9],
 [24, 16, 27, 6],
 [25, 16, 22, 65],
 [26, 12, 22, 75],
 [27, 18, 32, 7],
 [28, 14, 23, 39],
 [29, 20, 17, 9],
 [30, 16, 18, 25],
 [31, 15, 21, 23]]
Data2 = [["cena",'zniżka'],
        [1, 13],
        [2, 12],
        [3, 12],
        [4, 12],
        [5, 10],
        [6, 10],
        [7, 11],
        [8, 1],
        [9, 5],
        [10, 5],
        [11, 0],
        [12, 11],
        [13, 22],
        [14, 25],
        [15, 20],
        [16, 24],
        [17, 20],
        [18, 20],
        [19, 16],
        [20, 16],
        [21, 14],
        [22, 17],
        [23, 15],
        [24, 16],
        [25, 16],
        [26, 12],
        [27, 18],
        [28, 14],
        [29, 20],
        [30, 16],
        [31, 15],
        [30,30],
        [19,21]
]

class Main:
    def __init__(self,data,clusters,k):
        self.data = data
        self.clusters = clusters
        self.k = k




#etylkiety : globalne bo tu są klasy dla k punktów
Etykiety = [x for x in string.ascii_uppercase]

K_means.initilaize_Kmenas(Data2[1:],2,Etykiety)
#Dane:
#Inicjalizacja testów przekazanie danych do klasy testującej gdzie dane są niepoprawne
# x1 =Tests_Kmeans.Tests([[2,3,4,5],[2,3,4,5],[2,3,4,58]],Etykiety,3)
x2 =Tests_Kmeans.Tests([[2,3,4,5],[34,23,11,2],(2,3,4,58)],Etykiety,3)
# x3 =Tests_Kmeans.Tests([[2,3,4,5,5],[2,3,4,5],[2,3,4,58],[2,3,4,5]],Etykiety,5)
# x4 =Tests_Kmeans.Tests([[2,3,4,5],["2",3,4,5],[2,3,4,58],[2,3,4,5]],["1",2,"3"],"5")
# x5 =Tests_Kmeans.Tests([[2,3,4,5],["2",3,4,5],[2,3,4,58],[2,3,4,5]],["1",2,"3"],5.0)
# x6 =Tests_Kmeans.Tests([[2,3,4,5],[2,3,4,5],[2,3,4,58],[2,3,4,5],[1,2,3,6]],["A","B","C"],8)
#
#
# #x2.data_errors()
# #x3.data_errors()
# #x4.labels_K_errors()
#x2.data_errors()


# testy kiedy kontynuacja algorytmu ma być wstrzymana
#
# print(Tests_Kmeans.Tests.continuation_conditions_centers([[2, 3, "A"], [4, 5, "B"], [2, 3, "C"]],
#                                                          [[3, 5, "A"], [6, 2], [2, 3, "C"]]))
# print(Tests_Kmeans.Tests.continuation_conditions_centers([[2, 3, "A"], [4, 5, "B"], [2, 3, "C"]],
#                                                          [[3, 5, "A"], [6, 2, "B"]]))
# print(Tests_Kmeans.Tests.continuation_conditions_centers([[2, 3, "A"], [4, 5, "B"], [2, 3, "C"]],
#                                                          [[2, 3, "A"], [6, 2, "B"], [5, 7, "C"]]))
# print(Tests_Kmeans.Tests.continuation_conditions_centers([[5, 3, "A"], [4, 5, "B"], [2, 3, "C"]],
#                                                          [[2, 4, "A"], [6, 2, "B"], [5, 7, "C"]]))