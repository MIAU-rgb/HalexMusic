"""
HalexMusic Player 2.31V
GitHub: https://github.com/MIAU-rgb/AudioPleer
Created by MIAU-rgb | © 2026
"""

import os
import json
import pygame
import math
import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from datetime import datetime

class MusicPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎵 HalexMusic 2.31V")
        self.root.geometry("750x520")
        self.root.configure(bg='#0a0a0a')
        self.root.minsize(650, 470)
        
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        self.desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.music_folder = os.path.join(self.desktop, "Music")
        self.info_file = os.path.join(self.music_folder, "Info.txt")
        self.settings_file = os.path.join(self.music_folder, "settings.json")
        
        self.playlists = {}
        self.current_playlist = None
        self.current_track_index = -1
        self.is_playing = False
        self.is_paused = False
        self.current_time = 0
        self.shuffle_mode = False
        self.shuffled_tracks = []
        self.original_tracks = []
        self.volume = 70
        self.screen_mode = "HD"
        self.viz_data = [0.0] * 64
        self.viz_peaks = [0.0] * 64
        self.color_mode = "normal"
        self.colors = self.get_color_scheme()
        self.mini_player = None
        self.search_dialog = None
        
        self.load_settings()
        self.bind_hotkeys()
        self.create_folders()
        self.load_info()
        self.setup_ui()
        self.update_time()
        self.update_visualizer()
    
    def copy_vk(self):
        self.root.clipboard_clear()
        self.root.clipboard_append("Halexplay")
        self.show_copy_notification("VK скопирован!")
    
    def copy_tg(self):
        self.root.clipboard_clear()
        self.root.clipboard_append("@HalerLuntic3045")
        self.show_copy_notification("TG скопирован!")
    
    def copy_ds(self):
        self.root.clipboard_clear()
        self.root.clipboard_append("_halex_halex_")
        self.show_copy_notification("DS скопирован!")
    
    def set_screen_mode(self, mode):
        self.screen_mode = mode
        self.save_settings()
        # Обновляем кнопки
        c = self.colors
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for subchild in child.winfo_children():
                            if isinstance(subchild, tk.Frame):
                                for btn in subchild.winfo_children():
                                    if isinstance(btn, tk.Button) and btn.cget('text') in ['HD', '2K', '4K']:
                                        if btn.cget('text') == mode:
                                            btn.config(bg=c['accent'], fg=c['yellow'])
                                        else:
                                            btn.config(bg=c['screen_btn'], fg='#888')
        # Если мини-плеер открыт - пересоздаём с новыми границами
        if self.mini_player and self.mini_player.winfo_exists():
            self.mini_player.destroy()
            self.mini_player = None
            self.create_mini_player()
            self.update_mini_player()
    
    def get_screen_bounds(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        mini_w = 280
        mini_h = 130
        taskbar_h = 48
        
        if self.screen_mode == "HD":
            return 0, 0, screen_w - mini_w - 5, screen_h - mini_h - taskbar_h - 5
        elif self.screen_mode == "2K":
            return 0, 0, screen_w - mini_w - 10, screen_h - mini_h - taskbar_h - 10
        else:  # 4K
            return 0, 0, screen_w - mini_w - 15, screen_h - mini_h - taskbar_h - 15
    
    def show_copy_notification(self, text):
        notif = tk.Toplevel(self.root)
        notif.title("")
        notif.geometry("150x25")
        notif.overrideredirect(True)
        notif.configure(bg=self.colors['accent'])
        notif.geometry(f"+{self.root.winfo_x() + 300}+{self.root.winfo_y() + 5}")
        tk.Label(notif, text=text, font=('Arial', 8, 'bold'), fg='white', bg=self.colors['accent']).pack(expand=True)
        notif.after(1000, notif.destroy)
    
    def update_visualizer(self):
        if hasattr(self, 'viz_canvas') and self.viz_canvas:
            if self.is_playing and not self.is_paused:
                try:
                    sound_buffer = pygame.mixer.get_sound_buffer()
                    if sound_buffer is not None and len(sound_buffer) > 0:
                        num_bars = 64
                        chunk_size = max(1, len(sound_buffer) // num_bars)
                        for i in range(num_bars):
                            start = i * chunk_size
                            end = min(start + chunk_size, len(sound_buffer))
                            if start < len(sound_buffer):
                                chunk = sound_buffer[start:end]
                                if len(chunk) > 0:
                                    rms = math.sqrt(sum(s * s for s in chunk) / len(chunk))
                                    amplitude = rms / 32768.0
                                else:
                                    amplitude = 0.01
                            else:
                                amplitude = 0.01
                            if i < 16: amplitude *= 3.0
                            elif i < 48: amplitude *= 2.0
                            else: amplitude *= 1.5
                            amplitude *= (0.5 + self.volume / 100.0)
                            amplitude = min(1.0, amplitude)
                            if amplitude > self.viz_data[i]:
                                self.viz_data[i] = self.viz_data[i] * 0.3 + amplitude * 0.7
                            else:
                                self.viz_data[i] = self.viz_data[i] * 0.85 + amplitude * 0.15
                            if amplitude > self.viz_peaks[i]:
                                self.viz_peaks[i] = amplitude
                            else:
                                self.viz_peaks[i] *= 0.95
                    else:
                        for i in range(64):
                            self.viz_data[i] *= 0.8
                            self.viz_peaks[i] *= 0.9
                except:
                    vol = self.volume / 100.0
                    for i in range(64):
                        wave = abs(math.sin(i * 0.3 + self.current_time * 0.15))
                        target = vol * (0.2 + 0.8 * wave) * random.uniform(0.7, 1.3)
                        if target > self.viz_data[i]:
                            self.viz_data[i] = self.viz_data[i] * 0.4 + target * 0.6
                        else:
                            self.viz_data[i] = self.viz_data[i] * 0.9 + target * 0.1
            else:
                for i in range(64):
                    self.viz_data[i] *= 0.85
                    self.viz_peaks[i] *= 0.88
            self.draw_viz_bars()
        self.root.after(25, self.update_visualizer)
    
    def draw_viz_bars(self):
        if not hasattr(self, 'viz_canvas') or not self.viz_canvas: return
        self.viz_canvas.delete('all')
        cw = self.viz_canvas.winfo_width()
        ch = self.viz_canvas.winfo_height()
        if cw < 10 or ch < 10: return
        bar_count = 64
        bar_width = max(1.5, (cw - bar_count * 2) / bar_count)
        gap = 2
        for i in range(bar_count):
            height = int(self.viz_data[i] * (ch - 10))
            height = max(1, min(height, ch - 10))
            peak_h = int(self.viz_peaks[i] * (ch - 10))
            peak_h = max(1, min(peak_h, ch - 10))
            x1 = gap + i * (bar_width + gap)
            y1 = ch - height - 5
            x2 = x1 + bar_width
            y2 = ch - 5
            hue = (i * 5.6 + int(self.current_time * 3)) % 360
            r = int((math.sin(math.radians(hue)) * 127 + 128))
            g = int((math.sin(math.radians(hue + 120)) * 127 + 128))
            b = int((math.sin(math.radians(hue + 240)) * 127 + 128))
            brightness = 0.4 + (self.viz_data[i] * 0.6)
            r, g, b = int(r*brightness), int(g*brightness), int(b*brightness)
            color = '#{:02x}{:02x}{:02x}'.format(min(255,r), min(255,g), min(255,b))
            self.viz_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='', width=0)
            if peak_h > height + 1:
                peak_y = ch - peak_h - 5
                peak_color = '#{:02x}{:02x}{:02x}'.format(min(255,int(r*1.5)), min(255,int(g*1.5)), min(255,int(b*1.5)))
                self.viz_canvas.create_rectangle(x1, peak_y, x2, peak_y+2, fill=peak_color, outline='', width=0)
    
    def export_playlist(self):
        if not self.current_playlist or self.current_playlist not in self.playlists:
            messagebox.showwarning("Экспорт", "Выберите плейлист!"); return
        tracks = self.playlists[self.current_playlist]['tracks']
        if not tracks: messagebox.showwarning("Экспорт", "Плейлист пуст!"); return
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Playlist", "*.json"), ("All Files", "*.*")], initialfile=self.playlists[self.current_playlist]['name']+".json")
        if filepath:
            data = {'name':self.playlists[self.current_playlist]['name'],'exported':datetime.now().strftime("%d.%m.%Y %H:%M:%S"),'tracks':[]}
            for t in tracks: data['tracks'].append({'title':t['title'],'artist':t['artist'],'duration':t['duration'],'filepath':t['path']})
            with open(filepath, 'w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Экспорт", f"Плейлист сохранён в:\n{filepath}")
    
    def get_color_scheme(self):
        schemes = {
            "normal": {'bg':'#0a0a0a','panel':'#1a1a1a','accent':'#2d1b69','text':'#ffffff','yellow':'#fcb424','progress':'#8A2BE2','btn_bg':'#2d1b69','tree_bg':'#1a1a1a','selected':'#8A2BE2','mini_bg':'#0d1117','mini_accent':'#fcb424','mini_text':'#e6edf3','mini_secondary':'#161b22','hotkeys':'#555','copyright':'#444','social_btn':'#2d1b69','viz_bg':'#0a0a0a','screen_btn':'#1a1a1a'},
            "deuteranopia": {'bg':'#0a0a0a','panel':'#1a1a1a','accent':'#FFD700','text':'#ffffff','yellow':'#FFD700','progress':'#FFD700','btn_bg':'#8B7500','tree_bg':'#1a1a1a','selected':'#FFD700','mini_bg':'#0d1117','mini_accent':'#FFD700','mini_text':'#ffffff','mini_secondary':'#161b22','hotkeys':'#777','copyright':'#666','social_btn':'#8B7500','viz_bg':'#0a0a0a','screen_btn':'#1a1a1a'},
            "tritanopia": {'bg':'#0a0a0a','panel':'#1a1a1a','accent':'#FF6B35','text':'#ffffff','yellow':'#FF6B35','progress':'#FF6B35','btn_bg':'#CC5500','tree_bg':'#1a1a1a','selected':'#FF6B35','mini_bg':'#0d1117','mini_accent':'#FF6B35','mini_text':'#ffffff','mini_secondary':'#161b22','hotkeys':'#777','copyright':'#666','social_btn':'#CC5500','viz_bg':'#0a0a0a','screen_btn':'#1a1a1a'},
            "protanopia": {'bg':'#0a0a0a','panel':'#1a1a1a','accent':'#00BFFF','text':'#ffffff','yellow':'#FFD700','progress':'#00BFFF','btn_bg':'#0080AA','tree_bg':'#1a1a1a','selected':'#00BFFF','mini_bg':'#0d1117','mini_accent':'#00BFFF','mini_text':'#ffffff','mini_secondary':'#161b22','hotkeys':'#777','copyright':'#666','social_btn':'#0080AA','viz_bg':'#0a0a0a','screen_btn':'#1a1a1a'}
        }
        return schemes.get(self.color_mode, schemes["normal"])
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.volume = data.get('volume', 70)
                    self.shuffle_mode = data.get('shuffle_mode', False)
                    self.color_mode = data.get('color_mode', 'normal')
                    self.screen_mode = data.get('screen_mode', 'HD')
                    self.colors = self.get_color_scheme()
            except: pass
    
    def save_settings(self):
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump({'volume':self.volume,'shuffle_mode':self.shuffle_mode,'color_mode':self.color_mode,'screen_mode':self.screen_mode,'last_updated':datetime.now().strftime("%d.%m.%Y %H:%M:%S")}, f, ensure_ascii=False, indent=2)
    
    def set_color_mode(self, mode):
        self.color_mode = mode
        self.colors = self.get_color_scheme()
        self.save_settings()
        was_playing = self.is_playing
        was_paused = self.is_paused
        idx = self.current_track_index
        ctime = self.current_time
        for widget in self.root.winfo_children(): widget.destroy()
        self.setup_ui()
        self.is_playing = was_playing
        self.is_paused = was_paused
        self.current_track_index = idx
        self.current_time = ctime
        self.update_playlists_list()
        self.update_tracks_list()
        if idx >= 0 and self.current_playlist:
            tracks = self.playlists[self.current_playlist]['tracks']
            if idx < len(tracks):
                self.current_track_label.config(text=f"🎵 {tracks[idx]['title'][:35]}")
                self.total_time_label.config(text=tracks[idx]['duration_str'])
    
    def create_folders(self):
        if not os.path.exists(self.music_folder): os.makedirs(self.music_folder)
        for pl in ["Playlist1","Playlist2","Playlist3"]:
            pp = os.path.join(self.music_folder, pl)
            if not os.path.exists(pp): os.makedirs(pp)
    
    def load_info(self):
        if os.path.exists(self.info_file):
            try:
                with open(self.info_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.playlists = data.get('playlists', {})
                    self.current_playlist = data.get('current_playlist')
            except: self.playlists = {}
        self.scan_music_folders()
    
    def save_info(self):
        with open(self.info_file, 'w', encoding='utf-8') as f:
            json.dump({'playlists':self.playlists,'current_playlist':self.current_playlist,'last_updated':datetime.now().strftime("%d.%m.%Y %H:%M:%S")}, f, ensure_ascii=False, indent=2)
    
    def scan_music_folders(self):
        if not os.path.exists(self.music_folder): return
        for folder in os.listdir(self.music_folder):
            fp = os.path.join(self.music_folder, folder)
            if os.path.isdir(fp):
                if folder not in self.playlists: self.playlists[folder] = {'name':folder.replace('Playlist','Плейлист '),'folder':folder,'tracks':[]}
                tracks = []
                for file in os.listdir(fp):
                    if file.endswith('.mp3'): tracks.append(self.get_track_info(os.path.join(fp, file)))
                self.playlists[folder]['tracks'] = tracks
        root_tracks = []
        for file in os.listdir(self.music_folder):
            if file.endswith('.mp3'): root_tracks.append(self.get_track_info(os.path.join(self.music_folder, file)))
        if root_tracks:
            if 'All Music' not in self.playlists: self.playlists['All Music'] = {'name':'Вся музыка','folder':'','tracks':root_tracks}
            else: self.playlists['All Music']['tracks'] = root_tracks
        self.save_info()
    
    def get_track_info(self, filepath):
        try:
            audio = MP3(filepath)
            duration = int(audio.info.length)
            try:
                tags = ID3(filepath)
                artist = str(tags.get('TPE1', 'Неизвестный исполнитель'))
                title = str(tags.get('TIT2', os.path.basename(filepath)))
            except:
                artist = 'Неизвестный исполнитель'
                title = os.path.basename(filepath).replace('.mp3', '')
            return {'path':filepath,'filename':os.path.basename(filepath),'title':title,'artist':artist,'duration':duration,'duration_str':f"{duration//60}:{duration%60:02d}"}
        except:
            return {'path':filepath,'filename':os.path.basename(filepath),'title':os.path.basename(filepath).replace('.mp3',''),'artist':'Неизвестный исполнитель','duration':0,'duration_str':'?:??'}
    
    def bind_hotkeys(self):
        self.root.bind('<space>', lambda e: self.play_pause())
        self.root.bind('<Left>', lambda e: self.prev_track())
        self.root.bind('<Right>', lambda e: self.next_track())
        self.root.bind('<Control-f>', lambda e: self.show_search())
        self.root.bind('<Control-m>', lambda e: self.toggle_mini_player())
        self.root.bind('<Escape>', lambda e: self.minimize_to_mini())
    
    def setup_ui(self):
        c = self.colors
        top = tk.Frame(self.root, bg=c['bg'], height=28)
        top.pack(fill='x', padx=5, pady=(5,0))
        top.pack_propagate(False)
        btn_cfg = {'font':('Arial',7),'bg':c['btn_bg'],'fg':'white','relief':'flat','padx':6,'pady':2}
        tk.Button(top, text="🔍 Ctrl+F", **btn_cfg, command=self.show_search).pack(side='left', padx=1)
        tk.Button(top, text="🖥 Ctrl+M", **btn_cfg, command=self.toggle_mini_player).pack(side='left', padx=1)
        for text, mode in [("👁 Norm","normal"),("🟢 Deut","deuteranopia"),("🔵 Trit","tritanopia"),("🔴 Prot","protanopia")]:
            is_active = (self.color_mode == mode)
            cfg = {'font':('Arial',6),'bg':c['accent'] if is_active else c['panel'],'fg':c['yellow'] if is_active else '#888','relief':'flat','padx':4,'pady':1}
            tk.Button(top, text=text, **cfg, command=lambda m=mode: self.set_color_mode(m)).pack(side='left', padx=1)
        self.current_track_label = tk.Label(top, text="🎵 Нет трека", font=('Arial',9,'bold'), fg=c['yellow'], bg=c['bg'], anchor='e')
        self.current_track_label.pack(side='right', padx=10)
        
        main = tk.Frame(self.root, bg=c['bg'])
        main.pack(fill='both', expand=True, padx=5, pady=3)
        left = tk.Frame(main, bg=c['panel'], width=140)
        left.pack(side='left', fill='y', padx=(0,4))
        left.pack_propagate(False)
        tk.Label(left, text="Плейлисты", font=('Arial',9,'bold'), fg='white', bg=c['panel']).pack(pady=4)
        self.playlist_listbox = tk.Listbox(left, bg=c['bg'], fg='white', selectbackground=c['selected'], font=('Arial',8), relief='flat', bd=0, height=11)
        self.playlist_listbox.pack(fill='both', expand=True, padx=4, pady=3)
        self.playlist_listbox.bind('<<ListboxSelect>>', self.on_playlist_select)
        pl_btns = tk.Frame(left, bg=c['panel'])
        pl_btns.pack(pady=2)
        for txt, cmd in [("+",self.create_playlist),("🔄",self.refresh_music),("✏️",self.rename_playlist),("💾",self.export_playlist)]:
            bg = c['btn_bg'] if txt != "✏️" else '#333'
            tk.Button(pl_btns, text=txt, font=('Arial',7), bg=bg, fg='white', relief='flat', padx=6, command=cmd).pack(side='left', padx=1)
        
        right = tk.Frame(main, bg=c['bg'])
        right.pack(side='right', fill='both', expand=True)
        prog_frame = tk.Frame(right, bg=c['bg'])
        prog_frame.pack(fill='x', pady=2)
        self.current_time_label = tk.Label(prog_frame, text="0:00", font=('Arial',7), fg='#aaa', bg=c['bg'])
        self.current_time_label.pack(side='left')
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(prog_frame, from_=0, to=100, variable=self.progress_var, orient='horizontal', command=self.seek_track)
        self.progress_bar.pack(side='left', fill='x', expand=True, padx=4)
        self.total_time_label = tk.Label(prog_frame, text="0:00", font=('Arial',7), fg='#aaa', bg=c['bg'])
        self.total_time_label.pack(side='right')
        
        ctrl_vol = tk.Frame(right, bg=c['bg'])
        ctrl_vol.pack(fill='x', pady=4)
        for text, cmd in [("⏮",self.prev_track),("⏯",self.play_pause),("⏭",self.next_track),("🔀",self.toggle_shuffle)]:
            tk.Button(ctrl_vol, text=text, font=('Arial',14), bg=c['panel'], fg='white', relief='flat', width=2, command=cmd).pack(side='left', padx=2)
        self.volume_var = tk.DoubleVar(value=self.volume)
        self.volume_scale = ttk.Scale(ctrl_vol, from_=0, to=100, variable=self.volume_var, orient='horizontal', command=self.change_volume, length=100)
        self.volume_scale.pack(side='right', padx=5)
        self.volume_label = tk.Label(ctrl_vol, text=f"{self.volume}%", font=('Arial',8), fg='white', bg=c['bg'], width=4)
        self.volume_label.pack(side='right')
        tk.Label(ctrl_vol, text="🔊", font=('Arial',9), fg='white', bg=c['bg']).pack(side='right')
        hotkeys_frame = tk.Frame(right, bg=c['bg'])
        hotkeys_frame.pack(fill='x', pady=1)
        tk.Label(hotkeys_frame, text="Space: pause | Arrows: tracks | Esc: mini", font=('Arial',6), fg=c['hotkeys'], bg=c['bg']).pack(side='left')
        
        columns = ('#','Название','Исполнитель','Время')
        self.tracks_tree = ttk.Treeview(right, columns=columns, show='headings', height=10)
        for col, txt, w in [('#','№',28),('Название','Название',220),('Исполнитель','Исполнитель',150),('Время','Время',45)]:
            self.tracks_tree.heading(col, text=txt); self.tracks_tree.column(col, width=w)
        style = ttk.Style(); style.theme_use("default")
        style.configure("Treeview", background=c['tree_bg'], foreground="white", fieldbackground=c['tree_bg'], rowheight=20, font=('Arial',8))
        style.configure("Treeview.Heading", background=c['btn_bg'], foreground="white", font=('Arial',8,'bold'))
        style.map("Treeview", background=[('selected', c['selected'])])
        self.tracks_tree.pack(fill='x', expand=False)
        self.tracks_tree.bind('<Double-1>', self.play_selected_track)
        
        viz_frame = tk.Frame(right, bg=c['viz_bg'], height=70)
        viz_frame.pack(fill='x', pady=(5,0))
        viz_frame.pack_propagate(False)
        self.viz_canvas = tk.Canvas(viz_frame, bg=c['viz_bg'], highlightthickness=0)
        self.viz_canvas.pack(fill='both', expand=True)
        
        bottom_frame = tk.Frame(right, bg=c['bg'], height=22)
        bottom_frame.pack(fill='x', side='bottom', pady=(2,0))
        bottom_frame.pack_propagate(False)
        tk.Label(bottom_frame, text="© 2026 HalexMusic 2.31V | github.com/MIAU-rgb/AudioPleer", font=('Arial',6), fg=c['copyright'], bg=c['bg']).pack(side='left', padx=5)
        btn_frame = tk.Frame(bottom_frame, bg=c['bg'])
        btn_frame.pack(side='right', padx=5)
        sbtn = {'font':('Arial',6,'bold'),'bg':c['social_btn'],'fg':'white','relief':'flat','padx':7,'pady':1}
        tk.Button(btn_frame, text="VK", command=self.copy_vk, **sbtn).pack(side='left', padx=2)
        tk.Button(btn_frame, text="TG", command=self.copy_tg, **sbtn).pack(side='left', padx=2)
        tk.Button(btn_frame, text="DS", command=self.copy_ds, **sbtn).pack(side='left', padx=2)
        tk.Label(btn_frame, text="│", font=('Arial',7), fg='#555', bg=c['bg']).pack(side='left', padx=5)
        for sm in ["HD","2K","4K"]:
            is_active = (self.screen_mode == sm)
            cfg = {'font':('Arial',6,'bold'),'relief':'flat','padx':6,'pady':1,'bg':c['accent'] if is_active else c['screen_btn'],'fg':c['yellow'] if is_active else '#888'}
            tk.Button(btn_frame, text=sm, command=lambda m=sm: self.set_screen_mode(m), **cfg).pack(side='left', padx=1)
        
        self.update_playlists_list()
        self.change_volume(self.volume)
    
    # ====== ОСТАЛЬНЫЕ МЕТОДЫ (воспроизведение, мини-плеер и т.д.) ======
    # Все методы которые были в версии 2.3V остаются здесь без изменений
    # (play_current_track, play_pause, next_track, prev_track, change_volume, seek_track,
    #  update_time, create_mini_player, toggle_mini_player, minimize_to_mini,
    #  toggle_shuffle, show_search, export_playlist, refresh_music, create_playlist, rename_playlist)
    
    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        if self.shuffle_mode and self.current_playlist in self.playlists:
            tracks = self.playlists[self.current_playlist]['tracks']
            if tracks:
                self.original_tracks = tracks.copy()
                self.shuffled_tracks = tracks.copy()
                random.shuffle(self.shuffled_tracks)
                self.playlists[self.current_playlist]['tracks'] = self.shuffled_tracks
                self.current_track_index = 0
                self.update_tracks_list()
                self.play_current_track()
        elif not self.shuffle_mode and self.original_tracks:
            self.playlists[self.current_playlist]['tracks'] = self.original_tracks
            self.shuffled_tracks = []
            self.original_tracks = []
            self.update_tracks_list()
        self.save_settings()
    
    def show_search(self):
        c = self.colors
        if self.search_dialog and self.search_dialog.winfo_exists(): self.search_dialog.destroy()
        self.search_dialog = tk.Toplevel(self.root)
        self.search_dialog.title("Поиск")
        self.search_dialog.geometry("380x320")
        self.search_dialog.configure(bg=c['panel'])
        tk.Label(self.search_dialog, text="Поиск треков", font=('Arial',12,'bold'), fg='white', bg=c['panel']).pack(pady=8)
        search_entry = tk.Entry(self.search_dialog, font=('Arial',10), bg=c['bg'], fg='white')
        search_entry.pack(fill='x', padx=12, ipady=3)
        results_list = tk.Listbox(self.search_dialog, bg=c['bg'], fg='white', font=('Arial',9))
        results_list.pack(fill='both', expand=True, padx=12, pady=8)
        def search(*args):
            query = search_entry.get().lower()
            results_list.delete(0, 'end')
            for pl_name, pl_data in self.playlists.items():
                for track in pl_data['tracks']:
                    if query in track['title'].lower() or query in track['artist'].lower():
                        results_list.insert('end', f"{track['title']} - {track['artist']}")
        search_entry.bind('<KeyRelease>', search)
        def play_selected():
            sel = results_list.curselection()
            if sel:
                text = results_list.get(sel[0])
                for pl_name, pl_data in self.playlists.items():
                    for i, track in enumerate(pl_data['tracks']):
                        if track['title'] in text:
                            self.current_playlist = pl_name
                            self.current_track_index = i
                            self.shuffle_mode = False
                            self.shuffled_tracks = []
                            self.original_tracks = []
                            self.play_current_track()
                            self.search_dialog.destroy()
                            return
        tk.Button(self.search_dialog, text="▶ Играть", font=('Arial',9,'bold'), bg=c['btn_bg'], fg='white', relief='flat', padx=12, pady=4, command=play_selected).pack(pady=5)
    
    def toggle_mini_player(self):
        if self.mini_player and self.mini_player.winfo_exists():
            self.mini_player.destroy()
            self.mini_player = None
            self.root.deiconify()
        else:
            self.minimize_to_mini()
    
    def minimize_to_mini(self):
        if self.mini_player and self.mini_player.winfo_exists(): return
        self.root.withdraw()
        self.create_mini_player()
    
    def create_mini_player(self):
        c = self.colors
        self.mini_player = tk.Toplevel(self.root)
        self.mini_player.title("Mini")
        min_x, min_y, max_x, max_y = self.get_screen_bounds()
        self.mini_player.geometry(f"280x130+{max_x}+{max_y}")
        self.mini_player.overrideredirect(True)
        self.mini_player.attributes('-topmost', True)
        self.mini_player.configure(bg=c['mini_bg'])
        self.mini_x = None; self.mini_y = None
        rb, ra, rt, rs = c['mini_bg'], c['mini_accent'], c['mini_text'], c['mini_secondary']
        mf = tk.Frame(self.mini_player, bg=rb)
        mf.pack(fill='both', expand=True, padx=1, pady=1)
        tb = tk.Frame(mf, bg=rs, height=16)
        tb.pack(fill='x'); tb.pack_propagate(False)
        tk.Label(tb, text="HALEX 2.31V", font=('Segoe UI',5,'bold'), fg=ra, bg=rs).pack(side='left', padx=4)
        tbf = tk.Frame(tb, bg=rs); tbf.pack(side='right')
        tk.Button(tbf, text="—", font=('Arial',5), bg=rs, fg=rt, relief='flat', bd=0, padx=4, command=self.root.deiconify).pack(side='left')
        tk.Button(tbf, text="✕", font=('Arial',5,'bold'), bg=rs, fg='#ff4444', relief='flat', bd=0, padx=4, command=self.close_mini_player).pack(side='left')
        ct = tk.Frame(mf, bg=rb); ct.pack(fill='both', expand=True, padx=5, pady=1)
        self.mini_track_label = tk.Label(ct, text="Нет трека", font=('Segoe UI',7,'bold'), fg=rt, bg=rb, anchor='w')
        self.mini_track_label.pack(fill='x')
        self.mini_progress = ttk.Progressbar(ct, length=250, mode='determinate')
        self.mini_progress.pack(fill='x', pady=1)
        ctrl = tk.Frame(ct, bg=rb); ctrl.pack(pady=1)
        bs = {'font':('Arial',8),'bg':rb,'fg':rt,'relief':'flat','bd':0,'padx':3}
        tk.Button(ctrl, text="⏮", **bs, command=self.prev_track).pack(side='left')
        self.mini_play_btn = tk.Button(ctrl, text="▶️", **bs, command=self.play_pause)
        self.mini_play_btn.pack(side='left', padx=3)
        tk.Button(ctrl, text="⏭", **bs, command=self.next_track).pack(side='left')
        tk.Button(ctrl, text="🔀", **bs, command=self.toggle_shuffle).pack(side='left', padx=(4,0))
        tk.Button(ctrl, text="🔄", **bs, command=self.refresh_music).pack(side='left', padx=2)
        vf = tk.Frame(ct, bg=rb); vf.pack(fill='x', pady=1)
        tk.Button(vf, text="➖", font=('Arial',5), bg=rs, fg=rt, relief='flat', bd=0, padx=2, command=lambda:self.change_volume_mini(-5)).pack(side='left')
        self.mini_volume_var = tk.DoubleVar(value=self.volume_var.get())
        ttk.Scale(vf, from_=0, to=100, variable=self.mini_volume_var, orient='horizontal', length=150, command=self.change_volume_mini_scale).pack(side='left', padx=2)
        tk.Button(vf, text="➕", font=('Arial',5), bg=rs, fg=rt, relief='flat', bd=0, padx=2, command=lambda:self.change_volume_mini(5)).pack(side='left')
        self.mini_volume_label = tk.Label(vf, text=f"{int(self.volume_var.get())}%", font=('Segoe UI',5), fg='#8b949e', bg=rb)
        self.mini_volume_label.pack(side='left', padx=2)
        tb.bind('<Button-1>', self.start_move_mini)
        tb.bind('<ButtonRelease-1>', self.stop_move_mini)
        tb.bind('<B1-Motion>', self.do_move_mini)
        self.update_mini_player()
    
    def change_volume_mini(self, delta):
        new_vol = max(0, min(100, self.volume_var.get() + delta))
        self.volume_var.set(new_vol); self.mini_volume_var.set(new_vol)
        self.change_volume(new_vol)
        self.mini_volume_label.config(text=f"{int(new_vol)}%")
    
    def change_volume_mini_scale(self, value):
        vol = float(value)
        self.volume_var.set(vol); self.change_volume(vol)
        self.mini_volume_label.config(text=f"{int(vol)}%")
    
    def start_move_mini(self, event):
        self.mini_x = event.x; self.mini_y = event.y
    
    def stop_move_mini(self, event):
        self.mini_x = None; self.mini_y = None
    
    def do_move_mini(self, event):
        if self.mini_x and self.mini_y:
            new_x = self.mini_player.winfo_x() + event.x - self.mini_x
            new_y = self.mini_player.winfo_y() + event.y - self.mini_y
            min_x, min_y, max_x, max_y = self.get_screen_bounds()
            if new_x < min_x: new_x = min_x
            if new_y < min_y: new_y = min_y
            if new_x > max_x: new_x = max_x
            if new_y > max_y: new_y = max_y
            self.mini_player.geometry(f"+{new_x}+{new_y}")
    
    def close_mini_player(self):
        self.mini_player.destroy()
        self.mini_player = None
        self.root.deiconify()
    
    def update_mini_player(self):
        if self.mini_player and self.mini_player.winfo_exists():
            self.mini_play_btn.config(text="⏸" if self.is_playing else "▶️")
            if self.current_playlist and self.current_track_index >= 0:
                tracks = self.playlists[self.current_playlist]['tracks']
                if self.current_track_index < len(tracks):
                    t = tracks[self.current_track_index]
                    self.mini_track_label.config(text=t['title'][:25])
                    if t['duration'] > 0:
                        self.mini_progress['value'] = min(100, (self.current_time / t['duration']) * 100)
        self.root.after(500, self.update_mini_player)
    
    def show_notification(self, title, artist):
        if self.mini_player and self.mini_player.winfo_exists():
            notif = tk.Toplevel(self.mini_player)
            notif.title("")
            notif.geometry("200x40")
            notif.overrideredirect(True)
            notif.attributes('-topmost', True)
            notif.configure(bg='#0d1117')
            notif.geometry(f"+{self.mini_player.winfo_x()+30}+{self.mini_player.winfo_y()-45}")
            f = tk.Frame(notif, bg='#161b22'); f.pack(fill='both', expand=True, padx=1, pady=1)
            tk.Label(f, text=f"🎵 {title[:25]}", font=('Segoe UI',6,'bold'), fg='#fcb424', bg='#161b22').pack(pady=(3,0))
            tk.Label(f, text=artist[:25], font=('Segoe UI',5), fg='#8b949e', bg='#161b22').pack(pady=(0,2))
            notif.after(3000, notif.destroy)
    
    def play_current_track(self):
        if self.current_playlist and self.current_track_index >= 0:
            tracks = self.playlists[self.current_playlist]['tracks']
            if self.current_track_index < len(tracks):
                t = tracks[self.current_track_index]
                pygame.mixer.music.load(t['path'])
                pygame.mixer.music.play()
                self.is_playing = True; self.is_paused = False; self.current_time = 0
                self.current_track_label.config(text=f"🎵 {t['title'][:35]}")
                self.total_time_label.config(text=t['duration_str'])
                self.show_notification(t['title'], t['artist'])
                self.update_tracks_list()
    
    def play_pause(self):
        if self.is_playing:
            if self.is_paused:
                pygame.mixer.music.unpause(); self.is_paused = False
            else:
                pygame.mixer.music.pause(); self.is_paused = True
        else:
            if self.current_track_index == -1 and self.current_playlist:
                tracks = self.playlists[self.current_playlist]['tracks']
                if tracks: self.current_track_index = 0
            self.play_current_track()
    
    def next_track(self):
        if self.current_playlist:
            tracks = self.playlists[self.current_playlist]['tracks']
            self.current_track_index = (self.current_track_index + 1) % len(tracks) if tracks else -1
            self.play_current_track()
    
    def prev_track(self):
        if self.current_track_index > 0:
            self.current_track_index -= 1
            self.play_current_track()
    
    def change_volume(self, value):
        self.volume = int(float(value))
        pygame.mixer.music.set_volume(self.volume / 100)
        self.volume_label.config(text=f"{self.volume}%")
        self.save_settings()
    
    def seek_track(self, value):
        if self.is_playing and self.current_playlist:
            tracks = self.playlists[self.current_playlist]['tracks']
            if self.current_track_index < len(tracks):
                t = tracks[self.current_track_index]
                if t['duration'] > 0:
                    pygame.mixer.music.play(start=float(value) * t['duration'] / 100)
                    self.current_time = int(float(value) * t['duration'] / 100)
    
    def update_time(self):
        if self.is_playing and not self.is_paused:
            self.current_time += 1
            self.current_time_label.config(text=f"{self.current_time//60}:{self.current_time%60:02d}")
            if self.current_playlist:
                tracks = self.playlists[self.current_playlist]['tracks']
                if self.current_track_index < len(tracks):
                    t = tracks[self.current_track_index]
                    if t['duration'] > 0:
                        self.progress_var.set(min(100, (self.current_time / t['duration']) * 100))
            if not pygame.mixer.music.get_busy() and self.is_playing:
                self.next_track(); self.current_time = 0
        self.root.after(1000, self.update_time)
    
    def update_playlists_list(self):
        self.playlist_listbox.delete(0, 'end')
        for pl_folder, pl_data in self.playlists.items():
            self.playlist_listbox.insert('end', f"{pl_data['name']} ({len(pl_data['tracks'])})")
    
    def update_tracks_list(self):
        for item in self.tracks_tree.get_children(): self.tracks_tree.delete(item)
        if self.current_playlist in self.playlists:
            for i, t in enumerate(self.playlists[self.current_playlist]['tracks'], 1):
                self.tracks_tree.insert('', 'end', values=(i, t['title'][:28], t['artist'][:22], t['duration_str']))
    
    def on_playlist_select(self, event):
        sel = self.playlist_listbox.curselection()
        if sel:
            pl_folders = list(self.playlists.keys())
            if sel[0] < len(pl_folders):
                self.current_playlist = pl_folders[sel[0]]
                self.shuffle_mode = False; self.shuffled_tracks = []; self.original_tracks = []
                self.update_tracks_list(); self.save_info()
    
    def play_selected_track(self, event):
        sel = self.tracks_tree.selection()
        if sel:
            item = self.tracks_tree.item(sel[0])
            idx = int(item['values'][0]) - 1
            if self.current_playlist and idx < len(self.playlists[self.current_playlist]['tracks']):
                self.current_track_index = idx
                self.play_current_track()
    
    def create_playlist(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Новый плейлист"); dialog.geometry("280x160"); dialog.configure(bg='#1a1a1a')
        tk.Label(dialog, text="Создание плейлиста", font=('Arial',11,'bold'), fg='white', bg='#1a1a1a').pack(pady=8)
        tk.Label(dialog, text="Название:", fg='#aaa', bg='#1a1a1a').pack()
        name_entry = tk.Entry(dialog, font=('Arial',9), bg='#0a0a0a', fg='white')
        name_entry.pack(pady=6, ipady=2, ipadx=6)
        def create():
            name = name_entry.get().strip()
            if name:
                fp = os.path.join(self.music_folder, name.replace(' ','_'))
                if not os.path.exists(fp): os.makedirs(fp)
                self.playlists[name.replace(' ','_')] = {'name':name,'folder':name.replace(' ','_'),'tracks':[]}
                self.save_info(); self.update_playlists_list(); dialog.destroy()
                messagebox.showinfo("HalexMusic", f"Плейлист '{name}' создан!")
        tk.Button(dialog, text="Создать", font=('Arial',9,'bold'), bg='#8A2BE2', fg='white', relief='flat', padx=12, pady=4, command=create).pack(pady=8)
    
    def rename_playlist(self):
        sel = self.playlist_listbox.curselection()
        if not sel: messagebox.showwarning("HalexMusic", "Выберите плейлист!"); return
        old = list(self.playlists.keys())[sel[0]]
        dialog = tk.Toplevel(self.root)
        dialog.title("Переименовать"); dialog.geometry("280x140"); dialog.configure(bg='#1a1a1a')
        tk.Label(dialog, text="Новое название:", fg='white', bg='#1a1a1a').pack(pady=8)
        name_entry = tk.Entry(dialog, font=('Arial',9), bg='#0a0a0a', fg='white')
        name_entry.insert(0, self.playlists[old]['name']); name_entry.pack(pady=6, ipady=2, ipadx=6)
        def rename():
            new_name = name_entry.get().strip()
            if new_name:
                self.playlists[old]['name'] = new_name
                self.save_info(); self.update_playlists_list(); dialog.destroy()
        tk.Button(dialog, text="Переименовать", font=('Arial',9,'bold'), bg='#8A2BE2', fg='white', relief='flat', padx=12, pady=4, command=rename).pack(pady=8)
    
    def refresh_music(self):
        self.scan_music_folders(); self.update_playlists_list(); self.update_tracks_list()
        self.shuffle_mode = False; self.shuffled_tracks = []; self.original_tracks = []
        messagebox.showinfo("HalexMusic 2.31V", "Музыка обновлена!")
    
    def run(self):
        self.root.mainloop()
        pygame.mixer.music.stop(); pygame.mixer.quit(); pygame.quit()

if __name__ == '__main__':
    app = MusicPlayer()
    app.run()
