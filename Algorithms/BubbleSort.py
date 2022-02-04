def sort(arr):
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