import random

"""
Selection Sort 
"""
def __init__(arr):
    pass

def SelectionSort(arr):
    n=len(arr)
    for i in range(n):
        yield arr
        small_sub = i
        for j in range(i+1,n):
            if(arr[j]<arr[small_sub]):
                small_sub = j
        temp=arr[i]
        arr[i] = arr[small_sub]
        arr[small_sub] = temp
    yield arr

def InsertionSort(arr):
    n=len(arr)
    for i in range(n):
        j=i
        while j>0 and (arr[j]<arr[j-1]):
            temp = arr[j]
            arr[j] = arr[j-1]
            arr[j-1] = temp
            j-=1
        yield arr

def BubbleSort(arr):
    n=len(arr)
    fine = False
    while not fine:
        fine = True
        for i in range(n-1): 
            if arr[i] > arr[i+1]:
                temp = arr[i]
                arr[i] = arr[i+1]
                arr[i+1] = temp
                fine = False
        
            yield arr

def insertionSortRecursive(arr,n):
    # base case
    if n<=1:
        return
     
    # Sort first n-1 elements
    insertionSortRecursive(arr,n-1)
    '''Insert last element at its correct position
        in sorted array.'''
    last = arr[n-1]
    j = n-2
     
      # Move elements of arr[0..i-1], that are
      # greater than key, to one position ahead
      # of their current position
    while (j>=0 and arr[j]>last):
        arr[j+1] = arr[j]
        j = j-1
 
    arr[j+1]=last


import os
import importlib

if __name__ == "__main__":
    # print(f'{InsertionSort=}'.split('=')[0].split('.')[-1])
    folderN = "Algorithms"
    
    foundFiles = list(filter(lambda x: x.endswith('.py'),os.listdir(folderN)))
    print(foundFiles)

    gens = []

    for mod in foundFiles:
        module = importlib.import_module(f"{folderN}.{mod.strip('.py')}")
        gens.append(module.sort(arr))
        print(gens[-1])
    
    print(arr)
        


    # sorter = SelectionSort(arr,n)
    # print(next(sorter))