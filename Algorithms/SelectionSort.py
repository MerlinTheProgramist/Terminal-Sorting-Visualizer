def sort(arr):
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