
# Importation of the relevant modules. All these are default modules except tablulate
# To import it, first install it using pip. 
import collections
from tabulate import tabulate
import collections
import sys

# Getting rid of the tracebacks if an exception is raised.
sys.tracebacklimit = -1

# This stores all the revelant information of all the processes
track = collections.defaultdict(lambda : [0,0,0,0,0])
track1 = collections.defaultdict(lambda : [0,0,0,0,0,0])  # This has an extra index for schedules where a flag helps

# This function helps to take the arrival and burst times of the processes from the user
def getInput(track):
    
    processes = input("Enter the processes in the form: arrival:burst,arrival:burst etc: Eg 1:2,3:4 etc \nNow enter the processes: ")
    print()

    if len(processes) == 0:
        raise Exception("You must enter a list of processes.")

    # Get both the arrival and burst times of each process, run a check on them and add the 
    # information to the information store declared above
    # After this, sort the store according to the arrival times of the processes
    processes = processes.split(",")
    for i in range(1, len(processes) + 1):
        try :
            arrivalTime, burstTime = processes[i - 1].split(":")
            try:
                track[i][0], track[i][1] = int(arrivalTime), int(burstTime)
                sorted_proceses = sorted(track.items(), key=lambda x:x[1][0])
            except:
                raise Exception("Invalid Input format. Try again")
        except:
            raise Exception("Invalid Input format. Try again")
    return sorted_proceses

def get_average_turnaround_waiting(track):
    waiting, turnaround = 0 , 0
    
    for i in range(len(track)):
        waiting += track[i][1][3]
        turnaround += track[i][1][4]

    print(f"\nAverage Waiting Time is {round(waiting / len(track), 2)}s.")
    print(f"Average Turn Around Time is {round(turnaround / len(track), 2)}s.\n")

def tabulate_data(data):
    headers = ["Process", "Arrival Time", "Burst Time", "Response Time", "Waiting Time", "Turn Around Time"]
    tablefmt="mixed_grid"
    print(tabulate(data, headers, tablefmt))

# This function simlates the first-in-first-out scheduling algorithm.
def first_in_first_out():
    # Get all the processes in a sorted order by their arrival times
    sorted_proceses = getInput(track)

    # Get the response time of the first process scheduled to run. And set the execution run to zero
    response_time, finishTime = sorted_proceses[0][1][0], 0

    # Update both the response time, waiting time and the turnaround times of each process.
    for i  in range(len(sorted_proceses)):
        response_time = max(response_time, sorted_proceses[i][1][0])
        finishTime = response_time + sorted_proceses[i][1][1]
         
        #     response time             waiting time          
        sorted_proceses[i][1][2], sorted_proceses[i][1][3] = response_time, response_time - sorted_proceses[i][1][0]

        #     turnaround time
        sorted_proceses[i][1][-1] = sorted_proceses[i][1][1] + sorted_proceses[i][1][3]

        response_time = finishTime

    # Tabulating the results obtained in tabular form

    print("\nRESULTS FROM FIFO SDCHEDULING ALGORITHM")
    print("=======================================\n")
    result = [[str(x[0]), *x[1]] for x in  sorted_proceses]
    tabulate_data(result)

    # Getting the average waiting and turnaround times
    get_average_turnaround_waiting(sorted_proceses)

# This function helps to take the arrival and burst times of the processes from the user
def getInput(track):
    
    processes = input("Enter the processes in the form: arrival:burst,arrival:burst etc: Eg 1:2,3:4 etc \nNow enter the processes: ")
    print()

    if len(processes) == 0:
        raise Exception("You must enter a list of processes.")

    # Get both the arrival and burst times of each process, run a check on them and add the 
    # information to the information store declared above
    # After this, sort the store according to the arrival times of the processes
    processes = processes.split(",")
    for i in range(1, len(processes) + 1):
        try :
            arrivalTime, burstTime = processes[i - 1].split(":")
            try:
                track[i][0], track[i][1] = int(arrivalTime), int(burstTime)
                sorted_proceses = sorted(track.items(), key=lambda x:x[1][0])
            except:
                raise Exception("Invalid Input format. Try again")
        except:
            raise Exception("Invalid Input format. Try again")
    return sorted_proceses

