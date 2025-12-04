"""
Primality Testing GUI
A graphical interface for running various primality tests
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
import time

# Add the uploads directory to the path to import the test modules
sys.path.insert(0, '/mnt/user-data/uploads')

# Import test functions
from AKS import aks
from BailliePSW import baillie_psw
from Fermat import FPT
from MilerRabin import mrTest

fontsize= 2; #multiplied by this


class PrimalityTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Primality Testing Suite")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10*fontsize))
        style.configure('Header.TLabel', font=('Arial', 14*fontsize, 'bold'), foreground='#2c3e50')
        style.configure('TButton', font=('Arial', 10*fontsize), padding=5)
        style.configure('Run.TButton', font=('Arial', 11*fontsize, 'bold'))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Primality Testing Suite", 
                               style='Header.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Test Configuration", padding="15")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Number input
        ttk.Label(input_frame, text="Number to test:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.number_entry = ttk.Entry(input_frame, font=('Arial', 11*fontsize))
        self.number_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        self.number_entry.insert(0, "97")
        
        # Test selection
        ttk.Label(input_frame, text="Select Test:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.test_var = tk.StringVar(value="AKS")
        test_frame = ttk.Frame(input_frame)
        test_frame.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        tests = [("AKS", "AKS"), ("Baillie-PSW", "BPSW"), 
                ("Fermat", "Fermat"), ("Miller-Rabin", "MR")]
        for i, (text, value) in enumerate(tests):
            ttk.Radiobutton(test_frame, text=text, variable=self.test_var, 
                           value=value).grid(row=0, column=i, padx=5)
        
        # Additional parameters frame
        self.params_frame = ttk.Frame(input_frame)
        self.params_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        self.params_frame.columnconfigure(1, weight=1)
        
        # Witness input (for Miller-Rabin)
        self.witness_label = ttk.Label(self.params_frame, text="Witness (a):")
        self.witness_entry = ttk.Entry(self.params_frame, font=('Arial', 11*fontsize))
        self.witness_entry.insert(0, "2")
        
        # Number of tests (for Fermat)
        self.tests_label = ttk.Label(self.params_frame, text="Number of tests:")
        self.tests_entry = ttk.Entry(self.params_frame, font=('Arial', 11*fontsize))
        self.tests_entry.insert(0, "10")
        
        # Bind test selection to update parameters
        self.test_var.trace('w', self.update_parameters)
        self.update_parameters()
        
        # Timing option
        self.timing_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="Show execution time", 
                       variable=self.timing_var).grid(row=3, column=0, columnspan=2, 
                                                      sticky=tk.W, pady=(10, 0))
        
        # Run button
        run_button = ttk.Button(main_frame, text="Run Test", command=self.run_test,
                               style='Run.TButton')
        run_button.grid(row=2, column=0, pady=10)
        
        # Clear button
        clear_button = ttk.Button(main_frame, text="Clear Output", command=self.clear_output)
        clear_button.grid(row=3, column=0, pady=(0, 10))
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        output_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD,
                                                     font=('Consolas', 11*fontsize),
                                                     height=15)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for colored output
        self.output_text.tag_config("prime", foreground="#27ae60", font=('Consolas', 10*fontsize, 'bold'))
        self.output_text.tag_config("composite", foreground="#e74c3c", font=('Consolas', 10*fontsize, 'bold'))
        self.output_text.tag_config("info", foreground="#2980b9")
        self.output_text.tag_config("time", foreground="#8e44ad", font=('Consolas', 10*fontsize, 'italic'))
        self.output_text.tag_config("error", foreground="#c0392b", font=('Consolas', 10*fontsize, 'bold'))
        
    def update_parameters(self, *args):
        """Update parameter inputs based on selected test"""
        # Hide all parameter widgets first
        self.witness_label.grid_remove()
        self.witness_entry.grid_remove()
        self.tests_label.grid_remove()
        self.tests_entry.grid_remove()
        
        test = self.test_var.get()
        
        if test == "MR":
            self.witness_label.grid(row=0, column=0, sticky=tk.W, pady=5)
            self.witness_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        elif test == "Fermat":
            self.tests_label.grid(row=0, column=0, sticky=tk.W, pady=5)
            self.tests_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
    
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
    
    def write_output(self, text, tag=None):
        """Write text to output area with optional tag"""
        self.output_text.insert(tk.END, text, tag)
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def run_test(self):
        """Execute the selected primality test"""
        try:
            # Get and validate input
            n = int(self.number_entry.get())
            test = self.test_var.get()
            
            if n < 2:
                messagebox.showerror("Invalid Input", "Please enter a number >= 2")
                return
            
            # Clear previous output
            self.clear_output()
            
            # Display test information
            self.write_output("=" * 60 + "\n")
            self.write_output(f"Testing: {n}\n", "info")
            self.write_output(f"Algorithm: {test}\n", "info")
            self.write_output("=" * 60 + "\n\n")
            
            # Run the appropriate test with timing
            start_time = time.time()
            result = None
            
            if test == "AKS":
                result = aks(n)
                self.write_output(f"Result: {result}\n")
                
            elif test == "BPSW":
                is_prime = baillie_psw(n)
                result = f"{n} is {'prime' if is_prime else 'composite'}"
                self.write_output(f"Result: {result}\n")
                
            elif test == "Fermat":
                num_tests = int(self.tests_entry.get())
                if num_tests > n - 3:
                    messagebox.showerror("Invalid Input", 
                                       f"Number of tests must be <= {n - 3}")
                    return
                
                is_composite = FPT(n, num_tests)
                result = f"{n} is {'composite' if is_composite else 'probably prime'}"
                self.write_output(f"Tests performed: {num_tests}\n", "info")
                self.write_output(f"Result: {result}\n")
                
            elif test == "MR":
                witness = int(self.witness_entry.get())
                if witness < 2 or witness >= n:
                    messagebox.showerror("Invalid Input", 
                                       f"Witness must be between 2 and {n-1}")
                    return
                
                # Capture the printed output
                test_passed = mrTest(n, witness)
                result = f"Test {'passed' if test_passed else 'failed, , number is composite'} for witness {witness}"
                self.write_output(f"Witness: {witness}\n", "info")
                self.write_output(f"Result: {result}\n")
            
            end_time = time.time()
            
            # Display timing if enabled
            if self.timing_var.get():
                elapsed = end_time - start_time
                self.write_output(f"\nExecution time: {elapsed:.6f} seconds\n", "time")
            
            # Color code the result
            if result and ("prime" in result.lower() or "passed" in result.lower()):
                if "composite" not in result.lower():
                    self.write_output("\n✓ ", "prime")
                    self.write_output("Number appears to be PRIME\n", "prime")
                else:
                    self.write_output("\n✗ ", "composite")
                    self.write_output("Number is COMPOSITE\n", "composite")
            elif result and "composite" in result.lower():
                self.write_output("\n✗ ", "composite")
                self.write_output("Number is COMPOSITE\n", "composite")
            
            self.write_output("\n" + "=" * 60 + "\n")
            
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid integers")
        except Exception as e:
            self.write_output(f"\nError: {str(e)}\n", "error")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


def main():
    root = tk.Tk()
    app = PrimalityTestGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()