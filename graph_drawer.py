import curses
import random
import time
import asyncio
import argparse

import os
import importlib

TIME_STEP = 0
ARR_LENGTH = 50

IS_CONTROL = False

sc,gh,gw = 0,0,0


green,yellow,red,cyan = 0,0,0,0

class GraphWindow():
    def __init__(self,n, name):
        global gw,gh
    
        self.last_arr = None

        self.col_w = min(max(int(gw/n)-1, 1),5)
        self.win = curses.newpad(gh-5, n*(self.col_w+1)+2)#curses.newwin(gh-5, gw, 5, 0)
        self.mh = gh-6
        self.mw = gw
        
        self.max_col = n
        
        self.info = InfoWindow(name)

        self.win.erase()

    async def update_graph(self,arr,orginal_arr,step_time=0):
        global gw,gh

        self.win.erase()
        self.win.border(0)
        correct = 0
        for i,val in zip(range(len(arr)),arr):
            if orginal_arr[i]==val: 
                correct+=1
                await self.drawStep(val, i, 3)
            else:
                await self.drawStep(val, i,1)

        self.win.refresh(0,0, 5,0, gh-1,gw-1)
        self.last_arr = arr

        self.info.update(step_time,correct,len(arr))
        

    #draws one column of the graph    
    async def drawStep(self,h,index, colour):
        height = min(max( self.mh - int(h/self.max_col*self.mh), 2),self.mh - 1)
        # draw columns
        try:
            for y in range(height,self.mh): #self.mh - self.col_h_mult * h,self.mh):
                self.win.addstr(y,  index*(self.col_w+1)+1,  "."*self.col_w,  curses.color_pair(colour))
        except:pass
        # print labels
        centr = int(self.col_w/2-len(str(h)))
        try:
            self.win.addstr(height-1,  index*(self.col_w+1)+1+centr,  str(h),curses.color_pair(2))
        except:pass


class InfoWindow():
    def __init__(self, name):
        global gh,gw
        self.name = name
        self.win = curses.newwin(6, gw, 0, 0)
        
        self.step_count = 0
        
        self.win.erase()

    def update(self,step_time, corr_len, all_len):
        self.win.erase()

        self.step_count+=1
        self.win.addstr(1,3, self.name)
        self.win.addstr(2,3, f"step {self.step_count}; last step took {step_time:.30f} sec;")
        self.win.addstr(3,3,str(corr_len)+" / "+str(all_len))
        self.win.border()
        self.win.refresh()

def show_results_msgbox(**info):
    w = 50
    win = curses.newwin(len(info)+3,w,int((gh-len(info))/2)-2,int((gw-w)/2))
    win.border(0)
    
    i = 1
    for key,val in info.items():
        win.addstr(i,1,f"{key}: {val}")
        i+=1
    win.addstr(i,1, "press Enter to continue")
    win.refresh()
    
    while sc.getch() != 10: #IF ENTER
        pass


def test_sorting(algorithm,n, name = "Yet another Sorting Algorithm"):
    global IS_CONTROL

    graph = GraphWindow(n, name) #reset graph window
    
    totalTime = 0

    arr = [i for i in range(1,n+1)]
    orginal_arr = arr.copy()
    random.shuffle(arr)
    sorter_generator = algorithm(arr)

    def sorter_process_instecting():
        curr_step = 0

        # Handle arrow movment in time
        
        event = sc.getch()
        while event!= curses.KEY_ENTER:
            event = sc.getch()
                # Left / Right
            if event == curses.KEY_LEFT:
                curr_step = min(len(steps_list)-1,max(0,curr_step-1))
                display_frame()
            elif event == curses.KEY_RIGHT:
                curr_step = min(len(steps_list)-1,max(0,curr_step+1))
                display_frame()

            def display_frame():   
                graph.info.step_count = curr_step
                asyncio.run( 
                    graph.update_graph(steps_list[curr_step][0],
                        orginal_arr, steps_list[curr_step][1])
                )

    steps_list = []        

    s_time = time.time()
    for step in sorter_generator:

        timePassed = time.time()-s_time
        totalTime+=timePassed

        asyncio.run( graph.update_graph(step, orginal_arr, timePassed))

        curses.napms(int(TIME_STEP*1000))
        steps_list.append([step.copy(), timePassed])

        s_time=time.time()
        
    show_results_msgbox(total_time=totalTime)

    if IS_CONTROL:
        sorter_process_instecting()

    return [name, graph.info.step_count, totalTime]

    



def wrap(scc):
        global sc,gh,gw, TIME_STEP, ARR_LENGTH
        sc = curses.initscr()
        gh, gw = sc.getmaxyx()

        global green,yellow,red,cyan, orginal_arr, TIME_STEP, SelectedAlgorithms

        if curses.has_colors():
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
            curses.init_pair(2, curses.COLOR_CYAN,-1)
            cyan = curses.color_pair(2)
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_GREEN)

        #START
        curses.noecho()
        curses.cbreak()
        scc.keypad(True)
        curses.curs_set(False)
        scc.timeout(20)
        
        results = [] # NAME, STEPS, TIME

        for alg in SelectedAlgorithms:
            results.append(test_sorting(alg[1], ARR_LENGTH, alg[0]))

SelectedAlgorithms = []


if __name__=="__main__":

    folderN = "Algorithms"
    foundFiles = list(filter(lambda x: x.endswith('.py'),os.listdir(folderN)))
    
    helpList = str('\n'.join([f"{i}. {a.strip('.py')}" for a,i in zip(foundFiles,range(1,1+len(foundFiles)))]))
    parser = argparse.ArgumentParser(description='Compare Sorting Algorithms')
    parser.add_argument('-a','--algorithms',type=int, nargs='*', required=False, choices=range(1,len(foundFiles)+1), 
        help=f"Algorithms you want to test and compare: {helpList}", 
        default=[i for i in range(1,1+len(foundFiles))])
    parser.add_argument('-dt','--delaytime',type=float,required=False,
        help='delay time of the visualization steps, has no influence on testing times',
        default=0.08)
    parser.add_argument('-l','--length',type=int,required=False,help="Length of the shuffled array that will be passes to all algorithms, default=50",default=50)

    parser.add_argument('-c','--control', action='store_true', default=False, required=False)

    args = parser.parse_args()

    TIME_STEP = args.delaytime
    ARR_LENGTH = args.length
    IS_CONTROL = args.control
    
    for aid in args.algorithms:
        mod = foundFiles[aid-1].strip('.py')
        try:
            module = importlib.import_module(f"{folderN}.{mod}")
            SelectedAlgorithms.append([str(mod),module.sort])
        except Exception as e:
            pass

    curses.wrapper(wrap)
    
    