def get_average_turnaround_waiting(track):
    waiting, turnaround = 0 , 0
    
    for i in range(len(track)):
        waiting += track[i][1][3]
        turnaround += track[i][1][4]

    print(f"\nAverage Waiting Time is {round(waiting / len(track), 2)}s.")
    print(f"Average Turn Around Time is {round(turnaround / len(track), 2)}s.\n")

def tabulate_data(data):
    headers = ["Process", "Arrival Time", "Burst Time", "Response Time", "Waiting Time", "Turn Around Time"]
    tablefmt="mixed_grid"
    print(tabulate(data, headers, tablefmt))

# This function simlates the shortest job first scheduling algorithm.
def shortest_job_first():
    # Get all the processes in a sorted order by their arrival times
    sorted_proceses = getInput(track1)

    # Declaring some helper variables
    time, queue, tempt, track = 0 , [] , [], 0

    # This loops continues till all the processes are processed / executed
    while len(queue) < len(sorted_proceses):
        # Get all processes which have arrived in the system at a given time
        for i in range(len(sorted_proceses)):
            if sorted_proceses[i][1][0] <= time and sorted_proceses[i][1][-1] == 0:  
                tempt.append(sorted_proceses[i])
                sorted_proceses[i][1][-1] = 1
                track = max(track, sorted_proceses[i][1][0] + sorted_proceses[i][1][1])
        
        # Sort all the arrived processes accoring to their burst times
        # And adjust the timer
        if len(tempt) > 0:
            tempt = sorted(tempt, key=lambda x:x[1][1])
            queue.extend(tempt)
            time += tempt[-1][1][1]
            tempt = []

        else:
            time += 1
        
    # Now update all the data in the information store, to get the scheduling information.
    response_time, finishTime = sorted_proceses[0][1][0], 0
    for i  in range(len(queue)):
        tempt = []
        queue[i][1][-1] = 2

        response_time = max(response_time, queue[i][1][0])
        finishTime = response_time + queue[i][1][1]

        #response time   waiting time
        queue[i][1][2], queue[i][1][3] = response_time, max(0, response_time - queue[i][1][0])
        
        # turnaround time
        queue[i][1][4] = queue[i][1][1] + queue[i][1][3]

        response_time = finishTime

        # Resorting the list of process which have not been processed yet, and arrived at different times
        # Sorting is done according to their burst times.
        for j in range(len(queue)):
            if queue[j][1][-1] == 1 and queue[j][1][1] < finishTime:
                tempt.append(queue[j])

        # Recreating the ready queue based on the sorted subset ready queue.
        if len(tempt) > 1:
            tempt = sorted(tempt, key=lambda x:x[1][1])
            queue = queue[0:i+1] + tempt + queue[(i + 1 )+ len(tempt) : ]

    # Prepare results for tabulation
    print(queue)

    result = [["Process " + str(x[0]), *x[1][0:-1]] for x in  queue]
    print("\nRESULTS FROM SJF SDCHEDULING ALGORITHM")
    print("=======================================\n")
    tabulate_data(result)

    # Gettin the average waiting and turnaround times
    get_average_turnaround_waiting(queue)
