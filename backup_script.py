#imports
import os,shutil,datetime,filecmp,time

class dircmp(filecmp.dircmp): # Class to compare 2 directories and the files in them
    def phase3(self):#Finding differences between common files
        fcomp = filecmp.cmpfiles(self.left, self.right, self.common_files,
                                 shallow=False) #shallow=False so we check the content of the files aswell
        self.same_files, self.diff_files, self.funny_files = fcomp

#Function that compares 2 directories tree content
#Return true if its the same or false if they're different
def backup_check(folder1,folder2):
    comp=dircmp(folder1,folder2)
    if (comp.left_only or comp.right_only or comp.diff_files or comp.funny_files):
        return False
    for subdir in comp.common_dirs:
        if not backup_check(os.path.join(folder1, subdir), os.path.join(folder2, subdir)):
            return False
    return True

#Function that checks if the folder already exists, removes the existing backup and creates a new updated backup
#I was having issues where it wouldn't let me overwrite the files so i had to delete the old backup first
def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)
#--------------------------------------MAIN PART----------------------------------------------------
#--------------------INITIALIZING BACKUP--------------------
print("-----------------------------------Welcome-----------------------------------")
valid_interval_time_flag=False
while valid_interval_time_flag==False:
    interval_time = input("\nHow often would you like to perform a backup (in seconds)\n")
    if interval_time.isnumeric():#checking if the input is valid INTEGER
        interval_time=int(interval_time)
        if interval_time>0:#checking if the time value is not negative
            print("Your interval time has been set to :",interval_time)
            valid_interval_time_flag=True
    else:
        print("Entered Value is Not an Integer. Please enter a valid value.")
loop_time=int(interval_time) #casting the read value into an integer 
#-------------------ORIGINAL FOLDER PATH-------------------
folder_check=False
while folder_check==False: #loop that checks that given original folder exists 
    original_folder_path=input("\nPlease provide the path to the original folder\n")
    folder_check=os.path.exists(original_folder_path)
    if folder_check==False:
        print("Unable to locate directory. Please make sure you're entering a valid path to an existing directory")
    else:
        print("Original Folder Path set to: ",original_folder_path)

#-------------------BACKUP FOLDER PATH-------------------
folder_check=True
while folder_check==True: #loop that checks that given original folder doesn't exist
    backup_folder_path=input("\nPlease provide the path to the new backup folder\n")
    folder_check=os.path.exists(backup_folder_path)
    if folder_check==False:
        print("Original Folder Path set to: ",backup_folder_path)
        folder_check==False
    else:
         print("Directory already exists! Please make sure you're NOT entering a path to an existing directory")
#-------------------INITIAL BACKUP-------------------
ts=datetime.datetime.now()
folder_check=False
while folder_check==False: #loop that checks that given original folder exists 
    log_file_path=input("\nPlease provide the folder path to the new log file location\n")
    folder_check=os.path.exists(log_file_path)
    if folder_check==False:
         print("Unable to locate directory. Please make sure you're entering a valid path to an existing directory")
    else:
        print("Log File Folder Path set to: ",log_file_path)


f= open(log_file_path+"/backup_log_file.txt", "w") #Opening the log file to write on it. If it doesnt already exist in the folder it will create a new file.
print("Initializing Backup... Time:", ts)#console message
tsStr = ts.strftime("%d-%b-%Y (%H:%M:%S.%f)") #Cant pass a datetime type of value into a file so i had to convert it into a string5
f.write("Initializing Backup... Time:"+ tsStr)#log file message
f.close()
shutil.copytree(original_folder_path,backup_folder_path)#Updating the back up folder

#Checking for Differences every X amount of seconds(User's Choice)
#-------------------CONTINUOUS BACKUP-------------------
while True:
    if backup_check(original_folder_path,backup_folder_path)==False: #if there's differences in the folders then it creates a new backup
        copy_and_overwrite(original_folder_path,backup_folder_path)
        ts=datetime.datetime.now()
        tsStr = ts.strftime("%d-%b-%Y (%H:%M:%S.%f)") 
        f= open("backup_log_file.txt", "a") #adds line to existing file
        f.write("\n---DIFFERENT FILES DETECTED--- Backup Complete Time:"+tsStr )
        f.close()
        print("---DIFFERENT FILES DETECTED--- Backup Complete Time:",ts )
    time.sleep(loop_time) #last line of the while loop that defines how much time it will take until the next loop




