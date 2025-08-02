data  = [2,41,61,72,2,1,12,45,23,21,14,34,11]

data.sort(key= lambda x: x)
print(data)

count = 0

def Bin_search(data,szukana,start=0,end=None):
    if end is  None:
        end = len(data)
    mid = (start+end)//2
    if start > end:
        return -1
    if szukana==data[mid]:
        return mid
    if szukana> data[mid]:
        return Bin_search(data,szukana,start=mid+1,end=end)

    return Bin_search(data,szukana,start,end = mid-1)

print(Bin_search(data,12))
#assert(Bin_search(data,61))== 10
#assert(Bin_search(data,72))== 11
#assert(Bin_search(data,45))== 9
#assert(Bin_search(data,1))== 0
#assert(Bin_search(data,12))== 3

def odwrucenie_tablicy(data,first=0,last=len(data)-1):
    if not isinstance(data,list):
        data = [x for x in data]
        last= len(data)-1
    # condition to exit function
    if first>=last:
        return data

    data[first],data[last] = data[last],data[first]

    # return recurection in reversing list
    return odwrucenie_tablicy(data,first+1,last-1)
print(odwrucenie_tablicy(data))
import math
def zamiana_na_dwojkowe(number, i=2,j =None):
    if j is None:
        j = int(math.sqrt(number))+1
    if number == 0 and j == 0 :
        return "0"
    if j <= 0 and number <=1:
        return "1"
    if number/(math.pow(i,j))>=1:
        return "1"+ zamiana_na_dwojkowe(number-math.pow(i,j),2,j-1)

    return "0"+zamiana_na_dwojkowe(number,2,j-1)

print(zamiana_na_dwojkowe(8))
print(zamiana_na_dwojkowe(6))
print(zamiana_na_dwojkowe(5))
print(zamiana_na_dwojkowe(4))
print(zamiana_na_dwojkowe(13))
print(zamiana_na_dwojkowe(16))
print(zamiana_na_dwojkowe(255))


def nwd(a,b):
    if b ==0:
        return a
    return nwd(b,a%b)


def deflation_counting(x,y):
    try:
        if x <= 0 :
            raise Exception("firt parameter must be positive value >=0")
        drate = ((x**2) /2)+y
        if drate== 0 :
            raise ValueError("outcome must be positive")
        print("wykonalo się to")

        return float(drate)
    except TypeError as e:
        raise TypeError(f"niedozwolona wartość dla {type(x)} {type(y)} for <=  ")



def define_brutto_netto(brutto,netto):
    try:
        thresh = deflation_counting(brutto,netto)
        net = brutto -(brutto *0.23) +thresh/brutto
        if net <= 0:
            raise ZeroDivisionError(f"net value must be positive value, {net}<0")
        print("wykonalo sie 2")
        print(f"{brutto}  - netto {net}=={netto}")
        if not isinstance(net,int):
            raise ArithmeticError("Walue must be a integer not float number")
        return net
    except ValueError as e:
        raise Exception("Exception turned out from second function")
#print(define_brutto_netto(23,"0"))



brutto,netto= 2300,1771

#define_brutto_netto(brutto,netto)

import datetime as dt



class Trip:
    list_of_erors= []
    def __init__(self, symbol, title, start, end):
        self.symbol = symbol
        self.title = title
        self.start = start
        self.end = end


    def check_data(self):
        assert (len(self.title) > 0), Exception("Title is empty!")
        assert (self.start <= self.end), ValueError("Start date is later than end date!")

    def Public_offer(self,trip_lists):
        for trip in trip_lists:
            try:
                trip.check_data()
            except ValueError as e:
               Trip.list_of_erors.append(f"error on  {trip_lists.index(trip)} as {e}")

            except Exception as e :
                Trip.list_of_erors.append(f"{trip_lists.index(trip)} occured {e}")
            except Exception as e:
                raise AttributeError(f"type error in line  {e} ")
        assert len(Trip.list_of_erors)<=0, "The list of trips has error"


trips = [
    Trip('IT-VNC', 'Italy-Venice', dt.date(2023, 6, 1), dt.date(2023, 6,21)),
    Trip('SP-BRC', 'Spain-Barcelona', dt.date(2023, 6, 12), dt.date(2023, 5, 22)),
    Trip('IT-ROM', 'Italy-Rome', dt.date(2023, 6, 21), dt.date(2023, 6, 12))
]
try:
    Trip.Public_offer(Trip,trips)
    print(Trip.list_of_erors)
except Exception as e:
    print(e)