# This function simlates the round robin scheduling algorithm.
def round_robin():
    # Getting user input of the processes and time slice
    sorted_proceses = getInput(track1)
    time_slice = int(input("Enter the time slice: "))
    print()

    # Setting a timer - the arrival time of the first processes to run
    time_track = sorted_proceses[0][1][0]

    # ready_queue - all processes qualified to run given a time frame
    # Track of the number of processes done running
    # runtime - keeps track of the execution time
    ready_queue, completed, runtime = collections.deque() , 0 , 0

    # This helps store the arrival time, burst time and response time of processes before they are manipulated
    arrival_response_times = collections.defaultdict(lambda: [0,0,0])

    # Reform processes for tabulation
    to_aid_tabulation = []

    print("\nRESULTS FROM SJF SDCHEDULING ALGORITHM")
    print("=======================================\n")

    # This loop runs till processes are executed
    while completed < len(sorted_proceses):

        # Push ready processes to the processing queue
        for i in range(len(sorted_proceses)):
            if sorted_proceses[i][1][-1] < 1 and sorted_proceses[i][1][0] <= time_track:
                ready_queue.append(sorted_proceses[i])
                sorted_proceses[i][1][-1] = 1

        # Processing execution of processes start here
        if len(ready_queue) > 0:

            # Take the leftmost process, affect it by the time slice
            # Push at the back of the queue if it has a value greater than the time slice
            # Else it is popped for good, but printed out first
            process = ready_queue.popleft()
            if process[0] not in arrival_response_times:
                arrival_response_times[process[0]] = [process[1][0], process[1][1], time_track]
            burst_left = process[1][1] - time_slice
            time_track += time_slice
            runtime += time_slice if burst_left > 0 else process[1][1]

            # Here, the remaining value of the burst time is checked after deducting by the time slice
            if burst_left <= 0:
                process[1][-1] = time_track
                to_aid_tabulation.append(process)

                print(f"At time {time_track -1}s Process {process[0]} run for {process[1][1]} and Ended \n")
                time_track = time_track - time_slice + process[1][1]
                completed += 1
                turnaround = runtime - process[1][0]
                process[1][2] += (turnaround) 

            # Push process back to the queue and update the value of the burst time of the process.
            else:    
                process[1][1] = burst_left
                print(f"At time {time_track - 1}s Process {process[0]} run for {time_slice} \n")
                ready_queue.append(process)
        else:
            # If nothing is in the ready queue, append the first process of the original data structure that keeps track of all
            # the processes sorted by arrival times.
            sorted_proceses[completed][1][-1] = 2
            ready_queue.append(sorted_proceses[completed])

            time_track = sorted_proceses[completed][1][0]
            runtime = time_track

    # Recreating processes with relevant information
    for i in range(len(to_aid_tabulation)):
        #  burst time
        to_aid_tabulation[i][1][1] = arrival_response_times[to_aid_tabulation[i][0]][1]
        # response time
        to_aid_tabulation[i][1][2] = arrival_response_times[to_aid_tabulation[i][0]][2]
        # Turn around time
        to_aid_tabulation[i][1][4] = to_aid_tabulation[i][1][-1] - to_aid_tabulation[i][1][0]
        # Waiting time
        to_aid_tabulation[i][1][3] = to_aid_tabulation[i][1][4] - to_aid_tabulation[i][1][1]

    # Prepare results for tabulation
    print("\nTABLE SUMMARY FOR RESULTS ACCORDING TO WHICH PROCESS FINISHED FIRST")
    print("===================================================================\n")
    result = [["Process " + str(x[0]), *x[1][0:5]] for x in  to_aid_tabulation]
    tabulate_data(result)

    # Gettin the average waiting and turnaround times
    get_average_turnaround_waiting(to_aid_tabulation)

