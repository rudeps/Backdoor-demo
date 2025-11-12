import os
import glob

def get_cmd_files():
    cmd_files = glob.glob("*.cmd")
    return [f for f in cmd_files if os.path.isfile(f)]

def display_menu(cmd_files):
    print("\n" + "="*50)
    print("          SELECT CMD FILE TO RUN")
    print("="*50)
    
    for i, cmd_file in enumerate(cmd_files, 1):
        print(f"  {i}. {cmd_file}")
    
    print(f"  0. Exit")
    print("="*50)

def run_selected_cmd(cmd_file):
    print(f"\nRunning file: {cmd_file}")
    print("-" * 30)
    os.system(f'cmd /c "{cmd_file}"')

def main():
    if not os.path.exists("src"):
        print("Error: Run from project root folder!")
        input("Press Enter to exit...")
        return
    
    cmd_files = get_cmd_files()
    
    if not cmd_files:
        print("No .cmd files found in root folder!")
        input("Press Enter to exit...")
        return
    
    while True:
        display_menu(cmd_files)
        
        try:
            choice = input("\nSelect file number to run: ").strip()
            
            if choice == '0':
                print("Exiting program.")
                break
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(cmd_files):
                selected_file = cmd_files[choice_num - 1]
                run_selected_cmd(selected_file)
            else:
                print("Invalid choice! Try again.")
                
        except ValueError:
            print("Please enter a number!")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            break
        
        if choice != '0':
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()