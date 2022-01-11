import sys, os, signal, time, getpass, subprocess

while True:
    while True:
        op_type = str(input("1 to kill by name, 2 to kill by PID "))
        if op_type == "1" or op_type == "2":
            break

    if op_type == "1":
        var = input("Name of the process: ")
        for x in os.popen(f"qprocess {var}"):
            y = x.split()
            pid = y[3]
            if pid == "PID":
                continue
            try:
                os.kill(int(pid), signal.SIGTERM)
            except PermissionError:
                print("Advanced Mode ...")
                pc = os.environ["COMPUTERNAME"]
                user = getpass.getuser()
                secret = input("Windows password required to proceed, close the program if you do not wish to enter your password.")
                if secret == "":
                    passw = ""
                else:
                    passw = f"/P {secret} "
                os.popen(f"taskkill /S {pc} /U {user} /P {secret} /PID {pid} /F /T")
            print(f"{var} closed successfully.")
        time.sleep(1)    

    if op_type == "2":
        while True:
            try:
                pid = int(input("PID: "))
            except:
                print("Input isn't a number.")
                continue

            process = None
            for x in os.popen(f"qprocess {pid}"):
                y = x.split()
                process = y[4]

            try:
                os.kill(int(pid), signal.SIGTERM)
            except PermissionError:
                pass
                # select = input("Closing the process failed. Would you like to use advanced mode? (Y/N) ").lower()
                # if select != "y":
                #     break
                # else:
                #     pc = os.environ["COMPUTERNAME"]
                #     print(f"PC name obtained {pc}")
                #     user = getpass.getuser()
                #     print(f"Username obtained {user}")
                #     secret = getpass.getpass()
                #     #input("Windows password required to proceed, close the program if you do not wish to enter your password.").encode()
                #     time.sleep(1)
                #     #if secret == "":
                #     #    passw = ""
                #     #os.popen(f"taskkill /S {pc} /U {user} /P {secret} /PID {pid} /F /T")
                #     killer = subprocess.Popen(["runas", f"/user:Administrator", f"""cmd /C "taskkill /PID {pid} /F /T" """], stdin=subprocess.PIPE)
                #     killer.stdin.write(b"admin\n")
                #     killer.stdin.flush()
                #     time.sleep(1)    
                # print(f"{process} closed successfully.")
                # choice = input("Would you like to enter another PID? (Y/N) ").lower()
                # if choice == "n":
                #     break

