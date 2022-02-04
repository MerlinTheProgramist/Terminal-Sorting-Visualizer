def sort(arr):
    n=len(arr)
    for i in range(n):
        j=i
        while j>0 and (arr[j]<arr[j-1]):
            temp = arr[j]
            arr[j] = arr[j-1]
            arr[j-1] = temp
            j-=1
        yield arr