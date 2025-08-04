import tkinter as tk
from tkinter import ttk, messagebox
import win32gui
import win32con
import win32api
import win32process
import psutil
from typing import Dict, List
import threading
import time
import os

class ModernButton(tk.Button):
    """Botão moderno personalizado"""
    def __init__(self, master, **kwargs):
        # Extrair parâmetros customizados antes de passar para o tk.Button
        hover_bg = kwargs.pop('hover_bg', '#4f46e5')
        active_bg = kwargs.pop('active_bg', '#4338ca')
        
        super().__init__(master, **kwargs)
        self.configure(
            relief="flat",
            borderwidth=0,
            font=('Segoe UI', 9, 'bold'),
            cursor="hand2",
            padx=15,
            pady=8,
            height=2,
            width=12
        )
        
        # Cores padrão
        self.normal_bg = kwargs.get('bg', '#6366f1')
        self.hover_bg = hover_bg
        self.active_bg = active_bg
        self.fg = kwargs.get('fg', '#ffffff')
        
        self.configure(bg=self.normal_bg, fg=self.fg)
        
        # Bindings para efeitos hover
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        
    def on_enter(self, e):
        self.configure(bg=self.hover_bg)
        
    def on_leave(self, e):
        self.configure(bg=self.normal_bg)
        
    def on_click(self, e):
        self.configure(bg=self.active_bg)
        self.after(100, lambda: self.configure(bg=self.normal_bg))

class ModernSlider(tk.Scale):
    """Slider moderno personalizado"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            relief="flat",
            borderwidth=0,
            font=('Segoe UI', 9),
            bg='#1e293b',
            fg='#ffffff',
            highlightthickness=0,
            troughcolor='#334155',
            activebackground='#6366f1',
            sliderrelief="flat",
            sliderlength=20
        )

class ModernListbox(tk.Listbox):
    """Listbox moderno personalizado"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            relief="flat",
            borderwidth=1,
            font=('Segoe UI', 9),
            bg='#334155',
            fg='#ffffff',
            selectbackground='#6366f1',
            selectforeground='#ffffff',
            highlightthickness=0,
            activestyle='none'
        )

