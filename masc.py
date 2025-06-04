import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import random
import time
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import io
import math
import threading

class ResponsivePetZoneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PetZone")
        
        # Configuración responsive
        self.setup_responsive_window()
        
        # Variables para el tema
        self.is_dark_mode = False
        self.update_theme_colors()
        
        # Configurar fuentes responsivas
        self.setup_responsive_fonts()
        
        # Variables para almacenar datos de usuario
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.new_username_var = tk.StringVar()
        self.new_password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        self.search_var = tk.StringVar()
        
        # Variables para animaciones
        self.current_frame = None
        self.animation_in_progress = False
        
        # Datos de ejemplo para el carrito (precios en pesos argentinos)
        self.cart_items = []
        self.products = [
            {"id": 1, "name": "Comida para perros", "price": 15990, "category": "Alimentos", "rating": 4.5, "image": self.create_pet_image("dog_food")},
            {"id": 2, "name": "Juguete para gatos", "price": 8500, "category": "Juguetes", "rating": 4.2, "image": self.create_pet_image("cat_toy")},
            {"id": 3, "name": "Correa para paseo", "price": 12750, "category": "Accesorios", "rating": 4.0, "image": self.create_pet_image("leash")},
            {"id": 4, "name": "Cama para mascotas", "price": 24990, "category": "Hogar", "rating": 4.8, "image": self.create_pet_image("pet_bed")},
            {"id": 5, "name": "Shampoo para perros", "price": 9990, "category": "Higiene", "rating": 4.3, "image": self.create_pet_image("shampoo")},
            {"id": 6, "name": "Rascador para gatos", "price": 18500, "category": "Hogar", "rating": 4.6, "image": self.create_pet_image("scratcher")},
            {"id": 7, "name": "Comedero automático", "price": 32990, "category": "Alimentación", "rating": 4.7, "image": self.create_pet_image("feeder")},
            {"id": 8, "name": "Juguete interactivo", "price": 14500, "category": "Juguetes", "rating": 4.4, "image": self.create_pet_image("toy")}
        ]
        
        # Categorías de productos
        self.categories = ["Todos", "Alimentos", "Juguetes", "Accesorios", "Hogar", "Higiene", "Alimentación"]
        self.selected_category = "Todos"
        
        # Crear frames para cada pantalla
        self.welcome_frame = tk.Frame(self.root)
        self.login_frame = tk.Frame(self.root)
        self.register_frame = tk.Frame(self.root)
        self.home_frame = tk.Frame(self.root)
        self.cart_frame = tk.Frame(self.root)
        self.product_detail_frame = tk.Frame(self.root)
        self.profile_frame = tk.Frame(self.root)
        
        # Inicializar todas las pantallas
        self.setup_welcome_screen()
        self.setup_login_screen()
        self.setup_register_screen()
        self.setup_home_screen()
        self.setup_cart_screen()
        self.setup_product_detail_screen()
        self.setup_profile_screen()
        
        # Configurar eventos de redimensionamiento
        self.root.bind('<Configure>', self.on_window_resize)
        
        # Mostrar la pantalla de bienvenida al inicio
        self.show_frame_with_animation(self.welcome_frame)
        
        # Iniciar animaciones de fondo
        self.start_background_animations()
    
    def setup_responsive_window(self):
        """Configura la ventana para ser responsive"""
        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Determinar si es móvil (ancho menor a 600px)
        self.is_mobile = screen_width < 600
        
        if self.is_mobile:
            # Configuración para móvil
            self.window_width = min(screen_width - 20, 400)
            self.window_height = min(screen_height - 100, 700)
            self.root.geometry(f"{self.window_width}x{self.window_height}")
            # Centrar en pantalla
            x = (screen_width - self.window_width) // 2
            y = (screen_height - self.window_height) // 2
            self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        else:
            # Configuración para desktop
            self.window_width = 400
            self.window_height = 700
            self.root.geometry(f"{self.window_width}x{self.window_height}")
        
        # Configurar redimensionamiento
        self.root.minsize(320, 500)  # Tamaño mínimo
        self.root.maxsize(600, 900)  # Tamaño máximo
        
        # Permitir redimensionamiento
        self.root.resizable(True, True)
    
    def setup_responsive_fonts(self):
        """Configura fuentes que se adaptan al tamaño de pantalla"""
        base_size = 10 if self.is_mobile else 12
        
        self.title_font = tkfont.Font(family="Arial", size=base_size + 8, weight="bold")
        self.welcome_font = tkfont.Font(family="Arial", size=base_size + 6, slant="italic")
        self.button_font = tkfont.Font(family="Arial", size=base_size)
        self.label_font = tkfont.Font(family="Arial", size=base_size - 1)
        self.copyright_font = tkfont.Font(family="Arial", size=base_size - 2)
    
    def on_window_resize(self, event):
        """Maneja el redimensionamiento de la ventana"""
        if event.widget == self.root:
            # Actualizar variables de tamaño
            self.window_width = self.root.winfo_width()
            self.window_height = self.root.winfo_height()
            
            # Determinar si cambió a móvil
            was_mobile = self.is_mobile
            self.is_mobile = self.window_width < 500
            
            # Si cambió el modo, actualizar fuentes
            if was_mobile != self.is_mobile:
                self.setup_responsive_fonts()
                self.update_all_fonts()
    
    def update_all_fonts(self):
        """Actualiza todas las fuentes en la aplicación"""
        for frame in [self.welcome_frame, self.login_frame, self.register_frame, 
                     self.home_frame, self.cart_frame, self.product_detail_frame,
                     self.profile_frame]:
            self.update_fonts_in_frame(frame)
    
    def update_fonts_in_frame(self, frame):
        """Actualiza fuentes en un frame específico"""
        for widget in frame.winfo_children():
            try:
                widget_type = widget.winfo_class()
                if widget_type in ('Label', 'Button', 'Entry'):
                    current_font = widget.cget('font')
                    if 'title' in str(current_font):
                        widget.configure(font=self.title_font)
                    elif 'welcome' in str(current_font):
                        widget.configure(font=self.welcome_font)
                    elif 'button' in str(current_font):
                        widget.configure(font=self.button_font)
                    elif 'label' in str(current_font):
                        widget.configure(font=self.label_font)
                elif widget_type in ('Frame', 'Labelframe'):
                    self.update_fonts_in_frame(widget)
            except:
                pass
    
    def get_responsive_padding(self, base_padding=10):
        """Calcula padding responsive"""
        if self.is_mobile:
            return max(5, base_padding // 2)
        return base_padding
    
    def get_responsive_size(self, base_size):
        """Calcula tamaño responsive"""
        if self.is_mobile:
            return max(base_size // 2, base_size - 20)
        return base_size
    
    def update_theme_colors(self):
        """Actualiza colores del tema"""
        if not self.is_dark_mode:
            self.bg_color = "#f0f0f0"
            self.fg_color = "#000000"
            self.header_color = "#e69138"
            self.header_text_color = "#000000"
            self.button_color = "#e69138"
            self.button_text_color = "#000000"
            self.card_bg = "#ffffff"
            self.highlight_color = "#ffd700"
        else:
            self.bg_color = "#121212"
            self.fg_color = "#ffffff"
            self.header_color = "#b36b1d"
            self.header_text_color = "#ffffff"
            self.button_color = "#b36b1d"
            self.button_text_color = "#ffffff"
            self.card_bg = "#1e1e1e"
            self.highlight_color = "#ffd700"
    
    def toggle_theme(self):
        """Cambia entre tema claro y oscuro"""
        self.is_dark_mode = not self.is_dark_mode
        self.update_theme_colors()
        
        for frame in [self.welcome_frame, self.login_frame, self.register_frame, 
                     self.home_frame, self.cart_frame, self.product_detail_frame,
                     self.profile_frame]:
            self.update_frame_colors(frame)
        
        self.flash_screen_animation()
    
    def update_frame_colors(self, frame):
        """Actualiza colores de un frame"""
        frame.configure(bg=self.bg_color)
        
        for widget in frame.winfo_children():
            try:
                widget_type = widget.winfo_class()
                
                if widget_type in ('Frame', 'Labelframe'):
                    widget.configure(bg=self.bg_color)
                    self.update_frame_colors(widget)
                elif widget_type == 'Label':
                    if 'header' in str(widget):
                        widget.configure(bg=self.header_color, fg=self.header_text_color)
                    else:
                        widget.configure(bg=self.bg_color, fg=self.fg_color)
                elif widget_type == 'Button':
                    if 'theme' not in str(widget):
                        widget.configure(bg=self.button_color, fg=self.button_text_color)
                elif widget_type == 'Entry':
                    widget.configure(bg=self.card_bg, fg=self.fg_color)
            except:
                pass
    
    def flash_screen_animation(self):
        """Animación de cambio de tema"""
        overlay = tk.Frame(self.root, bg="white" if self.is_dark_mode else "black")
        overlay.place(x=0, y=0, width=self.window_width, height=self.window_height)
        
        def animate_opacity():
            for alpha in range(10, 0, -1):
                overlay.configure(bg=f"{'white' if self.is_dark_mode else 'black'}")
                overlay.update()
                time.sleep(0.02)
            overlay.destroy()
        
        threading.Thread(target=animate_opacity, daemon=True).start()
    
    def create_pet_image(self, image_type):
        """Crea imágenes de productos simuladas"""
        size = self.get_responsive_size(100)
        image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        
        colors = {
            "dog_food": "#8B4513", "cat_toy": "#FF69B4", "leash": "#4682B4",
            "pet_bed": "#6B8E23", "shampoo": "#87CEEB", "scratcher": "#CD853F",
            "feeder": "#708090", "toy": "#FF6347"
        }
        
        color = colors.get(image_type, "#FF9800")
        
        # Dibujar formas adaptadas al tamaño
        margin = size // 5
        if "food" in image_type:
            draw.ellipse((margin, size//2, size-margin, size-margin//2), fill=color)
            draw.ellipse((margin*1.5, margin*1.5, size-margin*1.5, size//2), fill="#D2B48C")
        elif "toy" in image_type:
            draw.rectangle((margin*1.5, margin*1.5, size-margin*1.5, size-margin*1.5), 
                         fill=color, outline="#000000", width=2)
            draw.ellipse((margin*2, margin*2, size-margin*2, size-margin*2), fill="#FFFFFF")
        else:
            draw.ellipse((margin, margin, size-margin, size-margin), fill=color)
        
        image = image.filter(ImageFilter.GaussianBlur(radius=1))
        return ImageTk.PhotoImage(image)
    
    def show_frame_with_animation(self, frame):
        """Muestra un frame con animación suave"""
        if self.animation_in_progress:
            return
            
        self.animation_in_progress = True
        frame.configure(bg=self.bg_color)
        self.update_frame_colors(frame)
        
        if self.current_frame is None:
            frame.pack(fill=tk.BOTH, expand=True)
            self.current_frame = frame
            self.animation_in_progress = False
            return
        
        old_frame = self.current_frame
        
        # Animación más suave para móvil
        steps = 5 if self.is_mobile else 10
        
        frame.place(x=self.window_width, y=0, width=self.window_width, height=self.window_height)
        
        def animate_transition():
            for i in range(steps):
                old_x = -i * (self.window_width // steps)
                new_x = self.window_width + old_x
                
                old_frame.place(x=old_x)
                frame.place(x=new_x)
                
                self.root.update()
                time.sleep(0.02)
            
            old_frame.place_forget()
            frame.place(x=0, y=0, width=self.window_width, height=self.window_height)
            self.current_frame = frame
            self.animation_in_progress = False
        
        threading.Thread(target=animate_transition, daemon=True).start()
    
    def start_background_animations(self):
        """Inicia animaciones de fondo optimizadas"""
        def animate_background():
            while True:
                if self.current_frame in [self.welcome_frame, self.home_frame] and not self.is_mobile:
                    try:
                        buttons = [w for w in self.current_frame.winfo_children() if isinstance(w, tk.Button)]
                        if buttons:
                            button = random.choice(buttons)
                            original_bg = button.cget("background")
                            button.configure(background=self.highlight_color)
                            time.sleep(0.2)
                            button.configure(background=original_bg)
                    except:
                        pass
                
                time.sleep(random.uniform(5, 10))  # Menos frecuente en móvil
        
        threading.Thread(target=animate_background, daemon=True).start()
    
    def create_responsive_header(self, parent, title_text="PetZone"):
        """Crea un header responsive"""
        # Barra superior más pequeña en móvil
        bar_height = 15 if self.is_mobile else 20
        top_bar = tk.Frame(parent, bg="#333333", height=bar_height)
        top_bar.pack(fill=tk.X)
        
        time_label = tk.Label(
            top_bar, 
            text=time.strftime("%H:%M"),
            font=self.copyright_font,
            bg="#333333",
            fg="#FFFFFF"
        )
        time_label.pack(side=tk.RIGHT, padx=self.get_responsive_padding(5))
        
        # Header adaptativo
        header_height = 50 if self.is_mobile else 60
        header = tk.Frame(parent, bg=self.header_color, height=header_height)
        header.pack(fill=tk.X)
        
        title_label = tk.Label(
            header, 
            text=title_text, 
            font=self.title_font, 
            bg=self.header_color, 
            fg=self.header_text_color
        )
        title_label.pack(pady=self.get_responsive_padding(10))
        
        return header
    
    def create_responsive_footer(self, parent):
        """Crea un footer responsive"""
        footer_height = 30 if self.is_mobile else 40
        footer = tk.Frame(parent, bg=self.bg_color, height=footer_height)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        theme_button = tk.Button(
            footer,
            text="🌙" if not self.is_dark_mode else "☀️",
            font=self.button_font,
            bg=self.bg_color,
            fg=self.fg_color,
            relief=tk.FLAT,
            command=self.toggle_theme
        )
        theme_button.pack(side=tk.LEFT, padx=self.get_responsive_padding(10))
        
        copyright_label = tk.Label(
            footer, 
            text="© PetZone 2025", 
            font=self.copyright_font, 
            bg=self.bg_color,
            fg=self.fg_color
        )
        copyright_label.pack(side=tk.RIGHT, pady=self.get_responsive_padding(5), 
                           padx=self.get_responsive_padding(10))
        
        return footer
    
    def create_hover_effect(self, widget):
        """Añade efecto hover optimizado"""
        if self.is_mobile:
            return  # Desactivar hover en móvil
            
        original_bg = widget.cget("background")
        original_fg = widget.cget("foreground")
        
        def on_enter(e):
            widget.config(background=self.highlight_color, foreground="#000000")
            
        def on_leave(e):
            widget.config(background=original_bg, foreground=original_fg)
            
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def setup_welcome_screen(self):
        """Configura la pantalla de bienvenida responsive"""
        self.create_responsive_header(self.welcome_frame)
        
        content = tk.Frame(self.welcome_frame, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, 
                    padx=self.get_responsive_padding(20), 
                    pady=self.get_responsive_padding(20))
        
        # Logo adaptativo
        logo_size = self.get_responsive_size(200)
        logo_canvas = tk.Canvas(content, width=logo_size, height=logo_size, 
                               bg=self.bg_color, highlightthickness=0)
        logo_canvas.pack(pady=self.get_responsive_padding(20))
        
        # Dibujar logo adaptado
        center = logo_size // 2
        radius = logo_size // 4
        logo_canvas.create_oval(center-radius, center-radius, center+radius, center+radius, 
                               fill=self.button_color, outline="")
        logo_canvas.create_text(center, center, text="PZ", 
                               font=("Arial", logo_size//5, "bold"), fill="#FFFFFF")
        
        # Mensaje de bienvenida
        welcome_label = tk.Label(
            content, 
            text="¡Bienvenidos a PetZone!", 
            font=self.welcome_font, 
            bg=self.bg_color,
            fg=self.fg_color
        )
        welcome_label.pack(pady=self.get_responsive_padding(20))
        
        subtitle_label = tk.Label(
            content, 
            text="Todo lo que tu mascota necesita", 
            font=self.label_font, 
            bg=self.bg_color,
            fg=self.fg_color
        )
        subtitle_label.pack(pady=self.get_responsive_padding(5))
        
        # Botones responsivos
        buttons_frame = tk.Frame(content, bg=self.bg_color)
        buttons_frame.pack(pady=self.get_responsive_padding(30))
        
        button_padding = self.get_responsive_padding(15)
        
        if self.is_mobile:
            # En móvil, botones verticales
            login_button = tk.Button(
                buttons_frame, 
                text="Iniciar sesión", 
                font=self.button_font,
                bg=self.button_color, 
                fg=self.button_text_color,
                relief=tk.RAISED,
                borderwidth=2,
                padx=button_padding,
                pady=self.get_responsive_padding(8),
                command=lambda: self.show_frame_with_animation(self.login_frame)
            )
            login_button.pack(pady=5, fill=tk.X)
            
            register_button = tk.Button(
                buttons_frame, 
                text="Registrarse", 
                font=self.button_font,
                bg=self.button_color, 
                fg=self.button_text_color,
                relief=tk.RAISED,
                borderwidth=2,
                padx=button_padding,
                pady=self.get_responsive_padding(8),
                command=lambda: self.show_frame_with_animation(self.register_frame)
            )
            register_button.pack(pady=5, fill=tk.X)
        else:
            # En desktop, botones horizontales
            login_button = tk.Button(
                buttons_frame, 
                text="Iniciar sesión", 
                font=self.button_font,
                bg=self.button_color, 
                fg=self.button_text_color,
                relief=tk.RAISED,
                borderwidth=2,
                padx=button_padding,
                pady=self.get_responsive_padding(8),
                command=lambda: self.show_frame_with_animation(self.login_frame)
            )
            login_button.pack(side=tk.LEFT, padx=10)
            
            register_button = tk.Button(
                buttons_frame, 
                text="Registrarse", 
                font=self.button_font,
                bg=self.button_color, 
                fg=self.button_text_color,
                relief=tk.RAISED,
                borderwidth=2,
                padx=button_padding,
                pady=self.get_responsive_padding(8),
                command=lambda: self.show_frame_with_animation(self.register_frame)
            )
            register_button.pack(side=tk.LEFT, padx=10)
        
        self.create_hover_effect(login_button)
        self.create_hover_effect(register_button)
        
        guest_button = tk.Button(
            content, 
            text="Continuar como invitado", 
            font=self.label_font,
            bg=self.bg_color, 
            fg=self.fg_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame_with_animation(self.home_frame)
        )
        guest_button.pack(pady=self.get_responsive_padding(10))
        
        self.create_responsive_footer(self.welcome_frame)
    
    def setup_login_screen(self):
        """Configura la pantalla de login responsive"""
        header = self.create_responsive_header(self.login_frame, "Iniciar Sesión")
        
        back_button = tk.Button(
            header,
            text="← Volver",
            font=self.label_font,
            bg=self.header_color,
            fg=self.header_text_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame_with_animation(self.welcome_frame)
        )
        back_button.place(x=10, y=10)
        
        content = tk.Frame(self.login_frame, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, 
                    padx=self.get_responsive_padding(30), 
                    pady=self.get_responsive_padding(30))
        
        # Icono de usuario adaptativo
        icon_size = self.get_responsive_size(100)
        user_canvas = tk.Canvas(content, width=icon_size, height=icon_size, 
                               bg=self.bg_color, highlightthickness=0)
        user_canvas.pack(pady=self.get_responsive_padding(20))
        
        center = icon_size // 2
        radius = icon_size // 4
        user_canvas.create_oval(center-radius//2, center-radius//2, 
                               center+radius//2, center+radius//2, 
                               fill=self.button_color, outline="")
        
        # Campos de login responsivos
        self.create_responsive_input_field(content, "👤", "Usuario:", self.username_var)
        self.create_responsive_input_field(content, "🔒", "Contraseña:", self.password_var, show="•")
        
        # Checkbox responsive
        remember_var = tk.BooleanVar()
        remember_frame = tk.Frame(content, bg=self.bg_color)
        remember_frame.pack(fill=tk.X, pady=self.get_responsive_padding(10))
        
        remember_check = tk.Checkbutton(
            remember_frame,
            text="Recordarme",
            variable=remember_var,
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.card_bg,
            activebackground=self.bg_color,
            activeforeground=self.fg_color
        )
        remember_check.pack(side=tk.LEFT)
        
        # Botón de login responsive
        login_button = tk.Button(
            content, 
            text="Iniciar Sesión", 
            font=self.button_font,
            bg=self.button_color, 
            fg=self.button_text_color,
            relief=tk.RAISED,
            borderwidth=2,
            padx=self.get_responsive_padding(20),
            pady=self.get_responsive_padding(10),
            command=self.do_login
        )
        login_button.pack(pady=self.get_responsive_padding(30), fill=tk.X if self.is_mobile else None)
        
        self.create_responsive_footer(self.login_frame)
    
    def create_responsive_input_field(self, parent, icon, label_text, variable, show=None):
        """Crea un campo de entrada responsive"""
        field_frame = tk.Frame(parent, bg=self.bg_color)
        field_frame.pack(fill=tk.X, pady=self.get_responsive_padding(10))
        
        if not self.is_mobile:
            icon_label = tk.Label(
                field_frame,
                text=icon,
                font=("Arial", 16),
                bg=self.bg_color,
                fg=self.fg_color
            )
            icon_label.pack(side=tk.LEFT, padx=5)
        
        label = tk.Label(
            field_frame, 
            text=label_text, 
            font=self.label_font, 
            bg=self.bg_color, 
            fg=self.fg_color,
            width=12 if not self.is_mobile else 8,
            anchor="w"
        )
        label.pack(side=tk.LEFT)
        
        entry = tk.Entry(
            field_frame,
            textvariable=variable,
            font=self.label_font,
            bd=2,
            relief=tk.GROOVE,
            bg=self.card_bg,
            fg=self.fg_color,
            show=show
        )
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        return entry
    
    def setup_register_screen(self):
        """Configura la pantalla de registro responsive"""
        header = self.create_responsive_header(self.register_frame, "Registrarse")
        
        back_button = tk.Button(
            header,
            text="← Volver",
            font=self.label_font,
            bg=self.header_color,
            fg=self.header_text_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame_with_animation(self.welcome_frame)
        )
        back_button.place(x=10, y=10)
        
        # Contenido con scroll para móvil
        if self.is_mobile:
            canvas = tk.Canvas(self.register_frame, bg=self.bg_color, highlightthickness=0)
            scrollbar = ttk.Scrollbar(self.register_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True, 
                       padx=self.get_responsive_padding(20), 
                       pady=self.get_responsive_padding(20))
            scrollbar.pack(side="right", fill="y")
            
            content = scrollable_frame
        else:
            content = tk.Frame(self.register_frame, bg=self.bg_color)
            content.pack(fill=tk.BOTH, expand=True, 
                        padx=self.get_responsive_padding(30), 
                        pady=self.get_responsive_padding(30))
        
        register_title = tk.Label(
            content,
            text="Crear cuenta nueva",
            font=self.welcome_font,
            bg=self.bg_color,
            fg=self.fg_color
        )
        register_title.pack(pady=self.get_responsive_padding(10))
        
        # Campos de registro
        self.create_responsive_input_field(content, "👤", "Usuario:", self.new_username_var)
        
        email_var = tk.StringVar()
        self.create_responsive_input_field(content, "✉️", "Email:", email_var)
        self.create_responsive_input_field(content, "🔒", "Contraseña:", self.new_password_var, show="•")
        self.create_responsive_input_field(content, "🔐", "Confirmar:", self.confirm_password_var, show="•")
        
        # Términos y condiciones
        terms_var = tk.BooleanVar()
        terms_check = tk.Checkbutton(
            content,
            text="Acepto términos y condiciones",
            variable=terms_var,
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.card_bg,
            activebackground=self.bg_color,
            activeforeground=self.fg_color,
            wraplength=self.window_width - 100
        )
        terms_check.pack(pady=self.get_responsive_padding(10))
        
        # Botón de registro
        register_button = tk.Button(
            content, 
            text="Crear Cuenta", 
            font=self.button_font,
            bg=self.button_color, 
            fg=self.button_text_color,
            relief=tk.RAISED,
            borderwidth=2,
            padx=self.get_responsive_padding(20),
            pady=self.get_responsive_padding(10),
            command=lambda: self.do_register(terms_var)
        )
        register_button.pack(pady=self.get_responsive_padding(20), 
                           fill=tk.X if self.is_mobile else None)
        
        self.create_responsive_footer(self.register_frame)
    
    def setup_home_screen(self):
        """Configura la pantalla principal responsive"""
        header = self.create_responsive_header(self.home_frame, "PetZone - Tienda")
        
        # Botones del header adaptados
        button_size = 12 if self.is_mobile else 14
        
        cart_button = tk.Button(
            header,
            text="🛒",
            font=tkfont.Font(family="Arial", size=button_size),
            bg=self.header_color,
            fg=self.header_text_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame_with_animation(self.cart_frame)
        )
        cart_x = self.window_width - 80 if self.is_mobile else 350
        cart_button.place(x=cart_x, y=10)
        
        self.cart_count_label = tk.Label(
            header,
            text="0",
            font=tkfont.Font(family="Arial", size=8 if self.is_mobile else 10),
            bg="red",
            fg="white",
            width=2,
            height=1
        )
        self.cart_count_label.place(x=cart_x + 20, y=5)
        
        profile_button = tk.Button(
            header,
            text="👤",
            font=tkfont.Font(family="Arial", size=button_size),
            bg=self.header_color,
            fg=self.header_text_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame_with_animation(self.profile_frame)
        )
        profile_x = self.window_width - 120 if self.is_mobile else 310
        profile_button.place(x=profile_x, y=10)
        
        logout_button = tk.Button(
            header,
            text="Salir",
            font=self.label_font,
            bg=self.header_color,
            fg=self.header_text_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame_with_animation(self.welcome_frame)
        )
        logout_button.place(x=10, y=10)
        
        content = tk.Frame(self.home_frame, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, 
                    padx=self.get_responsive_padding(10), 
                    pady=self.get_responsive_padding(10))
        
        # Barra de búsqueda responsive
        search_frame = tk.Frame(content, bg=self.bg_color)
        search_frame.pack(fill=tk.X, pady=self.get_responsive_padding(10), 
                         padx=self.get_responsive_padding(10))
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=self.label_font,
            bd=2,
            relief=tk.GROOVE,
            bg=self.card_bg,
            fg=self.fg_color
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        search_button = tk.Button(
            search_frame,
            text="🔍",
            font=self.label_font,
            bg=self.button_color,
            fg=self.button_text_color,
            command=self.search_products
        )
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Categorías con scroll horizontal
        self.setup_responsive_categories(content)
        
        # Banner promocional adaptativo
        if not self.is_mobile:
            self.setup_promotional_banner(content)
        
        # Contenedor de productos
        self.products_container = tk.Frame(content, bg=self.bg_color)
        self.products_container.pack(fill=tk.BOTH, expand=True, 
                                   pady=self.get_responsive_padding(10))
        
        self.display_products()
        self.create_responsive_footer(self.home_frame)
    
    def setup_responsive_categories(self, parent):
        """Configura las categorías de forma responsive"""
        categories_frame = tk.Frame(parent, bg=self.bg_color)
        categories_frame.pack(fill=tk.X, pady=self.get_responsive_padding(10))
        
        if self.is_mobile:
            # En móvil, usar un combobox
            category_label = tk.Label(
                categories_frame,
                text="Categoría:",
                font=self.label_font,
                bg=self.bg_color,
                fg=self.fg_color
            )
            category_label.pack(side=tk.LEFT, padx=5)
            
            self.category_var = tk.StringVar(value=self.selected_category)
            category_combo = ttk.Combobox(
                categories_frame,
                textvariable=self.category_var,
                values=self.categories,
                state="readonly",
                font=self.label_font
            )
            category_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            category_combo.bind('<<ComboboxSelected>>', 
                               lambda e: self.filter_by_category(self.category_var.get()))
        else:
            # En desktop, usar botones con scroll
            categories_canvas = tk.Canvas(categories_frame, height=40, 
                                        bg=self.bg_color, highlightthickness=0)
            categories_canvas.pack(fill=tk.X)
            
            categories_inner = tk.Frame(categories_canvas, bg=self.bg_color)
            categories_canvas.create_window((0, 0), window=categories_inner, anchor="nw")
            
            for category in self.categories:
                category_button = tk.Button(
                    categories_inner,
                    text=category,
                    font=self.label_font,
                    bg=self.button_color if category == self.selected_category else self.card_bg,
                    fg=self.button_text_color if category == self.selected_category else self.fg_color,
                    relief=tk.RAISED if category == self.selected_category else tk.GROOVE,
                    borderwidth=1,
                    padx=self.get_responsive_padding(10),
                    pady=self.get_responsive_padding(5),
                    command=lambda c=category: self.filter_by_category(c)
                )
                category_button.pack(side=tk.LEFT, padx=5)
            
            categories_inner.update_idletasks()
            categories_canvas.config(scrollregion=categories_canvas.bbox("all"))
    
    def setup_promotional_banner(self, parent):
        """Configura el banner promocional (solo desktop)"""
        banner_frame = tk.Frame(parent, bg=self.bg_color, height=80)
        banner_frame.pack(fill=tk.X, pady=self.get_responsive_padding(10), 
                         padx=self.get_responsive_padding(10))
        
        banner_canvas = tk.Canvas(banner_frame, height=80, bg=self.button_color, 
                                 highlightthickness=0)
        banner_canvas.pack(fill=tk.X)
        
        banner_text = banner_canvas.create_text(
            200, 40, 
            text="¡OFERTA ESPECIAL! 20% de descuento", 
            font=self.button_font,
            fill="white"
        )
    
    def display_products(self, search_term=None):
        """Muestra productos de forma responsive"""
        for widget in self.products_container.winfo_children():
            widget.destroy()
        
        # Filtrar productos
        filtered_products = []
        for product in self.products:
            category_match = self.selected_category == "Todos" or product["category"] == self.selected_category
            search_match = True
            if search_term:
                search_match = search_term in product["name"].lower()
            
            if category_match and search_match:
                filtered_products.append(product)
        
        if not filtered_products:
            no_products_label = tk.Label(
                self.products_container,
                text="No se encontraron productos",
                font=self.label_font,
                bg=self.bg_color,
                fg=self.fg_color
            )
            no_products_label.pack(pady=30)
            return
        
        # Grid responsive: 1 columna en móvil, 2 en desktop
        columns = 1 if self.is_mobile else 2
        row_frame = None
        
        for i, product in enumerate(filtered_products):
            if i % columns == 0:
                row_frame = tk.Frame(self.products_container, bg=self.bg_color)
                row_frame.pack(fill=tk.X, pady=5)
            
            self.create_product_card(row_frame, product, columns)
    
    def create_product_card(self, parent, product, columns):
        """Crea una tarjeta de producto responsive"""
        card_width = (self.window_width - 40) if columns == 1 else (self.window_width - 60) // 2
        card_height = 200 if self.is_mobile else 250
        
        product_card = tk.Frame(parent, bg=self.card_bg, bd=1, relief=tk.SOLID, 
                               width=card_width, height=card_height)
        product_card.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        product_card.pack_propagate(False)
        
        # Imagen del producto
        image_label = tk.Label(
            product_card,
            image=product["image"],
            bg=self.card_bg
        )
        image_label.pack(pady=self.get_responsive_padding(10))
        
        # Nombre del producto
        name_label = tk.Label(
            product_card,
            text=product["name"],
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color,
            wraplength=card_width - 20
        )
        name_label.pack(pady=self.get_responsive_padding(5))
        
        # Precio
        price_label = tk.Label(
            product_card,
            text=f"$ {product['price']:,.0f} ARS",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        price_label.pack(pady=self.get_responsive_padding(5))
        
        # Estrellas de calificación (simplificadas en móvil)
        if not self.is_mobile:
            rating_frame = tk.Frame(product_card, bg=self.card_bg)
            rating_frame.pack(pady=5)
            
            for j in range(5):
                star_color = "#FFD700" if j < int(product["rating"]) else self.bg_color
                star_label = tk.Label(
                    rating_frame,
                    text="★",
                    font=self.label_font,
                    bg=self.card_bg,
                    fg=star_color
                )
                star_label.pack(side=tk.LEFT, padx=1)
        
        # Botones de acción
        buttons_frame = tk.Frame(product_card, bg=self.card_bg)
        buttons_frame.pack(pady=self.get_responsive_padding(10), side=tk.BOTTOM)
        
        if self.is_mobile:
            # En móvil, solo botón de añadir
            add_button = tk.Button(
                buttons_frame,
                text="Añadir al carrito",
                font=self.label_font,
                bg=self.button_color,
                fg=self.button_text_color,
                relief=tk.RAISED,
                borderwidth=1,
                command=lambda p=product: self.add_to_cart(p)
            )
            add_button.pack(fill=tk.X, padx=5)
        else:
            # En desktop, botones separados
            view_button = tk.Button(
                buttons_frame,
                text="Ver",
                font=self.label_font,
                bg=self.card_bg,
                fg=self.fg_color,
                relief=tk.GROOVE,
                borderwidth=1,
                command=lambda p=product: self.show_product_detail(p)
            )
            view_button.pack(side=tk.LEFT, padx=5)
            
            add_button = tk.Button(
                buttons_frame,
                text="Añadir",
                font=self.label_font,
                bg=self.button_color,
                fg=self.button_text_color,
                relief=tk.RAISED,
                borderwidth=1,
                command=lambda p=product: self.add_to_cart(p)
            )
            add_button.pack(side=tk.LEFT, padx=5)
        
        # Hacer la tarjeta clickeable
        for widget in [product_card, image_label, name_label, price_label]:
            widget.bind("<Button-1>", lambda e, p=product: self.show_product_detail(p))
            
            if not self.is_mobile:
                widget.bind("<Enter>", lambda e, card=product_card: card.configure(bg=self.highlight_color))
                widget.bind("<Leave>", lambda e, card=product_card: card.configure(bg=self.card_bg))
    
    # Métodos simplificados para las otras pantallas
    def setup_cart_screen(self):
        """Configura la pantalla del carrito responsive"""
        header = self.create_responsive_header(self.cart_frame, "Carrito")
        
        back_button = tk.Button(
            header,
            text="← Volver",
            font=self.label_font,
            bg=self.header_color,
            fg=self.header_text_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame_with_animation(self.home_frame)
        )
        back_button.place(x=10, y=10)
        
        content = tk.Frame(self.cart_frame, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, 
                    padx=self.get_responsive_padding(20), 
                    pady=self.get_responsive_padding(20))
        
        cart_label = tk.Label(
            content, 
            text="Tus Productos", 
            font=self.welcome_font, 
            bg=self.bg_color,
            fg=self.fg_color
        )
        cart_label.pack(pady=self.get_responsive_padding(10))
        
        # Contenedor de items con scroll
        cart_items_container = tk.Frame(content, bg=self.bg_color)
        cart_items_container.pack(fill=tk.BOTH, expand=True, 
                                 pady=self.get_responsive_padding(10))
        
        self.cart_canvas = tk.Canvas(cart_items_container, bg=self.bg_color, highlightthickness=0)
        self.cart_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        cart_scrollbar = ttk.Scrollbar(cart_items_container, orient=tk.VERTICAL, 
                                      command=self.cart_canvas.yview)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_canvas.configure(yscrollcommand=cart_scrollbar.set)
        
        self.cart_items_frame = tk.Frame(self.cart_canvas, bg=self.bg_color)
        self.cart_canvas.create_window((0, 0), window=self.cart_items_frame, anchor="nw")
        
        def configure_cart_scroll(event):
            self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))
        
        self.cart_items_frame.bind("<Configure>", configure_cart_scroll)
        
        # Etiqueta para carrito vacío
        self.empty_cart_label = tk.Label(
            self.cart_items_frame,
            text="Tu carrito está vacío",
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.empty_cart_label.pack(pady=30)
        
        # Resumen responsive
        self.setup_cart_summary(content)
        
        self.create_responsive_footer(self.cart_frame)
    
    def setup_cart_summary(self, parent):
        """Configura el resumen del carrito de forma responsive"""
        summary_frame = tk.Frame(parent, bg=self.card_bg, bd=1, relief=tk.SOLID)
        summary_frame.pack(fill=tk.X, pady=self.get_responsive_padding(10))
        
        # Subtotal
        subtotal_frame = tk.Frame(summary_frame, bg=self.card_bg)
        subtotal_frame.pack(fill=tk.X, padx=self.get_responsive_padding(10), 
                           pady=self.get_responsive_padding(5))
        
        subtotal_label = tk.Label(
            subtotal_frame,
            text="Subtotal:",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        subtotal_label.pack(side=tk.LEFT)
        
        self.subtotal_value = tk.Label(
            subtotal_frame,
            text="$ 0 ARS",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        self.subtotal_value.pack(side=tk.RIGHT)
        
        # Total
        total_frame = tk.Frame(summary_frame, bg=self.card_bg)
        total_frame.pack(fill=tk.X, padx=self.get_responsive_padding(10), 
                        pady=self.get_responsive_padding(5))
        
        total_label = tk.Label(
            total_frame,
            text="Total:",
            font=self.button_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        total_label.pack(side=tk.LEFT)
        
        self.total_label = tk.Label(
            total_frame,
            text="$ 0 ARS",
            font=self.button_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        self.total_label.pack(side=tk.RIGHT)
        
        # Botones de acción
        buttons_frame = tk.Frame(parent, bg=self.bg_color)
        buttons_frame.pack(fill=tk.X, pady=self.get_responsive_padding(20))
        
        if self.is_mobile:
            # En móvil, botones verticales
            continue_shopping = tk.Button(
                buttons_frame,
                text="Seguir comprando",
                font=self.label_font,
                bg=self.card_bg,
                fg=self.fg_color,
                relief=tk.RAISED,
                borderwidth=1,
                command=lambda: self.show_frame_with_animation(self.home_frame)
            )
            continue_shopping.pack(fill=tk.X, pady=5)
            
            checkout_button = tk.Button(
                buttons_frame, 
                text="Proceder al Pago", 
                font=self.button_font,
                bg=self.button_color, 
                fg=self.button_text_color,
                relief=tk.RAISED,
                borderwidth=2,
                command=self.checkout
            )
            checkout_button.pack(fill=tk.X, pady=5)
        else:
            # En desktop, botones horizontales
            continue_shopping = tk.Button(
                buttons_frame,
                text="Seguir comprando",
                font=self.label_font,
                bg=self.card_bg,
                fg=self.fg_color,
                relief=tk.RAISED,
                borderwidth=1,
                padx=10,
                pady=5,
                command=lambda: self.show_frame_with_animation(self.home_frame)
            )
            continue_shopping.pack(side=tk.LEFT, padx=10)
            
            checkout_button = tk.Button(
                buttons_frame, 
                text="Proceder al Pago", 
                font=self.button_font,
                bg=self.button_color, 
                fg=self.button_text_color,
                relief=tk.RAISED,
                borderwidth=2,
                padx=15,
                pady=8,
                command=self.checkout
            )
            checkout_button.pack(side=tk.RIGHT, padx=10)
    
    def setup_product_detail_screen(self):
        """Configura la pantalla de detalles responsive"""
        header = self.create_responsive_header(self.product_detail_frame, "Detalle")
        
        back_button = tk.Button(
            header,
            text="← Volver",
            font=self.label_font,
            bg=self.header_color,
            fg=self.header_text_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame_with_animation(self.home_frame)
        )
        back_button.place(x=10, y=10)
        
        # Contenido con scroll para móvil
        if self.is_mobile:
            canvas = tk.Canvas(self.product_detail_frame, bg=self.bg_color, highlightthickness=0)
            scrollbar = ttk.Scrollbar(self.product_detail_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True, 
                       padx=self.get_responsive_padding(20), 
                       pady=self.get_responsive_padding(20))
            scrollbar.pack(side="right", fill="y")
            
            self.product_detail_container = scrollable_frame
        else:
            content = tk.Frame(self.product_detail_frame, bg=self.bg_color)
            content.pack(fill=tk.BOTH, expand=True, 
                        padx=self.get_responsive_padding(20), 
                        pady=self.get_responsive_padding(20))
            self.product_detail_container = content
        
        self.create_responsive_footer(self.product_detail_frame)
    
    def setup_profile_screen(self):
        """Configura la pantalla de perfil responsive"""
        header = self.create_responsive_header(self.profile_frame, "Mi Perfil")
        
        back_button = tk.Button(
            header,
            text="← Volver",
            font=self.label_font,
            bg=self.header_color,
            fg=self.header_text_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame_with_animation(self.home_frame)
        )
        back_button.place(x=10, y=10)
        
        content = tk.Frame(self.profile_frame, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, 
                    padx=self.get_responsive_padding(20), 
                    pady=self.get_responsive_padding(20))
        
        # Avatar responsive
        avatar_size = self.get_responsive_size(100)
        avatar_canvas = tk.Canvas(content, width=avatar_size, height=avatar_size, 
                                 bg=self.bg_color, highlightthickness=0)
        avatar_canvas.pack(pady=self.get_responsive_padding(20))
        
        center = avatar_size // 2
        radius = avatar_size // 4
        avatar_canvas.create_oval(center-radius, center-radius, center+radius, center+radius, 
                                 fill=self.button_color, outline="")
        avatar_canvas.create_text(center, center, text="👤", 
                                 font=("Arial", avatar_size//3), fill="white")
        
        # Información del usuario
        username_label = tk.Label(
            content,
            text="Usuario de Ejemplo",
            font=self.welcome_font,
            bg=self.bg_color,
            fg=self.fg_color
        )
        username_label.pack(pady=self.get_responsive_padding(10))
        
        email_label = tk.Label(
            content,
            text="usuario@ejemplo.com",
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color
        )
        email_label.pack(pady=self.get_responsive_padding(5))
        
        # Opciones de perfil
        options_frame = tk.Frame(content, bg=self.bg_color)
        options_frame.pack(fill=tk.X, pady=self.get_responsive_padding(20))
        
        # Crear opciones responsivas
        options = [
            ("🔑", "Cambiar contraseña"),
            ("📦", "Mis pedidos"),
            ("❤️", "Favoritos"),
            ("🏠", "Direcciones"),
            ("💳", "Métodos de pago"),
            ("⚙️", "Configuración")
        ]
        
        for icon, text in options:
            self.create_profile_option(options_frame, icon, text)
        
        # Botón de cerrar sesión
        logout_button = tk.Button(
            content, 
            text="Cerrar Sesión", 
            font=self.button_font,
            bg="#ff6b6b", 
            fg="white",
            relief=tk.RAISED,
            borderwidth=2,
            padx=self.get_responsive_padding(20),
            pady=self.get_responsive_padding(10),
            command=lambda: self.show_frame_with_animation(self.welcome_frame)
        )
        logout_button.pack(pady=self.get_responsive_padding(20), 
                          fill=tk.X if self.is_mobile else None)
        
        self.create_responsive_footer(self.profile_frame)
    
    def create_profile_option(self, parent, icon, text):
        """Crea una opción de perfil responsive"""
        option_frame = tk.Frame(parent, bg=self.card_bg, bd=1, relief=tk.SOLID)
        option_frame.pack(fill=tk.X, pady=5, padx=self.get_responsive_padding(10))
        
        icon_label = tk.Label(
            option_frame,
            text=icon,
            font=("Arial", 14 if not self.is_mobile else 12),
            bg=self.card_bg,
            fg=self.fg_color
        )
        icon_label.pack(side=tk.LEFT, padx=self.get_responsive_padding(10), 
                       pady=self.get_responsive_padding(10))
        
        text_label = tk.Label(
            option_frame,
            text=text,
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        text_label.pack(side=tk.LEFT, padx=self.get_responsive_padding(10), 
                       pady=self.get_responsive_padding(10))
        
        arrow_label = tk.Label(
            option_frame,
            text="→",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        arrow_label.pack(side=tk.RIGHT, padx=self.get_responsive_padding(10), 
                        pady=self.get_responsive_padding(10))
        
        # Hacer clickeable solo en desktop
        if not self.is_mobile:
            def on_enter(e):
                option_frame.config(bg=self.highlight_color)
                icon_label.config(bg=self.highlight_color)
                text_label.config(bg=self.highlight_color)
                arrow_label.config(bg=self.highlight_color)
                
            def on_leave(e):
                option_frame.config(bg=self.card_bg)
                icon_label.config(bg=self.card_bg)
                text_label.config(bg=self.card_bg)
                arrow_label.config(bg=self.card_bg)
                
            option_frame.bind("<Enter>", on_enter)
            option_frame.bind("<Leave>", on_leave)
    
    # Métodos de funcionalidad simplificados pero funcionales
    def do_login(self):
        """Maneja el login con validación"""
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor ingrese usuario y contraseña")
            return
        
        # Simular verificación
        messagebox.showinfo("Éxito", f"Bienvenido, {username}!")
        self.show_frame_with_animation(self.home_frame)
        
        # Limpiar campos
        self.username_var.set("")
        self.password_var.set("")
    
    def do_register(self, terms_var):
        """Maneja el registro con validación"""
        username = self.new_username_var.get()
        password = self.new_password_var.get()
        confirm = self.confirm_password_var.get()
        
        if not username or not password or not confirm:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        if not terms_var.get():
            messagebox.showerror("Error", "Debe aceptar los términos y condiciones")
            return
        
        messagebox.showinfo("Éxito", f"Usuario {username} registrado correctamente")
        self.show_frame_with_animation(self.login_frame)
        
        # Limpiar campos
        self.new_username_var.set("")
        self.new_password_var.set("")
        self.confirm_password_var.set("")
    
    def filter_by_category(self, category):
        """Filtra productos por categoría"""
        self.selected_category = category
        self.display_products()
    
    def search_products(self):
        """Busca productos por término"""
        search_term = self.search_var.get().lower()
        if not search_term:
            messagebox.showinfo("Búsqueda", "Por favor ingrese un término de búsqueda")
            return
        
        self.display_products(search_term)
    
    def show_product_detail(self, product):
        """Muestra detalles del producto de forma responsive"""
        # Limpiar contenedor
        for widget in self.product_detail_container.winfo_children():
            widget.destroy()
        
        if self.is_mobile:
            # Layout vertical para móvil
            # Imagen
            image_frame = tk.Frame(self.product_detail_container, bg=self.card_bg, 
                                  bd=1, relief=tk.SOLID)
            image_frame.pack(fill=tk.X, padx=10, pady=10)
            
            image_label = tk.Label(image_frame, image=product["image"], bg=self.card_bg)
            image_label.pack(pady=10)
            
            # Detalles
            details_frame = tk.Frame(self.product_detail_container, bg=self.bg_color)
            details_frame.pack(fill=tk.X, padx=10, pady=10)
        else:
            # Layout horizontal para desktop
            top_frame = tk.Frame(self.product_detail_container, bg=self.bg_color)
            top_frame.pack(fill=tk.X, pady=10)
            
            # Imagen
            image_frame = tk.Frame(top_frame, bg=self.card_bg, bd=1, relief=tk.SOLID, 
                                  width=200, height=200)
            image_frame.pack(side=tk.LEFT, padx=10, pady=10)
            image_frame.pack_propagate(False)
            
            image_label = tk.Label(image_frame, image=product["image"], bg=self.card_bg)
            image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            
            # Detalles
            details_frame = tk.Frame(top_frame, bg=self.bg_color)
            details_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Información del producto
        name_label = tk.Label(
            details_frame,
            text=product["name"],
            font=self.welcome_font,
            bg=self.bg_color,
            fg=self.fg_color,
            wraplength=self.window_width - 100,
            justify=tk.LEFT,
            anchor="w"
        )
        name_label.pack(fill=tk.X, pady=5)
        
        price_label = tk.Label(
            details_frame,
            text=f"Precio: $ {product['price']:,.0f} ARS",
            font=self.button_font,
            bg=self.bg_color,
            fg=self.fg_color,
            anchor="w"
        )
        price_label.pack(fill=tk.X, pady=10)
        
        # Botón de añadir al carrito
        add_button = tk.Button(
            details_frame,
            text="Añadir al carrito",
            font=self.button_font,
            bg=self.button_color,
            fg=self.button_text_color,
            relief=tk.RAISED,
            borderwidth=2,
            padx=self.get_responsive_padding(15),
            pady=self.get_responsive_padding(8),
            command=lambda: self.add_to_cart(product)
        )
        add_button.pack(pady=10, fill=tk.X if self.is_mobile else None)
        
        # Descripción
        description_frame = tk.Frame(self.product_detail_container, bg=self.card_bg, 
                                   bd=1, relief=tk.SOLID)
        description_frame.pack(fill=tk.X, padx=10, pady=10)
        
        description_title = tk.Label(
            description_frame,
            text="Descripción",
            font=self.button_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        description_title.pack(pady=10)
        
        description_text = tk.Label(
            description_frame,
            text=f"Producto de alta calidad para tu mascota. {product['name']} está diseñado para proporcionar la mejor experiencia.",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color,
            wraplength=self.window_width - 40,
            justify=tk.LEFT
        )
        description_text.pack(padx=10, pady=10)
        
        self.show_frame_with_animation(self.product_detail_frame)
    
    def add_to_cart(self, product):
        """Añade producto al carrito con notificación responsive"""
        self.cart_items.append(product)
        
        # Notificación adaptativa
        notification = tk.Toplevel(self.root)
        notification.overrideredirect(True)
        notification.configure(bg=self.button_color)
        notification.attributes("-topmost", True)
        
        # Posición responsive
        if self.is_mobile:
            notification.geometry(f"200x60+{self.root.winfo_x() + 10}+{self.root.winfo_y() + 60}")
        else:
            notification.geometry(f"250x80+{self.root.winfo_x() + self.window_width - 270}+{self.root.winfo_y() + 80}")
        
        notification_label = tk.Label(
            notification,
            text=f"{product['name']}\nañadido al carrito",
            font=self.label_font,
            bg=self.button_color,
            fg="white",
            padx=10,
            pady=10
        )
        notification_label.pack(fill=tk.BOTH, expand=True)
        
        # Cerrar automáticamente
        def close_notification():
            time.sleep(2)
            try:
                notification.destroy()
            except:
                pass
        
        threading.Thread(target=close_notification, daemon=True).start()
        
        # Actualizar contador
        self.cart_count_label.config(text=str(len(self.cart_items)))
        self.update_cart_display()
    
    def update_cart_display(self):
        """Actualiza la visualización del carrito de forma responsive"""
        # Limpiar items
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()
        
        if not self.cart_items:
            self.empty_cart_label = tk.Label(
                self.cart_items_frame,
                text="Tu carrito está vacío",
                font=self.label_font,
                bg=self.bg_color,
                fg=self.fg_color
            )
            self.empty_cart_label.pack(pady=30)
            
            self.subtotal_value.config(text="$ 0 ARS")
            self.total_label.config(text="$ 0 ARS")
            return
        
        # Calcular totales
        subtotal = sum(item["price"] for item in self.cart_items)
        tax = subtotal * 0.21
        shipping = 1500 if subtotal < 30000 else 0
        total = subtotal + tax + shipping
        
        # Mostrar items
        for i, item in enumerate(self.cart_items):
            item_frame = tk.Frame(self.cart_items_frame, bg=self.card_bg, bd=1, relief=tk.SOLID)
            item_frame.pack(fill=tk.X, pady=5, padx=5)
            
            if not self.is_mobile:
                # Imagen en desktop
                image_label = tk.Label(item_frame, image=item["image"], bg=self.card_bg)
                image_label.pack(side=tk.LEFT, padx=5, pady=5)
            
            # Detalles
            details_frame = tk.Frame(item_frame, bg=self.card_bg)
            details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            item_name = tk.Label(
                details_frame,
                text=item["name"],
                font=self.label_font,
                bg=self.card_bg,
                fg=self.fg_color,
                anchor="w"
            )
            item_name.pack(fill=tk.X)
            
            item_price = tk.Label(
                details_frame,
                text=f"$ {item['price']:,.0f} ARS",
                font=self.label_font,
                bg=self.card_bg,
                fg=self.fg_color,
                anchor="w"
            )
            item_price.pack(fill=tk.X)
            
            # Botón eliminar
            remove_button = tk.Button(
                item_frame,
                text="✕",
                font=self.label_font,
                bg=self.card_bg,
                fg="#FF0000",
                relief=tk.FLAT,
                command=lambda idx=i: self.remove_from_cart(idx)
            )
            remove_button.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Actualizar totales
        self.subtotal_value.config(text=f"$ {subtotal:,.0f} ARS")
        self.total_label.config(text=f"$ {total:,.0f} ARS")
        
        # Configurar scroll
        self.cart_items_frame.update_idletasks()
        self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))
    
    def remove_from_cart(self, index):
        """Elimina item del carrito"""
        if 0 <= index < len(self.cart_items):
            removed_item = self.cart_items.pop(index)
            self.cart_count_label.config(text=str(len(self.cart_items)))
            self.update_cart_display()
            messagebox.showinfo("Eliminado", f"{removed_item['name']} eliminado del carrito")
    
    def checkout(self):
        """Proceso de checkout simplificado"""
        if not self.cart_items:
            messagebox.showinfo("Carrito Vacío", "No hay productos en el carrito")
            return
        
        # Calcular total
        subtotal = sum(item["price"] for item in self.cart_items)
        total = subtotal * 1.21 + (1500 if subtotal < 30000 else 0)
        
        # Confirmación simple
        result = messagebox.askyesno("Confirmar Compra", 
                                   f"Total: $ {total:,.0f} ARS\n¿Confirmar compra?")
        
        if result:
            messagebox.showinfo("Compra Exitosa", 
                              "¡Su pedido ha sido procesado con éxito!")
            
            # Vaciar carrito
            self.cart_items = []
            self.cart_count_label.config(text="0")
            self.update_cart_display()
            self.show_frame_with_animation(self.home_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = ResponsivePetZoneApp(root)
    root.mainloop()