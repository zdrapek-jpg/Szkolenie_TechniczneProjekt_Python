import logging
class Tests():
    errors_list = []
    def __init__(self,data,labels_points,k):
        self.Data= data
        self.labels_points = labels_points
        self.k=k


    # gdy dane nie są listą
    # gdy dane są krótsze o 2 nie ma sensu uruchamiać algorytmu
    # dane przekazane muszą być listą
    # jeśli jedna z zmiennyh   jest typu innego niż  int lub float
    # gdy jeden z punktów ma inną długość danych niż pozostałe
    def data_errors(self):
        if len(self.Data)<=2:
            raise TestKmeans_Info(f"Data provided for model sholud be longer than 2 and is : {len(self.Data)}")

        if not isinstance(self.Data,list):
            raise TestKmeans_data(f"Data provided for model must be type of list not  {type(self.Data)}")


        x_basic_length = len(self.Data[0])
        for one_line in self.Data:
            if not isinstance(one_line,list):
                raise TestKmeans_data("Object type error" ,f"object type supposed to be a list not {type(one_line)}",f"{self.Data.index(one_line)}")

            if x_basic_length != len(one_line):
                raise TestKmeans_data(
                    "different length " ,f" objects with {len(one_line)}!= {x_basic_length}",f"{self.Data.index(one_line)} and 0")

            if not all(isinstance(element, (int, float)) for element in one_line):
                raise TestKmeans_data("wrong type , ",f"Error occured for: {one_line} all numbers must be integer or float", self.Data.index(one_line))
        print("data checked!!!")
    #gdy etykiety są  rużnych typów wyrzucamy błąd
    # gdy k jest większe od ilości naych lub k jest większe od ilości etykiet
    # gdy k jest większe od ilości etykiet
    def labels_K_errors(self):
        if not isinstance(self.k,int):
            raise TestKmeans_data("k is wrong type :",f"{type(self.k)}  and must be <class 'str'>","0")
        if self.k > len(self.Data) or self.k<=0 :
            raise TestKmeans_Info(f"""k count of clusters must by greater than 0 \n
                                    k must be lower or equal to count of labels \n
                                   {self.k} must be  {len(self.Data)}""")
        if self.k >len(self.labels_points):
            raise TestKmeans_area(f"k count of clusters must by greater or equal to labels you give",self.k, len(self.labels_points))

        if not all(isinstance(element, str) for element in self.labels_points):
            raise TestKmeans_area("Center Points Data invalid ",f"elements must be strings not int  {self.labels_points}")


    @classmethod
    def continuation_conditions_centers(cls,current_centers,previous_centers):
        # na aktualnych centrach możęmy sprawdzić czy centra mają odwpiednią długość czy nie brakuje danych lub jest ich za dużo
        sprawdzenie = {}
        x = current_centers[0]
        sprawdzenie = [x]
        for y in current_centers[1:]:
            if len(x) != len(y):
                return False
            sprawdzenie.append(y)

        if len(current_centers) != len(sprawdzenie):
            return False
        if len(previous_centers) != len(current_centers):
            return False  # Grupy mają różną liczbę elementów kontynuujemy
        # current_centers i previous_centers powinny być listami o tej samej strukturze
        total_error = 0
        count = 0
        same= 1
        for prev_group, curr_group in zip(previous_centers, current_centers):
            if prev_group == curr_group:
                same+=1
            for c, p in zip(prev_group[:-1], curr_group[:-1]):
                total_error += abs(c - p)
                count += 1
        # Obliczamy średni błąd bezwzględny
        mean_absolute_error = total_error / count if count != 0 else 0
        print("error",mean_absolute_error)
        # sprawdzamy czy jest więszky od warotści
        print(f"{mean_absolute_error} < {0.50} and {True} and {same/len(current_centers)}>=1")
        return (mean_absolute_error < 0.50 and True) and same/len(current_centers)>=1   #kontynuujemy jeśli błąd jest mniejszy od 0.45 albo żadne z powyższych nie zwruciły inaczej
        #
        #([[1, 13], [2, 12], [3, 12], [4, 12], [5, 10], [6, 10], [7, -11], [8, 1], [9, 5], [10, -5], [11, 0], [12, 11.3],
        #   [13, 22], [14, 25], [15, 20], [16, 24], [17, 20], [18, 20], [19, 16], [20, 16], [21, 14], [22, 17], [23, 15],
        #   [24, 16], [25, 16], [26, 12], [27, 18], [28, 14], [29, 20], [30, 16], [31, 15]]
    @classmethod
    def continuation_conditions_groups(cls,previous_group,current_group):
        count =0
        for p,c in zip(previous_group,current_group):
            for points_p,points_c in zip(p,c):
                if points_c!=points_p:  # długość grup inna to znaczy że algorytm wprowadza zmiany
                    return False



        return True
        pass
    def write_file(self,error):
        logging.basicConfig(filename="ProgramLogs.txt",
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')


class TestKmeans_Info(Exception):
    pass
    def __init__(self,text):

        super().__init__(text)
    def __str__(self):
        return '\033[93m'+"{} ".format(super().__str__())


class TestKmeans_area(TestKmeans_Info):
    def __init__(self,text,area):
        super().__init__(text)
        self.area= area

    def __str__(self):
        return "{} at: {} in data".format(super().__str__(),self.area)
class TestKmeans_data(TestKmeans_Info):

    def __init__(self,text,data,index):
        super().__init__(text)
        self.data=data
        self.index=index

    def __str__(self):
        return "{} with: \033[91m{} , \n at index : {}".format(super().__str__(),self.data,self.index)



try:
    pass
    #raise TestKmeans_area("smthing is wrong","distances")
except TestKmeans_area as a:
    print("area error at : ",a)
except TestKmeans_data as d:
    print("data error at",d)
except TestKmeans_Info as t:
    print(f"error at place with ",t)
except Exception as e:
    print("not solved error: ",e)

