import tkinter as tk


#def main():
#    root = tk.Tk()
#    window1= AcquisitionSetupWindow(root, "Acquisition Setup", "500x100")
#    return None
    
#def main():
#    root = tk.Tk()
#    window1= AcquisitionSetupWindow(root, "Acquisition Setup", "500x100")
#    return None

class AcquisitionSetupWindow(tk.Frame):
    def __init__(self, root, title="Window 1", geometry="500x100"):
        super().__init__(root)
        self.root=root
        self.root.title(title)
        self.root.geometry(geometry)

        #draw a canvas to place widgets on
        self.canvas1 = tk.Canvas(self.root, width=400, height=150, relief = 'raised')
        self.canvas1.pack()

        #define labels for number of acquisitions and acquisition time 
        self.canvas1.create_text(100, 20, text="Number of Acquisitions")
        self.canvas1.create_text(300, 20, text="Acquisition Time (s)")
        
        #define entry boxes for number of acquisitions and acquisition time
        self.n_acquisitions = tk.StringVar()
        self.n_acquisitions_entry = tk.Entry(self.root, textvariable = self.n_acquisitions)
        self.n_acquisitions_entry.pack()
        self.n_acquisitions_entry_window = self.canvas1.create_window(100, 40, window=self.n_acquisitions_entry)


        self.time_acquisition = tk.StringVar()
        self.time_acquisition_entry = tk.Entry(self.root, textvariable = self.time_acquisition)
        self.time_acquisition_entry.pack()
        self.time_acquisition_entry_window = self.canvas1.create_window(300, 40, window=self.time_acquisition_entry)



        #define button for number of acquisitions and acquisition time 
        self.button_acquisitions_setup = tk.Button(self.root, text="Submit", command=self.get_acquisitions_params)
        
        #define window for button
        self.button_acquisitions_setup_window = self.canvas1.create_window(200, 80, window=self.button_acquisitions_setup)

        self.root.mainloop()



    def get_acquisitions_params(self): 
        #get value from entry box and save it in n_acquisitions variable
        #print("type of n_acquisitions_entry:", type(self.n_acquisitions_entry))
        self.n_acquisitions = int(self.n_acquisitions_entry.get())
        self.time_acquisition = float(self.time_acquisition_entry.get())
        #print("Number of acquisitions:", self.n_acquisitions)
        #print("Acquisition time:", self.time_acquisition)
        #params = [self.n_acquisitions, self.time_acquisition]
        self.root.destroy()
        


    def print_setup_params(self):
        print("Number of acquisitions:", self.n_acquisitions)
        print("Acquisition time:", self.time_acquisition)
        params= [self.n_acquisitions, self.time_acquisition]


    def return_params(self):
        return self.n_acquisitions, self.time_acquisition  

    def run(self):
        self.root.mainloop()
        return self.get_acquisitions_params()


    #define a function to combine multiple functions
    def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func




#if __name__ == "__main__":
#    main()