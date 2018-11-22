import os,sys,time
import codecs
import threading
import getpass

session_over = True
paused = False

def handle_pause_resume():
    global session_over
    global paused
    while(not session_over):
        time.sleep(1)
        interrupt = getpass.getpass(prompt="") 
        if interrupt == "p":
            paused = True
        elif interrupt == "r":
            paused = False

def get_pretty_time(time_):
    local_time = time.asctime(time.localtime(time_))
    return local_time 

def start_work_analyzer():
    global session_over
    global paused

    #print login time
    login_time = time.time()
    print("login time: {}".format(get_pretty_time(login_time)))

    num_sessions = 0
    session_duration_in_mins = 25 
    pauseresume_actor = None

    while True:
        if pauseresume_actor:
            pauseresume_actor.join()

        continue_work = input("start a {} min session [type yes to start, no to end work] :".format(session_duration_in_mins))

        if continue_work == "yes":
            #print session start time
            session_start_time = time.time()
            print("session start time: {}".format(get_pretty_time(session_start_time)))
            
            session_duration_in_mins_ = session_duration_in_mins
            session_duration_in_secs = session_duration_in_mins_*60
            timer_value = ""
            
            #start pauseresume handler thread
            session_over = False
            pauseresume_actor = threading.Thread(target=handle_pause_resume)
            pauseresume_actor.start()
            
            #start the timer
            while session_duration_in_secs>=0:
                for i in range(len(timer_value)):
                    sys.stdout.write('\b')
                sys.stdout.flush()
                time.sleep(1)
                timer_value = "{}m:{}s ".format(session_duration_in_mins_,session_duration_in_secs%60)
                sys.stdout.write(timer_value)
                sys.stdout.flush()
                if (session_duration_in_secs % 60) == 0:
                    session_duration_in_mins_ -= 1
                session_duration_in_secs -= 1

                while(paused):
                    time.sleep(1)

            #print session end time
            session_over = True
            session_end_time = time.time()
            print("\nsession end time: {}".format(get_pretty_time(session_end_time)))

            num_sessions += 1

        elif continue_work == "no":
            #print logoff time
            logoff_time = time.time()
            print("logoff time: {}".format(get_pretty_time(logoff_time)))
            break

        else:
            print("invalid input, please type in yes or no")
    
    #print today's efficiency    
    total_time_in_office = (logoff_time - login_time)/60
    total_working_time = num_sessions * session_duration_in_mins
    print("total time in office: {}hr | total working time: {}hr | sessions completed: {}".format(total_time_in_office/60,total_working_time/60,num_sessions))
    efficiency = total_working_time/total_time_in_office * 100
    print("today's work efficiency percentage: {}".format(efficiency))

    with codecs.open("work_analyzer.db","a","utf-8") as db:
        unit = "{}:{}\n".format(login_time,efficiency)
        db.write(unit)

    return

def plot_work_efficiency():
    pass

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print("usage: work_analyzer.py [--login] [--plot_efficiency]")
        sys.exit(1)

    action = args[0]
    if action == "--login":
        start_work_analyzer()
    elif action == "--plot_efficiency":
        plot_work_efficiency()
    
    return

if __name__ == "__main__":
    main()