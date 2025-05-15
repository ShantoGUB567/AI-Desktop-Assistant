import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from main import takeCommand, say, chat, ai
import datetime
import webbrowser
import os
from PIL import Image, ImageTk
import re

class AIAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ShanBot - AI Desktop Assistant")
        self.root.geometry("800x700")
        self.root.configure(bg="#1A1A1A")
        
        # Configure style
        style = ttk.Style()
        style.configure("Custom.TButton", 
                       padding=15,
                       font=("Helvetica", 12, "bold"),
                       background="#3498DB",
                       foreground="white")
        style.configure("Custom.TFrame", background="#1A1A1A")
        style.configure("Custom.TLabel", 
                       background="#1A1A1A",
                       foreground="#ECF0F1",
                       font=("Helvetica", 10))
        
        # Create main container with two columns
        main_container = ttk.Frame(root, padding="20", style="Custom.TFrame")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left column for chat
        left_column = ttk.Frame(main_container, style="Custom.TFrame")
        left_column.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 20))
        
        # Right column for robot image
        right_column = ttk.Frame(main_container, style="Custom.TFrame")
        right_column.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(left_column, 
                               text="ShanBot AI Assistant",
                               style="Custom.TLabel",
                               font=("Helvetica", 24, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Chat display area with custom styling
        self.chat_display = scrolledtext.ScrolledText(
            left_column,
            wrap=tk.WORD,
            width=50,
            height=25,
            font=("Helvetica", 11),
            bg="#34495E",
            fg="#ECF0F1",
            insertbackground="white"
        )
        self.chat_display.grid(row=1, column=0, pady=(0, 20), sticky="nsew")
        
        # Status label with modern styling
        self.status_label = ttk.Label(
            left_column,
            text="Status: Ready",
            style="Custom.TLabel",
            font=("Helvetica", 12)
        )
        self.status_label.grid(row=2, column=0, pady=(0, 20))
        
        # Modern listen button
        self.listen_button = tk.Button(
            left_column,
            text="🎤 Press Space or Click to Listen",
            command=self.toggle_listening,
            font=("Helvetica", 14, "bold"),
            bg="#3498DB",
            fg="white",
            activebackground="#2980B9",
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self.listen_button.grid(row=3, column=0, pady=(0, 20))
        
        # Configure right column for center alignment
        right_column.grid_rowconfigure(1, weight=1)  # Add weight to middle row
        right_column.grid_columnconfigure(0, weight=1)  # Center horizontally
        
        # Load and display robot image
        try:
            image = Image.open("robot.jpg")
            image = image.resize((300, 400), Image.Resampling.LANCZOS)
            self.robot_image = ImageTk.PhotoImage(image)
            robot_label = ttk.Label(right_column, image=self.robot_image, background="#1A1A1A")
            robot_label.grid(row=1, column=0)  # Place in middle row
        except Exception as e:
            print(f"Could not load robot image: {e}")
        
        # Configure grid weights
        main_container.columnconfigure(0, weight=3)  # Left column takes more space
        main_container.columnconfigure(1, weight=1)  # Right column takes less space
        left_column.columnconfigure(0, weight=1)
        left_column.rowconfigure(1, weight=1)
        
        # Initialize variables
        self.listening = False
        self.listening_thread = None
        
        # Bind space bar events
        self.root.bind("<space>", self.start_listening_space)
        self.root.bind("<KeyRelease-space>", self.stop_listening_space)
        
        # Welcome message
        self.update_chat("🤖 Welcome to ShanBot AI Assistant!")
        self.update_chat("Press Space or Click the button to start listening...")
        say("Hello I am your Assistant ShanBot")

    def clean_response(self, text):
        # Remove patterns like "ShanBot: (1/2)" or similar
        text = re.sub(r'ShanBot:\s*\([0-9]/[0-9]\)\s*', '', text)
        return text

    def update_chat(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"[{timestamp}] {message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.tag_add("all", "1.0", tk.END)

    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")

    def toggle_listening(self):
        if not self.listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.listen_button.config(
                text="🛑 Release to Stop",
                bg="#E74C3C",
                activebackground="#C0392B"
            )
            self.update_status("Listening...")
            self.listening_thread = threading.Thread(target=self.listen_loop)
            self.listening_thread.daemon = True
            self.listening_thread.start()

    def stop_listening(self):
        if self.listening:
            self.listening = False
            self.listen_button.config(
                text="🎤 Press Space or Click to Listen",
                bg="#3498DB",
                activebackground="#2980B9"
            )
            self.update_status("Ready")

    def start_listening_space(self, event):
        self.start_listening()

    def stop_listening_space(self, event):
        self.stop_listening()

    def handle_command(self, query):
        query_lower = query.lower()
        
        # Handle website commands
        sites = [
            ["youtube", "https://youtube.com"],
            ["wikipedia", "https://wikipedia.com"],
            ["facebook", "https://facebook.com"],
            ["google", "https://google.com"],
            ["keep", "https://keep.google.com"],
            ["email", "https://mail.google.com"],
        ]
        
        for site in sites:
            if f"open {site[0]}".lower() in query_lower:
                message = f"🌐 Opening {site[0]}..."
                self.update_chat(message)
                webbrowser.open(site[1])
                return True

        # Handle app commands
        apps = {
            "calculator": "start calc",
            "calendar": "start outlookcal:",
            "notepad": "start notepad",
            "snipping tool": "start snippingtool",
            "settings": "start ms-settings:",
        }
        
        for app, command in apps.items():
            if app in query_lower:
                message = f"📱 Opening {app}..."
                self.update_chat(message)
                os.system(command)
                return True

        # Handle music command
        if "open music" in query_lower or "play music" in query_lower:
            message = "🎵 Playing music..."
            self.update_chat(message)
            musicPath = "D:\GitHub\AI-Desktop-Assistant\music1.mp3"
            os.startfile(musicPath)
            return True

        # Handle VS Code command
        elif "vs code" in query_lower or "open code" in query_lower:
            message = "💻 Opening VS Code..."
            self.update_chat(message)
            vscode_path = r"C:\Users\alsha\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            os.startfile(vscode_path)
            return True

        # Handle browser command
        elif "browser" in query_lower or "open chrome" in query_lower:
            message = "🌐 Opening Chrome..."
            self.update_chat(message)
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            os.startfile(chrome_path)
            return True

        # Handle time command
        elif "the time" in query_lower:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            message = f"🕒 The time is {time}"
            self.update_chat(message)
            say(time)
            return True

        return False

    def listen_loop(self):
        while self.listening:
            query = takeCommand()
            if query:
                self.update_chat(f"🎤 You: {query}")
                
                # Handle exit command
                if "exit" in query.lower() or "close" in query.lower() or "stop" in query.lower():
                    self.update_chat("👋 Goodbye!")
                    say("Goodbye")
                    self.listening = False
                    self.root.quit()
                    return
                
                # Try to handle as a system command first
                if not self.handle_command(query):
                    # If not a system command, process with AI
                    self.update_status("Processing...")
                    if "using AI" in query.lower():
                        response = ai(query)
                    else:
                        response = chat(query)
                    
                    if response:
                        # Clean the response and update UI
                        clean_response = self.clean_response(response)
                        self.update_chat(f"🤖 ShanBot: {clean_response}")
                        # Only speak the clean response once
                        # say(clean_response)
                
                self.update_status("Listening...")

def main():
    root = tk.Tk()
    app = AIAssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 