import tkinter as tk
from tkinter import ttk
import random
import math
import pygame
from PIL import Image, ImageTk
import os

class NewYearApp:
    def __init__(self, root):
        self.root = root
        self.root.title("New Year Celebration 2025!")
        self.root.geometry("800x600")
        
        # Initialize pygame mixer for music
        pygame.mixer.init()
        self.is_playing = False
        
        self.setup_colors()
        self.setup_styles()
        self.setup_frames()
        self.setup_variables()
        
        # Show welcome screen initially
        self.show_welcome()
        
    def setup_colors(self):
        self.colors = {
            'primary': '#6C63FF',
            'secondary': '#FF6584',
            'accent': '#4CAF50',
            'background': '#1A1A1A',
            'text': '#FFFFFF'
        }
        
        self.themes = {
            'default': self.colors.copy(),
            'cosmic': {
                'primary': '#8A2BE2',
                'secondary': '#FF69B4',
                'accent': '#00CED1',
                'background': '#0B0B2A',
                'text': '#FFFFFF'
            },
            'neon': {
                'primary': '#FF1493',
                'secondary': '#00FF00',
                'accent': '#FF4500',
                'background': '#000000',
                'text': '#FFFFFF'
            },
            'elegant': {
                'primary': '#FFD700',
                'secondary': '#FF69B4',
                'accent': '#4169E1',
                'background': '#1C1C1C',
                'text': '#FFFFFF'
            }
        }
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure(
            "Festive.TLabel",
            font=("Helvetica", 24, "bold"),
            foreground=self.colors['secondary']
        )
        self.style.configure(
            "Wish.TLabel",
            font=("Helvetica", 14),
            foreground=self.colors['primary']
        )
        
    def setup_frames(self):
        # Create main frames
        self.frames = {}
        for frame_name in ['welcome', 'celebration', 'settings']:
            self.frames[frame_name] = ttk.Frame(self.root, padding="20")
            
        self.setup_welcome_screen()
        self.setup_celebration_screen()
        self.setup_settings_screen()
        
    def setup_variables(self):
        self.firework_positions = []
        self.sparkles = []
        self.current_theme = 'default'
        self.animation_running = True
        
        self.wishes = [
            "May your year be filled with endless possibilities! ✨",
            "Here's to 365 new chances to make your dreams come true! 🌟",
            "Wishing you health, wealth, and happiness! 💖",
            "May this year bring you amazing adventures! 🎉",
            "Let your dreams take flight this year! 🚀"
        ]
        self.current_wish = 0
        
    def setup_welcome_screen(self):
        frame = self.frames['welcome']
        
        # Canvas for animations
        self.welcome_canvas = tk.Canvas(
            frame,
            width=800,
            height=600,
            bg=self.colors['background']
        )
        self.welcome_canvas.pack(fill="both", expand=True)
        
        # Welcome text
        welcome_text = self.welcome_canvas.create_text(
            400, 100,
            text="Welcome to New Year Celebrations!",
            font=("Helvetica", 28, "bold"),
            fill=self.colors['secondary']
        )
        
        # Name entry
        entry_frame = ttk.Frame(frame)
        entry_frame.place(relx=0.5, rely=0.4, anchor="center")
        
        ttk.Label(
            entry_frame,
            text="Enter your name:",
            style="Wish.TLabel"
        ).pack(pady=5)
        
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(
            entry_frame,
            textvariable=self.name_var,
            font=("Helvetica", 14),
            width=30
        )
        name_entry.pack(pady=10)
        
        # Buttons
        self.create_button(
            entry_frame,
            "Start Celebration!",
            self.start_celebration,
            'primary'
        ).pack(pady=5)
        
        self.create_button(
            entry_frame,
            "Settings",
            self.show_settings,
            'accent'
        ).pack(pady=5)
        
    def setup_celebration_screen(self):
        frame = self.frames['celebration']
        
        self.celebration_canvas = tk.Canvas(
            frame,
            width=800,
            height=600,
            bg=self.colors['background']
        )
        self.celebration_canvas.pack(fill="both", expand=True)
        
        # Header and wish labels
        self.header_label = self.celebration_canvas.create_text(
            400, 50,
            text="",
            font=("Helvetica", 28, "bold"),
            fill=self.colors['secondary']
        )
        
        self.wish_label = self.celebration_canvas.create_text(
            400, 500,
            text="",
            font=("Helvetica", 16),
            fill=self.colors['primary']
        )
        
        # Control buttons
        control_frame = ttk.Frame(frame)
        control_frame.pack(side="bottom", pady=10)
        
        for text, command in [
            ("Add Firework", self.add_manual_firework),
            ("Toggle Music", self.toggle_music),
            ("Back", self.show_welcome)
        ]:
            self.create_button(
                control_frame,
                text,
                command,
                'primary'
            ).pack(side="left", padx=5)
    
    def setup_settings_screen(self):
        frame = self.frames['settings']
        
        ttk.Label(
            frame,
            text="Settings",
            style="Festive.TLabel"
        ).pack(pady=20)
        
        # Theme selection
        theme_frame = ttk.LabelFrame(frame, text="Theme", padding=10)
        theme_frame.pack(pady=10, fill="x")
        
        self.theme_var = tk.StringVar(value='default')
        for theme in self.themes.keys():
            ttk.Radiobutton(
                theme_frame,
                text=theme.title(),
                value=theme,
                variable=self.theme_var,
                command=self.change_theme
            ).pack(pady=5)
        
        # Effect toggles
        self.effects = {
            'fireworks': tk.BooleanVar(value=True),
            'sparkles': tk.BooleanVar(value=True),
            'music': tk.BooleanVar(value=True)
        }
        
        effect_frame = ttk.LabelFrame(frame, text="Effects", padding=10)
        effect_frame.pack(pady=10, fill="x")
        
        for effect, var in self.effects.items():
            ttk.Checkbutton(
                effect_frame,
                text=effect.title(),
                variable=var
            ).pack(pady=5)
        
        self.create_button(
            frame,
            "Back",
            self.show_welcome,
            'primary'
        ).pack(pady=20)
    
    def create_button(self, parent, text, command, color_key):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Helvetica", 12),
            bg=self.colors[color_key],
            fg=self.colors['text'],
            relief="raised",
            padx=20,
            pady=10,
            activebackground=self.lighten_color(self.colors[color_key])
        )
    
    def create_firework(self, x, y):
        particles = []
        colors = [self.colors['primary'], self.colors['secondary'], self.colors['accent']]
        
        for i in range(20):
            angle = (i / 20) * 2 * math.pi
            speed = random.uniform(3, 6)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            
            particle = self.celebration_canvas.create_oval(
                x-2, y-2, x+2, y+2,
                fill=random.choice(colors),
                outline=""
            )
            
            particles.append({
                'id': particle,
                'dx': dx,
                'dy': dy,
                'life': 1.0
            })
        
        return particles
    
    def animate(self):
        if not self.animation_running:
            return
            
        # Update fireworks
        if self.effects['fireworks'].get():
            self.update_fireworks()
            
        # Create random fireworks
        if random.random() < 0.05:
            x = random.randint(50, 750)
            y = random.randint(50, 300)
            self.firework_positions.extend(self.create_firework(x, y))
        
        self.root.after(20, self.animate)
    
    def update_fireworks(self):
        for particle in self.firework_positions[:]:
            # Update position
            self.celebration_canvas.move(
                particle['id'],
                particle['dx'],
                particle['dy'] + 0.1
            )
            
            # Update life
            particle['life'] -= 0.02
            if particle['life'] <= 0:
                self.celebration_canvas.delete(particle['id'])
                self.firework_positions.remove(particle)
    
    def toggle_music(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            try:
                music_file = "celebration_music.mp3"
                if os.path.exists(music_file):
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load(music_file)
                    pygame.mixer.music.play(-1)
                    self.is_playing = True
            except Exception as e:
                print(f"Music error: {e}")
    
    def add_manual_firework(self):
        self.celebration_canvas.bind('<Button-1>', 
            lambda event: self.firework_positions.extend(
                self.create_firework(event.x, event.y)
            )
        )
    
    def show_frame(self, frame_name):
        for name, frame in self.frames.items():
            if name == frame_name:
                frame.pack(expand=True, fill="both")
            else:
                frame.pack_forget()
    
    def show_welcome(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
        self.show_frame('welcome')
    
    def show_celebration(self):
        self.show_frame('celebration')
        self.animation_running = True
        self.animate()
        self.update_wish()
    
    def show_settings(self):
        self.show_frame('settings')
    
    def start_celebration(self):
        name = self.name_var.get() or "Friend"
        self.celebration_canvas.itemconfig(
            self.header_label,
            text=f"Happy New Year, {name}!"
        )
        self.show_celebration()
        
        if self.effects['music'].get():
            self.toggle_music()
    
    def update_wish(self):
        if not self.animation_running:
            return
            
        self.current_wish = (self.current_wish + 1) % len(self.wishes)
        self.celebration_canvas.itemconfig(
            self.wish_label,
            text=self.wishes[self.current_wish]
        )
        self.root.after(3000, self.update_wish)
    
    @staticmethod
    def lighten_color(color):
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        factor = 1.2
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def change_theme(self):
        self.current_theme = self.theme_var.get()
        self.colors = self.themes[self.current_theme].copy()
        self.update_theme_elements()
    
    def update_theme_elements(self):
        # Update canvas backgrounds
        self.celebration_canvas.configure(bg=self.colors['background'])
        self.welcome_canvas.configure(bg=self.colors['background'])
        
        # Update styles
        self.setup_styles()
        
        # Update text colors
        for canvas_item in [self.header_label, self.wish_label]:
            self.celebration_canvas.itemconfig(
                canvas_item,
                fill=self.colors['secondary']
            )
    
    def cleanup(self):
        self.animation_running = False
        if self.is_playing:
            pygame.mixer.music.stop()
        pygame.mixer.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = NewYearApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.cleanup(), root.destroy()))
    root.mainloop()