class WindowOpacityController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎛️ Controlador de Transparência")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        
        # Configurar ícone da aplicação
        try:
            import os
            import ctypes
            
            # Tentar diferentes caminhos para o ícone
            possible_paths = [
                "window.ico",
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "window.ico"),
                os.path.abspath("window.ico")
            ]
            
            icon_loaded = False
            for icon_path in possible_paths:
                if os.path.exists(icon_path):
                    try:
                        # Método 1: Usar iconbitmap
                        self.root.iconbitmap(icon_path)
                        
                        # Método 2: Definir ícone para a barra de tarefas (Windows)
                        try:
                            # Obter handle da janela
                            hwnd = self.root.winfo_id()
                            # Definir ícone para a barra de tarefas
                            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("OpacityWindow.App")
                        except:
                            pass
                        
                        print(f"✅ Ícone carregado com sucesso: {icon_path}")
                        icon_loaded = True
                        break
                    except Exception as e:
                        print(f"❌ Erro ao carregar ícone de {icon_path}: {e}")
                        continue
            
            if not icon_loaded:
                print("⚠️ Não foi possível carregar o ícone")
                
        except Exception as e:
            print(f"❌ Erro geral ao carregar ícone: {e}")
            # Se não conseguir carregar o ícone, continua sem ele
            pass
        
        # Configurar cores e estilo
        self.setup_styles()
        
        # Variáveis
        self.windows_data: Dict[str, dict] = {}
        self.applied_windows: Dict[str, dict] = {}  # Janelas com opacidade aplicada
        self.selected_window = tk.StringVar()
        self.opacity_value = tk.DoubleVar(value=100)
        self.show_only_exe = tk.BooleanVar(value=True)  # Filtrar apenas .exe
        
        # Criar interface
        self.create_widgets()
        
        # Atualizar lista de janelas periodicamente
        self.update_windows_list()
        
    def setup_styles(self):
        """Configurar estilos modernos para a interface"""
        # Cores modernas
        self.colors = {
            'bg_dark': '#0f172a',
            'bg_medium': '#1e293b',
            'bg_light': '#334155',
            'primary': '#6366f1',
            'primary_hover': '#4f46e5',
            'primary_active': '#4338ca',
            'success': '#10b981',
            'success_hover': '#059669',
            'warning': '#f59e0b',
            'warning_hover': '#d97706',
            'danger': '#ef4444',
            'danger_hover': '#dc2626',
            'text_primary': '#ffffff',
            'text_secondary': '#94a3b8',
            'border': '#475569'
        }
        
        # Configurar janela principal
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Configurar estilo ttk
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilos
        style.configure('Main.TFrame', background=self.colors['bg_dark'])
        style.configure('Card.TFrame', background=self.colors['bg_medium'])
        style.configure('Title.TLabel', 
                       background=self.colors['bg_dark'], 
                       foreground=self.colors['text_primary'], 
                       font=('Segoe UI', 16, 'bold'))
        style.configure('Subtitle.TLabel', 
                       background=self.colors['bg_medium'], 
                       foreground=self.colors['text_primary'], 
                       font=('Segoe UI', 11, 'bold'))
        style.configure('Text.TLabel', 
                       background=self.colors['bg_medium'], 
                       foreground=self.colors['text_secondary'], 
                       font=('Segoe UI', 9))
        style.configure('Status.TLabel', 
                       background=self.colors['bg_dark'], 
                       foreground=self.colors['text_secondary'], 
                       font=('Segoe UI', 8))
        style.configure('TCheckbutton', 
                       background=self.colors['bg_medium'], 
                       foreground=self.colors['text_primary'], 
                       font=('Segoe UI', 9))
        
    def create_widgets(self):
        """Criar todos os widgets da interface"""
        # Frame principal com padding
        main_frame = ttk.Frame(self.root, style='Main.TFrame', padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header com título
        header_frame = ttk.Frame(main_frame, style='Main.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(header_frame, 
                               text="🎛️ Controlador de Transparência", 
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Maximize sua produtividade com monitor único", 
                                  style='Text.TLabel')
        subtitle_label.pack(pady=(3, 0))
        
        # Frame para as duas listas lado a lado
        lists_frame = ttk.Frame(main_frame, style='Main.TFrame')
        lists_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Lista 1: Janelas Disponíveis
        available_card = ttk.Frame(lists_frame, style='Card.TFrame', padding="12")
        available_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        available_title = ttk.Label(available_card, 
                                   text="📋 Janelas Disponíveis", 
                                   style='Subtitle.TLabel')
        available_title.pack(anchor=tk.W, pady=(0, 8))
        
        # Checkbox para filtrar apenas .exe
        filter_frame = ttk.Frame(available_card, style='Card.TFrame')
        filter_frame.pack(fill=tk.X, pady=(0, 8))
        
        self.filter_checkbox = ttk.Checkbutton(filter_frame, 
                                               text="Mostrar apenas processos .exe", 
                                               variable=self.show_only_exe,
                                               command=self.update_windows_list,
                                               style='Text.TLabel')
        self.filter_checkbox.pack(anchor=tk.W)
        
        # Listbox para janelas disponíveis
        available_listbox_frame = ttk.Frame(available_card, style='Card.TFrame')
        available_listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.available_listbox = ModernListbox(available_listbox_frame, height=10)
        available_scrollbar = ttk.Scrollbar(available_listbox_frame, orient=tk.VERTICAL, command=self.available_listbox.yview)
        self.available_listbox.configure(yscrollcommand=available_scrollbar.set)
        
        self.available_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 3))
        available_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Binding para seleção
        self.available_listbox.bind('<<ListboxSelect>>', self.on_available_select)
        
        # Lista 2: Janelas com Opacidade Aplicada
        applied_card = ttk.Frame(lists_frame, style='Card.TFrame', padding="12")
        applied_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))
        
        applied_title = ttk.Label(applied_card, 
                                 text="🎨 Janelas com Transparência", 
                                 style='Subtitle.TLabel')
        applied_title.pack(anchor=tk.W, pady=(0, 8))
        
        # Listbox para janelas com opacidade aplicada
        applied_listbox_frame = ttk.Frame(applied_card, style='Card.TFrame')
        applied_listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.applied_listbox = ModernListbox(applied_listbox_frame, height=10)
        applied_scrollbar = ttk.Scrollbar(applied_listbox_frame, orient=tk.VERTICAL, command=self.applied_listbox.yview)
        self.applied_listbox.configure(yscrollcommand=applied_scrollbar.set)
        
        self.applied_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 3))
        applied_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Binding para seleção
        self.applied_listbox.bind('<<ListboxSelect>>', self.on_applied_select)
        
        # Card para controles de transparência
        opacity_card = ttk.Frame(main_frame, style='Card.TFrame', padding="12")
        opacity_card.pack(fill=tk.X, pady=(0, 12))
        
        # Título do card
        opacity_title = ttk.Label(opacity_card, 
                                 text="🎚️ Controle de Transparência", 
                                 style='Subtitle.TLabel')
        opacity_title.pack(anchor=tk.W, pady=(0, 8))
        
        # Frame para slider
        slider_frame = ttk.Frame(opacity_card, style='Card.TFrame')
        slider_frame.pack(fill=tk.X, pady=(0, 8))
        
        # Slider moderno
        self.opacity_slider = ModernSlider(slider_frame, 
                                          from_=0, 
                                          to=100, 
                                          orient=tk.HORIZONTAL,
                                          variable=self.opacity_value,
                                          command=self.on_opacity_change)
        self.opacity_slider.pack(fill=tk.X)
        
        # Label para valor atual
        self.opacity_value_label = ttk.Label(slider_frame, 
                                            text="100%", 
                                            style='Text.TLabel')
        self.opacity_value_label.pack(pady=(3, 0))
        
        # Card para botões
        buttons_card = ttk.Frame(main_frame, style='Card.TFrame', padding="12")
        buttons_card.pack(fill=tk.X, pady=(0, 12))
        
        # Título do card
        buttons_title = ttk.Label(buttons_card, 
                                 text="⚡ Ações", 
                                 style='Subtitle.TLabel')
        buttons_title.pack(anchor=tk.W, pady=(0, 8))
        
        # Frame para botões - 2x2 grid
        buttons_frame = ttk.Frame(buttons_card, style='Card.TFrame')
        buttons_frame.pack(fill=tk.X)
        
        # Primeira linha de botões
        buttons_row1 = ttk.Frame(buttons_frame, style='Card.TFrame')
        buttons_row1.pack(fill=tk.X, pady=(0, 8))
        
        # Botão aplicar transparência
        apply_button = ModernButton(buttons_row1, 
                                   text="✅ Aplicar", 
                                   command=self.apply_opacity,
                                   bg=self.colors['success'],
                                   hover_bg=self.colors['success_hover'],
                                   active_bg=self.colors['success_hover'])
        apply_button.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        # Botão resetar janela específica
        reset_button = ModernButton(buttons_row1, 
                                   text="🔄 Resetar", 
                                   command=self.reset_selected_opacity,
                                   bg=self.colors['warning'],
                                   hover_bg=self.colors['warning_hover'],
                                   active_bg=self.colors['warning_hover'])
        reset_button.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        # Segunda linha de botões
        buttons_row2 = ttk.Frame(buttons_frame, style='Card.TFrame')
        buttons_row2.pack(fill=tk.X)
        
        # Botão resetar todas
        reset_all_button = ModernButton(buttons_row2, 
                                       text="🔄 Resetar Todas", 
                                       command=self.reset_all_opacity,
                                       bg=self.colors['danger'],
                                       hover_bg=self.colors['danger_hover'],
                                       active_bg=self.colors['danger_hover'])
        reset_all_button.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        # Botão atualizar lista
        refresh_button = ModernButton(buttons_row2, 
                                     text="🔄 Atualizar", 
                                     command=self.update_windows_list,
                                     bg=self.colors['primary'],
                                     hover_bg=self.colors['primary_hover'],
                                     active_bg=self.colors['primary_active'])
        refresh_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Status bar
        status_frame = ttk.Frame(main_frame, style='Main.TFrame')
        status_frame.pack(fill=tk.X, pady=(8, 0))
        
        self.status_label = ttk.Label(status_frame, 
                                     text="✨ Pronto para usar", 
                                     style='Status.TLabel')
        self.status_label.pack()
        
    def get_windows_list(self) -> List[dict]:
        """Obter lista de janelas abertas com informações do processo"""
        windows = []
        try:
            # Usar win32gui para enumerar todas as janelas
            def enum_windows_callback(hwnd, windows_list):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if title and title.strip():
                        try:
                            # Obter informações do processo
                            _, pid = win32process.GetWindowThreadProcessId(hwnd)
                            if pid:
                                process = psutil.Process(pid)
                                exe_path = process.exe()
                                exe_name = os.path.basename(exe_path) if exe_path else "Desconhecido"
                                
                                # Filtrar apenas janelas do próprio aplicativo
                                if not any(exclude in title.lower() for exclude in ['controlador de transparência', 'opacity']):
                                    # Incluir todos os processos, mas marcar os .exe
                                    is_exe = exe_path and exe_path.lower().endswith('.exe')
                                    
                                    # Verificar se é uma janela de aplicação válida (não apenas janelas do sistema)
                                    if is_exe or exe_name.lower() in ['cursor.exe', 'code.exe', 'notepad++.exe', 'sublime_text.exe', 'atom.exe', 'vim.exe', 'emacs.exe']:
                                        windows_list.append({
                                            'title': title,
                                            'hwnd': hwnd,
                                            'pid': pid,
                                            'exe_name': exe_name,
                                            'exe_path': exe_path,
                                            'process_name': process.name(),
                                            'is_exe': is_exe
                                        })
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                            # Processo não acessível, mas ainda pode ser uma janela válida
                            try:
                                # Incluir janelas do sistema que podem ser úteis
                                if any(keyword in title.lower() for keyword in ['cursor', 'code', 'notepad', 'chrome', 'firefox', 'edge', 'opera']):
                                    windows_list.append({
                                        'title': title,
                                        'hwnd': hwnd,
                                        'pid': None,
                                        'exe_name': "Sistema",
                                        'exe_path': None,
                                        'process_name': "Sistema",
                                        'is_exe': False
                                    })
                            except:
                                pass
                return True
            
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            # Filtrar janelas duplicadas e ordenar por nome do processo
            unique_windows = []
            seen_titles = set()
            
            for window in windows:
                if window['title'] not in seen_titles:
                    seen_titles.add(window['title'])
                    unique_windows.append(window)
            
            # Ordenar por nome do processo
            unique_windows.sort(key=lambda x: x['exe_name'].lower())
            
        except Exception as e:
            print(f"Erro ao obter janelas: {e}")
            
        return unique_windows
    
    def update_windows_list(self):
        """Atualizar a lista de janelas na interface"""
        try:
            self.available_listbox.delete(0, tk.END)
            self.windows_data.clear()
            
            windows = self.get_windows_list()
            print(f"DEBUG: Encontradas {len(windows)} janelas no total")
            
            for window in windows:
                title = window['title']
                exe_name = window.get('exe_name', 'Desconhecido')
                is_exe = window.get('is_exe', False)
                print(f"DEBUG: Janela encontrada: {title} ({exe_name}) - EXE: {is_exe}")
                
                # Aplicar filtro se necessário
                if self.show_only_exe.get() and not is_exe:
                    continue
                
                # Verificar se a janela já tem opacidade aplicada
                if title not in self.applied_windows:
                    # Criar display com nome do processo e título
                    if exe_name and exe_name != "Desconhecido":
                        display_title = f"{exe_name} - {title}"
                    else:
                        display_title = title
                    
                    # Truncar se for muito longo
                    if len(display_title) > 60:
                        display_title = display_title[:57] + "..."
                    
                    self.available_listbox.insert(tk.END, display_title)
                    self.windows_data[display_title] = window
                    print(f"DEBUG: Adicionada à lista: {display_title}")
            
            self.status_label.config(text=f"📊 Encontradas {len(windows)} janelas disponíveis")
            
        except Exception as e:
            self.status_label.config(text=f"⚠️ Erro: {str(e)}")
            print(f"DEBUG: Erro na atualização: {e}")
    
    def update_applied_list(self):
        """Atualizar a lista de janelas com opacidade aplicada"""
        try:
            self.applied_listbox.delete(0, tk.END)
            
            for title, data in self.applied_windows.items():
                display_title = f"{title[:45]}... ({data['opacity']}%)" if len(title) > 45 else f"{title} ({data['opacity']}%)"
                self.applied_listbox.insert(tk.END, display_title)
                
        except Exception as e:
            print(f"Erro ao atualizar lista aplicada: {e}")
    
    def on_available_select(self, event):
        """Callback quando uma janela disponível é selecionada"""
        selection = self.available_listbox.curselection()
        if selection:
            index = selection[0]
            window_title = self.available_listbox.get(index)
            self.selected_window.set(window_title)
            self.status_label.config(text=f"🎯 Selecionado: {window_title}")
    
    def on_applied_select(self, event):
        """Callback quando uma janela aplicada é selecionada"""
        selection = self.applied_listbox.curselection()
        if selection:
            index = selection[0]
            display_title = self.applied_listbox.get(index)
            # Extrair o título original
            original_title = display_title.split(" (")[0]
            if len(original_title) > 45:
                original_title = original_title[:-3]  # Remover "..."
            self.selected_window.set(original_title)
            self.status_label.config(text=f"🎨 Selecionado: {original_title}")
    
    def on_opacity_change(self, value):
        """Callback quando o slider é movido"""
        opacity = int(float(value))
        self.opacity_value_label.config(text=f"{opacity}%")
    
    def apply_opacity(self):
        """Aplicar transparência à janela selecionada"""
        if not self.selected_window.get():
            messagebox.showwarning("Aviso", "Por favor, selecione uma janela primeiro!")
            return
        
        try:
            window_title = self.selected_window.get()
            window_data = self.windows_data.get(window_title)
            
            if not window_data:
                messagebox.showerror("Erro", "Janela não encontrada!")
                return
            
            hwnd = window_data['hwnd']
            opacity = int(self.opacity_value.get())
            
            # Converter porcentagem para valor de transparência (0-255)
            alpha = int((opacity / 100) * 255)
            
            # Aplicar transparência usando win32gui
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                                  win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
            win32gui.SetLayeredWindowAttributes(hwnd, 0, alpha, win32con.LWA_ALPHA)
            
            # Adicionar à lista de janelas aplicadas
            original_title = window_data['title']
            self.applied_windows[original_title] = {
                'hwnd': hwnd,
                'opacity': opacity,
                'alpha': alpha
            }
            
            # Atualizar listas
            self.update_windows_list()
            self.update_applied_list()
            
            self.status_label.config(text=f"✅ Transparência aplicada: {opacity}%")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar transparência: {str(e)}")
            self.status_label.config(text="❌ Erro ao aplicar transparência")
    
    def reset_selected_opacity(self):
        """Resetar transparência da janela selecionada"""
        if not self.selected_window.get():
            messagebox.showwarning("Aviso", "Por favor, selecione uma janela primeiro!")
            return
        
        try:
            window_title = self.selected_window.get()
            
            # Procurar na lista de janelas aplicadas
            original_title = None
            for title in self.applied_windows.keys():
                if title.startswith(window_title) or window_title.startswith(title):
                    original_title = title
                    break
            
            if not original_title:
                messagebox.showerror("Erro", "Janela não encontrada na lista de aplicadas!")
                return
            
            hwnd = self.applied_windows[original_title]['hwnd']
            
            # Resetar para opacidade total
            win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
            
            # Remover da lista de aplicadas
            del self.applied_windows[original_title]
            
            # Atualizar listas
            self.update_windows_list()
            self.update_applied_list()
            
            self.status_label.config(text="🔄 Transparência resetada com sucesso")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao resetar transparência: {str(e)}")
            self.status_label.config(text="❌ Erro ao resetar transparência")
    
    def reset_all_opacity(self):
        """Resetar transparência de todas as janelas"""
        try:
            if not self.applied_windows:
                messagebox.showinfo("Info", "Nenhuma janela com transparência aplicada!")
                return
            
            # Resetar todas as janelas
            for title, data in self.applied_windows.items():
                try:
                    hwnd = data['hwnd']
                    win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
                except:
                    continue
            
            # Limpar lista de aplicadas
            self.applied_windows.clear()
            
            # Atualizar listas
            self.update_windows_list()
            self.update_applied_list()
            
            self.status_label.config(text="🔄 Todas as transparências foram resetadas")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao resetar todas as transparências: {str(e)}")
            self.status_label.config(text="❌ Erro ao resetar todas as transparências")
    
    def run(self):
        """Executar o programa"""
        # Centralizar janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f"900x750+{x}+{y}")
        
        # Forçar atualização do ícone na barra de tarefas
        try:
            import ctypes
            # Definir ID único para a aplicação
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("OpacityWindow.App")
            # Forçar atualização da barra de tarefas
            self.root.update()
        except:
            pass
        
        # Iniciar thread para atualizar lista periodicamente
        def update_loop():
            while True:
                time.sleep(3)  # Atualizar a cada 3 segundos
                try:
                    self.root.after(0, self.update_windows_list)
                except:
                    break
        
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        
        # Executar interface
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = WindowOpacityController()
        app.run()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        input("Pressione Enter para sair...") 