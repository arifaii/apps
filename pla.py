import tkinter as tk
from tkinter import ttk, font, messagebox
import time
import random

class TiendaRopaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fashion Store")
        
        # Configurar tamaño fijo para móvil
        self.app_width = 380
        self.app_height = 680
        self.root.geometry(f"{self.app_width}x{self.app_height}")
        self.root.resizable(False, False)
        
        # Centrar ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.app_width) // 2
        y = (screen_height - self.app_height) // 2
        self.root.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")
        
        # Colores del tema
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db', 
            'accent': '#e74c3c',
            'background': '#f8f9fa',
            'card': '#ffffff',
            'text': '#2c3e50',
            'text_light': '#7f8c8d',
            'border': '#ecf0f1',
            'success': '#27ae60'
        }
        
        self.root.configure(bg=self.colors['background'])
        
        # Configurar fuentes
        self.title_font = font.Font(family="Arial", size=16, weight="bold")
        self.nav_font = font.Font(family="Arial", size=12)
        self.product_font = font.Font(family="Arial", size=10)
        self.price_font = font.Font(family="Arial", size=12, weight="bold")
        self.button_font = font.Font(family="Arial", size=11, weight="bold")
        self.small_font = font.Font(family="Arial", size=9)
        
        # Variables
        self.cart_items = []
        self.current_product = None
        self.current_category = "Todos"
        
        # Crear productos
        self.create_products()
        
        # Crear container principal
        self.main_container = tk.Frame(self.root, bg=self.colors['background'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Crear frames para cada pantalla
        self.home_frame = None
        self.product_detail_frame = None
        self.cart_frame = None
        self.favorites_frame = None
        
        # Inicializar pantalla de inicio
        self.show_home_screen()
        
    def create_products(self):
        self.categories = ["Todos", "Remeras", "Pantalones", "Vestidos", "Abrigos"]
        
        self.products = [
            {
                "id": 1,
                "name": "Remera Básica",
                "category": "Remeras",
                "price": 9800,
                "description": "Remera básica de algodón 100%, cómoda y versátil para uso diario.",
                "sizes": ["S", "M", "L", "XL"],
                "color": "Negro",
                "image_color": "#2c3e50",
                "favorite": False,
                "rating": 4.5,
                "stock": 15
            },
            {
                "id": 2,
                "name": "Remera Estampada",
                "category": "Remeras", 
                "price": 12500,
                "description": "Remera con diseño moderno y estampado exclusivo.",
                "sizes": ["S", "M", "L"],
                "color": "Blanco",
                "image_color": "#ecf0f1",
                "favorite": False,
                "rating": 4.2,
                "stock": 8
            },
            {
                "id": 3,
                "name": "Jean Clásico",
                "category": "Pantalones",
                "price": 24990,
                "description": "Jean de corte recto clásico, denim de alta calidad.",
                "sizes": ["38", "40", "42", "44"],
                "color": "Azul",
                "image_color": "#3498db",
                "favorite": False,
                "rating": 4.7,
                "stock": 12
            },
            {
                "id": 4,
                "name": "Vestido Floral",
                "category": "Vestidos",
                "price": 32000,
                "description": "Vestido elegante con estampado floral, perfecto para ocasiones especiales.",
                "sizes": ["S", "M", "L"],
                "color": "Rosa",
                "image_color": "#f8c291",
                "favorite": False,
                "rating": 4.8,
                "stock": 5
            },
            {
                "id": 5,
                "name": "Campera Jean",
                "category": "Abrigos",
                "price": 35900,
                "description": "Campera de jean clásica, ideal para entretiempo.",
                "sizes": ["S", "M", "L", "XL"],
                "color": "Azul",
                "image_color": "#5dade2",
                "favorite": False,
                "rating": 4.4,
                "stock": 7
            },
            {
                "id": 6,
                "name": "Sweater Lana",
                "category": "Abrigos",
                "price": 28500,
                "description": "Sweater de lana suave y abrigado para invierno.",
                "sizes": ["S", "M", "L"],
                "color": "Gris",
                "image_color": "#95a5a6",
                "favorite": False,
                "rating": 4.6,
                "stock": 9
            }
        ]
    
    def clear_main_container(self):
        """Limpiar el container principal"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def show_home_screen(self):
        """Mostrar pantalla de inicio"""
        self.clear_main_container()
        
        # Status bar
        status_bar = tk.Frame(self.main_container, bg=self.colors['primary'], height=30)
        status_bar.pack(fill=tk.X)
        status_bar.pack_propagate(False)
        
        # Hora
        time_label = tk.Label(
            status_bar,
            text=time.strftime("%H:%M"),
            font=self.small_font,
            bg=self.colors['primary'],
            fg='white'
        )
        time_label.place(x=10, y=8)
        
        # Título
        title_label = tk.Label(
            status_bar,
            text="Fashion Store",
            font=self.small_font,
            bg=self.colors['primary'],
            fg='white'
        )
        title_label.place(relx=0.5, y=8, anchor='n')
        
        # Batería
        battery_label = tk.Label(
            status_bar,
            text="🔋 📶",
            font=self.small_font,
            bg=self.colors['primary'],
            fg='white'
        )
        battery_label.place(x=self.app_width-50, y=8)
        
        # Header con navegación
        header = tk.Frame(self.main_container, bg=self.colors['card'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Botones de navegación
        nav_frame = tk.Frame(header, bg=self.colors['card'])
        nav_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Favoritos
        fav_btn = tk.Button(
            nav_frame,
            text="❤️",
            font=self.nav_font,
            bg=self.colors['card'],
            fg=self.colors['accent'],
            relief=tk.FLAT,
            command=self.show_favorites_screen
        )
        fav_btn.pack(side=tk.LEFT)
        
        # Carrito
        cart_btn = tk.Button(
            nav_frame,
            text=f"🛒 ({len(self.cart_items)})",
            font=self.nav_font,
            bg=self.colors['card'],
            fg=self.colors['secondary'],
            relief=tk.FLAT,
            command=self.show_cart_screen
        )
        cart_btn.pack(side=tk.LEFT, padx=10)
        
        # Usuario
        user_label = tk.Label(
            nav_frame,
            text="¡Hola, Shain! 👋",
            font=self.product_font,
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        user_label.pack(side=tk.RIGHT)
        
        # Separador
        separator = tk.Frame(self.main_container, bg=self.colors['border'], height=1)
        separator.pack(fill=tk.X)
        
        # Contenido principal con scroll
        canvas = tk.Canvas(self.main_container, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Categorías
        cat_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        cat_frame.pack(fill=tk.X, pady=10)
        
        cat_title = tk.Label(
            cat_frame,
            text="Categorías",
            font=self.title_font,
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        cat_title.pack(pady=(10, 5))
        
        # Botones de categorías
        cat_buttons_frame = tk.Frame(cat_frame, bg=self.colors['background'])
        cat_buttons_frame.pack()
        
        for i, category in enumerate(self.categories):
            is_selected = category == self.current_category
            btn = tk.Button(
                cat_buttons_frame,
                text=category,
                font=self.small_font,
                bg=self.colors['primary'] if is_selected else self.colors['card'],
                fg='white' if is_selected else self.colors['text'],
                relief=tk.FLAT,
                padx=10,
                pady=5,
                command=lambda c=category: self.filter_category(c)
            )
            btn.grid(row=i//3, column=i%3, padx=3, pady=3, sticky="ew")
        
        # Configurar grid
        for i in range(3):
            cat_buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Título productos
        products_title = tk.Label(
            scrollable_frame,
            text="✨ Your Look ✨",
            font=self.title_font,
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        products_title.pack(pady=(20, 5))
        
        subtitle = tk.Label(
            scrollable_frame,
            text="Descubre tu estilo perfecto",
            font=self.small_font,
            bg=self.colors['background'],
            fg=self.colors['text_light']
        )
        subtitle.pack(pady=(0, 15))
        
        # Grid de productos
        self.products_grid = tk.Frame(scrollable_frame, bg=self.colors['background'])
        self.products_grid.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)
        
        # Mostrar productos
        self.display_products()
    
    def filter_category(self, category):
        """Filtrar productos por categoría"""
        self.current_category = category
        self.show_home_screen()  # Recargar pantalla con nueva categoría
    
    def display_products(self):
        """Mostrar productos en grid"""
        # Limpiar grid anterior
        for widget in self.products_grid.winfo_children():
            widget.destroy()
        
        # Filtrar productos
        if self.current_category == "Todos":
            filtered_products = self.products
        else:
            filtered_products = [p for p in self.products if p["category"] == self.current_category]
        
        if not filtered_products:
            no_products = tk.Label(
                self.products_grid,
                text="No hay productos en esta categoría",
                font=self.product_font,
                bg=self.colors['background'],
                fg=self.colors['text_light']
            )
            no_products.pack(pady=50)
            return
        
        # Crear tarjetas de productos (2 columnas)
        for i, product in enumerate(filtered_products):
            row = i // 2
            col = i % 2
            self.create_product_card(product, row, col)
        
        # Configurar grid
        self.products_grid.grid_columnconfigure(0, weight=1)
        self.products_grid.grid_columnconfigure(1, weight=1)
    
    def create_product_card(self, product, row, col):
        """Crear tarjeta individual de producto"""
        card_width = 160
        card_height = 220
        
        # Frame principal de la tarjeta
        card_frame = tk.Frame(
            self.products_grid,
            bg=self.colors['card'],
            width=card_width,
            height=card_height,
            relief=tk.RAISED,
            borderwidth=1
        )
        card_frame.grid(row=row, column=col, padx=5, pady=8, sticky="nsew")
        card_frame.grid_propagate(False)
        
        # Imagen del producto
        image_frame = tk.Frame(card_frame, bg=product["image_color"], height=120)
        image_frame.pack(fill=tk.X, padx=5, pady=5)
        image_frame.pack_propagate(False)
        
        # Icono del producto
        category_icons = {
            "Remeras": "👕",
            "Pantalones": "👖",
            "Vestidos": "👗", 
            "Abrigos": "🧥"
        }
        
        icon = category_icons.get(product["category"], "👕")
        icon_label = tk.Label(
            image_frame,
            text=icon,
            font=("Arial", 24),
            bg=product["image_color"],
            fg='white'
        )
        icon_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Información del producto
        info_frame = tk.Frame(card_frame, bg=self.colors['card'])
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Nombre
        name_label = tk.Label(
            info_frame,
            text=product["name"],
            font=self.small_font,
            bg=self.colors['card'],
            fg=self.colors['text'],
            wraplength=150
        )
        name_label.pack(anchor="w")
        
        # Rating
        stars = "⭐" * int(product["rating"])
        rating_label = tk.Label(
            info_frame,
            text=f"{stars} {product['rating']}",
            font=("Arial", 8),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        )
        rating_label.pack(anchor="w", pady=2)
        
        # Precio y botones
        bottom_frame = tk.Frame(info_frame, bg=self.colors['card'])
        bottom_frame.pack(fill=tk.X, pady=(5, 0))
        
        price_label = tk.Label(
            bottom_frame,
            text=f"${product['price']:,}",
            font=self.product_font,
            bg=self.colors['card'],
            fg=self.colors['primary']
        )
        price_label.pack(side=tk.LEFT)
        
        # Botones
        buttons_frame = tk.Frame(bottom_frame, bg=self.colors['card'])
        buttons_frame.pack(side=tk.RIGHT)
        
        # Favorito
        fav_icon = "❤️" if product["favorite"] else "🤍"
        fav_btn = tk.Button(
            buttons_frame,
            text=fav_icon,
            font=("Arial", 10),
            bg=self.colors['card'],
            fg=self.colors['accent'],
            relief=tk.FLAT,
            command=lambda p=product: self.toggle_favorite(p)
        )
        fav_btn.pack(side=tk.LEFT, padx=2)
        
        # Carrito
        cart_btn = tk.Button(
            buttons_frame,
            text="🛒",
            font=("Arial", 10),
            bg=self.colors['secondary'],
            fg='white',
            relief=tk.FLAT,
            padx=5,
            command=lambda p=product: self.add_to_cart(p)
        )
        cart_btn.pack(side=tk.LEFT, padx=2)
        
        # Click en tarjeta para ver detalles
        def on_card_click(event, p=product):
            self.show_product_detail(p)
        
        # Bind click events
        for widget in [card_frame, image_frame, name_label, price_label]:
            widget.bind("<Button-1>", on_card_click)
        
        # Efecto hover
        def on_enter(event):
            card_frame.config(relief=tk.RAISED, borderwidth=2)
        
        def on_leave(event):
            card_frame.config(relief=tk.RAISED, borderwidth=1)
        
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
    
    def toggle_favorite(self, product):
        """Alternar favorito"""
        product["favorite"] = not product["favorite"]
        self.display_products()  # Refrescar vista
    
    def add_to_cart(self, product):
        """Añadir producto al carrito"""
        if product["stock"] <= 0:
            messagebox.showwarning("Sin Stock", "Este producto no tiene stock disponible")
            return
        
        # Buscar si ya existe en carrito
        for item in self.cart_items:
            if item["product_id"] == product["id"]:
                item["quantity"] += 1
                messagebox.showinfo("Añadido", f"{product['name']} añadido al carrito")
                return
        
        # Añadir nuevo item
        cart_item = {
            "product_id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": 1,
            "size": product["sizes"][0] if product["sizes"] else "Único",
            "color": product["color"],
            "image_color": product["image_color"]
        }
        
        self.cart_items.append(cart_item)
        messagebox.showinfo("Añadido", f"{product['name']} añadido al carrito")
    
    def show_product_detail(self, product):
        """Mostrar detalles del producto"""
        self.current_product = product
        self.clear_main_container()
        
        # Header con botón volver
        header = tk.Frame(self.main_container, bg=self.colors['card'], height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        back_btn = tk.Button(
            header,
            text="← Volver",
            font=self.nav_font,
            bg=self.colors['card'],
            fg=self.colors['primary'],
            relief=tk.FLAT,
            command=self.show_home_screen
        )
        back_btn.place(x=10, y=10)
        
        title_label = tk.Label(
            header,
            text="Detalles del Producto",
            font=self.title_font,
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        title_label.place(relx=0.5, y=15, anchor='n')
        
        # Contenido con scroll
        canvas = tk.Canvas(self.main_container, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Imagen grande del producto
        image_container = tk.Frame(scrollable_frame, bg=product["image_color"], height=250)
        image_container.pack(fill=tk.X, padx=20, pady=20)
        image_container.pack_propagate(False)
        
        # Icono grande
        category_icons = {
            "Remeras": "👕",
            "Pantalones": "👖", 
            "Vestidos": "👗",
            "Abrigos": "🧥"
        }
        
        icon = category_icons.get(product["category"], "👕")
        big_icon = tk.Label(
            image_container,
            text=icon,
            font=("Arial", 48),
            bg=product["image_color"],
            fg='white'
        )
        big_icon.place(relx=0.5, rely=0.5, anchor='center')
        
        # Información del producto
        info_container = tk.Frame(scrollable_frame, bg=self.colors['card'])
        info_container.pack(fill=tk.X, padx=20, pady=10)
        
        # Nombre y precio
        name_label = tk.Label(
            info_container,
            text=product["name"],
            font=self.title_font,
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        name_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        price_label = tk.Label(
            info_container,
            text=f"${product['price']:,}",
            font=self.price_font,
            bg=self.colors['card'],
            fg=self.colors['primary']
        )
        price_label.pack(anchor="w", padx=15, pady=5)
        
        # Rating y stock
        details_frame = tk.Frame(info_container, bg=self.colors['card'])
        details_frame.pack(fill=tk.X, padx=15, pady=5)
        
        stars = "⭐" * int(product["rating"])
        rating_label = tk.Label(
            details_frame,
            text=f"{stars} {product['rating']}",
            font=self.product_font,
            bg=self.colors['card'],
            fg=self.colors['text_light']
        )
        rating_label.pack(side=tk.LEFT)
        
        stock_color = self.colors['success'] if product["stock"] > 5 else self.colors['accent']
        stock_label = tk.Label(
            details_frame,
            text=f"Stock: {product['stock']}",
            font=self.product_font,
            bg=self.colors['card'],
            fg=stock_color
        )
        stock_label.pack(side=tk.RIGHT)
        
        # Descripción
        desc_label = tk.Label(
            info_container,
            text=product["description"],
            font=self.product_font,
            bg=self.colors['card'],
            fg=self.colors['text'],
            wraplength=320,
            justify=tk.LEFT
        )
        desc_label.pack(anchor="w", padx=15, pady=10)
        
        # Color y tallas
        color_label = tk.Label(
            info_container,
            text=f"Color: {product['color']}",
            font=self.product_font,
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        color_label.pack(anchor="w", padx=15, pady=5)
        
        sizes_label = tk.Label(
            info_container,
            text=f"Tallas: {', '.join(product['sizes'])}",
            font=self.product_font,
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        sizes_label.pack(anchor="w", padx=15, pady=(5, 15))
        
        # Botones de acción
        actions_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        actions_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Añadir al carrito
        add_cart_btn = tk.Button(
            actions_frame,
            text="Añadir al Carrito 🛒",
            font=self.button_font,
            bg=self.colors['primary'],
            fg='white',
            relief=tk.FLAT,
            pady=12,
            command=lambda: self.add_to_cart(product)
        )
        add_cart_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Favorito
        fav_text = "❤️ Quitar de Favoritos" if product["favorite"] else "🤍 Añadir a Favoritos"
        fav_btn = tk.Button(
            actions_frame,
            text=fav_text,
            font=self.product_font,
            bg=self.colors['card'],
            fg=self.colors['accent'],
            relief=tk.FLAT,
            pady=8,
            command=lambda: self.toggle_favorite(product)
        )
        fav_btn.pack(fill=tk.X)
    
    def show_cart_screen(self):
        """Mostrar pantalla del carrito"""
        self.clear_main_container()
        
        # Header
        header = tk.Frame(self.main_container, bg=self.colors['card'], height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        back_btn = tk.Button(
            header,
            text="← Volver",
            font=self.nav_font,
            bg=self.colors['card'],
            fg=self.colors['primary'],
            relief=tk.FLAT,
            command=self.show_home_screen
        )
        back_btn.place(x=10, y=10)
        
        title_label = tk.Label(
            header,
            text=f"Carrito ({len(self.cart_items)})",
            font=self.title_font,
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        title_label.place(relx=0.5, y=15, anchor='n')
        
        if not self.cart_items:
            # Carrito vacío
            empty_frame = tk.Frame(self.main_container, bg=self.colors['background'])
            empty_frame.pack(fill=tk.BOTH, expand=True)
            
            empty_icon = tk.Label(
                empty_frame,
                text="🛒",
                font=("Arial", 64),
                bg=self.colors['background'],
                fg=self.colors['text_light']
            )
            empty_icon.pack(pady=(100, 20))
            
            empty_label = tk.Label(
                empty_frame,
                text="Tu carrito está vacío",
                font=self.title_font,
                bg=self.colors['background'],
                fg=self.colors['text_light']
            )
            empty_label.pack()
            
            empty_subtitle = tk.Label(
                empty_frame,
                text="¡Agrega algunos productos increíbles!",
                font=self.product_font,
                bg=self.colors['background'],
                fg=self.colors['text_light']
            )
            empty_subtitle.pack(pady=10)
            
            return
        
        # Contenido del carrito
        canvas = tk.Canvas(self.main_container, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Items del carrito
        for i, item in enumerate(self.cart_items):
            self.create_cart_item(scrollable_frame, item, i)
        
        # Resumen
        self.create_cart_summary(scrollable_frame)
    
    def create_cart_item(self, parent, item, index):
        """Crear item del carrito"""
        item_frame = tk.Frame(parent, bg=self.colors['card'])
        item_frame.pack(fill=tk.X, padx=15, pady=5)
        
        # Color del producto
        color_canvas = tk.Canvas(
            item_frame,
            width=50,
            height=50,
            bg=item["image_color"],
            highlightthickness=0
        )
        color_canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Información
        info_frame = tk.Frame(item_frame, bg=self.colors['card'])
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
        
        name_label = tk.Label(
            info_frame,
            text=item["name"],
            font=self.product_font,
            bg=self.colors['card'],
            fg=self.colors['text'],
            anchor="w"
        )
        name_label.pack(fill=tk.X)
        
        details_label = tk.Label(
            info_frame,
            text=f"Talla: {item['size']} • Color: {item['color']}",
            font=self.small_font,
            bg=self.colors['card'],
            fg=self.colors['text_light'],
            anchor="w"
        )
        details_label.pack(fill=tk.X)
        
        price_label = tk.Label(
            info_frame,
            text=f"${item['price']:,} × {item['quantity']} = ${item['price'] * item['quantity']:,}",
            font=self.product_font,
            bg=self.colors['card'],
            fg=self.colors['primary'],
            anchor="w"
        )
        price_label.pack(fill=tk.X, pady=5)
        
        # Controles de cantidad
        controls_frame = tk.Frame(info_frame, bg=self.colors['card'])
        controls_frame.pack(fill=tk.X)
        
        minus_btn = tk.Button(
            controls_frame,
            text="−",
            font=self.product_font,
            bg=self.colors['border'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            width=2,
            command=lambda: self.decrease_quantity(index)
        )
        minus_btn.pack(side=tk.LEFT)
        
        qty_label = tk.Label(
            controls_frame,
            text=str(item["quantity"]),
            font=self.product_font,
            bg=self.colors['card'],
            fg=self.colors['text'],
            width=3
        )
        qty_label.pack(side=tk.LEFT, padx=5)
        
        plus_btn = tk.Button(
            controls_frame,
            text="+",
            font=self.product_font,
            bg=self.colors['border'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            width=2,
            command=lambda: self.increase_quantity(index)
        )
        plus_btn.pack(side=tk.LEFT)
        
        # Botón eliminar
        delete_btn = tk.Button(
            item_frame,
            text="🗑️",
            font=self.nav_font,
            bg=self.colors['card'],
            fg=self.colors['accent'],
            relief=tk.FLAT,
            command=lambda: self.remove_item(index)
        )
        delete_btn.pack(side=tk.RIGHT, padx=10)
    
    def create_cart_summary(self, parent):
        """Crear resumen del carrito"""
        summary_frame = tk.Frame(parent, bg=self.colors['card'])
        summary_frame.pack(fill=tk.X, padx=15, pady=20)
        
        summary_title = tk.Label(
            summary_frame,
            text="Resumen de Compra",
            font=self.title_font,
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        summary_title.pack(pady=15)
        
        # Calcular totales
        subtotal = sum(item["price"] * item["quantity"] for item in self.cart_items)
        shipping = 1500 if subtotal < 20000 else 0
        total = subtotal + shipping
        
        # Subtotal
        subtotal_label = tk.Label(
            summary_frame,
            text=f"Subtotal: ${subtotal:,}",
            font=self.product_font,
            bg=self.colors['card'],
            fg=self.colors['text'],
            anchor="w"
        )
        subtotal_label.pack(fill=tk.X, padx=15, pady=2)
        
        # Envío
        shipping_text = "Envío: GRATIS 🎉" if shipping == 0 else f"Envío: ${shipping:,}"
        shipping_label = tk.Label(
            summary_frame,
            text=shipping_text,
            font=self.product_font,
            bg=self.colors['card'],
            fg=self.colors['success'] if shipping == 0 else self.colors['text'],
            anchor="w"
        )
        shipping_label.pack(fill=tk.X, padx=15, pady=2)
        
        # Total
        total_label = tk.Label(
            summary_frame,
            text=f"Total: ${total:,}",
            font=self.price_font,
            bg=self.colors['card'],
            fg=self.colors['primary'],
            anchor="w"
        )
        total_label.pack(fill=tk.X, padx=15, pady=(5, 15))
        
        # Botones
        checkout_btn = tk.Button(
            summary_frame,
            text="Finalizar Compra 💳",
            font=self.button_font,
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            pady=12,
            command=self.checkout
        )
        checkout_btn.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        clear_btn = tk.Button(
            summary_frame,
            text="Vaciar Carrito 🗑️",
            font=self.product_font,
            bg=self.colors['card'],
            fg=self.colors['accent'],
            relief=tk.FLAT,
            pady=8,
            command=self.clear_cart
        )
        clear_btn.pack(fill=tk.X, padx=15, pady=(0, 15))
    
    def show_favorites_screen(self):
        """Mostrar pantalla de favoritos"""
        self.clear_main_container()
        
        # Header
        header = tk.Frame(self.main_container, bg=self.colors['card'], height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        back_btn = tk.Button(
            header,
            text="← Volver",
            font=self.nav_font,
            bg=self.colors['card'],
            fg=self.colors['primary'],
            relief=tk.FLAT,
            command=self.show_home_screen
        )
        back_btn.place(x=10, y=10)
        
        title_label = tk.Label(
            header,
            text="Mis Favoritos ❤️",
            font=self.title_font,
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        title_label.place(relx=0.5, y=15, anchor='n')
        
        # Productos favoritos
        favorite_products = [p for p in self.products if p["favorite"]]
        
        if not favorite_products:
            # Sin favoritos
            empty_frame = tk.Frame(self.main_container, bg=self.colors['background'])
            empty_frame.pack(fill=tk.BOTH, expand=True)
            
            empty_icon = tk.Label(
                empty_frame,
                text="💔",
                font=("Arial", 64),
                bg=self.colors['background'],
                fg=self.colors['text_light']
            )
            empty_icon.pack(pady=(100, 20))
            
            empty_label = tk.Label(
                empty_frame,
                text="No tienes favoritos aún",
                font=self.title_font,
                bg=self.colors['background'],
                fg=self.colors['text_light']
            )
            empty_label.pack()
            
            return
        
        # Mostrar favoritos
        canvas = tk.Canvas(self.main_container, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Grid de favoritos
        self.products_grid = tk.Frame(scrollable_frame, bg=self.colors['background'])
        self.products_grid.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        for i, product in enumerate(favorite_products):
            row = i // 2
            col = i % 2
            self.create_product_card(product, row, col)
        
        self.products_grid.grid_columnconfigure(0, weight=1)
        self.products_grid.grid_columnconfigure(1, weight=1)
    
    def increase_quantity(self, index):
        """Aumentar cantidad"""
        if 0 <= index < len(self.cart_items):
            self.cart_items[index]["quantity"] += 1
            self.show_cart_screen()
    
    def decrease_quantity(self, index):
        """Disminuir cantidad"""
        if 0 <= index < len(self.cart_items):
            if self.cart_items[index]["quantity"] > 1:
                self.cart_items[index]["quantity"] -= 1
            else:
                self.remove_item(index)
            self.show_cart_screen()
    
    def remove_item(self, index):
        """Eliminar item del carrito"""
        if 0 <= index < len(self.cart_items):
            removed_item = self.cart_items.pop(index)
            messagebox.showinfo("Eliminado", f"{removed_item['name']} eliminado del carrito")
            self.show_cart_screen()
    
    def clear_cart(self):
        """Vaciar carrito"""
        if messagebox.askyesno("Confirmar", "¿Vaciar todo el carrito?"):
            self.cart_items = []
            self.show_cart_screen()
    
    def checkout(self):
        """Proceso de compra"""
        total = sum(item["price"] * item["quantity"] for item in self.cart_items)
        shipping = 1500 if total < 20000 else 0
        final_total = total + shipping
        
        order_number = f"ORD-{random.randint(10000, 99999)}"
        
        message = f"🎉 ¡Compra exitosa!\n\n"
        message += f"📋 Orden: {order_number}\n"
        message += f"💰 Total: ${final_total:,}\n\n"
        message += "¡Gracias por tu compra!"
        
        messagebox.showinfo("Compra Confirmada", message)
        
        # Vaciar carrito
        self.cart_items = []
        self.show_home_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = TiendaRopaApp(root)
    root.mainloop()