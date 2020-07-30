#decorator
def verify(function):
    def wrap(request, *args, **kwargs):

        os_info = request.request.GET.get('os', '')
        mac_id = request.request.GET.get('id', '')
        os_info = os_info.lower()
        mac_id = mac_id.lower()
        if os_info == 'window':
            entry = get_or_none(ModelObj, mac_id__icontains=id)
            if entry:
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"status": False,
                                     "message": error_code.get('106'), 'error_code': 106})
        elif os_info == 'appile':
            return function(request, *args, **kwargs)
        else:
            return JsonResponse({"status": False, "message": "%s not supported." % (os_info)})

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def decorator(fun):
    def inner_deco(*args):
        print((args[0]-args[1]))
    return inner_deco

@decorator
def sums(a,b):
    return a+b

#sums(2,3)


################################################################################################################################
#generator:

def Foo():
    for i in range(10):
        yield i*2

a = Foo()
# print(next(a))
# print(next(a))

def Fib(n):
    a,b =0,1
    while a <n:
        yield a
        a,b  = b,a+b
a =Fib(10)
# print(next(a))
# print(next(a))
# for i in Fib(10):
#     print(i)

################################################################################################################################
#recurence

#example01:
lst = [1,2,3,4,5]

def recur(lst):
    if not lst:
        return 0
    else:
        return lst[0]+recur(lst[1:])

#print(recur(lst))

lst = [1, [2, [3, 4], 5], 6, [7, 8]]

def recur(lst):
    tot = 0
    for each in lst:
        if not isinstance(each,list):
            tot+=each
        else:
            tot+=recur(each)
    return tot

#print(recur(lst))
################################################################################################################################
#Closures

def closur(num):
    def inner(value):
        return num*value
    return inner

obj = closur(3)
#print(obj(3))

################################################################################################################################
#Monkey Patching

class Foo:
    def __init__(self,num):
        self.num= num

def test(self):
    return self.num

Foo.test = test

obj = Foo(30)

#print(obj.test())

################################################################################################################################
#Duck typing & Polymorphism

class Pen:
    def get(self):
        print('pen')
class Book:
    def get(self):
        print('book')

def interface(obj):
    return obj.get()

p = Pen()
b = Book()

#interface(b)
################################################################################################################################
#Operator Overloading

class T:
    def __init__(self,v1):
        self.v1 = v1
    def __add__(self,v2):
        return self.v1 +v2.v1

a =T(1)
b = T(2)
#print(a+b)

#Override class methods

class T:
    def __init__(self):
        self.value = 4
    def get(self):
        return self.value
class V(T):
    def get(self):
        return self.value+1

t = T()
#print(t.get())
v = V()
#print(v.get())

################################################################################################################################
#merge sort
arr=[1,5,3,2]
def merge(arr):
    if len(arr)>1:
        mid = len(arr)//2
        l = arr[:mid]
        r = arr[mid:]
        merge(l)
        merge(r)
        i=0
        j=0
        k=0
        while i <len(l) and j <len(r):
            if l[i] < r[j]:
                arr[k] = l[i]
                i+=1
            else:
                arr[k] = r[j]
                j+=1
            k+=1
        while i <len(l):
            arr[k] = l[i]
            i+=1
            k+=1
        while j <len(r):
            arr[k] = r[j]
            j+=1
            k+=1
        return arr

#print(merge(arr))
################################################################################################################################

#sort list of 0,1

lst = [0,1,0,1,0,1,0]
#first way [swapping]

first =0
last =len(lst)-1

while first < last: 
    if lst[first] ==1:
        lst[first],lst[last] = lst[last],lst[first]
        last -=1
    else:
        first +=1

#print(lst)

#second way

count =0
for i in range(len(lst)):
    if lst[i] !=1:
        lst[count] = lst[i]
        count+=1
while count < len(lst):
    lst[count] = 1
    count+=1

#print(lst)

################################################################################################################################
#maxof three

def max_of_three(a,b,c):
    if a >=b and a >=c:
        largest = a
    elif b >=a and b >=c:
        largest = b
    else:
        largest =c
    return largest
#print max_of_three(44,23,67)

################################################################################################################################
#max of sub array
from functools import reduce
l = [3,5,6,2,3,8,9,2,1]

def max_of_sub_array(arr,size):
    new = []
    for i in range(0,len(arr),size):
        new.append(arr[i:i+size])
    print(new)
    return reduce(lambda x,y:x if sum(x) >sum(y) else y,new)

#print(max_of_sub_array(l,3))

################################################################################################################################
#palindrome or not
#first way

s = 'malayalam'

def palen(s):
    if s == s[::-1]:
        return True
    else:
        return False
#print(palen(s))

#second way

first =0
last = len(s)-1
status = False
while first < last:
    if s[first] == s[last]:
        first +=1
        last -=1
        status = True
    else:
        status = False
        break
#print(status)

################################################################################################################################
#highest 1 and 2 
#lowest 1 and 2

l = [45,12, 2, 41, 31, 10, 8, 6, 4]

highest1 = l[0]
highest2 = None

low1 = l[0]
low2 = None
for each in l[1:]:
    if each > highest1:
        highest2 = highest1
        highest1 = each
    elif highest2 ==None or each > highest2:
        highest2 = each

    if each < low1:
        low2 = low1
        low1 = each
    elif low2 ==None or each < low2:
        low2 = each

# print('highest1',highest1)
# print('highest2',highest2)

# print('low1',low1)
# print('low2',low2)

################################################################################################################################

#sum of triplets

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
target = 10 

for i in range(len(arr)):
    left = i+1
    right = len(arr)-1
    current = arr[0]
    while left < right:
        if current+arr[left]+arr[right] == target:
            #print(current, arr[left], arr[right])
            left+=1
            right -=1
        elif current+arr[left]+arr[right] < target:
            left+=1
        else:
            right-=1


################################################################################################################################
#sequense

s="aabbbbbddeeeccbdaaa"


cur =s[0]
count=1
for i in s[1:]:
    if cur == i:
        count+=1
    else:
        if count%2:
            #print(cur*count)
            pass
        cur = i
        count =1
if count%2:
    #print(cur*count)
    pass
################################################################################################################################

num = 365
s = ''
while num >0:
    d = num%10
    s+=str(d)
    num = num//10
#print(int(s))

################################################################################################################################