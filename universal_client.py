import subprocess
import os

def run_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
    except FileNotFoundError:
        print(f"Script '{script_name}' not found.")
    except subprocess.CalledProcessError:
        print(f"Error running script '{script_name}', please report the error")

def main():
    while True:
        print("Select an SPM Tool to execute:")
        print("1. AutoSplitter")
        print("2. Hide and Seek")
        print("3. Shared Stats")
        print("4. Racing REL")
        print("5. Exit")

        choice = input("Enter your choice: ")
        # choice = "1" # debug

        if choice == "1":
            run_script("autosplitter.py")
        elif choice == "2":
            run_script("hide_client.py")
        elif choice == "3":
            run_script("ss_client.py")
        elif choice == "4":
            run_script(os.path.join("SPMRacingREL", "visualClient.py"))
        elif choice == "5":
            break
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()