# This function simlates the round robin scheduling algorithm.
def shortest_job_completion():
    sorted_proceses = getInput(track1)

    # This keeps track of the time a process run either to completion or before an interrupt
    time_tracker = collections.defaultdict(int)

    time, completed, queue, prev = 0 , 0 , [], 0

     # This helps store the arrival time, burst time and response time of processes before they are manipulated
    arrival_response_times = collections.defaultdict(lambda: [0,0,0])

    print("\nRESULTS FROM SJCF SDCHEDULING ALGORITHM")
    print("=======================================\n")

    # Reform processes for tabulation
    to_aid_tabulation = []

    # This loop till all processes are done executing.
    while completed < len(sorted_proceses):

        # Push all processes which are ready to the processing array - used as queue here.
        for i in range(len(sorted_proceses)):
            if sorted_proceses[i][1][0] <= time and sorted_proceses[i][1][-1] == 0:  
                queue.append(sorted_proceses[i])
                sorted_proceses[i][1][-1] = 1

        # After a new job enters the queue, it is sorted to get the process with the least job to finish
        queue = sorted(queue, key=lambda x:x[1][1])

        if len(queue) > completed:
            # This keeps track of the time a process run either to completion or before an interrupt
            if len(time_tracker) == 0:
                prev = queue[completed][0]
            
            # If a process is done, add it to the tabulation array. The next process is then set for processing
            if queue[completed][1][1] <= 0:
                queue[completed][1][-1] = time
                to_aid_tabulation.append(queue[completed])
                print(f"Process {queue[completed][0]} runs for {time_tracker[prev]}s and Ended \n")
                del time_tracker[queue[completed][0]]
                completed += 1
            
            # If process is not done, keep processing it till it finishes or an interrpt occurs
            else:
                # Update the auxiliary dictionary that stores the relevant information of processes 
                # (arrival time, burst time, response time)
                if  queue[completed][0] not in arrival_response_times:
                    arrival_response_times[queue[completed][0]] = [queue[completed][0], queue[completed][1][1] , time]

                # If no interrupt happens, continue to run it and updating the total time it has continually processed for
                if queue[completed][0] == prev:
                    time_tracker[prev] += 1
                    queue[completed][1][1] -= 1
                else:
                    # If an interrupt occurs, output the time the previous process run for before the interrupt
                    print(f"Process {prev} runs for {time_tracker[prev]}s and got Interrupted by Process {queue[completed][0]}\n")

                    # Set the current running process to the interrupting process
                    del time_tracker[prev]
                    prev = queue[completed][0]
                    queue[completed][1][1] -= 1
                    time_tracker[prev] += 1

                # This initiates of the auxiliary data structure that keeps the relevant information of every process.
                if  queue[completed][0] not in arrival_response_times:
                    arrival_response_times[queue[completed][0]] = [queue[completed][0], queue[completed][1][1] , time]

        # If the ready queue is empty, continue to update the timer until a ready process enters the data structure
        time += 1

    # Recreating processes with relevant information
    for i in range(len(to_aid_tabulation)):
        #  burst time
        to_aid_tabulation[i][1][1] = arrival_response_times[to_aid_tabulation[i][0]][1]
        # response time
        to_aid_tabulation[i][1][2] = arrival_response_times[to_aid_tabulation[i][0]][2]
        # Turn around time
        to_aid_tabulation[i][1][4] = to_aid_tabulation[i][1][-1] - to_aid_tabulation[i][1][0]
        # Waiting time
        to_aid_tabulation[i][1][3] = max(0, to_aid_tabulation[i][1][4] - to_aid_tabulation[i][1][1] - 1)
        
        to_aid_tabulation[i][1][4] = to_aid_tabulation[i][1][4] if to_aid_tabulation[i][1][3] == 0 else to_aid_tabulation[i][1][4] - 1
        

    # Prepare results for tabulation
    print("\nTABLE SUMMARY FOR RESULTS ACCORDING TO WHICH PROCESS FINISHED FIRST")
    print("===================================================================\n")
    result = [["Process " + str(x[0]), *x[1][0:5]] for x in  to_aid_tabulation]
    tabulate_data(result)

    # Gettin the average waiting and turnaround times
    get_average_turnaround_waiting(to_aid_tabulation)
    print(arrival_response_times)

# This function helps put the entire algorithm together.
def main():
    print("\nBELOW REPRESENTS THE LIST OF SCHEDULING ALGORITHMS")
    print("===================================================\n")
    print("1 : FIRST IN FIRST OUT")
    print("2 : SHORTEST JOB FIRST")
    print("3 : SORTEST TIME TO COMPLETION FIRST")
    print("4 : ROUND ROBIN \n")

    algorithm = input("Enter the numeric mapping of the algorithm to use. Eg enter 1 for FIFO: ")

    if algorithm == "1":
        first_in_first_out()
    elif algorithm == "2":
        shortest_job_first()
    elif algorithm == "3":
        shortest_job_completion()
    elif algorithm == "4":
        round_robin()
    else:
        print("Invalid numeric mapping. Try again!")
main()

