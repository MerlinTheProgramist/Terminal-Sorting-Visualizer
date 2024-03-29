# Terminal Sorting Visualizer
A python script for visualizing sorting algoritms in terminal.  
It uses curses, that is build in to python3, so you dont need to install anything.

![caption](https://i.imgur.com/gbmtdZk.gif)
## Run defaults by 
`python3 ./graph_drawer.py`

## Test your favorite Sorting Algorithms!
Create new python script inside `/Algorithms` folder.  
Name your main function `sort`, the visualizer will call that and it will parse the shuffled array as an argument.  
Every step of your algorithm must [yield](https://wiki.python.org/moin/Generators) with the current state of the array to visualize it in the terminal.  

## Example
Bubble Sort
```py
def sort(arr:List[int]) -> Generator[List[int]]:
    n = len(arr)
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
```
## [optional] `--help`
`-a 1 3 4` choice which algorithms to compare  
`-t` specify frametime of Visualizer in seconds

