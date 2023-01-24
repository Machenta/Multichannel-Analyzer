import tkinter as tk
import tkinter.filedialog
from dataclasses import dataclass, field
import re
import os
import csv

class FileSelectionWindow(tk.Frame):
    def __init__(self, 
                    root, 
                    title : str = "File Selection",
                    geometry : str = "800x600"):
        super().__init__(root)
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        self.current_dir : str = os.getcwd()
        self.file_name : str = None
        self.file_path : str = None
        self.file_count :int = 0
        self.regular_expression : str = "Analog_Data"
        self.all_files : dict = {}

        #creating a frame to hold the file selection widgets
        self.file_frame = tk.Frame(self.root)
        self.file_frame.grid(row=0, column=0, sticky="nsew")

        #add label for savefile directory
        self.savefile_directory_label = tk.Label(self.file_frame, text="Current Savefile Directory:")
        self.savefile_directory_label.grid(row=0, column=0, sticky="nsew")
        
        #label with current savefile directory
        self.savefile_directory = tk.Label(self.file_frame, text=self.current_dir)
        self.savefile_directory.grid(row=1, column=0, sticky="nsew")

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
        self.file_list.config(width=70, height=20)
        self.file_list.grid(row=2, column=0, sticky="nsew", columnspan=10)
        
        #create a label for the common file name 
        self.regular_expression = tk.Label(self.file_frame, text="Common File Name:")
        self.regular_expression.grid(row=4, column=0, sticky="nsew")

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
        self.total_files_count = tk.Label(self.file_frame, text=str (self.file_count))
        self.total_files_count.grid(row=5, column=1, sticky="nsew")

        #create a button to load the files to memory
        self.load_files_button = tk.Button(self.file_frame, text="Load Files", command=self.combine_funcs(self.get_regular_expression, self.get_file_list))
        self.load_files_button.grid(row=6, column=0, sticky="nsew", columnspan=2)



        #create a label for the file extension

    def open_file_dialog(self):
        self.file_path = tkinter.filedialog.askdirectory()
        self.savefile_directory.config(text=self.file_path)
        print(self.file_path)
        os.chdir(str(self.file_path))
        self.get_file_list()

    def get_file_list(self):
        files = os.listdir(self.file_path)
        self.file_list.delete(0, tk.END)
        #number of files in the directory
        self.file_count = len(files)
        print("Number of files in directory: ", str(self.file_count))
        self.total_files_count.config(text=str(self.file_count))
        self.file_count = 0
        for file in files:
            if re.search(self.common_file_name.get(), file):
                self.file_list.insert(tk.END, file)
                self.file_count += 1
                print("Number of files in directory: ", self.file_count)
        self.total_files_count.config(text=self.file_count)  

        for file in self.file_list: 
            self.all_files[file] = []      
     

    def get_regular_expression(self, event=None):
        try:
            self.common_file_name_var = str(self.common_file_name.get())
            self.get_file_list()
        except:
            print("Please enter a valid number")  
            self.common_file_name_var = str(self.regular_expression)
            self.get_file_list()

    def load_files(self):
        #create a dictionary to hold the files
        self.all_files = {}            
        for file in self.file_list: 
            self.all_files[file] = []
            with open(file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    self.all_files[file].append(row)

    def load_file(self):
        #create a dictionary to hold the files
        self.all_files = {}            
        for file in self.file_list: 
            self.all_files[file] = []
            with open(file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    self.all_files[file].append(row)        

    def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func
            
        
if __name__ == "__main__":
    root = tk.Tk()
    FileSelectionWindow(root)
    root.mainloop()