import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import random
import math
import pygame
import os
from pathlib import Path
import mutagen
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
import requests
import tempfile
import subprocess
import sys

class ModernButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            relief='flat',
            borderwidth=0,
            cursor='hand2',
            font=('Inter', 10, 'bold')
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
    def on_enter(self, e):
        self.configure(bg=self.hover_color if hasattr(self, 'hover_color') else '#3a5998')
        
    def on_leave(self, e):
        self.configure(bg=self.default_color if hasattr(self, 'default_color') else '#667eea')

class IzukuAudioPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎵 Izuku Audio Player - 2025 Edition")
        self.root.geometry("800x650")
        self.root.configure(bg='#667eea')
        self.root.resizable(False, False)
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Player state
        self.is_playing = False
        self.is_paused = False
        self.current_time = 0
        self.duration = 0
        self.volume = 0.7
        self.playlist = []
        self.current_index = 0
        self.current_file = None
        self.temp_files = []  # Keep track of temporary files
        
        # Theme colors
        self.themes = [
            {'bg': '#667eea', 'accent': '#764ba2'},
            {'bg': '#f093fb', 'accent': '#f5576c'},
            {'bg': '#4facfe', 'accent': '#00f2fe'},
            {'bg': '#43e97b', 'accent': '#38f9d7'},
            {'bg': '#fa709a', 'accent': '#fee140'}
        ]
        self.current_theme = 0
        
        self.setup_ui()
        self.setup_animations()
        self.bind_keyboard_shortcuts()
        
    def setup_ui(self):
        # Main container
        self.main_frame = tk.Frame(self.root, bg='#667eea')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.setup_header()
        
        # File selection section
        self.setup_file_section()
        
        # YouTube link section
        self.setup_youtube_section()
        
        # Controls section
        self.setup_controls()
        
        # Progress bar
        self.setup_progress()
        
        # Status section
        self.setup_status()
        
        # Volume control
        self.setup_volume()
        
        # Visualizer (placeholder)
        self.setup_visualizer()
        
        # Settings modal setup
        self.setup_settings_modal()
        
    def setup_header(self):
        header_frame = tk.Frame(self.main_frame, bg='#667eea')
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Logo
        logo_label = tk.Label(
            header_frame,
            text="🎵 Izuku Audio Player",
            font=('Inter', 18, 'bold'),
            fg='white',
            bg='#667eea'
        )
        logo_label.pack(side='left')
        
        # Settings button
        self.settings_btn = ModernButton(
            header_frame,
            text="⚙️",
            font=('Arial', 16),
            fg='white',
            bg='#5a6fd8',
            width=3,
            command=self.toggle_settings
        )
        self.settings_btn.default_color = '#5a6fd8'
        self.settings_btn.hover_color = '#4a5bc8'
        self.settings_btn.pack(side='right')
        
    def setup_file_section(self):
        file_frame = tk.Frame(self.main_frame, bg='#667eea')
        file_frame.pack(fill='x', pady=(0, 20))
        
        # File selection buttons
        btn_frame = tk.Frame(file_frame, bg='#667eea')
        btn_frame.pack()
        
        self.select_file_btn = ModernButton(
            btn_frame,
            text="📁 Select Audio File",
            font=('Inter', 11, 'bold'),
            fg='white',
            bg='#ff6b6b',
            padx=20,
            pady=10,
            command=self.select_file
        )
        self.select_file_btn.default_color = '#ff6b6b'
        self.select_file_btn.hover_color = '#ee5a52'
        self.select_file_btn.pack(side='left', padx=(0, 10))
        
        self.select_folder_btn = ModernButton(
            btn_frame,
            text="📂 Select Folder",
            font=('Inter', 11, 'bold'),
            fg='white',
            bg='#4ecdc4',
            padx=20,
            pady=10,
            command=self.select_folder
        )
        self.select_folder_btn.default_color = '#4ecdc4'
        self.select_folder_btn.hover_color = '#44a08d'
        self.select_folder_btn.pack(side='left')
        
    def setup_youtube_section(self):
        youtube_frame = tk.Frame(self.main_frame, bg='#667eea')
        youtube_frame.pack(fill='x', pady=(0, 30))
        
        # YouTube section title
        youtube_title = tk.Label(
            youtube_frame,
            text="🎬 YouTube Audio",
            font=('Inter', 12, 'bold'),
            fg='white',
            bg='#667eea'
        )
        youtube_title.pack(pady=(0, 10))
        
        # URL input frame
        url_input_frame = tk.Frame(youtube_frame, bg='#667eea')
        url_input_frame.pack(fill='x', pady=(0, 10))
        
        # URL entry
        self.url_entry = tk.Entry(
            url_input_frame,
            font=('Inter', 11),
            bg='white',
            fg='#333',
            relief='flat',
            bd=5
        )
        self.url_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.url_entry.insert(0, "Paste YouTube URL here...")
        self.url_entry.bind('<FocusIn>', self.clear_placeholder)
        self.url_entry.bind('<FocusOut>', self.restore_placeholder)
        
        # Play YouTube button
        self.youtube_play_btn = ModernButton(
            url_input_frame,
            text="▶️ Play",
            font=('Inter', 11, 'bold'),
            fg='white',
            bg='#ff4757',
            padx=15,
            pady=8,
            command=self.play_youtube_url
        )
        self.youtube_play_btn.default_color = '#ff4757'
        self.youtube_play_btn.hover_color = '#ff3742'
        self.youtube_play_btn.pack(side='right')
        
        # Download status
        self.download_status = tk.Label(
            youtube_frame,
            text="",
            font=('Inter', 9),
            fg='#cccccc',
            bg='#667eea'
        )
        self.download_status.pack()
        
    def clear_placeholder(self, event):
        if self.url_entry.get() == "Paste YouTube URL here...":
            self.url_entry.delete(0, tk.END)
            self.url_entry.configure(fg='#333')
            
    def restore_placeholder(self, event):
        if not self.url_entry.get():
            self.url_entry.insert(0, "Paste YouTube URL here...")
            self.url_entry.configure(fg='#999')
            
    def setup_controls(self):
        controls_frame = tk.Frame(self.main_frame, bg='#667eea')
        controls_frame.pack(pady=(0, 30))
        
        # Previous button
        self.prev_btn = ModernButton(
            controls_frame,
            text="⏮️",
            font=('Arial', 16),
            fg='white',
            bg='#5a6fd8',
            width=4,
            height=2,
            command=self.previous_song
        )
        self.prev_btn.default_color = '#5a6fd8'
        self.prev_btn.hover_color = '#4a5bc8'
        self.prev_btn.pack(side='left', padx=10)
        
        # Play/Pause button
        self.play_btn = ModernButton(
            controls_frame,
            text="▶️",
            font=('Arial', 20),
            fg='white',
            bg='#4ecdc4',
            width=5,
            height=2,
            command=self.toggle_play_pause
        )
        self.play_btn.default_color = '#4ecdc4'
        self.play_btn.hover_color = '#44a08d'
        self.play_btn.pack(side='left', padx=10)
        
        # Next button
        self.next_btn = ModernButton(
            controls_frame,
            text="⏭️",
            font=('Arial', 16),
            fg='white',
            bg='#5a6fd8',
            width=4,
            height=2,
            command=self.next_song
        )
        self.next_btn.default_color = '#5a6fd8'
        self.next_btn.hover_color = '#4a5bc8'
        self.next_btn.pack(side='left', padx=10)
        
    def setup_progress(self):
        progress_frame = tk.Frame(self.main_frame, bg='#667eea')
        progress_frame.pack(fill='x', pady=(0, 20))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(
            progress_frame,
            from_=0,
            to=100,
            orient='horizontal',
            variable=self.progress_var,
            command=self.seek_to
        )
        self.progress_bar.pack(fill='x')
        
    def setup_status(self):
        status_frame = tk.Frame(self.main_frame, bg='#667eea')
        status_frame.pack(pady=(0, 20))
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to play music",
            font=('Inter', 12, 'bold'),
            fg='white',
            bg='#667eea'
        )
        self.status_label.pack()
        
        self.time_label = tk.Label(
            status_frame,
            text="00:00 / 00:00",
            font=('Inter', 10),
            fg='#cccccc',
            bg='#667eea'
        )
        self.time_label.pack()
        
    def setup_volume(self):
        volume_frame = tk.Frame(self.main_frame, bg='#667eea')
        volume_frame.pack(fill='x', pady=(0, 20))
        
        volume_label = tk.Label(
            volume_frame,
            text="🔊 Volume",
            font=('Inter', 10),
            fg='white',
            bg='#667eea'
        )
        volume_label.pack()
        
        self.volume_var = tk.DoubleVar(value=70)
        self.volume_scale = ttk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient='horizontal',
            variable=self.volume_var,
            command=self.set_volume
        )
        self.volume_scale.pack(fill='x', padx=50)
        
    def setup_visualizer(self):
        # Placeholder for visualizer
        visualizer_frame = tk.Frame(self.main_frame, bg='#667eea', height=50)
        visualizer_frame.pack(fill='x')
        
        self.visualizer_bars = []
        for i in range(15):
            bar = tk.Frame(
                visualizer_frame,
                bg='#4ecdc4',
                width=4,
                height=random.randint(5, 30)
            )
            bar.pack(side='left', padx=2, pady=10)
            self.visualizer_bars.append(bar)
            
    def setup_settings_modal(self):
        self.settings_window = None
        
    def setup_animations(self):
        self.animate_visualizer()
        self.update_progress()
        
    def animate_visualizer(self):
        if self.is_playing and not self.is_paused:
            for bar in self.visualizer_bars:
                height = random.randint(5, 40)
                bar.configure(height=height)
        
        self.root.after(150, self.animate_visualizer)
        
    def update_progress(self):
        if self.is_playing and not self.is_paused:
            if pygame.mixer.music.get_busy():
                self.current_time += 0.1
                if self.duration > 0:
                    progress = (self.current_time / self.duration) * 100
                    self.progress_var.set(progress)
                    self.update_time_display()
            else:
                # Song ended
                self.next_song()
        
        self.root.after(100, self.update_progress)
    
    def is_youtube_url(self, url):
        """Check if the URL is a valid YouTube URL"""
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
        return any(domain in url.lower() for domain in youtube_domains)
    
    def download_youtube_audio(self, url):
        """Download audio from YouTube URL using yt-dlp"""
        try:
            self.download_status.configure(text="🔄 Downloading audio...")
            self.root.update()
            
            # Create temporary directory
            temp_dir = tempfile.mkdtemp()
            output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')
            
            # Try to use yt-dlp first, then fallback to youtube-dl
            commands = [
                ['yt-dlp', '--extract-audio', '--audio-format', 'mp3', '--audio-quality', '192K', '-o', output_template, url],
                ['youtube-dl', '--extract-audio', '--audio-format', 'mp3', '--audio-quality', '192K', '-o', output_template, url]
            ]
            
            for cmd in commands:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                    if result.returncode == 0:
                        # Find the downloaded file
                        for file in os.listdir(temp_dir):
                            if file.endswith('.mp3'):
                                audio_path = os.path.join(temp_dir, file)
                                self.temp_files.append(audio_path)
                                self.download_status.configure(text="✅ Download complete!")
                                return audio_path
                    break
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    continue
            
            # If both fail, try a simple approach with requests (won't work for YouTube but shows the attempt)
            self.download_status.configure(text="❌ Download failed. Please install yt-dlp or youtube-dl")
            return None
            
        except Exception as e:
            self.download_status.configure(text=f"❌ Error: {str(e)}")
            return None
    
    def play_youtube_url(self):
        """Handle YouTube URL playback"""
        url = self.url_entry.get().strip()
        
        if not url or url == "Paste YouTube URL here...":
            self.update_status("Please enter a YouTube URL")
            return
        
        if not self.is_youtube_url(url):
            self.update_status("Please enter a valid YouTube URL")
            return
        
        # Disable the button during download
        self.youtube_play_btn.configure(state='disabled', text="⏳ Loading...")
        
        def download_and_play():
            try:
                audio_path = self.download_youtube_audio(url)
                
                if audio_path and os.path.exists(audio_path):
                    # Add to playlist and play
                    self.playlist = [audio_path]
                    self.current_index = 0
                    self.load_current_song()
                    
                    # Auto-play the downloaded audio
                    self.root.after(100, self.start_playback)
                else:
                    self.update_status("Failed to download audio from YouTube")
                    
            except Exception as e:
                self.update_status(f"Error processing YouTube URL: {str(e)}")
            finally:
                # Re-enable the button
                self.youtube_play_btn.configure(state='normal', text="▶️ Play")
        
        # Run download in a separate thread to avoid blocking UI
        thread = threading.Thread(target=download_and_play, daemon=True)
        thread.start()
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.ogg *.m4a *.flac"),
                ("MP3 Files", "*.mp3"),
                ("WAV Files", "*.wav"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.playlist = [file_path]
            self.current_index = 0
            self.load_current_song()
            
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Select Music Folder")
        
        if folder_path:
            audio_extensions = {'.mp3', '.wav', '.ogg', '.m4a', '.flac'}
            self.playlist = []
            
            for file_path in Path(folder_path).rglob('*'):
                if file_path.suffix.lower() in audio_extensions:
                    self.playlist.append(str(file_path))
            
            if self.playlist:
                self.current_index = 0
                self.load_current_song()
                self.update_status(f"Loaded {len(self.playlist)} songs from folder")
            else:
                self.update_status("No audio files found in selected folder")
                
    def load_current_song(self):
        if not self.playlist:
            return
            
        file_path = self.playlist[self.current_index]
        self.current_file = file_path
        
        try:
            # Get song duration
            self.duration = self.get_audio_duration(file_path)
            
            # Load the file
            pygame.mixer.music.load(file_path)
            
            # Update display
            song_name = Path(file_path).stem
            self.update_status(f"Loaded: {song_name}")
            self.current_time = 0
            self.progress_var.set(0)
            self.update_time_display()
            
        except Exception as e:
            self.update_status(f"Error loading file: {str(e)}")
            
    def get_audio_duration(self, file_path):
        try:
            audio_file = mutagen.File(file_path)
            if audio_file:
                return audio_file.info.length
        except:
            pass
        return 0
        
    def toggle_play_pause(self):
        if not self.playlist:
            self.update_status("Please select an audio file or YouTube URL first")
            return
            
        if not self.is_playing:
            self.start_playback()
        else:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.play_btn.configure(text="⏸️")
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.play_btn.configure(text="▶️")
                
    def start_playback(self):
        try:
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            self.play_btn.configure(text="⏸️")
            
            song_name = Path(self.current_file).stem if self.current_file else "Unknown"
            self.update_status(f"Now playing: {song_name}")
            
        except Exception as e:
            self.update_status(f"Error playing file: {str(e)}")
            
    def previous_song(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.load_current_song()
            if self.is_playing:
                self.start_playback()
                
    def next_song(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.load_current_song()
            if self.is_playing:
                self.start_playback()
                
    def seek_to(self, value):
        if self.duration > 0:
            seek_time = (float(value) / 100) * self.duration
            self.current_time = seek_time
            # Note: pygame.mixer doesn't support seeking, so this is a limitation
            
    def set_volume(self, value):
        volume = float(value) / 100
        pygame.mixer.music.set_volume(volume)
        self.volume = volume
        
    def update_status(self, message):
        self.status_label.configure(text=message)
        
    def update_time_display(self):
        current_min = int(self.current_time // 60)
        current_sec = int(self.current_time % 60)
        total_min = int(self.duration // 60)
        total_sec = int(self.duration % 60)
        
        time_str = f"{current_min:02d}:{current_sec:02d} / {total_min:02d}:{total_sec:02d}"
        self.time_label.configure(text=time_str)
        
    def toggle_settings(self):
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.destroy()
            return
            
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("300x400")
        self.settings_window.configure(bg='#667eea')
        self.settings_window.resizable(False, False)
        
        # Settings title
        title_label = tk.Label(
            self.settings_window,
            text="Settings",
            font=('Inter', 16, 'bold'),
            fg='white',
            bg='#667eea'
        )
        title_label.pack(pady=20)
        
        # Settings buttons
        settings_buttons = [
            ("🎨 Change Theme", self.change_theme),
            ("🌙 Toggle Dark Mode", self.toggle_dark_mode),
            ("🔄 Reset Settings", self.reset_settings),
        ]
        
        for text, command in settings_buttons:
            btn = ModernButton(
                self.settings_window,
                text=text,
                font=('Inter', 11),
                fg='white',
                bg='#5a6fd8',
                padx=20,
                pady=10,
                command=command
            )
            btn.default_color = '#5a6fd8'
            btn.hover_color = '#4a5bc8'
            btn.pack(pady=10, padx=20, fill='x')
            
    def change_theme(self):
        self.current_theme = (self.current_theme + 1) % len(self.themes)
        theme = self.themes[self.current_theme]
        
        self.root.configure(bg=theme['bg'])
        self.main_frame.configure(bg=theme['bg'])
        
        # Update all frames and labels
        for widget in self.root.winfo_children():
            self.update_widget_theme(widget, theme['bg'])
            
        self.update_status("Theme changed!")
        
    def update_widget_theme(self, widget, bg_color):
        try:
            if isinstance(widget, (tk.Frame, tk.Label)):
                widget.configure(bg=bg_color)
        except:
            pass
            
        for child in widget.winfo_children():
            self.update_widget_theme(child, bg_color)
            
    def toggle_dark_mode(self):
        # Simple dark mode toggle
        current_bg = self.root.cget('bg')
        if current_bg == '#667eea':
            new_bg = '#2c3e50'
        else:
            new_bg = '#667eea'
            
        self.root.configure(bg=new_bg)
        self.main_frame.configure(bg=new_bg)
        
        for widget in self.root.winfo_children():
            self.update_widget_theme(widget, new_bg)
            
        self.update_status("Dark mode toggled!")
        
    def reset_settings(self):
        self.current_theme = 0
        self.root.configure(bg='#667eea')
        self.main_frame.configure(bg='#667eea')
        
        for widget in self.root.winfo_children():
            self.update_widget_theme(widget, '#667eea')
            
        self.update_status("Settings reset to default")
        
    def bind_keyboard_shortcuts(self):
        self.root.bind('<space>', lambda e: self.toggle_play_pause())
        self.root.bind('<Left>', lambda e: self.previous_song())
        self.root.bind('<Right>', lambda e: self.next_song())
        self.root.focus_set()  # Allow root to receive key events
        
    def cleanup_temp_files(self):
        """Clean up temporary downloaded files"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    # Also remove the parent directory if it's empty
                    parent_dir = os.path.dirname(temp_file)
                    if os.path.exists(parent_dir) and not os.listdir(parent_dir):
                        os.rmdir(parent_dir)
            except:
                pass
        
    def run(self):
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        finally:
            self.cleanup_temp_files()
            pygame.mixer.quit()
    
    def on_closing(self):
        """Handle application closing"""
        self.cleanup_temp_files()
        self.root.destroy()

if __name__ == "__main__":
    # Check if required libraries are installed
    try:
        import pygame
        import mutagen
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Please install required packages:")
        print("pip install pygame mutagen")
        exit(1)
    
    print("🎵 Izuku Audio Player - Enhanced with YouTube Support")
    print("📋 Features:")
    print("   • Play local audio files (MP3, WAV, FLAC, etc.)")
    print("   • Play audio from YouTube URLs")
    print("   • Modern UI with themes and dark mode")
    print("   • Keyboard shortcuts (Space, Left/Right arrows)")
    print("")
    print("📝 Note: For YouTube support, install yt-dlp or youtube-dl:")
    print("   pip install yt-dlp")
    print("   or")
    print("   pip install youtube-dl")
    print("")
    
    app = IzukuAudioPlayer()
    app.run()