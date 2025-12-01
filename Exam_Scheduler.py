"""
Project: Exam Scheduler.py
Author: Abdinoor Moallin
Date: November 2025

Description:
    This project implements an exam scheduling system using Python classes and recursive 
    backtracking. It allows users to input exam times and room availability from CSV files, 
    and generates a valid schedule if possible. 
    The program includes functionality to:
        - Represent times and time intervals
        - Check containment and disjointness of intervals
        - Parse CSV files for exams and rooms
        - Solve the scheduling problem using a recursive backtracking algorithm
        - Display the resulting schedule in a readable format

    The program also includes a tester function to automatically attempt scheduling 
    for multiple exam and room files, providing a quick summary of solvable and unsolvable cases.
"""

class Time:
    '''
    purpose:To create a Time object in the format of "hh:mm"
    '''
    def __init__(self,time_str):
        '''
        purpose:To initialize a Time object
        parameters:self,time_str
        return:None
        '''        
        split = time_str.split(":") 
        self._hour = split[0]
        self._minute = split[1]
        self._hour_i = int(split[0])
        self._minute_i = int(split[1])        

        
    def __str__(self):
        '''
        purpose:To return a str representation of a Time object
        parameters:self
        return:str
        '''        
        return f"{self._hour}:{self._minute}"
    
    
    def __eq__(self,other):
        '''
        purpose:To return if Time objects are equal to eachother
        parameters:self,other
        return:bool
        '''             
        if self._hour_i == other._hour_i and self._minute_i == other._minute_i:
            return True
        return False
    
    
    def __ne__(self,other):
        '''
        purpose:To return if one time object is not equal to another
        parameters:self,other
        return:bool
        '''             
        return self._hour_i != other._hour_i or self._minute_i != other._minute_i

    
    def __gt__(self,other):
        '''
        purpose:To return if one Time object is greater than another
        parameters:self,other
        return:bool
        '''             
        if self._hour_i > other._hour_i: #minutes can be '<','>', or '=='
            return True
        elif self._hour_i == other._hour_i:
            return self._minute_i > other._minute_i
        return False
    
    
    def __lt__(self,other):
        '''
        purpose:To return if one Time object is less than another
        parameters:self,other
        return:bool
        '''             
        if self._hour_i < other._hour_i: #minutes can be '<','>', or '=='
            return True
        elif self._hour_i == other._hour_i:
            return self._minute_i < other._minute_i
        return False    
    
    
    def __ge__(self,other):
        '''
        purpose:To return if one Time object is >= to another
        parameters:self,other
        return:bool
        '''             
        if self._hour_i > other._hour_i: #minutes can be '<','>', or '=='
            return True
        elif self._hour_i == other._hour_i:
            if self._minute_i == other._minute_i:
                return True
            else:
                return self._minute_i > other._minute_i
        return False    
    
    
    def __le__(self,other):
        '''
        purpose:To return if one Time object is <= to another
        parameters:self,other
        return:bool
        '''             
        if self._hour_i < other._hour_i: #minutes can be '<','>', or '=='
            return True
        elif self._hour_i == other._hour_i:
            if self._minute_i == other._minute_i:
                return True
            else:
                return self._minute_i < other._minute_i
        return False        
        
        
class TimeInterval:
    '''
    purpose:To create a Time Interval object in the format of "hh:mm"
    '''
    def __init__(self, start, end): 
        '''
        purpose:To initialize a TimeInterval object
        parameters:self, start, end
        return:None
        '''        
        self._start = start
        self._end = end
        
        
    def __str__(self):
        '''
        purpose:To return a str representation of a TimeInterval object
        parameters:self
        return:str
        '''        
        return f"{self._start}-{self._end}"     
        
        
    def contain(self,other):
        '''
        purpose:To return a bool on if an interval is contained in another
        parameters:self
        return:bool
        '''  
        if (self._start <= other._start) and (self._end >= other._end):
            #other is contained within self interval's start & end            
            return True
        return False    
        
        
    def disjoint(self,other):
        '''
        purpose:To return a bool on if an interval is disjoint from another
        parameters:self
        return:bool
        '''        
        if (self._end <= other._start) or (other._end <= self._start):
            #first case: self interval is before other interval
            #second case: other interval is before self interval
            return True
        return False

    
