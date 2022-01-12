import sys, os, signal, time, getpass, subprocess, re

######### FUNCTIONS #########

def re_search(t_compiled, t_in, t_print_true="", t_print_false=""):
    """Function will search provided string using provided regex rule, depending on the results it'll return True or False and optionally perform one print for each."""
    if re.search(t_compiled, t_in):
        if t_print_true != "":
            print(t_print_true)
        return True
    else:
        if t_print_false != "":
            print(t_print_false)
        return False


def append_exe(t_var, t_cfg):
    """Function will append .exe at the end of process name if it hasn't been done already. Change 'add_exe' to disable the function."""
    if not t_cfg:                       
        return t_var
    elif re.search(".exe", t_var):
        return t_var
    else:
        return t_var + ".exe"


def validate_closure(t_pid, t_var, t_search, t_adv, t_timeout=2):
    """Function will check if the process is closed and print results of that check."""
    t_error = None
    t_validate = subprocess.Popen(f"qprocess {t_pid}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
    t_read = t_validate.communicate(t_timeout)

    t_goelif = re_search(t_search, t_read[1], f"{t_var} (PID: {t_pid}) closed successfully.")
    if t_read[0] != "":
        if not t_adv:
            t_error = f"Failed to close {t_var} (PID: {t_pid})."
            print(t_error)
        if t_adv:
            t_error = f"Failed to close {t_var} (PID: {t_pid}). Make sure the app is running in Administrator Mode!"
            print(t_error)
    elif t_read[1] != "" and not t_goelif:
        t_error = f"An error occured: {t_read[1]}"
        print(t_error)
    return t_error


def pull_process_name(t_input):
    """Function will pull process name from CMD 'qprocess' using either manual input process name or PID. Additionally it'll convert returned tuple into a list."""
    t_pull = subprocess.Popen(f"qprocess {t_input}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
    t_tuple = t_pull.communicate(timeout=2)
    for x in t_tuple:
        qprocess_list.append(x)
    if t_tuple[0] == "":
        return None
    else:
        t_output = t_tuple[0]
        t_output = t_output.split()
        for x in t_output:
            x.replace(r"\n", "")
        return t_output[-1]                     # It's not perfect but it'll always be process name so no need to target 1st one


def pull_pid(t_cmd):
    """Function will attempt to pull PID from CMD output, if output is not present it'll return -1"""
    t_data = t_cmd.split()
    try:
        return t_data[7]
    except IndexError:
        return -1


def get_timestamp(t_friendly):
    """Function will pull the timestamp and return it in the desired format."""
    t_get = time.localtime()
    if t_friendly:
        t_raw = map(str, t_get)
        t_list = list(t_raw)
        return f"{t_list[0]}-{t_list[1].zfill(2)}-{t_list[2].zfill(2)} {t_list[3].zfill(2)}:{t_list[4].zfill(2)}:{t_list[5].zfill(2)}"
    return f"{t_get[0]}{t_get[1]}{t_get[2]}{t_get[3]}{t_get[4]}{t_get[5]}"


def raport_file(t_path=None):
    """Function creates a raport file and keeps it open for raport generator."""
    t_user = getpass.getuser()
    t_def_path = rf"C:\Users\{t_user}\Documents\ProcessKiller"
    if t_path == None:
        t_path = t_def_path
    t_timestamp = get_timestamp(False)
    t_failed = False
    while True:
        try:
            os.mkdir(t_path)
        except FileExistsError:
            pass
        
        try:
            t_log_file = open(rf"{t_path}\{t_timestamp}.txt", "a")
        except FileNotFoundError:
            t_log_file = open(rf"{t_path}\{t_timestamp}.txt", "x")
        except OSError:
            print(f"Couldn't open selected folder, saving in default folder {t_path}.")
            t_path = t_def_path
            if t_failed:
                break
            t_failed = True
            continue
        path.append(t_def_path)
        return t_log_file


def send_path(t_input):
    """Function will unpack path list and send string."""
    return t_input[0]


def generate_raport(gen_mode, t_full_list, t_method, t_id, t_proc_name, t_proc_pid, t_adv_mode, t_error, t_success, t_path=None):
    """Function will generate reports. Final report will be saved to the .txt file."""
    if gen_mode == "single":
        tt_method = None                            # Cries rly loud without it :(
        if t_method == "1":
            tt_method = "Name"
        elif t_method == "2":
            tt_method = "PID"

        if not t_adv_mode:
            t_kill_method = "Simple"
        else:
            t_kill_method = "Advanced"

        return {
            "id": t_id,
            "method": tt_method,
            "proc_pid": t_proc_pid,
            "proc_name": t_proc_name,
            "kill_method": t_kill_method,
            "success": t_success,
            "error": t_error,
        }

    elif gen_mode == "full":
        r_process = []

        rr_name = 0
        rr_pid = 0
        rr_simple = 0
        rr_advanced = 0
        rr_success = 0
        rr_error = 0

        r_runs = len(t_full_list)

        for x in t_full_list:
            if x["method"] == "Name":
                rr_name += 1
            elif x["method"] == "PID":
                rr_pid += 1

            if x["kill_method"] == "Simple":
                rr_simple += 1
            elif x["kill_method"] == "Advanced":
                rr_advanced += 1

            if x["success"]:
                rr_success += 1
                rr_success_str = "Closed"
                rr_error_str = "No errors!"

            else:
                rr_success_str = "Failed"
                rr_error_str = x["error"]
            
            if x["error"] != None:
                rr_error += 1
                

            r_process.append(f"""{rr_success_str} -- {x["proc_pid"]} -- {x["proc_name"]} -- {rr_error_str}""")

        try:
            rr_percentage = f"{rr_success / r_runs * 100} %"
        except ZeroDivisionError:
            rr_percentage = "0 %"

        r_file = raport_file()
        r_file.write(f"""Timestamp: {get_timestamp(True)}
Program ran {r_runs} time/s.
{rr_name} process/es targeted by name, {rr_pid} process/es targeted by PID.
Simple method (os.kill) used {rr_simple} time/s, advanced method (taskkill) used {rr_advanced} time/s.
{rr_success} process/es closed successfully, it's {rr_percentage} of all targeted. {rr_error} error/s occured.
""")
        for x in r_process:
            r_file.write(f"{x}\n")
        print(f"Raport generated in {send_path(t_path)}")
        return


########## PROGRAM ##########

add_exe = True   
timestamp_temp = []
raport_single = {
    "id": 0,
    "method": "",
    "proc_pid": 0,
    "proc_name": "",
    "kill_method": "",
    "success": False,
    "error": None,
}
raport_full = []
path = []

search = re.compile("No Process exists")
run_id = 0               
op_type = 9999

while op_type != 0:
    while True:
        op_type = str(input("1 to kill by name, 2 to kill by PID, 0 to exit. "))
        if op_type == "1" or op_type == "2":
            break

    while True:
        error = None
        success = False
        pid_list_raw = []
        pid_list = []
        passes = 0
        qprocess_list = []
        run_id =+ 1

        if op_type == "1":
            var = append_exe(input("Name of the process: "), add_exe)

        if op_type == "2":
            while True:
                try:
                    var = int(input("PID: "))
                    pid_list.append(var)
                    break
                except ValueError:
                    print("Input isn't a number.")
                    continue

        if op_type == "1":
            var_temp = var.replace(".exe", "")
            try:
                var_temp = int(var_temp)
                if var_temp in range(1, 100000):        # Checking for wrong mode selection
                    op_type = "2"
                    pid_list.append(var_temp)
                    var = var_temp
                    print("Changed killing mode to PID.")
            except ValueError:
                pass 

        process_name_cmd = pull_process_name(var)
        if process_name_cmd == None:                    # Edge case for op_type 1
            process_name_cmd = var
        # Since this error breaks it early from the loop, a raport must be generated here with dummy data
        if re_search(search, qprocess_list[1], f"Error, couldn't parse the process {process_name_cmd}"):
            error = f"Error, couldn't parse the process {process_name_cmd}"
            generate_raport("single", [], op_type, run_id, process_name_cmd, pull_pid(qprocess_list[0]), False, error, False)
            break

        if op_type == "1":
            pid_val = qprocess_list[0].split()
            for x in pid_val:
                if passes in range(3, 1024, 5):         # All PID positions in the tuple
                    pid_list_raw.append(x)
                passes += 1

            for x in pid_list_raw:
                try:
                    x = int(x)
                    pid_list.append(x)
                except ValueError:
                    continue                            # Get rid of table header
                print(f"Process found, PID: {x}")

        ran_adv_mode = False
        for x in pid_list:
            try:
                os.kill(x, signal.SIGTERM)
                time.sleep(1)
            except PermissionError:
                print("Failed. Initiating advanced mode ...")
                ran_adv_mode = True
                taskkill = subprocess.Popen(f"taskkill /PID {x} /F /T", stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")
                taskkill.communicate(timeout=2)         # Send output to limbo

            if op_type == "2":
                var = process_name_cmd

            error = validate_closure(x, var, search, ran_adv_mode)
            if error == None:
                success = True

            raport_full.append(generate_raport("single", [], op_type, run_id, var, x, ran_adv_mode, error, success))
            time.sleep(1)

        choice = input("Exit? (Y/N) ").lower()
        if choice == "y":
            op_type = 0
        break
generate_raport("full", raport_full, "", 0, "", 0, False, "", False, path)
input("Press ENTER to confirm and exit.")
sys.exit()