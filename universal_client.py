import subprocess

def run_script(script_name):
    try:
        subprocess.run(["python", script_name + ".py"], check=True)
    except FileNotFoundError:
        print(f"Script '{script_name}.py' not found.")
    except subprocess.CalledProcessError:
        print(f"Error running script '{script_name}.py'.")

def main():
    while True:
        print("Select an SPM Tool to execute:")
        print("1. AutoSplitter")
        print("2. Hide and Seek")
        print("3. Shared Stats")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            run_script("autosplitter")
        elif choice == "2":
            run_script("hide_client")
        elif choice == "3":
            run_script("ss_client")
        elif choice == "4":
            break
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()