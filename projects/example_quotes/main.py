#!/usr/bin/env python3
"""
Daily Quotes App - Example application for Claude App Launcher
Demonstrates dependency management with external packages
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json

try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    print("This app requires the 'requests' library.")
    print("The Claude App Launcher will install it automatically!")
    import sys
    sys.exit(1)


class QuotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Quotes")
        self.root.geometry("650x500")
        self.root.configure(bg='#f5f7fa')
        
        self.current_quote = None
        
        # Quote sources - dummyjson first since it's working reliably
        self.quote_sources = [
            {
                'name': 'dummyjson.com',
                'url': 'https://dummyjson.com/quotes/random',
                'parser': self.parse_dummyjson,
                'verify_ssl': True
            },
            {
                'name': 'quotable.io',
                'url': 'https://api.quotable.io/random',
                'parser': self.parse_quotable,
                'verify_ssl': False  # Has SSL cert issues currently
            }
        ]
        
        self.setup_ui()
        self.get_quote()
    
    def setup_ui(self):
        """Create the UI"""
        main_frame = tk.Frame(self.root, bg='#f5f7fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        title = tk.Label(
            main_frame,
            text="💭 Daily Inspiration",
            font=("Arial", 24, "bold"),
            bg='#f5f7fa',
            fg='#2c3e50'
        )
        title.pack(pady=(0, 30))
        
        quote_frame = tk.Frame(
            main_frame,
            bg='#ffffff',
            relief=tk.RAISED,
            borderwidth=2
        )
        quote_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        inner_frame = tk.Frame(quote_frame, bg='#ffffff')
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        self.quote_label = tk.Label(
            inner_frame,
            text="Click 'New Quote' to get started!",
            font=("Georgia", 16, "italic"),
            bg='#ffffff',
            fg='#2c3e50',
            wraplength=550,
            justify=tk.LEFT
        )
        self.quote_label.pack(pady=(20, 30))
        
        self.author_label = tk.Label(
            inner_frame,
            text="",
            font=("Arial", 12, "bold"),
            bg='#ffffff',
            fg='#7f8c8d'
        )
        self.author_label.pack(pady=(0, 20))
        
        self.source_label = tk.Label(
            inner_frame,
            text="",
            font=("Arial", 8),
            bg='#ffffff',
            fg='#95a5a6'
        )
        self.source_label.pack()
        
        button_frame = tk.Frame(main_frame, bg='#f5f7fa')
        button_frame.pack()
        
        new_quote_btn = tk.Button(
            button_frame,
            text="✨ New Quote",
            command=self.get_quote,
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='#ffffff',
            activebackground='#2980b9',
            activeforeground='#ffffff',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        new_quote_btn.pack(side=tk.LEFT, padx=5)
        
        copy_btn = tk.Button(
            button_frame,
            text="📋 Copy",
            command=self.copy_quote,
            font=("Arial", 12),
            bg='#2ecc71',
            fg='#ffffff',
            activebackground='#27ae60',
            activeforeground='#ffffff',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        info_label = tk.Label(
            main_frame,
            text="Free inspirational quotes",
            font=("Arial", 8),
            bg='#f5f7fa',
            fg='#95a5a6'
        )
        info_label.pack(pady=(15, 0))
    
    def parse_quotable(self, data):
        """Parse quotable.io response"""
        return {
            'quote': data.get('content', ''),
            'author': data.get('author', 'Unknown'),
            'source': 'quotable.io'
        }
    
    def parse_dummyjson(self, data):
        """Parse dummyjson.com response"""
        return {
            'quote': data.get('quote', ''),
            'author': data.get('author', 'Unknown'),
            'source': 'dummyjson.com'
        }
    
    def get_quote(self):
        """Fetch a random quote from available APIs"""
        self.quote_label.config(text="Loading quote...")
        self.author_label.config(text="")
        self.source_label.config(text="")
        self.root.update()
        
        # Try each source in order
        for source in self.quote_sources:
            try:
                response = requests.get(
                    source['url'],
                    timeout=5,
                    headers={'User-Agent': 'Mozilla/5.0'},
                    verify=source['verify_ssl']
                )
                
                if response.status_code == 200:
                    data = response.json()
                    parsed = source['parser'](data)
                    self.current_quote = parsed
                    self.display_quote(parsed)
                    return
                    
            except Exception:
                continue
        
        # If all sources failed
        self.show_error("Could not connect to quote service.\n\nPlease check your internet connection.")
    
    def display_quote(self, data):
        """Display the quote information"""
        quote_text = data.get('quote', 'No quote available')
        author = data.get('author', 'Unknown')
        source = data.get('source', '')
        
        self.quote_label.config(text=f'"{quote_text}"')
        self.author_label.config(text=f"— {author}")
        
        if source:
            self.source_label.config(text=f"via {source}")
    
    def copy_quote(self):
        """Copy the current quote to clipboard"""
        if self.current_quote:
            try:
                quote_text = self.current_quote.get('quote', '')
                author = self.current_quote.get('author', 'Unknown')
                
                full_text = f'"{quote_text}" — {author}'
                
                self.root.clipboard_clear()
                self.root.clipboard_append(full_text)
                self.root.update()
                
                messagebox.showinfo("Copied!", "Quote copied to clipboard!")
            
            except Exception as e:
                messagebox.showerror("Error", f"Could not copy quote: {str(e)}")
        else:
            messagebox.showwarning("No Quote", "Load a quote first!")
    
    def show_error(self, message):
        """Display an error message"""
        self.quote_label.config(
            text="Could not load quote",
            font=("Arial", 14)
        )
        self.author_label.config(text=message)


def main():
    """Entry point"""
    root = tk.Tk()
    app = QuotesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