class Schedule:
    '''
    purpose:To create a Schedule object   
    '''
    def parse_files(self,exam_file,room_file):
        '''
        purpose:Helper function to parse through files and save info into lists
        parameters: exam_file, room_file
        return:exam_lst, room_lst
        ''' 
        exam_lst = []
        room_lst = []
        
        try:
            exam_file = open(exam_file,'r')
            for i in exam_file:
                new_i = i.split(',')
                #print(new_i)
                for j in new_i:  
                    j = j.strip()
                    exam_lst.append(j)
            exam_file.close()
            
        except FileNotFoundError:
            print(f"{exam_file} does not exist! Please try again.")
            
        try:
            room_file = open(room_file,'r')
            for i in room_file:
                new_i = i.split(',')
                #print(new_i)
                for j in new_i:  
                    j = j.strip()                    
                    room_lst.append(j)
            room_file.close()
            
        except FileNotFoundError:
            print(f"{room_file} does not exist! Please try again.")   

        return exam_lst,room_lst
        
        
    def __init__(self,exam_file,room_file): 
        '''
        purpose:To initialize a Schedule object
        parameters:self, exam_file, room_file
        return:None
        '''  
        self._exam_lst,self._room_lst = self.parse_files(exam_file,room_file)
        #exam_lst contains the exam name, start time, end time
        #room list contains the room name, opening time, closing time
        self._schedule = [] #empty list which will have lists added inside
        self._room_interval_lst = [] # room opening and closing times
        self._exam_interval_lst = [] # exam starting and ending times
      
        self._exam_names = [] #storing just the exam names
        
        for i in range(0,len(self._exam_lst),3): 
            class_taking_exam = self._exam_lst[i]
            start_time = self._exam_lst[i+1]
            end_time = self._exam_lst[i+2]
            self._exam_names.append(class_taking_exam)
            if '\n' in end_time:
                #if end time includes \n, remove \n
                end_time = end_time.replace('\n','')  
                
            exam_time_interval = TimeInterval(Time(start_time),Time(end_time))
            self._exam_interval_lst.append(exam_time_interval)
            
        for i in range(0,len(self._room_lst),3): 
            exam_room = self._room_lst[i]
            opening_time = self._room_lst[i+1]
            closing_time = self._room_lst[i+2]
            if '\n' in closing_time:
                #if end time includes \n, remove \n
                closing_time = closing_time.replace('\n','')            
            classroom_time_interval = TimeInterval(Time(opening_time),Time(closing_time))
            self._room_interval_lst.append(classroom_time_interval)
            self._schedule.append([]) 
            #^this will eventually append the room & its exams
            

    def print_schedule(self):
        '''
        purpose:To iterate over the list of lists, and print room name/exam time
        parameters:self
        return:None
        '''        
        for room_ind in range(0,len(self._room_interval_lst)): 
            room_name = self._room_lst[room_ind*3]
            room_interval = self._room_interval_lst[room_ind]
            print(f"Room {room_name}: {room_interval._start} - {room_interval._end} :")
            
            for exam_ind in self._schedule[room_ind]: #search for exams in respective rooms
                exam_name = self._exam_names[exam_ind] 
                exam_interval = self._exam_interval_lst[exam_ind]
                print(f"\t{exam_name}: {exam_interval._start} - {exam_interval._end}\n")
        return None
    
    
    def solve(self):  
        '''
        purpose:To solve exam scheduler problem
        parameters:self
        return:self._solver(0)
        '''  
        return self._solver(0) 
        #start from exam_0, goes through _solver, returns result
        #recuring on the exam number
        
    
    def _solver(self,exam_index):  
        '''
        purpose:Helper function that actually preforms recursive backtracking
        parameters:self,exam_index
        return:bool
        '''  
        if exam_index == len(self._exam_names): #base case
            return True #all exams have been assigned rooms
        else:
            exam_interval = self._exam_interval_lst[exam_index]

            for room_ind in range(len(self._room_interval_lst)):
                if self._room_interval_lst[room_ind].contain(exam_interval):
                    available = True
                    for prev_exam_index in self._schedule[room_ind]:
                        prev_exam_interval = self._exam_interval_lst[prev_exam_index]
                        #go through exams in a room, check disjoint
                        if exam_interval.disjoint(prev_exam_interval):
                            pass #we can add this exam
                        else:
                            available = False
                            break #can_place = False still
                        
                    if available == True:
                        self._schedule[room_ind].append(exam_index)
                        solution = self._solver(exam_index+1) 
                        #^add and recur 
                        if solution:
                            return True
                        
                        self._schedule[room_ind].pop()
        return False
            
       
def main():
    '''
    purpose:Prompts for name of exam (ex. exam_times_1.csv) 
                and room files (ex. room_avail_1.csv), and runs the script
    parameters:None
    return:None
    '''
    exam_file = input("Please enter the name of the exam file: ")
    room_file = input("Please enter the name of the room file: ")

    try:
        e_file = open(exam_file,'r')
        e_file.close()
        
    except FileNotFoundError:
        print(f"{exam_file} does not exist! Please try again.")
        
    try:
        r_file = open(room_file,'r')     
        r_file.close()
        
    except FileNotFoundError:
        print(f"{room_file} does not exist! Please try again.") 
        return
        
    exam_schedule = Schedule(exam_file,room_file)
    solvable = exam_schedule.solve() #bool
    if solvable == True:
        print(f"\nSchedule for exam file {exam_file} and room file {room_file}: \n")
        exam_schedule.print_schedule()
        
    else:
        print(f"No schedule is possible for exams in {exam_file} using room availability "
              f"in {room_file}")
        
    
def tester():
    '''
    purpose: Runs the solver for all files provided
    parameters: None
    return None
    '''
    print("-"*97)
    
    exam_list = ['exam_times_1.csv','exam_times_2.csv', 'exam_times_3.csv', 'exam_times_4.csv', 'exam_times_5.csv'] 
    room_list = ['room_avail_1.csv','room_avail_2.csv','room_avail_3.csv','room_avail_4.csv','room_avail_5.csv','room_avail_6.csv']
    
    for exams in exam_list:
        try:
            exam_open = open(exams,'r')
        except FileNotFoundError:
            print(f"File {exams} not found")
            
        for rooms in room_list:
            try:
                room_open = open(rooms,'r')
            except FileNotFoundError:
                print(f"File {rooms} not found")
                continue
            
            schedules = Schedule(exams,rooms)
            can_be_solved = schedules.solve()
            if can_be_solved == True:
                print(f"\nSchedule for exam file {exams} and room file {rooms}: \n")
                schedules.print_schedule()
                print("-"*97)
            else:
                print(f"\nNo schedule is possible for exams in {exams} using room availability "
                      f"in {rooms}")                    
    return None


if __name__ == "__main__":
    main()