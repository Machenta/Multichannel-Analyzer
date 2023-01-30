import tkinter as tk
import tkinter.filedialog
from dataclasses import dataclass, field
import re
import os
import csv

@dataclass 
class file_data:
    name : str = None
    path : str = None
    file_count : int = 0
    regular_expression : str = "Analog_Data"
    current_dir : str = os.getcwd()
    default_savefile_folder_name : str = "DataAcquisition"
    default_savefile_dir : str = os.path.join(os.getcwd(), default_savefile_folder_name)
    all_files : dict = field(default_factory=dict)
    all_headers : dict = field(default_factory=dict)
    all_headless : dict = field(default_factory=dict)
    files_list : list = field(default_factory=list)


class FileSelectionWindow(tk.Frame):
    def __init__(self, 
                    root, 
                    title : str = "File Selection",
                    geometry : str = "450x500"):
        super().__init__(root)
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        self.files = file_data()

        #creating a frame to hold the file selection widgets
        self.file_frame = tk.Frame(self.root)
        self.file_frame.grid(row=0, column=0, sticky="nsew")
        self.file_frame.place(relx=0.5, rely=0.5, anchor="center")

        #add label for savefile directory
        self.savefile_directory_label = tk.Label(self.file_frame, text="Current Savefile Directory:")
        self.savefile_directory_label.grid(row=0, column=0, sticky="nsew")
        
        #label with current savefile directory
        self.savefile_directory = tk.Label(self.file_frame, text=self.files.current_dir)
        self.savefile_directory.grid(row=1, column=0, sticky="nsew")
        self.savefile_directory.config(wraplength=300)

        #create a filedialog button to select savefile directory
        self.savefile_directory_button = tk.Button(self.file_frame, text="Select Directory", command=self.open_file_dialog)
        self.savefile_directory_button.grid(row=0, column=1, sticky="nsew",rowspan=2)

        #create a label for the listbox
        self.file_list_label = tk.Label(self.file_frame, text="Files in Savefile Directory:")
        self.file_list_label.grid(row=3, column=0, sticky="nsew", columnspan=10)


        #create a scrollbar for the listbox
        self.scrollbar = tk.Scrollbar(self.file_frame, orient="vertical")

        #create a listbox to display the files in the savefile directory
        self.file_list = tk.Listbox(self.file_frame)
        self.file_list.config(width=50, height=20)
        self.file_list.grid(row=2, column=0, sticky="nsew", columnspan=10)
        
        #create a label for the common file name 
        self.files.regular_expression = tk.Label(self.file_frame, text="Common File Name:")
        self.files.regular_expression.grid(row=4, column=0, sticky="nsew")

        #create an entry for the common file name
        self.common_file_name_var = tk.StringVar()
        self.common_file_name = tk.Entry(self.file_frame, textvariable=self.common_file_name_var)
        self.common_file_name.insert(0, "Analog_Data")
        self.common_file_name.grid(row=4, column=1, sticky="nsew")
        self.common_file_name.bind("<Return>", self.get_regular_expression)

        #create  a label for total number of files
        self.total_files = tk.Label(self.file_frame, text="Total Files:")
        self.total_files.grid(row=5, column=0, sticky="nsew")

        #create a label for the total number of files
        self.total_files_count = tk.Label(self.file_frame, text=str(self.files.file_count))
        self.total_files_count.grid(row=5, column=1, sticky="nsew")

        #create a button to load the files to memory
        self.load_files_button = tk.Button(self.file_frame, text="Load Files", command=self.load_files)
        self.load_files_button.grid(row=6, column=0, sticky="nsew", columnspan=2)



        #create a label for the file extension

    def open_file_dialog(self):
        self.files.path = tkinter.filedialog.askdirectory()
        self.savefile_directory.config(text=self.files.path)
        #print(self.files.path)
        os.chdir(str(self.files.path))
        self.get_file_list()

    def get_file_list(self):
        self.files.files_list = os.listdir(self.files.path)
        self.file_list.delete(0, tk.END)
        #number of files in the directory
        self.files.file_count = len(self.files.files_list)
        #print("Number of files in directory: ", str(self.files.file_count))
        self.total_files_count.config(text=str(self.files.file_count))
        self.files.file_count = 0
        for file in self.files.files_list:
            if re.search(self.common_file_name.get(), file):
                self.file_list.insert(tk.END, file)
                self.files.file_count += 1
                print("Number of files in directory: ", self.files.file_count)
        self.total_files_count.config(text=self.files.file_count)  
        #print("files: ", str(self.files))

     

    def get_regular_expression(self, event=None):
        try:
            self.common_file_name_var = str(self.common_file_name.get())
            self.get_file_list()
        except:
            print("Please enter a valid number")  
            self.common_file_name_var = str(self.files.regular_expression)
            self.get_file_list()

    def load_files(self):  
        #print("file list: ", str(self.file_list))   
        #print file list
        file_index = 0
        #create a dictionary to hold all the files
        self.files.all_files = {}
        #create the necessary number of keys in the dictionary
        for index in range(self.files.file_count):
            self.files.all_files[index] = []
        #print("all files: ", str(self.files.all_files))
        #load the files into memory
        for file in self.files.files_list:
            self.load_file(file,file_index)
            file_index += 1

        self.files.all_headless = {}
        for index in range(self.files.file_count):
            self.files.all_headless[index] = []
        
        headless_index = 0
        for file in self.files.all_files:
            self.files.all_headless[headless_index]=self.remove_header(self.files.all_files[file])
            headless_index += 1
        #print("all files headless: ", str(self.files.all_headless))

        self.all_headers = {}
        for index in range(self.files.file_count):
            self.all_headers[index] = []

        header_index = 0
        for file in self.files.all_files:
            self.all_headers[header_index]=self.files.all_files[file][0]
            header_index += 1
        #print("all headers: ", str(self.all_headers))

    def load_file(self,file,index):
        #load the file into memory as a key in the all_files dictionary
        with open(file, "r") as f:
            for line in f:
                line = self.newline_remover(line)
                self.files.all_files[index].append(line)  
        #print("all files: ", str(self.files.all_files)) 
       

    def newline_remover(self, line):
        #remove newline characters from the end of the line
        return line.rstrip('\n')

    def remove_header(self, line):
        #remove the header from the line
        return line[1:]    

    def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func
            
        
if __name__ == "__main__":
    root = tk.Tk()
    FileSelectionWindow(root)
    root.mainloop()

