#!/usr/bin/env python3
"""
Professional Calculator App - Example for Claude App Launcher
A beautifully designed GUI calculator with proper layout
"""

import tkinter as tk
from tkinter import ttk


class ProfessionalCalculator:
    """A professional-looking calculator with proper UX design"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        self.current = ""
        self.operation = None
        self.first_number = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create modern calculator interface"""
        # Display frame
        display_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
        display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Display
        self.display = tk.Entry(
            display_frame,
            font=("Segoe UI", 28, "bold"),
            justify="right",
            bd=0,
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        self.display.pack(fill=tk.BOTH)
        self.display.insert(0, "0")
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg='#f0f0f0', padx=10, pady=10)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button configuration: (text, row, col, rowspan, colspan, style)
        buttons = [
            ('C', 0, 0, 1, 2, 'danger'),      # Clear - spans 2 columns
            ('←', 0, 2, 1, 1, 'warning'),     # Backspace
            ('÷', 0, 3, 1, 1, 'operator'),    # Divide
            
            ('7', 1, 0, 1, 1, 'number'),
            ('8', 1, 1, 1, 1, 'number'),
            ('9', 1, 2, 1, 1, 'number'),
            ('×', 1, 3, 1, 1, 'operator'),    # Multiply
            
            ('4', 2, 0, 1, 1, 'number'),
            ('5', 2, 1, 1, 1, 'number'),
            ('6', 2, 2, 1, 1, 'number'),
            ('-', 2, 3, 1, 1, 'operator'),    # Subtract
            
            ('1', 3, 0, 1, 1, 'number'),
            ('2', 3, 1, 1, 1, 'number'),
            ('3', 3, 2, 1, 1, 'number'),
            ('+', 3, 3, 1, 1, 'operator'),    # Add
            
            ('0', 4, 0, 1, 2, 'number'),      # Zero - spans 2 columns
            ('.', 4, 2, 1, 1, 'number'),
            ('=', 4, 3, 1, 1, 'equals'),      # Equals
        ]
        
        # Button colors
        colors = {
            'number': {'bg': '#ffffff', 'fg': '#2c3e50', 'hover': '#ecf0f1'},
            'operator': {'bg': '#3498db', 'fg': '#ffffff', 'hover': '#2980b9'},
            'equals': {'bg': '#2ecc71', 'fg': '#ffffff', 'hover': '#27ae60'},
            'danger': {'bg': '#e74c3c', 'fg': '#ffffff', 'hover': '#c0392b'},
            'warning': {'bg': '#f39c12', 'fg': '#ffffff', 'hover': '#e67e22'}
        }
        
        # Create buttons
        for (text, row, col, rowspan, colspan, style) in buttons:
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=("Segoe UI", 18, "bold"),
                command=lambda t=text: self.button_click(t),
                bg=colors[style]['bg'],
                fg=colors[style]['fg'],
                activebackground=colors[style]['hover'],
                activeforeground=colors[style]['fg'],
                bd=0,
                cursor='hand2',
                relief=tk.FLAT
            )
            
            btn.grid(
                row=row, 
                column=col, 
                rowspan=rowspan,
                columnspan=colspan,
                sticky="nsew",
                padx=5,
                pady=5
            )
            
            # Hover effects
            def on_enter(e, button=btn, hover_color=colors[style]['hover']):
                button.configure(bg=hover_color)
            
            def on_leave(e, button=btn, normal_color=colors[style]['bg']):
                button.configure(bg=normal_color)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        # Configure grid weights for proper sizing
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1, minsize=70)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1, minsize=80)
    
    def button_click(self, value):
        """Handle button clicks"""
        if value.isdigit() or value == '.':
            # Number or decimal point
            if self.current == "" or self.current == "0":
                self.current = value if value != '.' else "0."
            else:
                # Prevent multiple decimal points
                if value == '.' and '.' in self.current:
                    return
                self.current += value
            
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current)
        
        elif value in ['+', '-', '×', '÷']:
            # Operator
            if self.current:
                self.first_number = float(self.current)
                self.operation = value
                self.current = ""
                self.display.delete(0, tk.END)
        
        elif value == '=':
            # Calculate result
            if self.first_number is not None and self.current and self.operation:
                second_number = float(self.current)
                result = self.calculate(self.first_number, second_number, self.operation)
                
                self.display.delete(0, tk.END)
                
                if result == "Error":
                    self.display.insert(0, result)
                    self.current = ""
                else:
                    # Format result nicely
                    if isinstance(result, float) and result.is_integer():
                        result = int(result)
                    
                    self.display.insert(0, str(result))
                    self.current = str(result)
                
                self.first_number = None
                self.operation = None
        
        elif value == 'C':
            # Clear everything
            self.current = ""
            self.first_number = None
            self.operation = None
            self.display.delete(0, tk.END)
            self.display.insert(0, "0")
        
        elif value == '←':
            # Backspace
            if self.current:
                self.current = self.current[:-1]
                self.display.delete(0, tk.END)
                if self.current:
                    self.display.insert(0, self.current)
                else:
                    self.display.insert(0, "0")
    
    def calculate(self, first, second, op):
        """Perform calculation"""
        try:
            if op == '+':
                return first + second
            elif op == '-':
                return first - second
            elif op == '×':
                return first * second
            elif op == '÷':
                if second != 0:
                    return first / second
                else:
                    return "Error"
        except:
            return "Error"


def main():
    """Entry point"""
    root = tk.Tk()
    app = ProfessionalCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
