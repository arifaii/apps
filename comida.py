import tkinter as tk
from tkinter import ttk, font, messagebox
import time
import random
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io
import base64

class FoodloversApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Foodlovers")
        self.root.geometry("400x700")  # Tamaño similar a un móvil
        self.root.configure(bg="white")
        
        # Configurar fuentes
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold", slant="italic")
        self.nav_font = font.Font(family="Helvetica", size=12)
        self.location_font = font.Font(family="Helvetica", size=12)
        self.menu_font = font.Font(family="Helvetica", size=14)
        self.restaurant_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.description_font = font.Font(family="Helvetica", size=10)
        self.status_font = font.Font(family="Helvetica", size=10)
        self.sidebar_font = font.Font(family="Helvetica", size=14)
        self.sidebar_header_font = font.Font(family="Helvetica", size=16, weight="bold")
        
        # Color principal (verde menta)
        self.main_color = "#8cd9c0"
        
        # Lista de restaurantes
        self.restaurants = [
            {
                "id": 1,
                "name": "La Parrilla Argentina",
                "category": "Carnes",
                "rating": 4.5,
                "price_level": "$$",
                "distance": 0.8,
                "description": "Especialidad en cortes argentinos y parrilladas. Ambiente acogedor.",
                "address": "Av. Corrientes 1234, CABA",
                "menu": [
                    {"name": "Bife de Chorizo", "price": 3200, "description": "Corte de carne vacuna, jugoso y tierno."},
                    {"name": "Provoleta", "price": 1800, "description": "Queso provolone a la parrilla con orégano y aceite de oliva."},
                    {"name": "Ensalada Mixta", "price": 1200, "description": "Lechuga, tomate y cebolla con vinagreta."},
                    {"name": "Papas Fritas", "price": 950, "description": "Papas fritas caseras con sal."}
                ]
            },
            {
                "id": 2,
                "name": "Sushi Fusion",
                "category": "Japonesa",
                "rating": 4.7,
                "price_level": "$$$",
                "distance": 1.2,
                "description": "Sushi de autor con toques de cocina nikkei. Ingredientes frescos.",
                "address": "Av. Libertador 5678, CABA",
                "menu": [
                    {"name": "Rolls California (10 pzs)", "price": 2800, "description": "Kanikama, palta y pepino."},
                    {"name": "Nigiri Salmón (4 pzs)", "price": 2200, "description": "Arroz cubierto con salmón fresco."},
                    {"name": "Gyozas", "price": 1900, "description": "Empanadillas japonesas rellenas de cerdo y vegetales."},
                    {"name": "Miso Soup", "price": 900, "description": "Sopa tradicional japonesa."}
                ]
            },
            {
                "id": 3,
                "name": "Pasta & Pasta",
                "category": "Italiana",
                "rating": 4.3,
                "price_level": "$$",
                "distance": 0.5,
                "description": "Pastas caseras y pizzas a la piedra. Recetas tradicionales italianas.",
                "address": "Av. Cabildo 2468, CABA",
                "menu": [
                    {"name": "Spaghetti Carbonara", "price": 2400, "description": "Pasta con panceta, huevo, queso y pimienta."},
                    {"name": "Pizza Margherita", "price": 2100, "description": "Salsa de tomate, mozzarella y albahaca."},
                    {"name": "Lasagna Bolognesa", "price": 2600, "description": "Capas de pasta con salsa bolognesa y bechamel."},
                    {"name": "Tiramisú", "price": 1200, "description": "Postre italiano con café, mascarpone y cacao."}
                ]
            },
            {
                "id": 4,
                "name": "El Taco Loco",
                "category": "Mexicana",
                "rating": 4.2,
                "price_level": "$",
                "distance": 1.5,
                "description": "Auténtica comida mexicana. Tacos, burritos y margaritas.",
                "address": "Av. Córdoba 3579, CABA",
                "menu": [
                    {"name": "Tacos al Pastor (3 uds)", "price": 1800, "description": "Tortilla de maíz con carne de cerdo adobada, piña y cilantro."},
                    {"name": "Guacamole", "price": 1200, "description": "Palta, tomate, cebolla, cilantro y limón."},
                    {"name": "Quesadillas", "price": 1600, "description": "Tortilla de harina con queso y pollo."},
                    {"name": "Margarita", "price": 1100, "description": "Tequila, triple sec y jugo de limón."}
                ]
            },
            {
                "id": 5,
                "name": "Veggie Garden",
                "category": "Vegetariana",
                "rating": 4.6,
                "price_level": "$$",
                "distance": 1.0,
                "description": "Cocina vegetariana y vegana con productos orgánicos.",
                "address": "Av. Santa Fe 4321, CABA",
                "menu": [
                    {"name": "Bowl de Quinoa", "price": 2200, "description": "Quinoa, vegetales asados, aguacate y aderezo de tahini."},
                    {"name": "Hamburguesa de Lentejas", "price": 1900, "description": "Hamburguesa casera de lentejas con pan integral."},
                    {"name": "Ensalada de Kale", "price": 1700, "description": "Kale, manzana, nueces y aderezo de limón."},
                    {"name": "Smoothie Verde", "price": 950, "description": "Espinaca, manzana, jengibre y limón."}
                ]
            },
            {
                "id": 6,
                "name": "Burger House",
                "category": "Hamburguesas",
                "rating": 4.4,
                "price_level": "$$",
                "distance": 0.7,
                "description": "Las mejores hamburguesas gourmet de la ciudad.",
                "address": "Av. Scalabrini Ortiz 2345, CABA",
                "menu": [
                    {"name": "Burger Clásica", "price": 2100, "description": "Carne, lechuga, tomate, cebolla y queso cheddar."},
                    {"name": "Burger BBQ", "price": 2400, "description": "Carne, bacon, cebolla caramelizada y salsa BBQ."},
                    {"name": "Papas Rústicas", "price": 1100, "description": "Papas con cáscara y especias."},
                    {"name": "Milkshake", "price": 1300, "description": "Batido de helado de vainilla con chocolate."}
                ]
            }
        ]
        
        # Categorías de comida
        self.categories = ["Todas", "Carnes", "Japonesa", "Italiana", "Mexicana", "Vegetariana", "Hamburguesas"]
        
        # Variables para filtros
        self.current_category = "Todas"
        self.current_sort = "distance"  # Ordenar por distancia por defecto
        
        # Variable para el menú lateral
        self.sidebar_visible = False
        self.sidebar_frame = None
        self.overlay_frame = None
        
        # Datos del usuario
        self.user = {
            "name": "María García",
            "email": "maria@example.com",
            "phone": "+54 11 5555-1234",
            "address": "Av. Rivadavia 1234, CABA",
            "favorites": [],
            "orders": []
        }
        
        # Crear frames para cada pantalla
        self.home_frame = tk.Frame(self.root, bg="white")
        self.restaurant_detail_frame = tk.Frame(self.root, bg="white")
        self.search_frame = tk.Frame(self.root, bg="white")
        self.profile_frame = tk.Frame(self.root, bg="white")
        self.favorites_frame = tk.Frame(self.root, bg="white")
        self.orders_frame = tk.Frame(self.root, bg="white")
        
        # Inicializar todas las pantallas
        self.setup_home_screen()
        self.setup_restaurant_detail_screen()
        self.setup_search_screen()
        self.setup_profile_screen()
        self.setup_favorites_screen()
        self.setup_orders_screen()
        
        # Mostrar la pantalla de inicio
        self.show_frame(self.home_frame)
    
    def show_frame(self, frame):
        # Ocultar todos los frames
        for f in [self.home_frame, self.restaurant_detail_frame, self.search_frame, 
                 self.profile_frame, self.favorites_frame, self.orders_frame]:
            f.pack_forget()
        
        # Mostrar el frame solicitado
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Cerrar el menú lateral si está abierto
        if self.sidebar_visible:
            self.toggle_menu()
    
    def setup_home_screen(self):
        # Crear barra de estado
        self.create_status_bar(self.home_frame)
        
        # Crear header
        self.create_header(self.home_frame)
        
        # Contenedor principal con scroll
        main_container = tk.Frame(self.home_frame, bg="white")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(main_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Ubicación
        location_frame = tk.Frame(scrollable_frame, bg="white")
        location_frame.pack(fill=tk.X, padx=20, pady=10)
        
        location_icon = tk.Label(
            location_frame,
            text="📍",
            font=self.location_font,
            bg="white"
        )
        location_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        location_label = tk.Label(
            location_frame,
            text="restaurantes cerca de tu ubicación",
            font=self.location_font,
            bg="white"
        )
        location_label.pack(side=tk.LEFT)
        
        # Categorías (1, 2, 3)
        categories_frame = tk.Frame(scrollable_frame, bg="white")
        categories_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Crear los tres cuadrados con números
        for i in range(3):
            category_button = tk.Button(
                categories_frame,
                text=str(i+1),
                font=self.menu_font,
                bg=self.main_color,
                relief=tk.FLAT,
                width=5,
                height=2,
                command=lambda idx=i: self.filter_by_category_number(idx)
            )
            category_button.pack(side=tk.LEFT, padx=10)
        
        # Frame para los restaurantes
        self.restaurants_frame = tk.Frame(scrollable_frame, bg="white")
        self.restaurants_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Mostrar restaurantes
        self.display_restaurants()
    
    def setup_restaurant_detail_screen(self):
        # Crear barra de estado
        self.create_status_bar(self.restaurant_detail_frame)
        
        # Crear header con botón de volver
        header_frame = tk.Frame(self.restaurant_detail_frame, bg=self.main_color, height=60)
        header_frame.pack(fill=tk.X)
        
        back_button = tk.Button(
            header_frame,
            text="←",
            font=self.nav_font,
            bg=self.main_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame(self.home_frame)
        )
        back_button.place(x=10, y=15)
        
        title_label = tk.Label(
            header_frame,
            text="foodlovers",
            font=self.title_font,
            bg=self.main_color
        )
        title_label.pack(pady=10)
        
        # Contenedor principal con scroll
        main_container = tk.Frame(self.restaurant_detail_frame, bg="white")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(main_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        self.detail_scrollable_frame = tk.Frame(canvas, bg="white")
        
        self.detail_scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.detail_scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Nombre del restaurante
        self.detail_name_label = tk.Label(
            self.detail_scrollable_frame,
            text="Nombre del Restaurante",
            font=self.restaurant_font,
            bg="white"
        )
        self.detail_name_label.pack(pady=(20, 5), padx=20, anchor="w")
        
        # Categoría y precio
        self.detail_category_label = tk.Label(
            self.detail_scrollable_frame,
            text="Categoría | $$$",
            font=self.description_font,
            bg="white",
            fg="gray"
        )
        self.detail_category_label.pack(padx=20, anchor="w")
        
        # Valoración
        self.detail_rating_frame = tk.Frame(self.detail_scrollable_frame, bg="white")
        self.detail_rating_frame.pack(padx=20, pady=5, anchor="w")
        
        # Dirección
        self.detail_address_label = tk.Label(
            self.detail_scrollable_frame,
            text="Dirección del restaurante",
            font=self.description_font,
            bg="white"
        )
        self.detail_address_label.pack(padx=20, pady=5, anchor="w")
        
        # Separador
        separator = ttk.Separator(self.detail_scrollable_frame, orient='horizontal')
        separator.pack(fill=tk.X, padx=20, pady=10)
        
        # Descripción
        description_title = tk.Label(
            self.detail_scrollable_frame,
            text="Descripción",
            font=self.menu_font,
            bg="white"
        )
        description_title.pack(padx=20, anchor="w")
        
        self.detail_description_label = tk.Label(
            self.detail_scrollable_frame,
            text="Descripción del restaurante...",
            font=self.description_font,
            bg="white",
            wraplength=350,
            justify=tk.LEFT
        )
        self.detail_description_label.pack(padx=20, pady=5, anchor="w")
        
        # Separador
        separator2 = ttk.Separator(self.detail_scrollable_frame, orient='horizontal')
        separator2.pack(fill=tk.X, padx=20, pady=10)
        
        # Menú
        menu_title = tk.Label(
            self.detail_scrollable_frame,
            text="Menú destacado",
            font=self.menu_font,
            bg="white"
        )
        menu_title.pack(padx=20, anchor="w")
        
        # Frame para el menú
        self.menu_frame = tk.Frame(self.detail_scrollable_frame, bg="white")
        self.menu_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Botón de reservar
        reserve_button = tk.Button(
            self.detail_scrollable_frame,
            text="Reservar mesa",
            font=self.menu_font,
            bg=self.main_color,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.reserve_table
        )
        reserve_button.pack(pady=20)
    
    def setup_search_screen(self):
        # Crear barra de estado
        self.create_status_bar(self.search_frame)
        
        # Crear header con botón de volver
        header_frame = tk.Frame(self.search_frame, bg=self.main_color, height=60)
        header_frame.pack(fill=tk.X)
        
        back_button = tk.Button(
            header_frame,
            text="←",
            font=self.nav_font,
            bg=self.main_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame(self.home_frame)
        )
        back_button.place(x=10, y=15)
        
        title_label = tk.Label(
            header_frame,
            text="foodlovers",
            font=self.title_font,
            bg=self.main_color
        )
        title_label.pack(pady=10)
        
        # Contenedor principal con scroll
        main_container = tk.Frame(self.search_frame, bg="white")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(main_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        self.search_scrollable_frame = tk.Frame(canvas, bg="white")
        
        self.search_scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.search_scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Barra de búsqueda
        search_bar_frame = tk.Frame(self.search_scrollable_frame, bg="white")
        search_bar_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_bar_frame,
            textvariable=self.search_var,
            font=self.description_font,
            width=30
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        search_button = tk.Button(
            search_bar_frame,
            text="🔍",
            font=self.nav_font,
            bg="white",
            relief=tk.FLAT,
            command=self.search_restaurants
        )
        search_button.pack(side=tk.LEFT)
        
        # Categorías
        categories_frame = tk.Frame(self.search_scrollable_frame, bg="white")
        categories_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Scrollable horizontal para categorías
        categories_canvas = tk.Canvas(categories_frame, bg="white", height=40, highlightthickness=0)
        categories_canvas.pack(fill=tk.X)
        
        categories_scrollable = tk.Frame(categories_canvas, bg="white")
        categories_canvas.create_window((0, 0), window=categories_scrollable, anchor="nw")
        
        # Añadir botones de categoría
        for category in self.categories:
            cat_button = tk.Button(
                categories_scrollable,
                text=category,
                font=self.description_font,
                bg=self.main_color if category == self.current_category else "white",
                fg="black",
                relief=tk.FLAT,
                padx=10,
                command=lambda c=category: self.filter_by_category(c)
            )
            cat_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        categories_scrollable.update_idletasks()
        categories_canvas.config(scrollregion=categories_canvas.bbox("all"))
        
        # Opciones de ordenamiento
        sort_frame = tk.Frame(self.search_scrollable_frame, bg="white")
        sort_frame.pack(fill=tk.X, padx=20, pady=5)
        
        sort_label = tk.Label(
            sort_frame,
            text="Ordenar por:",
            font=self.description_font,
            bg="white"
        )
        sort_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.sort_var = tk.StringVar(value=self.current_sort)
        
        distance_radio = tk.Radiobutton(
            sort_frame,
            text="Distancia",
            variable=self.sort_var,
            value="distance",
            font=self.description_font,
            bg="white",
            command=self.sort_restaurants
        )
        distance_radio.pack(side=tk.LEFT, padx=5)
        
        rating_radio = tk.Radiobutton(
            sort_frame,
            text="Valoración",
            variable=self.sort_var,
            value="rating",
            font=self.description_font,
            bg="white",
            command=self.sort_restaurants
        )
        rating_radio.pack(side=tk.LEFT, padx=5)
        
        # Frame para los resultados de búsqueda
        self.search_results_frame = tk.Frame(self.search_scrollable_frame, bg="white")
        self.search_results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Etiqueta para resultados vacíos
        self.empty_search_label = tk.Label(
            self.search_results_frame,
            text="Ingresa un término de búsqueda",
            font=self.menu_font,
            bg="white"
        )
        self.empty_search_label.pack(pady=50)
    
    def setup_profile_screen(self):
        # Crear barra de estado
        self.create_status_bar(self.profile_frame)
        
        # Crear header con botón de volver
        header_frame = tk.Frame(self.profile_frame, bg=self.main_color, height=60)
        header_frame.pack(fill=tk.X)
        
        back_button = tk.Button(
            header_frame,
            text="←",
            font=self.nav_font,
            bg=self.main_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame(self.home_frame)
        )
        back_button.place(x=10, y=15)
        
        title_label = tk.Label(
            header_frame,
            text="Mi Perfil",
            font=self.title_font,
            bg=self.main_color
        )
        title_label.pack(pady=10)
        
        # Contenedor principal
        main_container = tk.Frame(self.profile_frame, bg="white")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Avatar
        avatar_frame = tk.Frame(main_container, bg="white")
        avatar_frame.pack(pady=10)
        
        avatar_canvas = tk.Canvas(
            avatar_frame,
            width=100,
            height=100,
            bg=self.main_color,
            highlightthickness=0
        )
        avatar_canvas.create_text(
            50, 50,
            text=self.user["name"][0],
            fill="white",
            font=font.Font(family="Helvetica", size=40, weight="bold")
        )
        avatar_canvas.pack()
        
        # Nombre de usuario
        name_label = tk.Label(
            main_container,
            text=self.user["name"],
            font=self.restaurant_font,
            bg="white"
        )
        name_label.pack(pady=5)
        
        # Información del usuario
        info_frame = tk.Frame(main_container, bg="white", bd=1, relief=tk.SOLID)
        info_frame.pack(fill=tk.X, pady=10)
        
        # Email
        email_frame = tk.Frame(info_frame, bg="white")
        email_frame.pack(fill=tk.X, padx=10, pady=5)
        
        email_label = tk.Label(
            email_frame,
            text="Email:",
            font=self.description_font,
            bg="white",
            width=10,
            anchor="w"
        )
        email_label.pack(side=tk.LEFT)
        
        email_value = tk.Label(
            email_frame,
            text=self.user["email"],
            font=self.description_font,
            bg="white",
            anchor="w"
        )
        email_value.pack(side=tk.LEFT)
        
        # Teléfono
        phone_frame = tk.Frame(info_frame, bg="white")
        phone_frame.pack(fill=tk.X, padx=10, pady=5)
        
        phone_label = tk.Label(
            phone_frame,
            text="Teléfono:",
            font=self.description_font,
            bg="white",
            width=10,
            anchor="w"
        )
        phone_label.pack(side=tk.LEFT)
        
        phone_value = tk.Label(
            phone_frame,
            text=self.user["phone"],
            font=self.description_font,
            bg="white",
            anchor="w"
        )
        phone_value.pack(side=tk.LEFT)
        
        # Dirección
        address_frame = tk.Frame(info_frame, bg="white")
        address_frame.pack(fill=tk.X, padx=10, pady=5)
        
        address_label = tk.Label(
            address_frame,
            text="Dirección:",
            font=self.description_font,
            bg="white",
            width=10,
            anchor="w"
        )
        address_label.pack(side=tk.LEFT)
        
        address_value = tk.Label(
            address_frame,
            text=self.user["address"],
            font=self.description_font,
            bg="white",
            anchor="w"
        )
        address_value.pack(side=tk.LEFT)
        
        # Botones de acción
        buttons_frame = tk.Frame(main_container, bg="white")
        buttons_frame.pack(fill=tk.X, pady=20)
        
        edit_button = tk.Button(
            buttons_frame,
            text="Editar Perfil",
            font=self.description_font,
            bg=self.main_color,
            relief=tk.FLAT,
            padx=10,
            pady=5,
            command=self.edit_profile
        )
        edit_button.pack(side=tk.LEFT, padx=5)
        
        logout_button = tk.Button(
            buttons_frame,
            text="Cerrar Sesión",
            font=self.description_font,
            bg="white",
            fg="red",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            command=self.logout
        )
        logout_button.pack(side=tk.RIGHT, padx=5)
    
    def setup_favorites_screen(self):
        # Crear barra de estado
        self.create_status_bar(self.favorites_frame)
        
        # Crear header con botón de volver
        header_frame = tk.Frame(self.favorites_frame, bg=self.main_color, height=60)
        header_frame.pack(fill=tk.X)
        
        back_button = tk.Button(
            header_frame,
            text="←",
            font=self.nav_font,
            bg=self.main_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame(self.home_frame)
        )
        back_button.place(x=10, y=15)
        
        title_label = tk.Label(
            header_frame,
            text="Mis Favoritos",
            font=self.title_font,
            bg=self.main_color
        )
        title_label.pack(pady=10)
        
        # Contenedor principal con scroll
        main_container = tk.Frame(self.favorites_frame, bg="white")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(main_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        self.favorites_scrollable_frame = tk.Frame(canvas, bg="white")
        
        self.favorites_scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.favorites_scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para los restaurantes favoritos
        self.favorites_restaurants_frame = tk.Frame(self.favorites_scrollable_frame, bg="white")
        self.favorites_restaurants_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Etiqueta para favoritos vacíos
        self.empty_favorites_label = tk.Label(
            self.favorites_restaurants_frame,
            text="No tienes restaurantes favoritos",
            font=self.menu_font,
            bg="white"
        )
        self.empty_favorites_label.pack(pady=50)
    
    def setup_orders_screen(self):
        # Crear barra de estado
        self.create_status_bar(self.orders_frame)
        
        # Crear header con botón de volver
        header_frame = tk.Frame(self.orders_frame, bg=self.main_color, height=60)
        header_frame.pack(fill=tk.X)
        
        back_button = tk.Button(
            header_frame,
            text="←",
            font=self.nav_font,
            bg=self.main_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame(self.home_frame)
        )
        back_button.place(x=10, y=15)
        
        title_label = tk.Label(
            header_frame,
            text="Mis Pedidos",
            font=self.title_font,
            bg=self.main_color
        )
        title_label.pack(pady=10)
        
        # Contenedor principal con scroll
        main_container = tk.Frame(self.orders_frame, bg="white")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(main_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        self.orders_scrollable_frame = tk.Frame(canvas, bg="white")
        
        self.orders_scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.orders_scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para los pedidos
        self.orders_list_frame = tk.Frame(self.orders_scrollable_frame, bg="white")
        self.orders_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Etiqueta para pedidos vacíos
        self.empty_orders_label = tk.Label(
            self.orders_list_frame,
            text="No tienes pedidos recientes",
            font=self.menu_font,
            bg="white"
        )
        self.empty_orders_label.pack(pady=50)
    
    def create_status_bar(self, parent):
        # Barra de estado (simula la barra superior del móvil)
        status_bar = tk.Frame(parent, bg="black", height=30)
        status_bar.pack(fill=tk.X)
        
        # Hora actual
        current_time = "9:41"
        time_label = tk.Label(
            status_bar, 
            text=current_time,
            font=self.status_font,
            bg="black",
            fg="white"
        )
        time_label.place(x=20, y=5)
        
        # Iconos de señal y batería (simulados con texto)
        icons_label = tk.Label(
            status_bar, 
            text="••• ■",
            font=self.status_font,
            bg="black",
            fg="white"
        )
        icons_label.place(x=350, y=5)
    
    def create_header(self, parent):
        # Header con logo
        header_frame = tk.Frame(parent, bg=self.main_color, height=60)
        header_frame.pack(fill=tk.X)
        
        # Icono de menú (hamburguesa)
        menu_button = tk.Button(
            header_frame,
            text="≡",
            font=self.nav_font,
            bg=self.main_color,
            relief=tk.FLAT,
            command=self.toggle_menu
        )
        menu_button.place(x=360, y=15)
        
        # Icono de búsqueda
        search_button = tk.Button(
            header_frame,
            text="🔍",
            font=self.nav_font,
            bg=self.main_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame(self.search_frame)
        )
        search_button.place(x=20, y=15)
        
        # Logo
        logo_label = tk.Label(
            header_frame,
            text="foodlovers",
            font=self.title_font,
            bg=self.main_color
        )
        logo_label.pack(pady=10)
    
    def toggle_menu(self):
        if self.sidebar_visible:
            # Cerrar el menú
            if self.sidebar_frame:
                self.sidebar_frame.destroy()
                self.sidebar_frame = None
            
            if self.overlay_frame:
                self.overlay_frame.destroy()
                self.overlay_frame = None
            
            self.sidebar_visible = False
        else:
            # Abrir el menú
            # Crear overlay semi-transparente
            self.overlay_frame = tk.Frame(self.root, bg="black")
            self.overlay_frame.place(x=0, y=0, width=400, height=700)
            self.overlay_frame.bind("<Button-1>", lambda e: self.toggle_menu())
            
            # Hacer el overlay semi-transparente
            self.overlay_frame.configure(bg="#000000")
            self.overlay_frame.attributes = {"alpha": 0.5}
            
            # Crear menú lateral
            self.sidebar_frame = tk.Frame(self.root, bg="white", width=300, height=700)
            self.sidebar_frame.place(x=0, y=0)
            
            # Evitar que el frame cambie de tamaño
            self.sidebar_frame.pack_propagate(False)
            
            # Cabecera del menú
            sidebar_header = tk.Frame(self.sidebar_frame, bg=self.main_color, height=150)
            sidebar_header.pack(fill=tk.X)
            
            # Cerrar menú
            close_button = tk.Button(
                sidebar_header,
                text="✕",
                font=self.nav_font,
                bg=self.main_color,
                relief=tk.FLAT,
                command=self.toggle_menu
            )
            close_button.place(x=260, y=10)
            
            # Avatar del usuario
            avatar_frame = tk.Frame(sidebar_header, bg=self.main_color)
            avatar_frame.place(x=20, y=40)
            
            avatar_canvas = tk.Canvas(
                avatar_frame,
                width=60,
                height=60,
                bg="white",
                highlightthickness=0
            )
            avatar_canvas.create_text(
                30, 30,
                text=self.user["name"][0],
                fill=self.main_color,
                font=font.Font(family="Helvetica", size=24, weight="bold")
            )
            avatar_canvas.pack()
            
            # Nombre de usuario
            user_name = tk.Label(
                sidebar_header,
                text=self.user["name"],
                font=self.sidebar_header_font,
                bg=self.main_color
            )
            user_name.place(x=100, y=50)
            
            # Email del usuario
            user_email = tk.Label(
                sidebar_header,
                text=self.user["email"],
                font=self.description_font,
                bg=self.main_color
            )
            user_email.place(x=100, y=75)
            
            # Opciones del menú
            menu_options_frame = tk.Frame(self.sidebar_frame, bg="white")
            menu_options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Inicio
            home_option = tk.Button(
                menu_options_frame,
                text="🏠  Inicio",
                font=self.sidebar_font,
                bg="white",
                relief=tk.FLAT,
                anchor="w",
                padx=10,
                pady=10,
                command=lambda: [self.toggle_menu(), self.show_frame(self.home_frame)]
            )
            home_option.pack(fill=tk.X, pady=5)
            
            # Perfil
            profile_option = tk.Button(
                menu_options_frame,
                text="👤  Mi Perfil",
                font=self.sidebar_font,
                bg="white",
                relief=tk.FLAT,
                anchor="w",
                padx=10,
                pady=10,
                command=lambda: [self.toggle_menu(), self.show_frame(self.profile_frame)]
            )
            profile_option.pack(fill=tk.X, pady=5)
            
            # Favoritos
            favorites_option = tk.Button(
                menu_options_frame,
                text="★  Mis Favoritos",
                font=self.sidebar_font,
                bg="white",
                relief=tk.FLAT,
                anchor="w",
                padx=10,
                pady=10,
                command=lambda: [self.toggle_menu(), self.show_frame(self.favorites_frame)]
            )
            favorites_option.pack(fill=tk.X, pady=5)
            
            # Pedidos
            orders_option = tk.Button(
                menu_options_frame,
                text="🛍️  Mis Pedidos",
                font=self.sidebar_font,
                bg="white",
                relief=tk.FLAT,
                anchor="w",
                padx=10,
                pady=10,
                command=lambda: [self.toggle_menu(), self.show_frame(self.orders_frame)]
            )
            orders_option.pack(fill=tk.X, pady=5)
            
            # Buscar
            search_option = tk.Button(
                menu_options_frame,
                text="🔍  Buscar",
                font=self.sidebar_font,
                bg="white",
                relief=tk.FLAT,
                anchor="w",
                padx=10,
                pady=10,
                command=lambda: [self.toggle_menu(), self.show_frame(self.search_frame)]
            )
            search_option.pack(fill=tk.X, pady=5)
            
            # Separador
            separator = ttk.Separator(menu_options_frame, orient='horizontal')
            separator.pack(fill=tk.X, pady=10)
            
            # Configuración
            settings_option = tk.Button(
                menu_options_frame,
                text="⚙️  Configuración",
                font=self.sidebar_font,
                bg="white",
                relief=tk.FLAT,
                anchor="w",
                padx=10,
                pady=10,
                command=self.show_settings
            )
            settings_option.pack(fill=tk.X, pady=5)
            
            # Ayuda
            help_option = tk.Button(
                menu_options_frame,
                text="❓  Ayuda",
                font=self.sidebar_font,
                bg="white",
                relief=tk.FLAT,
                anchor="w",
                padx=10,
                pady=10,
                command=self.show_help
            )
            help_option.pack(fill=tk.X, pady=5)
            
            # Cerrar sesión
            logout_option = tk.Button(
                menu_options_frame,
                text="🚪  Cerrar Sesión",
                font=self.sidebar_font,
                bg="white",
                fg="red",
                relief=tk.FLAT,
                anchor="w",
                padx=10,
                pady=10,
                command=self.logout
            )
            logout_option.pack(fill=tk.X, pady=5)
            
            self.sidebar_visible = True
    
    def display_restaurants(self):
        # Limpiar restaurantes anteriores
        for widget in self.restaurants_frame.winfo_children():
            widget.destroy()
        
        # Filtrar restaurantes por categoría
        filtered_restaurants = []
        if self.current_category == "Todas":
            filtered_restaurants = self.restaurants
        else:
            filtered_restaurants = [r for r in self.restaurants if r["category"] == self.current_category]
        
        # Ordenar restaurantes
        if self.current_sort == "distance":
            filtered_restaurants = sorted(filtered_restaurants, key=lambda x: x["distance"])
        elif self.current_sort == "rating":
            filtered_restaurants = sorted(filtered_restaurants, key=lambda x: x["rating"], reverse=True)
        
        if not filtered_restaurants:
            empty_label = tk.Label(
                self.restaurants_frame,
                text="No se encontraron restaurantes",
                font=self.menu_font,
                bg="white"
            )
            empty_label.pack(pady=50)
            return
        
        # Mostrar restaurantes
        for restaurant in filtered_restaurants:
            self.create_restaurant_card(restaurant)
    
    def create_restaurant_card(self, restaurant):
        # Crear tarjeta de restaurante
        card = tk.Frame(self.restaurants_frame, bg="white", bd=1, relief=tk.SOLID)
        card.pack(fill=tk.X, pady=10)
        
        # Contenido de la tarjeta
        content_frame = tk.Frame(card, bg="white")
        content_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Nombre del restaurante
        name_label = tk.Label(
            content_frame,
            text=restaurant["name"],
            font=self.restaurant_font,
            bg="white",
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # Categoría y precio
        category_price = tk.Label(
            content_frame,
            text=f"{restaurant['category']} | {restaurant['price_level']}",
            font=self.description_font,
            bg="white",
            fg="gray",
            anchor="w"
        )
        category_price.pack(anchor="w")
        
        # Valoración con estrellas
        rating_frame = tk.Frame(content_frame, bg="white")
        rating_frame.pack(anchor="w", pady=5)
        
        # Mostrar estrellas según la valoración
        rating = restaurant["rating"]
        for i in range(5):
            if i < int(rating):
                star = "★"  # Estrella completa
            elif i < rating and i >= int(rating):
                star = "⯪"  # Media estrella (aproximación)
            else:
                star = "☆"  # Estrella vacía
            
            star_label = tk.Label(
                rating_frame,
                text=star,
                font=self.description_font,
                bg="white",
                fg="gold"
            )
            star_label.pack(side=tk.LEFT)
        
        rating_value = tk.Label(
            rating_frame,
            text=f" {rating}",
            font=self.description_font,
            bg="white"
        )
        rating_value.pack(side=tk.LEFT)
        
        # Distancia
        distance_label = tk.Label(
            content_frame,
            text=f"{restaurant['distance']} km de distancia",
            font=self.description_font,
            bg="white",
            anchor="w"
        )
        distance_label.pack(anchor="w")
        
        # Descripción corta
        description_label = tk.Label(
            content_frame,
            text=restaurant["description"],
            font=self.description_font,
            bg="white",
            wraplength=350,
            justify=tk.LEFT,
            anchor="w"
        )
        description_label.pack(anchor="w", pady=5)
        
        # Hacer que la tarjeta sea clickeable
        for widget in [card, content_frame, name_label, category_price, rating_frame, distance_label, description_label]:
            widget.bind("<Button-1>", lambda event, r=restaurant: self.show_restaurant_details(r))
    
    def show_restaurant_details(self, restaurant):
        # Actualizar información en la pantalla de detalles
        self.detail_name_label.config(text=restaurant["name"])
        self.detail_category_label.config(text=f"{restaurant['category']} | {restaurant['price_level']}")
        self.detail_address_label.config(text=restaurant["address"])
        self.detail_description_label.config(text=restaurant["description"])
        
        # Limpiar frame de valoración
        for widget in self.detail_rating_frame.winfo_children():
            widget.destroy()
        
        # Mostrar estrellas según la valoración
        rating = restaurant["rating"]
        for i in range(5):
            if i < int(rating):
                star = "★"  # Estrella completa
            elif i < rating and i >= int(rating):
                star = "⯪"  # Media estrella (aproximación)
            else:
                star = "☆"  # Estrella vacía
            
            star_label = tk.Label(
                self.detail_rating_frame,
                text=star,
                font=self.description_font,
                bg="white",
                fg="gold"
            )
            star_label.pack(side=tk.LEFT)
        
        rating_value = tk.Label(
            self.detail_rating_frame,
            text=f" {rating}",
            font=self.description_font,
            bg="white"
        )
        rating_value.pack(side=tk.LEFT)
        
        # Limpiar menú anterior
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        
        # Mostrar menú del restaurante
        if "menu" in restaurant:
            for item in restaurant["menu"]:
                dish_frame = tk.Frame(self.menu_frame, bg="white")
                dish_frame.pack(fill=tk.X, pady=5)
                
                dish_name = tk.Label(
                    dish_frame,
                    text=item["name"],
                    font=self.description_font,
                    bg="white",
                    anchor="w"
                )
                dish_name.pack(side=tk.LEFT)
                
                dish_price = tk.Label(
                    dish_frame,
                    text=f"$ {item['price']}",
                    font=self.description_font,
                    bg="white"
                )
                dish_price.pack(side=tk.RIGHT)
                
                # Descripción del plato
                dish_desc = tk.Label(
                    self.menu_frame,
                    text=item["description"],
                    font=("Helvetica", 8),
                    bg="white",
                    fg="gray",
                    wraplength=350,
                    justify=tk.LEFT,
                    anchor="w"
                )
                dish_desc.pack(anchor="w", pady=(0, 10))
        
        # Mostrar pantalla de detalles
        self.show_frame(self.restaurant_detail_frame)
    
    def filter_by_category_number(self, index):
        # Filtrar por número (1, 2, 3)
        categories_by_number = {
            0: "Carnes",      # 1
            1: "Italiana",    # 2
            2: "Vegetariana"  # 3
        }
        
        if index in categories_by_number:
            self.current_category = categories_by_number[index]
            self.display_restaurants()
    
    def filter_by_category(self, category):
        self.current_category = category
        
        # Actualizar botones de categoría
        for widget in self.search_scrollable_frame.winfo_children()[1].winfo_children()[0].winfo_children():
            if isinstance(widget, tk.Button):
                if widget.cget("text") == category:
                    widget.config(bg=self.main_color)
                else:
                    widget.config(bg="white")
        
        # Actualizar resultados
        self.search_restaurants()
    
    def sort_restaurants(self):
        self.current_sort = self.sort_var.get()
        self.search_restaurants()
    
    def search_restaurants(self):
        # Limpiar resultados anteriores
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()
        
        search_term = self.search_var.get().lower()
        
        # Filtrar por categoría y término de búsqueda
        filtered_restaurants = []
        
        if self.current_category == "Todas":
            base_restaurants = self.restaurants
        else:
            base_restaurants = [r for r in self.restaurants if r["category"] == self.current_category]
        
        if search_term:
            for restaurant in base_restaurants:
                if (search_term in restaurant["name"].lower() or 
                    search_term in restaurant["category"].lower() or 
                    search_term in restaurant["description"].lower()):
                    filtered_restaurants.append(restaurant)
        else:
            filtered_restaurants = base_restaurants
        
        # Ordenar resultados
        if self.current_sort == "distance":
            filtered_restaurants = sorted(filtered_restaurants, key=lambda x: x["distance"])
        elif self.current_sort == "rating":
            filtered_restaurants = sorted(filtered_restaurants, key=lambda x: x["rating"], reverse=True)
        
        if not filtered_restaurants:
            empty_label = tk.Label(
                self.search_results_frame,
                text="No se encontraron resultados",
                font=self.menu_font,
                bg="white"
            )
            empty_label.pack(pady=50)
            return
        
        # Mostrar resultados
        results_label = tk.Label(
            self.search_results_frame,
            text=f"Resultados ({len(filtered_restaurants)})",
            font=self.menu_font,
            bg="white"
        )
        results_label.pack(anchor="w", pady=10)
        
        # Mostrar restaurantes filtrados
        for restaurant in filtered_restaurants:
            self.create_restaurant_card_search(restaurant)
    
    def create_restaurant_card_search(self, restaurant):
        # Similar a create_restaurant_card pero para la pantalla de búsqueda
        card = tk.Frame(self.search_results_frame, bg="white", bd=1, relief=tk.SOLID)
        card.pack(fill=tk.X, pady=10)
        
        # Contenido de la tarjeta
        content_frame = tk.Frame(card, bg="white")
        content_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Nombre del restaurante
        name_label = tk.Label(
            content_frame,
            text=restaurant["name"],
            font=self.restaurant_font,
            bg="white",
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # Categoría y precio
        category_price = tk.Label(
            content_frame,
            text=f"{restaurant['category']} | {restaurant['price_level']}",
            font=self.description_font,
            bg="white",
            fg="gray",
            anchor="w"
        )
        category_price.pack(anchor="w")
        
        # Valoración con estrellas
        rating_frame = tk.Frame(content_frame, bg="white")
        rating_frame.pack(anchor="w", pady=5)
        
        # Mostrar estrellas según la valoración
        rating = restaurant["rating"]
        for i in range(5):
            if i < int(rating):
                star = "★"  # Estrella completa
            elif i < rating and i >= int(rating):
                star = "⯪"  # Media estrella (aproximación)
            else:
                star = "☆"  # Estrella vacía
            
            star_label = tk.Label(
                rating_frame,
                text=star,
                font=self.description_font,
                bg="white",
                fg="gold"
            )
            star_label.pack(side=tk.LEFT)
        
        rating_value = tk.Label(
            rating_frame,
            text=f" {rating}",
            font=self.description_font,
            bg="white"
        )
        rating_value.pack(side=tk.LEFT)
        
        # Distancia
        distance_label = tk.Label(
            content_frame,
            text=f"{restaurant['distance']} km de distancia",
            font=self.description_font,
            bg="white",
            anchor="w"
        )
        distance_label.pack(anchor="w")
        
        # Hacer que la tarjeta sea clickeable
        for widget in [card, content_frame, name_label, category_price, rating_frame, distance_label]:
            widget.bind("<Button-1>", lambda event, r=restaurant: self.show_restaurant_details(r))
    
    def reserve_table(self):
        # Simular reserva de mesa
        messagebox.showinfo("Reserva", "¡Reserva realizada con éxito!")
    
    def edit_profile(self):
        # Simular edición de perfil
        messagebox.showinfo("Editar Perfil", "Función de edición de perfil en desarrollo")
    
    def logout(self):
        # Simular cierre de sesión
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas cerrar sesión?"):
            messagebox.showinfo("Cerrar Sesión", "Has cerrado sesión correctamente")
    
    def show_settings(self):
        # Simular configuración
        self.toggle_menu()
        messagebox.showinfo("Configuración", "Configuración en desarrollo")
    
    def show_help(self):
        # Simular ayuda
        self.toggle_menu()
        messagebox.showinfo("Ayuda", "Sección de ayuda en desarrollo")

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodloversApp(root)
    root.mainloop()