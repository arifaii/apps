import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont, filedialog
import json
import hashlib
import random
import time
from datetime import datetime, timedelta
import math
import threading
import os
from dataclasses import dataclass
from typing import List, Dict, Optional
import mysql.connector
from mysql.connector import Error

@dataclass
class Product:
    id: int
    name: str
    price: float
    category: str
    rating: float
    description: str
    stock: int
    image_path: str = None
    discount: float = 0.0
    marca: str = None
    tipo_mascota: str = None
    edad_mascota: str = None

@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    created_at: str
    is_premium: bool = False
    nombre: str = None
    apellido: str = None
    telefono: str = None
    direccion: str = None
    ciudad: str = None
    codigo_postal: str = None

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
        
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',  # Cambia por tu usuario de MySQL
                password='',  # Cambia por tu contraseña de MySQL
                database='petZone'
            )
            if self.connection.is_connected():
                print("Conexión a MySQL establecida")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            messagebox.showerror("Error de Base de Datos", f"No se pudo conectar a la base de datos: {e}")
    
    def reconnect(self):
        if not self.connection or not self.connection.is_connected():
            self.connect()
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False, commit=False):
        cursor = None
        try:
            self.reconnect()
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if commit:
                self.connection.commit()
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            
            return True
        except Error as e:
            print(f"Error en la consulta: {e}")
            if self.connection:
                self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
    
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def init_sample_data(self):
        """Inicializa datos de ejemplo si la base de datos está vacía"""
        # Verificar si ya hay productos
        query = "SELECT COUNT(*) as count FROM productos"
        result = self.execute_query(query, fetch_one=True)
        
        if result and result['count'] == 0:
            # Insertar categorías primero si no existen
            categories = ["Alimento Perros", "Juguetes", "Accesorios", "Higiene"]
            for cat in categories:
                self.execute_query(
                    "INSERT INTO categorias (nombre) VALUES (%s) ON DUPLICATE KEY UPDATE nombre=nombre",
                    (cat,),
                    commit=True
                )
            
            # Insertar productos de ejemplo
            sample_products = [
                ("Comida Premium para Perros", 15990, "Alimento Perros", 4.5, 
                 "Alimento balanceado premium para perros adultos", 50, 0.10, "Royal Canin", "perro", "adulto"),
                ("Juguete Interactivo para Gatos", 8500, "Juguetes", 4.2, 
                 "Juguete que estimula la mente de tu gato", 30, 0.15, "Kong", "gato", "todas"),
                ("Correa Retráctil", 12750, "Accesorios", 4.0, 
                 "Correa retráctil de 5 metros para paseos seguros", 25, 0.0, "PetSafe", "perro", "todas"),
                ("Cama Ortopédica", 24990, "Accesorios", 4.8, 
                 "Cama ortopédica para el descanso óptimo", 15, 0.20, "OrthoPet", "perro", "senior"),
                ("Shampoo Hipoalergénico", 9990, "Higiene", 4.3, 
                 "Shampoo especial para pieles sensibles", 40, 0.0, "VetPlus", "todas", "todas"),
                ("Rascador Torre", 18500, "Accesorios", 4.6, 
                 "Torre rascadora de 1.5m con múltiples niveles", 20, 0.0, "CatFurniture", "gato", "todas"),
                ("Comedero Automático Smart", 32990, "Accesorios", 4.7, 
                 "Comedero programable con app móvil", 10, 0.25, "PetTech", "todas", "todas"),
                ("Kit de Juguetes Variados", 14500, "Juguetes", 4.4, 
                 "Set de 5 juguetes diferentes para entretenimiento", 35, 0.0, "PetFun", "todas", "todas")
            ]
            
            for product in sample_products:
                query = """
                INSERT INTO productos (nombre, precio, descripcion, stock, marca, tipo_mascota, edad_mascota, categoria_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 
                    (SELECT id FROM categorias WHERE nombre = %s LIMIT 1))
                """
                params = (
                    product[0], product[1], product[4], product[5], 
                    product[7], product[8], product[9], product[2]
                )
                self.execute_query(query, params, commit=True)

    def create_user(self, username: str, email: str, password: str, nombre: str = None, apellido: str = None) -> bool:
        """Crea un nuevo usuario en la base de datos"""
        password_hash = self.hash_password(password)
        
        # Verificar si el usuario o email ya existe
        query = "SELECT id FROM usuarios WHERE email = %s"
        result = self.execute_query(query, (email,), fetch_one=True)
        
        if result:
            return False
        
        # Crear nuevo usuario
        query = """
        INSERT INTO usuarios (username, email, password, nombre, apellido, fecha_registro)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """
        params = (username, email, password_hash, nombre or username, apellido or "")
        result = self.execute_query(query, params, commit=True)
        
        return bool(result)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Autentica un usuario"""
        password_hash = self.hash_password(password)
        
        query = """
        SELECT id, username, email, password as password_hash, 
               fecha_registro as created_at, nombre, apellido, telefono, direccion, ciudad, codigo_postal
        FROM usuarios 
        WHERE email = %s AND password = %s
        """
        result = self.execute_query(query, (email, password_hash), fetch_one=True)
        
        if result:
            return User(
                id=result['id'],
                username=result['username'],
                email=result['email'],
                password_hash=result['password_hash'],
                created_at=str(result['created_at']),
                nombre=result['nombre'],
                apellido=result['apellido'],
                telefono=result['telefono'],
                direccion=result['direccion'],
                ciudad=result['ciudad'],
                codigo_postal=result['codigo_postal']
            )
        return None

    def get_products(self, category: str = None, search: str = None) -> List[Product]:
        """Obtiene productos con filtros opcionales"""
        query = """
        SELECT p.id, p.nombre as name, p.precio as price, c.nombre as category, 
               p.descripcion as description, p.stock, p.marca, p.tipo_mascota, p.edad_mascota
        FROM productos p
        JOIN categorias c ON p.categoria_id = c.id
        WHERE 1=1
        """
        params = []
        
        if category and category != "Todos":
            query += " AND c.nombre = %s"
            params.append(category)
        
        if search:
            query += " AND (p.nombre LIKE %s OR p.descripcion LIKE %s)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        query += " ORDER BY p.nombre"
        
        results = self.execute_query(query, params, fetch_all=True) or []
        
        products = []
        for row in results:
            # Obtener rating promedio si existe
            rating_query = "SELECT AVG(rating) as avg_rating FROM reseñas WHERE producto_id = %s"
            rating_result = self.execute_query(rating_query, (row['id'],), fetch_one=True)
            avg_rating = rating_result['avg_rating'] if rating_result and rating_result['avg_rating'] else 4.0
            
            products.append(Product(
                id=row['id'],
                name=row['name'],
                price=float(row['price']),
                category=row['category'],
                rating=float(avg_rating),
                description=row['description'],
                stock=row['stock'],
                marca=row['marca'],
                tipo_mascota=row['tipo_mascota'],
                edad_mascota=row['edad_mascota']
            ))
        
        return products

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Obtiene un producto por ID"""
        query = """
        SELECT p.id, p.nombre as name, p.precio as price, c.nombre as category, 
               p.descripcion as description, p.stock, p.marca, p.tipo_mascota, p.edad_mascota
        FROM productos p
        JOIN categorias c ON p.categoria_id = c.id
        WHERE p.id = %s
        """
        result = self.execute_query(query, (product_id,), fetch_one=True)
        
        if result:
            # Obtener rating promedio
            rating_query = "SELECT AVG(rating) as avg_rating FROM reseñas WHERE producto_id = %s"
            rating_result = self.execute_query(rating_query, (product_id,), fetch_one=True)
            avg_rating = rating_result['avg_rating'] if rating_result and rating_result['avg_rating'] else 4.0
            
            return Product(
                id=result['id'],
                name=result['name'],
                price=float(result['price']),
                category=result['category'],
                rating=float(avg_rating),
                description=result['description'],
                stock=result['stock'],
                marca=result['marca'],
                tipo_mascota=result['tipo_mascota'],
                edad_mascota=result['edad_mascota']
            )
        return None

    def create_order(self, user_id: int, items: List[Dict], total: float, shipping_address: str) -> int:
        """Crea un nuevo pedido en la base de datos"""
        try:
            # Crear el pedido principal
            query = """
            INSERT INTO pedidos (usuario_id, total, estado, direccion_envio, fecha_pedido)
            VALUES (%s, %s, 'pendiente', %s, NOW())
            """
            params = (user_id, total, shipping_address)
            self.execute_query(query, params, commit=True)
            
            # Obtener el ID del pedido recién creado
            order_id = self.execute_query("SELECT LAST_INSERT_ID() as id", fetch_one=True)['id']
            
            # Insertar los items del pedido
            for item in items:
                product = self.get_product_by_id(item['product_id'])
                if product:
                    query = """
                    INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    params = (order_id, item['product_id'], item['quantity'], product.price, 
                             product.price * item['quantity'])
                    self.execute_query(query, params, commit=True)
                    
                    # Actualizar el stock del producto
                    query = "UPDATE productos SET stock = stock - %s WHERE id = %s"
                    self.execute_query(query, (item['quantity'], item['product_id']), commit=True)
            
            return order_id
        except Error as e:
            print(f"Error al crear pedido: {e}")
            return None

    def get_user_orders(self, user_id: int) -> List[Dict]:
        """Obtiene los pedidos de un usuario"""
        query = """
        SELECT p.id, p.total, p.estado as status, p.fecha_pedido as created_at, 
               p.direccion_envio as shipping_address
        FROM pedidos p
        WHERE p.usuario_id = %s
        ORDER BY p.fecha_pedido DESC
        """
        results = self.execute_query(query, (user_id,), fetch_all=True) or []
        
        orders = []
        for row in results:
            # Obtener items del pedido
            items_query = """
            SELECT pr.nombre, dp.cantidad 
            FROM detalle_pedido dp
            JOIN productos pr ON dp.producto_id = pr.id
            WHERE dp.pedido_id = %s
            """
            items_result = self.execute_query(items_query, (row['id'],), fetch_all=True) or []
            items_str = ", ".join([f"{item['nombre']} x{item['cantidad']}" for item in items_result])
            
            orders.append({
                'id': row['id'],
                'total': float(row['total']),
                'status': row['status'],
                'created_at': str(row['created_at']),
                'shipping_address': row['shipping_address'],
                'items': items_str or "No hay detalles"
            })
        
        return orders

    def add_to_favorites(self, user_id: int, product_id: int) -> bool:
        """Agrega un producto a favoritos"""
        # Verificar si ya es favorito
        query = "SELECT id FROM favoritos WHERE usuario_id = %s AND producto_id = %s"
        result = self.execute_query(query, (user_id, product_id), fetch_one=True)
        
        if result:
            return False
        
        # Agregar a favoritos
        query = "INSERT INTO favoritos (usuario_id, producto_id, fecha_agregado) VALUES (%s, %s, NOW())"
        return bool(self.execute_query(query, (user_id, product_id), commit=True))

    def remove_from_favorites(self, user_id: int, product_id: int) -> bool:
        """Remueve un producto de favoritos"""
        query = "DELETE FROM favoritos WHERE usuario_id = %s AND producto_id = %s"
        return bool(self.execute_query(query, (user_id, product_id), commit=True))

    def get_user_favorites(self, user_id: int) -> List[Product]:
        """Obtiene los productos favoritos de un usuario"""
        query = """
        SELECT p.id, p.nombre as name, p.precio as price, c.nombre as category, 
               p.descripcion as description, p.stock, p.marca, p.tipo_mascota, p.edad_mascota
        FROM favoritos f
        JOIN productos p ON f.producto_id = p.id
        JOIN categorias c ON p.categoria_id = c.id
        WHERE f.usuario_id = %s
        ORDER BY f.fecha_agregado DESC
        """
        results = self.execute_query(query, (user_id,), fetch_all=True) or []
        
        favorites = []
        for row in results:
            # Obtener rating promedio
            rating_query = "SELECT AVG(rating) as avg_rating FROM reseñas WHERE producto_id = %s"
            rating_result = self.execute_query(rating_query, (row['id'],), fetch_one=True)
            avg_rating = rating_result['avg_rating'] if rating_result and rating_result['avg_rating'] else 4.0
            
            favorites.append(Product(
                id=row['id'],
                name=row['name'],
                price=float(row['price']),
                category=row['category'],
                rating=float(avg_rating),
                description=row['description'],
                stock=row['stock'],
                marca=row['marca'],
                tipo_mascota=row['tipo_mascota'],
                edad_mascota=row['edad_mascota']
            ))
        
        return favorites

    def is_favorite(self, user_id: int, product_id: int) -> bool:
        """Verifica si un producto está en favoritos"""
        query = "SELECT id FROM favoritos WHERE usuario_id = %s AND producto_id = %s"
        result = self.execute_query(query, (user_id, product_id), fetch_one=True)
        return bool(result)

    def get_categories(self) -> List[str]:
        """Obtiene todas las categorías disponibles"""
        query = "SELECT nombre FROM categorias ORDER BY nombre"
        results = self.execute_query(query, fetch_all=True) or []
        return ["Todos"] + [row['nombre'] for row in results]

class NotificationManager:
    def __init__(self, parent):
        self.parent = parent
        self.notifications = []

    def show_notification(self, message: str, type: str = "info", duration: int = 3000):
        """Muestra una notificación temporal"""
        notification = tk.Toplevel(self.parent)
        notification.overrideredirect(True)
        notification.attributes("-topmost", True)
        
        # Colores según tipo
        colors = {
            "info": "#2196F3",
            "success": "#4CAF50",
            "warning": "#FF9800",
            "error": "#F44336"
        }
        
        bg_color = colors.get(type, "#2196F3")
        
        # Posición
        try:
            x = self.parent.winfo_x() + self.parent.winfo_width() - 300
            y = self.parent.winfo_y() + 80 + len(self.notifications) * 70
        except:
            x = 100
            y = 100
        
        notification.geometry(f"280x60+{x}+{y}")
        notification.configure(bg=bg_color)
        
        # Contenido
        frame = tk.Frame(notification, bg=bg_color)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        label = tk.Label(
            frame,
            text=message,
            font=("Arial", 10),
            bg=bg_color,
            fg="white",
            wraplength=250,
            justify=tk.LEFT
        )
        label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        close_btn = tk.Button(
            frame,
            text="✕",
            font=("Arial", 8),
            bg=bg_color,
            fg="white",
            relief=tk.FLAT,
            command=lambda: self.close_notification(notification)
        )
        close_btn.pack(side=tk.RIGHT)
        
        self.notifications.append(notification)
        
        # Auto-cerrar
        self.parent.after(duration, lambda: self.close_notification(notification))

    def close_notification(self, notification):
        """Cierra una notificación"""
        if notification in self.notifications:
            self.notifications.remove(notification)
            try:
                notification.destroy()
            except:
                pass
            
            # Reposicionar notificaciones restantes
            for i, notif in enumerate(self.notifications):
                try:
                    x = self.parent.winfo_x() + self.parent.winfo_width() - 300
                    y = self.parent.winfo_y() + 80 + i * 70
                    notif.geometry(f"280x60+{x}+{y}")
                except:
                    pass

class ImprovedPetZoneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PetZone - Tienda de Mascotas")
        
        # Inicializar managers
        self.db = DatabaseManager()
        self.db.init_sample_data()
        self.notifications = NotificationManager(root)
        
        # Usuario actual
        self.current_user: Optional[User] = None
        
        # Configuración responsive
        self.setup_responsive_window()
        
        # Variables para el tema
        self.is_dark_mode = False
        self.update_theme_colors()
        
        # Configurar fuentes responsivas
        self.setup_responsive_fonts()
        
        # Variables para formularios
        self.setup_form_variables()
        
        # Variables para animaciones
        self.current_frame = None
        self.animation_in_progress = False
        
        # Carrito de compras
        self.cart_items = []
        
        # Categorías
        self.categories = self.db.get_categories()
        self.selected_category = "Todos"
        
        # Crear frames
        self.setup_frames()
        
        # Inicializar pantallas
        self.setup_all_screens()
        
        # Configurar eventos
        self.root.bind('<Configure>', self.on_window_resize)
        
        # Mostrar pantalla de bienvenida
        self.show_frame_with_animation(self.welcome_frame)
        
        # Configurar cierre de aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_form_variables(self):
        """Configura variables para formularios"""
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.new_username_var = tk.StringVar()
        self.new_email_var = tk.StringVar()
        self.new_password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.shipping_address_var = tk.StringVar()

    def setup_responsive_window(self):
        """Configura la ventana para ser responsive"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.is_mobile = screen_width < 600
        
        if self.is_mobile:
            self.window_width = min(screen_width - 20, 400)
            self.window_height = min(screen_height - 100, 700)
        else:
            self.window_width = 450
            self.window_height = 750
        
        # Centrar ventana
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        
        self.root.minsize(320, 500)
        self.root.maxsize(600, 900)
        self.root.resizable(True, True)

    def setup_responsive_fonts(self):
        """Configura fuentes responsivas"""
        base_size = 10 if self.is_mobile else 12
        
        self.title_font = tkfont.Font(family="Arial", size=base_size + 8, weight="bold")
        self.welcome_font = tkfont.Font(family="Arial", size=base_size + 6, slant="italic")
        self.button_font = tkfont.Font(family="Arial", size=base_size)
        self.label_font = tkfont.Font(family="Arial", size=base_size - 1)
        self.copyright_font = tkfont.Font(family="Arial", size=base_size - 2)

    def update_theme_colors(self):
        """Actualiza colores del tema"""
        if not self.is_dark_mode:
            self.bg_color = "#f5f5f5"
            self.fg_color = "#333333"
            self.header_color = "#e69138"
            self.header_text_color = "#ffffff"
            self.button_color = "#e69138"
            self.button_text_color = "#ffffff"
            self.card_bg = "#ffffff"
            self.highlight_color = "#ffd700"
            self.accent_color = "#4CAF50"
        else:
            self.bg_color = "#121212"
            self.fg_color = "#ffffff"
            self.header_color = "#b36b1d"
            self.header_text_color = "#ffffff"
            self.button_color = "#b36b1d"
            self.button_text_color = "#ffffff"
            self.card_bg = "#1e1e1e"
            self.highlight_color = "#ffd700"
            self.accent_color = "#66BB6A"

    def setup_frames(self):
        """Crea todos los frames de la aplicación"""
        self.welcome_frame = tk.Frame(self.root)
        self.login_frame = tk.Frame(self.root)
        self.register_frame = tk.Frame(self.root)
        self.home_frame = tk.Frame(self.root)
        self.cart_frame = tk.Frame(self.root)
        self.product_detail_frame = tk.Frame(self.root)
        self.profile_frame = tk.Frame(self.root)
        self.favorites_frame = tk.Frame(self.root)
        self.orders_frame = tk.Frame(self.root)
        self.settings_frame = tk.Frame(self.root)

    def setup_all_screens(self):
        """Inicializa todas las pantallas"""
        self.setup_welcome_screen()
        self.setup_login_screen()
        self.setup_register_screen()
        self.setup_home_screen()
        self.setup_cart_screen()
        self.setup_product_detail_screen()
        self.setup_profile_screen()
        self.setup_favorites_screen()
        self.setup_orders_screen()
        self.setup_settings_screen()

    def on_window_resize(self, event):
        """Maneja el redimensionamiento de la ventana"""
        if event.widget == self.root:
            self.window_width = self.root.winfo_width()
            self.window_height = self.root.winfo_height()
            
            was_mobile = self.is_mobile
            self.is_mobile = self.window_width < 500
            
            if was_mobile != self.is_mobile:
                self.setup_responsive_fonts()

    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
            self.root.destroy()

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
                    widget.configure(bg=self.bg_color, fg=self.fg_color)
                elif widget_type == 'Button':
                    if 'theme' not in str(widget):
                        widget.configure(bg=self.button_color, fg=self.button_text_color)
                elif widget_type == 'Entry':
                    widget.configure(bg=self.card_bg, fg=self.fg_color)
            except:
                pass

    def toggle_theme(self):
        """Cambia entre tema claro y oscuro"""
        self.is_dark_mode = not self.is_dark_mode
        self.update_theme_colors()
        
        for frame in [self.welcome_frame, self.login_frame, self.register_frame, 
                     self.home_frame, self.cart_frame, self.product_detail_frame,
                     self.profile_frame, self.favorites_frame, self.orders_frame,
                     self.settings_frame]:
            self.update_frame_colors(frame)
        
        self.notifications.show_notification(
            f"Tema {'oscuro' if self.is_dark_mode else 'claro'} activado",
            "success"
        )

    def create_responsive_header(self, parent, title_text="PetZone"):
        """Crea un header responsive"""
        # Barra superior
        top_bar = tk.Frame(parent, bg="#333333", height=15 if self.is_mobile else 20)
        top_bar.pack(fill=tk.X)
        
        time_label = tk.Label(
            top_bar, 
            text=time.strftime("%H:%M"),
            font=self.copyright_font,
            bg="#333333",
            fg="#FFFFFF"
        )
        time_label.pack(side=tk.RIGHT, padx=5)
        
        # Header principal
        header = tk.Frame(parent, bg=self.header_color, height=50 if self.is_mobile else 60)
        header.pack(fill=tk.X)
        
        title_label = tk.Label(
            header, 
            text=title_text, 
            font=self.title_font, 
            bg=self.header_color, 
            fg=self.header_text_color
        )
        title_label.pack(pady=10)
        
        return header

    def create_responsive_footer(self, parent):
        """Crea un footer responsive"""
        footer = tk.Frame(parent, bg=self.bg_color, height=30 if self.is_mobile else 40)
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
        theme_button.pack(side=tk.LEFT, padx=10)
        
        copyright_label = tk.Label(
            footer, 
            text="© PetZone 2025", 
            font=self.copyright_font, 
            bg=self.bg_color,
            fg=self.fg_color
        )
        copyright_label.pack(side=tk.RIGHT, pady=5, padx=10)
        
        return footer

    def setup_welcome_screen(self):
        """Configura la pantalla de bienvenida mejorada"""
        self.create_responsive_header(self.welcome_frame)
        
        content = tk.Frame(self.welcome_frame, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Logo animado
        logo_frame = tk.Frame(content, bg=self.bg_color)
        logo_frame.pack(pady=20)
        
        logo_canvas = tk.Canvas(logo_frame, width=150, height=150, 
                               bg=self.bg_color, highlightthickness=0)
        logo_canvas.pack()
        
        # Dibujar logo con animación
        self.animate_logo(logo_canvas)
        
        # Mensaje de bienvenida
        welcome_label = tk.Label(
            content, 
            text="¡Bienvenidos a PetZone!", 
            font=self.welcome_font, 
            bg=self.bg_color,
            fg=self.fg_color
        )
        welcome_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            content, 
            text="Todo lo que tu mascota necesita\ncon la mejor calidad y servicio", 
            font=self.label_font, 
            bg=self.bg_color,
            fg=self.fg_color,
            justify=tk.CENTER
        )
        subtitle_label.pack(pady=10)
        
        # Botones mejorados
        buttons_frame = tk.Frame(content, bg=self.bg_color)
        buttons_frame.pack(pady=30)
        
        login_button = tk.Button(
            buttons_frame, 
            text="🔑 Iniciar Sesión", 
            font=self.button_font,
            bg=self.button_color, 
            fg=self.button_text_color,
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=10,
            command=lambda: self.show_frame_with_animation(self.login_frame)
        )
        login_button.pack(pady=5, fill=tk.X if self.is_mobile else None)
        
        register_button = tk.Button(
            buttons_frame, 
            text="📝 Registrarse", 
            font=self.button_font,
            bg=self.accent_color, 
            fg="white",
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=10,
            command=lambda: self.show_frame_with_animation(self.register_frame)
        )
        register_button.pack(pady=5, fill=tk.X if self.is_mobile else None)
        
        guest_button = tk.Button(
            content, 
            text="👤 Continuar como invitado", 
            font=self.label_font,
            bg=self.bg_color, 
            fg=self.fg_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame_with_animation(self.home_frame)
        )
        guest_button.pack(pady=10)
        
        self.create_responsive_footer(self.welcome_frame)

    def animate_logo(self, canvas):
        """Anima el logo de bienvenida"""
        def draw_logo(angle=0):
            canvas.delete("all")
            center_x, center_y = 75, 75
            
            # Círculo principal
            radius = 40 + 5 * math.sin(angle)
            canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                fill=self.button_color, outline=""
            )
            
            # Texto
            canvas.create_text(
                center_x, center_y, 
                text="🐾", 
                font=("Arial", int(30 + 5 * math.sin(angle))), 
                fill="white"
            )
            
            # Continuar animación
            self.root.after(100, lambda: draw_logo(angle + 0.2))
        
        draw_logo()

    def setup_login_screen(self):
        """Configura la pantalla de login mejorada"""
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
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Icono de usuario
        icon_frame = tk.Frame(content, bg=self.bg_color)
        icon_frame.pack(pady=20)
        
        icon_label = tk.Label(
            icon_frame,
            text="👤",
            font=("Arial", 48),
            bg=self.bg_color,
            fg=self.fg_color
        )
        icon_label.pack()
        
        # Campos de entrada mejorados
        self.create_input_field(content, "Email:", self.new_email_var, "✉️")
        self.create_input_field(content, "Contraseña:", self.password_var, "🔒", show="•")
        
        # Checkbox recordar
        remember_frame = tk.Frame(content, bg=self.bg_color)
        remember_frame.pack(fill=tk.X, pady=10)
        
        self.remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(
            remember_frame,
            text="Recordarme",
            variable=self.remember_var,
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.card_bg
        )
        remember_check.pack(side=tk.LEFT)
        
        # Botón de login
        login_button = tk.Button(
            content, 
            text="🔑 Iniciar Sesión", 
            font=self.button_font,
            bg=self.button_color, 
            fg=self.button_text_color,
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=10,
            command=self.do_login
        )
        login_button.pack(pady=20, fill=tk.X)
        
        # Link de registro
        register_link = tk.Label(
            content,
            text="¿No tienes cuenta? Regístrate aquí",
            font=self.label_font,
            bg=self.bg_color,
            fg=self.button_color,
            cursor="hand2"
        )
        register_link.pack(pady=10)
        register_link.bind("<Button-1>", 
                          lambda e: self.show_frame_with_animation(self.register_frame))
        
        self.create_responsive_footer(self.login_frame)

    def create_input_field(self, parent, label_text, variable, icon="", show=None):
        """Crea un campo de entrada mejorado"""
        field_frame = tk.Frame(parent, bg=self.bg_color)
        field_frame.pack(fill=tk.X, pady=10)
        
        # Label con icono
        label_frame = tk.Frame(field_frame, bg=self.bg_color)
        label_frame.pack(fill=tk.X, pady=5)
        
        if icon:
            icon_label = tk.Label(
                label_frame,
                text=icon,
                font=("Arial", 14),
                bg=self.bg_color,
                fg=self.fg_color
            )
            icon_label.pack(side=tk.LEFT, padx=5)
        
        label = tk.Label(
            label_frame, 
            text=label_text, 
            font=self.label_font, 
            bg=self.bg_color, 
            fg=self.fg_color,
            anchor="w"
        )
        label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Entry con estilo
        entry = tk.Entry(
            field_frame,
            textvariable=variable,
            font=self.label_font,
            bd=2,
            relief=tk.GROOVE,
            bg=self.card_bg,
            fg=self.fg_color,
            show=show,
            insertbackground=self.fg_color
        )
        entry.pack(fill=tk.X, pady=5)
        
        # Efectos de foco
        def on_focus_in(event):
            entry.configure(bd=3, relief=tk.SOLID)
        
        def on_focus_out(event):
            entry.configure(bd=2, relief=tk.GROOVE)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
        return entry

    def do_login(self):
        """Maneja el login con validación mejorada"""
        email = self.new_email_var.get().strip()
        password = self.password_var.get()
        
        if not email or not password:
            self.notifications.show_notification(
                "Por favor ingrese email y contraseña", "warning"
            )
            return
        
        # Autenticar usuario
        user = self.db.authenticate_user(email, password)
        
        if user:
            self.current_user = user
            self.notifications.show_notification(
                f"¡Bienvenido, {user.nombre or user.username}!", "success"
            )
            self.show_frame_with_animation(self.home_frame)
            
            # Limpiar campos
            self.new_email_var.set("")
            self.password_var.set("")
        else:
            self.notifications.show_notification(
                "Email o contraseña incorrectos", "error"
            )

    def setup_register_screen(self):
        """Configura la pantalla de registro mejorada"""
        header = self.create_responsive_header(self.register_frame, "Crear Cuenta")
        
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
        
        # Contenido con scroll
        canvas = tk.Canvas(self.register_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.register_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        content = scrollable_frame
        
        # Título
        title_label = tk.Label(
            content,
            text="Crear cuenta nueva",
            font=self.welcome_font,
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack(pady=20)
        
        # Campos de registro
        self.create_input_field(content, "Nombre de usuario:", self.new_username_var, "👤")
        self.create_input_field(content, "Correo electrónico:", self.new_email_var, "✉️")
        self.create_input_field(content, "Contraseña:", self.new_password_var, "🔒", show="•")
        self.create_input_field(content, "Confirmar contraseña:", self.confirm_password_var, "🔐", show="•")
        
        # Indicador de fortaleza de contraseña
        self.password_strength_frame = tk.Frame(content, bg=self.bg_color)
        self.password_strength_frame.pack(fill=tk.X, pady=5)
        
        self.password_strength_label = tk.Label(
            self.password_strength_frame,
            text="",
            font=self.copyright_font,
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.password_strength_label.pack()
        
        # Vincular evento para verificar fortaleza
        self.new_password_var.trace("w", self.check_password_strength)
        
        # Términos y condiciones
        self.terms_var = tk.BooleanVar()
        terms_check = tk.Checkbutton(
            content,
            text="Acepto los términos y condiciones",
            variable=self.terms_var,
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.card_bg,
            wraplength=self.window_width - 100
        )
        terms_check.pack(pady=10)
        
        # Botón de registro
        register_button = tk.Button(
            content, 
            text="📝 Crear Cuenta", 
            font=self.button_font,
            bg=self.accent_color, 
            fg="white",
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=10,
            command=self.do_register
        )
        register_button.pack(pady=20, fill=tk.X)
        
        self.create_responsive_footer(self.register_frame)

    def check_password_strength(self, *args):
        """Verifica la fortaleza de la contraseña"""
        password = self.new_password_var.get()
        
        if not password:
            self.password_strength_label.config(text="", fg=self.fg_color)
            return
        
        score = 0
        feedback = []
        
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("mínimo 8 caracteres")
        
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("mayúsculas")
        
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("minúsculas")
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("números")
        
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        else:
            feedback.append("símbolos")
        
        if score < 2:
            strength = "Débil"
            color = "#F44336"
        elif score < 4:
            strength = "Media"
            color = "#FF9800"
        else:
            strength = "Fuerte"
            color = "#4CAF50"
        
        text = f"Fortaleza: {strength}"
        if feedback:
            text += f" (Falta: {', '.join(feedback)})"
        
        self.password_strength_label.config(text=text, fg=color)

    def do_register(self):
        """Maneja el registro con validación mejorada"""
        username = self.new_username_var.get().strip()
        email = self.new_email_var.get().strip()
        password = self.new_password_var.get()
        confirm = self.confirm_password_var.get()
        
        # Validaciones
        if not all([username, email, password, confirm]):
            self.notifications.show_notification(
                "Por favor complete todos los campos", "warning"
            )
            return
        
        if len(username) < 3:
            self.notifications.show_notification(
                "El usuario debe tener al menos 3 caracteres", "warning"
            )
            return
        
        if "@" not in email or "." not in email:
            self.notifications.show_notification(
                "Por favor ingrese un email válido", "warning"
            )
            return
        
        if len(password) < 6:
            self.notifications.show_notification(
                "La contraseña debe tener al menos 6 caracteres", "warning"
            )
            return
        
        if password != confirm:
            self.notifications.show_notification(
                "Las contraseñas no coinciden", "warning"
            )
            return
        
        if not self.terms_var.get():
            self.notifications.show_notification(
                "Debe aceptar los términos y condiciones", "warning"
            )
            return
        
        # Crear usuario
        if self.db.create_user(username, email, password):
            self.notifications.show_notification(
                f"Usuario {username} registrado correctamente", "success"
            )
            self.show_frame_with_animation(self.login_frame)
            
            # Limpiar campos
            self.new_username_var.set("")
            self.new_email_var.set("")
            self.new_password_var.set("")
            self.confirm_password_var.set("")
            self.terms_var.set(False)
        else:
            self.notifications.show_notification(
                "El email ya existe", "error"
            )

    def setup_home_screen(self):
        """Configura la pantalla principal mejorada"""
        header = self.create_responsive_header(self.home_frame, "Tienda")
        
        # Botones del header
        self.setup_header_buttons(header)
        
        content = tk.Frame(self.home_frame, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Barra de búsqueda mejorada
        self.setup_search_bar(content)
        
        # Filtros y categorías
        self.setup_filters(content)
        
        # Banner promocional
        if not self.is_mobile:
            self.setup_promotional_banner(content)
        
        # Contenedor de productos con scroll
        products_main_frame = tk.Frame(content, bg=self.bg_color)
        products_main_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Canvas y scrollbar para productos
        self.products_canvas = tk.Canvas(products_main_frame, bg=self.bg_color, highlightthickness=0)
        products_scrollbar = ttk.Scrollbar(products_main_frame, orient=tk.VERTICAL, command=self.products_canvas.yview)
        self.products_container = tk.Frame(self.products_canvas, bg=self.bg_color)

        self.products_container.bind(
            "<Configure>",
            lambda e: self.products_canvas.configure(scrollregion=self.products_canvas.bbox("all"))
        )

        self.products_canvas.create_window((0, 0), window=self.products_container, anchor="nw")
        self.products_canvas.configure(yscrollcommand=products_scrollbar.set)

        # Configurar scroll con rueda del mouse
        def _on_mousewheel(event):
            self.products_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.products_canvas.bind("<MouseWheel>", _on_mousewheel)

        self.products_canvas.pack(side="left", fill="both", expand=True)
        products_scrollbar.pack(side="right", fill="y")
        
        self.display_products()
        # Configurar scroll after showing products
        self.products_container.update_idletasks()
        self.products_canvas.configure(scrollregion=self.products_canvas.bbox("all"))
        self.create_responsive_footer(self.home_frame)

    def setup_header_buttons(self, header):
        """Configura los botones del header"""
        button_size = 12 if self.is_mobile else 14
        
        # Botón de carrito
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
        
        # Contador del carrito
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
        
        # Botón de perfil/favoritos
        if self.current_user:
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
            
            favorites_button = tk.Button(
                header,
                text="❤️",
                font=tkfont.Font(family="Arial", size=button_size),
                bg=self.header_color,
                fg=self.header_text_color,
                relief=tk.FLAT,
                command=lambda: self.show_frame_with_animation(self.favorites_frame)
            )
            favorites_button.place(x=profile_x - 40, y=10)
        
        # Botón de salir/volver
        logout_text = "Salir" if self.current_user else "← Inicio"
        logout_command = (lambda: self.logout()) if self.current_user else (lambda: self.show_frame_with_animation(self.welcome_frame))
        
        logout_button = tk.Button(
            header,
            text=logout_text,
            font=self.label_font,
            bg=self.header_color,
            fg=self.header_text_color,
            relief=tk.FLAT,
            command=logout_command
        )
        logout_button.place(x=10, y=10)

    def logout(self):
        """Cierra la sesión del usuario"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.current_user = None
            self.cart_items = []
            self.notifications.show_notification("Sesión cerrada", "info")
            self.show_frame_with_animation(self.welcome_frame)

    def setup_search_bar(self, parent):
        """Configura la barra de búsqueda mejorada"""
        search_frame = tk.Frame(parent, bg=self.card_bg, bd=1, relief=tk.SOLID)
        search_frame.pack(fill=tk.X, pady=10, padx=10)
        
        search_icon = tk.Label(
            search_frame,
            text="🔍",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        search_icon.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=self.label_font,
            bd=0,
            relief=tk.FLAT,
            bg=self.card_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5)
        self.search_entry.bind('<Return>', lambda e: self.search_products())
        
        search_button = tk.Button(
            search_frame,
            text="Buscar",
            font=self.label_font,
            bg=self.button_color,
            fg=self.button_text_color,
            relief=tk.FLAT,
            command=self.search_products
        )
        search_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def setup_filters(self, parent):
        """Configura los filtros de productos"""
        filters_frame = tk.Frame(parent, bg=self.bg_color)
        filters_frame.pack(fill=tk.X, pady=10)
        
        # Categorías
        categories_label = tk.Label(
            filters_frame,
            text="Categorías:",
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color
        )
        categories_label.pack(side=tk.LEFT, padx=5)
        
        if self.is_mobile:
            # Combobox para móvil
            self.category_var = tk.StringVar(value=self.selected_category)
            category_combo = ttk.Combobox(
                filters_frame,
                textvariable=self.category_var,
                values=self.categories,
                state="readonly",
                font=self.label_font,
                width=15
            )
            category_combo.pack(side=tk.LEFT, padx=5)
            category_combo.bind('<<ComboboxSelected>>', 
                               lambda e: self.filter_by_category(self.category_var.get()))
        else:
            # Botones para desktop
            categories_frame = tk.Frame(filters_frame, bg=self.bg_color)
            categories_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            for category in self.categories:
                is_selected = category == self.selected_category
                category_button = tk.Button(
                    categories_frame,
                    text=category,
                    font=self.copyright_font,
                    bg=self.button_color if is_selected else self.card_bg,
                    fg=self.button_text_color if is_selected else self.fg_color,
                    relief=tk.RAISED if is_selected else tk.GROOVE,
                    borderwidth=1,
                    padx=8,
                    pady=3,
                    command=lambda c=category: self.filter_by_category(c)
                )
                category_button.pack(side=tk.LEFT, padx=2)

    def setup_promotional_banner(self, parent):
        """Configura el banner promocional"""
        banner_frame = tk.Frame(parent, bg=self.bg_color, height=80)
        banner_frame.pack(fill=tk.X, pady=10, padx=10)
        
        banner_canvas = tk.Canvas(banner_frame, height=80, bg=self.accent_color, 
                                 highlightthickness=0)
        banner_canvas.pack(fill=tk.X)
        
        # Texto animado
        def animate_banner_text():
            banner_canvas.delete("all")
            current_time = time.time()
            offset = int(current_time * 50) % 400
            
            banner_canvas.create_text(
                200 + offset, 40, 
                text="🎉 ¡OFERTA ESPECIAL! 20% de descuento en productos seleccionados 🎉", 
                font=self.button_font,
                fill="white",
                anchor="w"
            )
            
            self.root.after(50, animate_banner_text)
        
        animate_banner_text()

    def display_products(self, search_term=None):
        """Muestra productos de forma mejorada"""
        for widget in self.products_container.winfo_children():
            widget.destroy()
        
        # Obtener productos de la base de datos
        products = self.db.get_products(
            category=self.selected_category if self.selected_category != "Todos" else None,
            search=search_term
        )
        
        if not products:
            no_products_label = tk.Label(
                self.products_container,
                text="No se encontraron productos",
                font=self.label_font,
                bg=self.bg_color,
                fg=self.fg_color
            )
            no_products_label.pack(pady=30)
            return
        
        # Crear grid responsive
        columns = 1 if self.is_mobile else 2
        row_frame = None
        
        for i, product in enumerate(products):
            if i % columns == 0:
                row_frame = tk.Frame(self.products_container, bg=self.bg_color)
                row_frame.pack(fill=tk.X, pady=5)
            
            self.create_product_card(row_frame, product, columns)

    def create_product_card(self, parent, product: Product, columns):
        """Crea una tarjeta de producto mejorada"""
        card_width = (self.window_width - 40) if columns == 1 else (self.window_width - 60) // 2
        card_height = 280 if self.is_mobile else 320
        
        product_card = tk.Frame(parent, bg=self.card_bg, bd=2, relief=tk.SOLID, 
                               width=card_width, height=card_height)
        product_card.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        product_card.pack_propagate(False)
        
        # Imagen del producto (placeholder mejorado)
        image_frame = tk.Frame(product_card, bg=self.card_bg, height=120)
        image_frame.pack(fill=tk.X, pady=10)
        image_frame.pack_propagate(False)
        
        # Crear imagen placeholder más atractiva
        image_canvas = tk.Canvas(image_frame, width=100, height=100, 
                               bg=self.card_bg, highlightthickness=0)
        image_canvas.pack()
        
        # Dibujar imagen según categoría
        self.draw_product_image(image_canvas, product.category)
        
        # Información del producto
        info_frame = tk.Frame(product_card, bg=self.card_bg)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Nombre del producto
        name_label = tk.Label(
            info_frame,
            text=product.name,
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color,
            wraplength=card_width - 20,
            justify=tk.LEFT
        )
        name_label.pack(anchor="w", pady=2)
        
        # Precio con descuento
        price_frame = tk.Frame(info_frame, bg=self.card_bg)
        price_frame.pack(fill=tk.X, pady=2)
        
        if product.discount > 0:
            original_price = product.price / (1 - product.discount)
            
            # Precio original tachado
            original_label = tk.Label(
                price_frame,
                text=f"$ {original_price:,.0f}",
                font=self.copyright_font,
                bg=self.card_bg,
                fg="gray"
            )
            original_label.pack(side=tk.LEFT)
            
            # Descuento
            discount_label = tk.Label(
                price_frame,
                text=f"-{product.discount*100:.0f}%",
                font=self.copyright_font,
                bg="red",
                fg="white",
                padx=3
            )
            discount_label.pack(side=tk.RIGHT)
        
        # Precio actual
        price_label = tk.Label(
            info_frame,
            text=f"$ {product.price:,.0f} ARS",
            font=self.button_font,
            bg=self.card_bg,
            fg=self.accent_color,
            anchor="w"
        )
        price_label.pack(fill=tk.X, pady=2)
        
        # Rating y stock
        details_frame = tk.Frame(info_frame, bg=self.card_bg)
        details_frame.pack(fill=tk.X, pady=2)
        
        # Estrellas
        stars_text = "★" * int(product.rating) + "☆" * (5 - int(product.rating))
        rating_label = tk.Label(
            details_frame,
            text=f"{stars_text} ({product.rating})",
            font=self.copyright_font,
            bg=self.card_bg,
            fg="#FFD700"
        )
        rating_label.pack(side=tk.LEFT)
        
        # Stock
        stock_color = self.accent_color if product.stock > 10 else "#FF9800" if product.stock > 0 else "#F44336"
        stock_text = f"Stock: {product.stock}" if product.stock > 0 else "Sin stock"
        
        stock_label = tk.Label(
            details_frame,
            text=stock_text,
            font=self.copyright_font,
            bg=self.card_bg,
            fg=stock_color
        )
        stock_label.pack(side=tk.RIGHT)
        
        # Botones de acción
        buttons_frame = tk.Frame(product_card, bg=self.card_bg)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        if self.is_mobile:
            # En móvil, solo botón de añadir
            add_button = tk.Button(
                buttons_frame,
                text="🛒 Añadir" if product.stock > 0 else "Sin stock",
                font=self.label_font,
                bg=self.button_color if product.stock > 0 else "gray",
                fg=self.button_text_color,
                relief=tk.RAISED,
                borderwidth=1,
                state=tk.NORMAL if product.stock > 0 else tk.DISABLED,
                command=lambda p=product: self.add_to_cart(p)
            )
            add_button.pack(fill=tk.X)
        else:
            # En desktop, botones separados
            view_button = tk.Button(
                buttons_frame,
                text="👁️ Ver",
                font=self.copyright_font,
                bg=self.card_bg,
                fg=self.fg_color,
                relief=tk.GROOVE,
                borderwidth=1,
                command=lambda p=product: self.show_product_detail(p)
            )
            view_button.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
            
            # Botón de favoritos
            if self.current_user:
                is_fav = self.db.is_favorite(self.current_user.id, product.id)
                fav_button = tk.Button(
                    buttons_frame,
                    text="❤️" if is_fav else "🤍",
                    font=self.copyright_font,
                    bg=self.card_bg,
                    fg="red" if is_fav else self.fg_color,
                    relief=tk.GROOVE,
                    borderwidth=1,
                    command=lambda p=product: self.toggle_favorite(p)
                )
                fav_button.pack(side=tk.LEFT, padx=2)
            
            add_button = tk.Button(
                buttons_frame,
                text="🛒" if product.stock > 0 else "❌",
                font=self.copyright_font,
                bg=self.button_color if product.stock > 0 else "gray",
                fg=self.button_text_color,
                relief=tk.RAISED,
                borderwidth=1,
                state=tk.NORMAL if product.stock > 0 else tk.DISABLED,
                command=lambda p=product: self.add_to_cart(p)
            )
            add_button.pack(side=tk.LEFT, padx=2)
        
        # Hacer la tarjeta clickeable
        def on_card_click(event):
            self.show_product_detail(product)
        
        for widget in [product_card, image_canvas, name_label, price_label]:
            widget.bind("<Button-1>", on_card_click)
            
            if not self.is_mobile:
                widget.bind("<Enter>", lambda e, card=product_card: card.configure(bg=self.highlight_color))
                widget.bind("<Leave>", lambda e, card=product_card: card.configure(bg=self.card_bg))

    def draw_product_image(self, canvas, category):
        """Dibuja una imagen representativa según la categoría"""
        canvas.delete("all")
        
        # Colores por categoría
        colors = {
            "Alimento Perros": "#8B4513",
            "Juguetes": "#FF69B4", 
            "Accesorios": "#4682B4",
            "Hogar": "#6B8E23",
            "Higiene": "#87CEEB",
            "Alimentación": "#CD853F"
        }
        
        color = colors.get(category, "#FF9800")
        
        # Dibujar forma básica
        canvas.create_oval(20, 20, 80, 80, fill=color, outline="")
        
        # Añadir icono según categoría
        icons = {
            "Alimento Perros": "🍖",
            "Juguetes": "🎾",
            "Accesorios": "🦮",
            "Hogar": "🏠",
            "Higiene": "🧼",
            "Alimentación": "🥣"
        }
        
        icon = icons.get(category, "🐾")
        canvas.create_text(50, 50, text=icon, font=("Arial", 20), fill="white")

    def filter_by_category(self, category):
        """Filtra productos por categoría"""
        self.selected_category = category
        self.display_products()
        self.notifications.show_notification(f"Mostrando: {category}", "info")

    def search_products(self):
        """Busca productos por término"""
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            self.notifications.show_notification("Ingrese un término de búsqueda", "warning")
            return
        
        self.display_products(search_term)
        self.notifications.show_notification(f"Buscando: {search_term}", "info")

    def add_to_cart(self, product: Product):
        """Añade producto al carrito con validaciones"""
        if product.stock <= 0:
            self.notifications.show_notification("Producto sin stock", "error")
            return
        
        # Verificar si ya está en el carrito
        existing_item = next((item for item in self.cart_items if item['product'].id == product.id), None)
        
        if existing_item:
            if existing_item['quantity'] >= product.stock:
                self.notifications.show_notification("No hay más stock disponible", "warning")
                return
            existing_item['quantity'] += 1
        else:
            self.cart_items.append({
                'product': product,
                'quantity': 1
            })
        
        # Actualizar contador
        total_items = sum(item['quantity'] for item in self.cart_items)
        self.cart_count_label.config(text=str(total_items))
        
        self.notifications.show_notification(f"{product.name} añadido al carrito", "success")
        if hasattr(self, 'update_cart_display'):
            self.update_cart_display()

    def toggle_favorite(self, product: Product):
        """Alterna el estado de favorito de un producto"""
        if not self.current_user:
            self.notifications.show_notification("Debe iniciar sesión", "warning")
            return
        
        is_fav = self.db.is_favorite(self.current_user.id, product.id)
        
        if is_fav:
            if self.db.remove_from_favorites(self.current_user.id, product.id):
                self.notifications.show_notification("Eliminado de favoritos", "info")
            else:
                self.notifications.show_notification("Error al eliminar favorito", "error")
        else:
            if self.db.add_to_favorites(self.current_user.id, product.id):
                self.notifications.show_notification("Añadido a favoritos", "success")
            else:
                self.notifications.show_notification("Error al añadir favorito", "error")
        
        # Refrescar la vista
        self.display_products()

    def show_product_detail(self, product: Product):
        """Muestra detalles del producto"""
        # Limpiar contenedor
        for widget in self.product_detail_container.winfo_children():
            widget.destroy()
        
        # Layout responsive
        if self.is_mobile:
            # Vertical para móvil
            self.create_mobile_product_detail(product)
        else:
            # Horizontal para desktop
            self.create_desktop_product_detail(product)
        
        self.show_frame_with_animation(self.product_detail_frame)

    def create_mobile_product_detail(self, product: Product):
        """Crea vista de detalle para móvil"""
        # Imagen
        image_frame = tk.Frame(self.product_detail_container, bg=self.card_bg, 
                              bd=1, relief=tk.SOLID, height=200)
        image_frame.pack(fill=tk.X, padx=10, pady=10)
        image_frame.pack_propagate(False)
        
        image_canvas = tk.Canvas(image_frame, width=150, height=150, 
                               bg=self.card_bg, highlightthickness=0)
        image_canvas.pack(expand=True)
        self.draw_product_image(image_canvas, product.category)
        
        # Información
        info_frame = tk.Frame(self.product_detail_container, bg=self.bg_color)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_product_info(info_frame, product)

    def create_desktop_product_detail(self, product: Product):
        """Crea vista de detalle para desktop"""
        top_frame = tk.Frame(self.product_detail_container, bg=self.bg_color)
        top_frame.pack(fill=tk.X, pady=10)
        
        # Imagen
        image_frame = tk.Frame(top_frame, bg=self.card_bg, bd=1, relief=tk.SOLID, 
                              width=250, height=250)
        image_frame.pack(side=tk.LEFT, padx=10, pady=10)
        image_frame.pack_propagate(False)
        
        image_canvas = tk.Canvas(image_frame, width=200, height=200, 
                               bg=self.card_bg, highlightthickness=0)
        image_canvas.pack(expand=True)
        self.draw_product_image(image_canvas, product.category)
        
        # Información
        info_frame = tk.Frame(top_frame, bg=self.bg_color)
        info_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.create_product_info(info_frame, product)

    def create_product_info(self, parent, product: Product):
        """Crea la información del producto"""
        # Nombre
        name_label = tk.Label(
            parent,
            text=product.name,
            font=self.welcome_font,
            bg=self.bg_color,
            fg=self.fg_color,
            wraplength=self.window_width - 100,
            justify=tk.LEFT,
            anchor="w"
        )
        name_label.pack(fill=tk.X, pady=5)
        
        # Categoría
        category_label = tk.Label(
            parent,
            text=f"Categoría: {product.category}",
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color,
            anchor="w"
        )
        category_label.pack(fill=tk.X, pady=2)
        
        # Marca
        if product.marca:
            marca_label = tk.Label(
                parent,
                text=f"Marca: {product.marca}",
                font=self.label_font,
                bg=self.bg_color,
                fg=self.fg_color,
                anchor="w"
            )
            marca_label.pack(fill=tk.X, pady=2)
        
        # Tipo y edad de mascota
        if product.tipo_mascota:
            tipo_label = tk.Label(
                parent,
                text=f"Para: {product.tipo_mascota} ({product.edad_mascota})",
                font=self.label_font,
                bg=self.bg_color,
                fg=self.fg_color,
                anchor="w"
            )
            tipo_label.pack(fill=tk.X, pady=2)
        
        # Rating
        stars_text = "★" * int(product.rating) + "☆" * (5 - int(product.rating))
        rating_label = tk.Label(
            parent,
            text=f"Calificación: {stars_text} ({product.rating}/5)",
            font=self.label_font,
            bg=self.bg_color,
            fg="#FFD700",
            anchor="w"
        )
        rating_label.pack(fill=tk.X, pady=2)
        
        # Stock
        stock_color = self.accent_color if product.stock > 10 else "#FF9800" if product.stock > 0 else "#F44336"
        stock_label = tk.Label(
            parent,
            text=f"Stock disponible: {product.stock} unidades",
            font=self.label_font,
            bg=self.bg_color,
            fg=stock_color,
            anchor="w"
        )
        stock_label.pack(fill=tk.X, pady=2)
        
        # Precio
        price_frame = tk.Frame(parent, bg=self.bg_color)
        price_frame.pack(fill=tk.X, pady=10)
        
        if product.discount > 0:
            original_price = product.price / (1 - product.discount)
            
            original_label = tk.Label(
                price_frame,
                text=f"Precio original: $ {original_price:,.0f} ARS",
                font=self.label_font,
                bg=self.bg_color,
                fg="gray"
            )
            original_label.pack(anchor="w")
            
            discount_label = tk.Label(
                price_frame,
                text=f"Descuento: {product.discount*100:.0f}%",
                font=self.label_font,
                bg=self.bg_color,
                fg="red"
            )
            discount_label.pack(anchor="w")
        
        current_price_label = tk.Label(
            price_frame,
            text=f"Precio: $ {product.price:,.0f} ARS",
            font=self.title_font,
            bg=self.bg_color,
            fg=self.accent_color
        )
        current_price_label.pack(anchor="w")
        
        # Botones de acción
        buttons_frame = tk.Frame(parent, bg=self.bg_color)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        # Cantidad
        quantity_frame = tk.Frame(buttons_frame, bg=self.bg_color)
        quantity_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            quantity_frame,
            text="Cantidad:",
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(side=tk.LEFT)
        
        self.quantity_var = tk.IntVar(value=1)
        quantity_spinbox = tk.Spinbox(
            quantity_frame,
            from_=1,
            to=min(product.stock, 10),
            textvariable=self.quantity_var,
            font=self.label_font,
            width=5,
            bg=self.card_bg,
            fg=self.fg_color
        )
        quantity_spinbox.pack(side=tk.LEFT, padx=10)
        
        # Botón añadir al carrito
        add_button = tk.Button(
            buttons_frame,
            text="🛒 Añadir al carrito" if product.stock > 0 else "Sin stock",
            font=self.button_font,
            bg=self.button_color if product.stock > 0 else "gray",
            fg=self.button_text_color,
            relief=tk.RAISED,
            borderwidth=2,
            padx=15,
            pady=8,
            state=tk.NORMAL if product.stock > 0 else tk.DISABLED,
            command=lambda: self.add_multiple_to_cart(product, self.quantity_var.get())
        )
        add_button.pack(fill=tk.X, pady=5)
        
        # Botón de favoritos (si está logueado)
        if self.current_user:
            is_fav = self.db.is_favorite(self.current_user.id, product.id)
            fav_text = "💔 Quitar de favoritos" if is_fav else "❤️ Añadir a favoritos"
            
            fav_button = tk.Button(
                buttons_frame,
                text=fav_text,
                font=self.button_font,
                bg=self.card_bg,
                fg="red" if is_fav else self.fg_color,
                relief=tk.GROOVE,
                borderwidth=1,
                padx=15,
                pady=8,
                command=lambda: self.toggle_favorite(product)
            )
            fav_button.pack(fill=tk.X, pady=5)
        
        # Descripción
        description_frame = tk.Frame(self.product_detail_container, bg=self.card_bg, 
                                   bd=1, relief=tk.SOLID)
        description_frame.pack(fill=tk.X, padx=10, pady=10)
        
        description_title = tk.Label(
            description_frame,
            text="Descripción del producto",
            font=self.button_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        description_title.pack(pady=10)
        
        description_text = tk.Label(
            description_frame,
            text=product.description or f"Producto de alta calidad para tu mascota. {product.name} está diseñado para proporcionar la mejor experiencia y cuidado.",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color,
            wraplength=self.window_width - 40,
            justify=tk.LEFT
        )
        description_text.pack(padx=10, pady=10)

    def add_multiple_to_cart(self, product: Product, quantity: int):
        """Añade múltiples unidades de un producto al carrito"""
        if product.stock < quantity:
            self.notifications.show_notification("No hay suficiente stock", "error")
            return
        
        # Verificar si ya está en el carrito
        existing_item = next((item for item in self.cart_items if item['product'].id == product.id), None)
        
        if existing_item:
            if existing_item['quantity'] + quantity > product.stock:
                self.notifications.show_notification("No hay suficiente stock", "warning")
                return
            existing_item['quantity'] += quantity
        else:
            self.cart_items.append({
                'product': product,
                'quantity': quantity
            })
        
        # Actualizar contador
        total_items = sum(item['quantity'] for item in self.cart_items)
        self.cart_count_label.config(text=str(total_items))
        
        self.notifications.show_notification(
            f"{quantity} x {product.name} añadido al carrito", "success"
        )
        if hasattr(self, 'update_cart_display'):
            self.update_cart_display()

    def setup_cart_screen(self):
        """Configura la pantalla del carrito mejorada"""
        header = self.create_responsive_header(self.cart_frame, "Mi Carrito")
        
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
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        cart_title = tk.Label(
            content, 
            text="🛒 Tus Productos", 
            font=self.welcome_font, 
            bg=self.bg_color,
            fg=self.fg_color
        )
        cart_title.pack(pady=10)
        
        # Contenedor de items con scroll
        cart_container = tk.Frame(content, bg=self.bg_color)
        cart_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.cart_canvas = tk.Canvas(cart_container, bg=self.bg_color, highlightthickness=0)
        self.cart_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        cart_scrollbar = ttk.Scrollbar(cart_container, orient=tk.VERTICAL, 
                                      command=self.cart_canvas.yview)
        cart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_canvas.configure(yscrollcommand=cart_scrollbar.set)
        
        self.cart_items_frame = tk.Frame(self.cart_canvas, bg=self.bg_color)
        self.cart_canvas.create_window((0, 0), window=self.cart_items_frame, anchor="nw")
        
        def configure_cart_scroll(event):
            self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))
        
        self.cart_items_frame.bind("<Configure>", configure_cart_scroll)
        
        # Resumen del carrito
        self.setup_cart_summary(content)
        
        # Inicializar vista
        self.update_cart_display()
        
        self.create_responsive_footer(self.cart_frame)

    def setup_cart_summary(self, parent):
        """Configura el resumen del carrito mejorado"""
        summary_frame = tk.Frame(parent, bg=self.card_bg, bd=2, relief=tk.SOLID)
        summary_frame.pack(fill=tk.X, pady=10)
        
        summary_title = tk.Label(
            summary_frame,
            text="📋 Resumen del pedido",
            font=self.button_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        summary_title.pack(pady=10)
        
        # Subtotal
        subtotal_frame = tk.Frame(summary_frame, bg=self.card_bg)
        subtotal_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            subtotal_frame,
            text="Subtotal:",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        ).pack(side=tk.LEFT)
        
        self.subtotal_label = tk.Label(
            subtotal_frame,
            text="$ 0 ARS",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        self.subtotal_label.pack(side=tk.RIGHT)
        
        # Descuentos
        discount_frame = tk.Frame(summary_frame, bg=self.card_bg)
        discount_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            discount_frame,
            text="Descuentos:",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        ).pack(side=tk.LEFT)
        
        self.discount_label = tk.Label(
            discount_frame,
            text="$ 0 ARS",
            font=self.label_font,
            bg=self.card_bg,
            fg="green"
        )
        self.discount_label.pack(side=tk.RIGHT)
        
        # Envío
        shipping_frame = tk.Frame(summary_frame, bg=self.card_bg)
        shipping_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            shipping_frame,
            text="Envío:",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        ).pack(side=tk.LEFT)
        
        self.shipping_label = tk.Label(
            shipping_frame,
            text="$ 0 ARS",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        self.shipping_label.pack(side=tk.RIGHT)
        
        # Total
        total_frame = tk.Frame(summary_frame, bg=self.card_bg)
        total_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            total_frame,
            text="TOTAL:",
            font=self.title_font,
            bg=self.card_bg,
            fg=self.fg_color
        ).pack(side=tk.LEFT)
        
        self.total_label = tk.Label(
            total_frame,
            text="$ 0 ARS",
            font=self.title_font,
            bg=self.card_bg,
            fg=self.accent_color
        )
        self.total_label.pack(side=tk.RIGHT)
        
        # Botones de acción
        buttons_frame = tk.Frame(parent, bg=self.bg_color)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        # Limpiar carrito
        clear_button = tk.Button(
            buttons_frame,
            text="🗑️ Limpiar carrito",
            font=self.label_font,
            bg="#F44336",
            fg="white",
            relief=tk.RAISED,
            borderwidth=1,
            command=self.clear_cart
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Continuar comprando
        continue_button = tk.Button(
            buttons_frame,
            text="🛍️ Seguir comprando",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color,
            relief=tk.RAISED,
            borderwidth=1,
            command=lambda: self.show_frame_with_animation(self.home_frame)
        )
        continue_button.pack(side=tk.LEFT, padx=5)
        
        # Proceder al pago
        self.checkout_button = tk.Button(
            buttons_frame, 
            text="💳 Proceder al pago", 
            font=self.button_font,
            bg=self.button_color, 
            fg=self.button_text_color,
            relief=tk.RAISED,
            borderwidth=2,
            padx=15,
            pady=8,
            command=self.checkout
        )
        self.checkout_button.pack(side=tk.RIGHT, padx=5)

    def update_cart_display(self):
        """Actualiza la visualización del carrito"""
        # Limpiar items
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()
        
        if not self.cart_items:
            empty_label = tk.Label(
                self.cart_items_frame,
                text="🛒 Tu carrito está vacío\n\n¡Explora nuestros productos y encuentra\nlo que tu mascota necesita!",
                font=self.label_font,
                bg=self.bg_color,
                fg=self.fg_color,
                justify=tk.CENTER
            )
            empty_label.pack(pady=50)
            
            # Deshabilitar botón de checkout
            if hasattr(self, 'checkout_button'):
                self.checkout_button.config(state=tk.DISABLED)
            
            self.update_cart_totals(0, 0, 0, 0)
            return
        
        # Habilitar botón de checkout
        if hasattr(self, 'checkout_button'):
            self.checkout_button.config(state=tk.NORMAL)
        
        # Mostrar items
        subtotal = 0
        total_discount = 0
        
        for i, item in enumerate(self.cart_items):
            product = item['product']
            quantity = item['quantity']
            
            item_frame = tk.Frame(self.cart_items_frame, bg=self.card_bg, bd=1, relief=tk.SOLID)
            item_frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Layout responsive
            if not self.is_mobile:
                # Imagen en desktop
                image_canvas = tk.Canvas(item_frame, width=60, height=60, 
                                       bg=self.card_bg, highlightthickness=0)
                image_canvas.pack(side=tk.LEFT, padx=5, pady=5)
                self.draw_product_image(image_canvas, product.category)
            
            # Detalles del producto
            details_frame = tk.Frame(item_frame, bg=self.card_bg)
            details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Nombre
            name_label = tk.Label(
                details_frame,
                text=product.name,
                font=self.label_font,
                bg=self.card_bg,
                fg=self.fg_color,
                anchor="w"
            )
            name_label.pack(fill=tk.X)
            
            # Precio unitario
            unit_price_label = tk.Label(
                details_frame,
                text=f"$ {product.price:,.0f} c/u",
                font=self.copyright_font,
                bg=self.card_bg,
                fg=self.fg_color,
                anchor="w"
            )
            unit_price_label.pack(fill=tk.X)
            
            # Controles de cantidad
            quantity_frame = tk.Frame(details_frame, bg=self.card_bg)
            quantity_frame.pack(fill=tk.X, pady=2)
            
            tk.Label(
                quantity_frame,
                text="Cantidad:",
                font=self.copyright_font,
                bg=self.card_bg,
                fg=self.fg_color
            ).pack(side=tk.LEFT)
            
            # Botón disminuir
            decrease_btn = tk.Button(
                quantity_frame,
                text="−",
                font=self.label_font,
                bg=self.card_bg,
                fg=self.fg_color,
                relief=tk.GROOVE,
                borderwidth=1,
                width=2,
                command=lambda idx=i: self.decrease_quantity(idx)
            )
            decrease_btn.pack(side=tk.LEFT, padx=2)
            
            # Cantidad actual
            quantity_label = tk.Label(
                quantity_frame,
                text=str(quantity),
                font=self.label_font,
                bg=self.card_bg,
                fg=self.fg_color,
                width=3
            )
            quantity_label.pack(side=tk.LEFT, padx=2)
            
            # Botón aumentar
            increase_btn = tk.Button(
                quantity_frame,
                text="+",
                font=self.label_font,
                bg=self.card_bg,
                fg=self.fg_color,
                relief=tk.GROOVE,
                borderwidth=1,
                width=2,
                command=lambda idx=i: self.increase_quantity(idx)
            )
            increase_btn.pack(side=tk.LEFT, padx=2)
            
            # Precio total del item
            item_total = product.price * quantity
            subtotal += item_total
            
            # Calcular descuento del item
            if product.discount > 0:
                original_item_total = (product.price / (1 - product.discount)) * quantity
                item_discount = original_item_total - item_total
                total_discount += item_discount
            
            # Controles del lado derecho
            controls_frame = tk.Frame(item_frame, bg=self.card_bg)
            controls_frame.pack(side=tk.RIGHT, padx=5, pady=5)
            
            # Precio total del item
            total_price_label = tk.Label(
                controls_frame,
                text=f"$ {item_total:,.0f}",
                font=self.button_font,
                bg=self.card_bg,
                fg=self.accent_color
            )
            total_price_label.pack()
            
            # Botón eliminar
            remove_button = tk.Button(
                controls_frame,
                text="🗑️",
                font=self.label_font,
                bg=self.card_bg,
                fg="#F44336",
                relief=tk.FLAT,
                command=lambda idx=i: self.remove_from_cart(idx)
            )
            remove_button.pack(pady=5)
        
        # Calcular envío
        shipping = 1500 if subtotal < 30000 else 0
        total = subtotal + shipping
        
        self.update_cart_totals(subtotal, total_discount, shipping, total)
        
        # Configurar scroll
        self.cart_items_frame.update_idletasks()
        self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))

    def update_cart_totals(self, subtotal, discount, shipping, total):
        """Actualiza los totales del carrito"""
        if hasattr(self, 'subtotal_label'):
            self.subtotal_label.config(text=f"$ {subtotal:,.0f} ARS")
        if hasattr(self, 'discount_label'):
            self.discount_label.config(text=f"- $ {discount:,.0f} ARS")
        if hasattr(self, 'shipping_label'):
            shipping_text = "GRATIS" if shipping == 0 else f"$ {shipping:,.0f} ARS"
            self.shipping_label.config(text=shipping_text)
        if hasattr(self, 'total_label'):
            self.total_label.config(text=f"$ {total:,.0f} ARS")

    def increase_quantity(self, index):
        """Aumenta la cantidad de un item"""
        if 0 <= index < len(self.cart_items):
            item = self.cart_items[index]
            if item['quantity'] < item['product'].stock:
                item['quantity'] += 1
                total_items = sum(item['quantity'] for item in self.cart_items)
                self.cart_count_label.config(text=str(total_items))
                self.update_cart_display()
            else:
                self.notifications.show_notification("No hay más stock disponible", "warning")

    def decrease_quantity(self, index):
        """Disminuye la cantidad de un item"""
        if 0 <= index < len(self.cart_items):
            item = self.cart_items[index]
            if item['quantity'] > 1:
                item['quantity'] -= 1
                total_items = sum(item['quantity'] for item in self.cart_items)
                self.cart_count_label.config(text=str(total_items))
                self.update_cart_display()
            else:
                self.remove_from_cart(index)

    def remove_from_cart(self, index):
        """Elimina un item del carrito"""
        if 0 <= index < len(self.cart_items):
            removed_item = self.cart_items.pop(index)
            total_items = sum(item['quantity'] for item in self.cart_items)
            self.cart_count_label.config(text=str(total_items))
            self.update_cart_display()
            self.notifications.show_notification(
                f"{removed_item['product'].name} eliminado del carrito", "info"
            )

    def clear_cart(self):
        """Limpia todo el carrito"""
        if not self.cart_items:
            return
        
        if messagebox.askyesno("Limpiar Carrito", "¿Está seguro que desea eliminar todos los productos?"):
            self.cart_items = []
            self.cart_count_label.config(text="0")
            self.update_cart_display()
            self.notifications.show_notification("Carrito limpiado", "info")

    def checkout(self):
        """Proceso de checkout mejorado"""
        if not self.cart_items:
            self.notifications.show_notification("No hay productos en el carrito", "warning")
            return
        
        if not self.current_user:
            self.notifications.show_notification("Debe iniciar sesión para comprar", "warning")
            self.show_frame_with_animation(self.login_frame)
            return
        
        # Calcular totales
        subtotal = sum(item['product'].price * item['quantity'] for item in self.cart_items)
        shipping = 1500 if subtotal < 30000 else 0
        total = subtotal + shipping
        
        # Ventana de checkout
        checkout_window = tk.Toplevel(self.root)
        checkout_window.title("Finalizar Compra")
        checkout_window.geometry("400x500")
        checkout_window.configure(bg=self.bg_color)
        checkout_window.transient(self.root)
        checkout_window.grab_set()
        
        # Centrar ventana
        checkout_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        # Título
        title_label = tk.Label(
            checkout_window,
            text="💳 Finalizar Compra",
            font=self.welcome_font,
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack(pady=20)
        
        # Resumen del pedido
        summary_frame = tk.Frame(checkout_window, bg=self.card_bg, bd=1, relief=tk.SOLID)
        summary_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            summary_frame,
            text="📋 Resumen del pedido",
            font=self.button_font,
            bg=self.card_bg,
            fg=self.fg_color
        ).pack(pady=10)
        
        # Items
        for item in self.cart_items:
            item_text = f"{item['quantity']}x {item['product'].name}"
            item_price = f"$ {item['product'].price * item['quantity']:,.0f}"
            
            item_frame = tk.Frame(summary_frame, bg=self.card_bg)
            item_frame.pack(fill=tk.X, padx=10, pady=2)
            
            tk.Label(
                item_frame,
                text=item_text,
                font=self.copyright_font,
                bg=self.card_bg,
                fg=self.fg_color
            ).pack(side=tk.LEFT)
            
            tk.Label(
                item_frame,
                text=item_price,
                font=self.copyright_font,
                bg=self.card_bg,
                fg=self.fg_color
            ).pack(side=tk.RIGHT)
        
        # Totales
        totals_frame = tk.Frame(summary_frame, bg=self.card_bg)
        totals_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            totals_frame,
            text=f"Subtotal: $ {subtotal:,.0f} ARS",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        ).pack(fill=tk.X)
        
        shipping_text = "GRATIS" if shipping == 0 else f"$ {shipping:,.0f} ARS"
        tk.Label(
            totals_frame,
            text=f"Envío: {shipping_text}",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        ).pack(fill=tk.X)
        
        tk.Label(
            totals_frame,
            text=f"TOTAL: $ {total:,.0f} ARS",
            font=self.button_font,
            bg=self.card_bg,
            fg=self.accent_color
        ).pack(fill=tk.X, pady=5)
        
        # Dirección de envío
        address_frame = tk.Frame(checkout_window, bg=self.bg_color)
        address_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            address_frame,
            text="🏠 Dirección de envío:",
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w")
        
        address_entry = tk.Text(
            address_frame,
            height=3,
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color,
            bd=1,
            relief=tk.SOLID
        )
        address_entry.pack(fill=tk.X, pady=5)
        
        # Pre-llenar con dirección del usuario si existe
        if self.current_user.direccion:
            address_entry.insert(tk.END, f"{self.current_user.direccion}, {self.current_user.ciudad or ''}")
        
        # Método de pago
        payment_frame = tk.Frame(checkout_window, bg=self.bg_color)
        payment_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            payment_frame,
            text="💳 Método de pago:",
            font=self.label_font,
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w")
        
        payment_var = tk.StringVar(value="Tarjeta de crédito")
        payment_methods = ["Tarjeta de crédito", "Tarjeta de débito", "Transferencia", "Efectivo"]
        
        for method in payment_methods:
            tk.Radiobutton(
                payment_frame,
                text=method,
                variable=payment_var,
                value=method,
                font=self.copyright_font,
                bg=self.bg_color,
                fg=self.fg_color,
                selectcolor=self.card_bg
            ).pack(anchor="w")
        
        # Botones
        buttons_frame = tk.Frame(checkout_window, bg=self.bg_color)
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        cancel_button = tk.Button(
            buttons_frame,
            text="❌ Cancelar",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color,
            relief=tk.RAISED,
            borderwidth=1,
            command=checkout_window.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        confirm_button = tk.Button(
            buttons_frame,
            text="✅ Confirmar Compra",
            font=self.button_font,
            bg=self.button_color,
            fg=self.button_text_color,
            relief=tk.RAISED,
            borderwidth=2,
            command=lambda: self.confirm_purchase(
                checkout_window, address_entry.get("1.0", tk.END).strip(),
                payment_var.get(), total
            )
        )
        confirm_button.pack(side=tk.RIGHT, padx=5)

    def confirm_purchase(self, window, address, payment_method, total):
        """Confirma la compra"""
        if not address:
            self.notifications.show_notification("Por favor ingrese la dirección de envío", "warning")
            return
        
        try:
            # Crear lista de items para la orden
            items = [{'product_id': item['product'].id, 'quantity': item['quantity']} 
                    for item in self.cart_items]
            
            # Crear la orden en la base de datos
            order_id = self.db.create_order(
                user_id=self.current_user.id,
                items=items,
                total=total,
                shipping_address=address
            )
            
            if order_id:
                success_message = f"¡Compra realizada con éxito!\n\nNúmero de pedido: #{order_id}\nTotal: $ {total:,.0f} ARS\nMétodo de pago: {payment_method}\n\n¡Gracias por tu compra!"
                
                # Mostrar confirmación
                messagebox.showinfo("Compra Exitosa", success_message)
                
                # Limpiar carrito
                self.cart_items = []
                self.cart_count_label.config(text="0")
                self.update_cart_display()
                
                # Cerrar ventana y volver al inicio
                window.destroy()
                self.show_frame_with_animation(self.home_frame)
                
                self.notifications.show_notification("¡Compra realizada con éxito!", "success")
            else:
                messagebox.showerror("Error", "Error al procesar la compra")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la compra: {str(e)}")

    def setup_product_detail_screen(self):
        """Configura la pantalla de detalles del producto"""
        header = self.create_responsive_header(self.product_detail_frame, "Detalle del Producto")
        
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
        
        # Contenido con scroll
        canvas = tk.Canvas(self.product_detail_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.product_detail_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        self.product_detail_container = scrollable_frame
        
        self.create_responsive_footer(self.product_detail_frame)

    def setup_profile_screen(self):
        """Configura la pantalla de perfil mejorada"""
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
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Contenido con scroll para el perfil
        profile_canvas = tk.Canvas(content, bg=self.bg_color, highlightthickness=0)
        profile_scrollbar = ttk.Scrollbar(content, orient="vertical", command=profile_canvas.yview)
        profile_scrollable_frame = tk.Frame(profile_canvas, bg=self.bg_color)

        profile_scrollable_frame.bind(
            "<Configure>",
            lambda e: profile_canvas.configure(scrollregion=profile_canvas.bbox("all"))
        )

        profile_canvas.create_window((0, 0), window=profile_scrollable_frame, anchor="nw")
        profile_canvas.configure(yscrollcommand=profile_scrollbar.set)

        profile_canvas.pack(side="left", fill="both", expand=True)
        profile_scrollbar.pack(side="right", fill="y")

        profile_content = profile_scrollable_frame

        # Avatar y información del usuario mejorada
        user_info_frame = tk.Frame(profile_content, bg=self.card_bg, bd=2, relief=tk.SOLID)
        user_info_frame.pack(fill=tk.X, pady=10)

        # Header del perfil
        profile_header = tk.Frame(user_info_frame, bg=self.button_color)
        profile_header.pack(fill=tk.X)

        tk.Label(
            profile_header,
            text="👤 Mi Perfil",
            font=self.welcome_font,
            bg=self.button_color,
            fg="white"
        ).pack(pady=10)

        # Avatar mejorado
        avatar_frame = tk.Frame(user_info_frame, bg=self.card_bg)
        avatar_frame.pack(pady=20)

        avatar_canvas = tk.Canvas(avatar_frame, width=100, height=100, 
                                 bg=self.card_bg, highlightthickness=0)
        avatar_canvas.pack()

        # Dibujar avatar más elaborado
        avatar_canvas.create_oval(10, 10, 90, 90, fill=self.button_color, outline="white", width=3)
        avatar_canvas.create_oval(20, 20, 80, 80, fill=self.accent_color, outline="")
        avatar_canvas.create_text(50, 50, text="👤", font=("Arial", 35), fill="white")

        # Información del usuario
        if self.current_user:
            # Nombre de usuario
            username_label = tk.Label(
                user_info_frame,
                text=self.current_user.username,
                font=self.title_font,
                bg=self.card_bg,
                fg=self.fg_color
            )
            username_label.pack(pady=5)
            
            # Email
            email_label = tk.Label(
                user_info_frame,
                text=self.current_user.email,
                font=self.label_font,
                bg=self.card_bg,
                fg=self.fg_color
            )
            email_label.pack(pady=2)
            
            # Fecha de registro
            created_date = self.current_user.created_at[:10] if self.current_user.created_at else "N/A"
            date_label = tk.Label(
                user_info_frame,
                text=f"Miembro desde: {created_date}",
                font=self.copyright_font,
                bg=self.card_bg,
                fg=self.fg_color
            )
            date_label.pack(pady=2)
            
            # Estadísticas del usuario
            stats_frame = tk.Frame(user_info_frame, bg=self.card_bg)
            stats_frame.pack(fill=tk.X, padx=20, pady=10)
            
            # Obtener estadísticas
            orders = self.db.get_user_orders(self.current_user.id)
            favorites = self.db.get_user_favorites(self.current_user.id)
            total_spent = sum(order['total'] for order in orders)
            
            stats_data = [
                ("📦", "Pedidos", len(orders)),
                ("❤️", "Favoritos", len(favorites)),
                ("💰", "Total gastado", f"${total_spent:,.0f}")
            ]
            
            for i, (icon, label, value) in enumerate(stats_data):
                stat_frame = tk.Frame(stats_frame, bg=self.card_bg)
                if i % 2 == 0:
                    stat_frame.pack(side=tk.LEFT, padx=10, expand=True)
                else:
                    stat_frame.pack(side=tk.RIGHT, padx=10, expand=True)
                
                tk.Label(
                    stat_frame,
                    text=icon,
                    font=("Arial", 20),
                    bg=self.card_bg,
                    fg=self.fg_color
                ).pack()
                
                tk.Label(
                    stat_frame,
                    text=str(value),
                    font=self.button_font,
                    bg=self.card_bg,
                    fg=self.accent_color
                ).pack()
                
                tk.Label(
                    stat_frame,
                    text=label,
                    font=self.copyright_font,
                    bg=self.card_bg,
                    fg=self.fg_color
                ).pack()

        else:
            guest_label = tk.Label(
                user_info_frame,
                text="Usuario Invitado",
                font=self.welcome_font,
                bg=self.card_bg,
                fg=self.fg_color
            )
            guest_label.pack(pady=20)
            
            guest_desc = tk.Label(
                user_info_frame,
                text="Inicia sesión para acceder a todas las funciones",
                font=self.label_font,
                bg=self.card_bg,
                fg=self.fg_color
            )
            guest_desc.pack(pady=10)

        # Sección de acceso rápido
        if self.current_user:
            quick_access_frame = tk.Frame(profile_content, bg=self.card_bg, bd=2, relief=tk.SOLID)
            quick_access_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(
                quick_access_frame,
                text="🚀 Acceso Rápido",
                font=self.button_font,
                bg=self.card_bg,
                fg=self.fg_color
            ).pack(pady=10)
            
            quick_buttons_frame = tk.Frame(quick_access_frame, bg=self.card_bg)
            quick_buttons_frame.pack(fill=tk.X, padx=20, pady=10)
            
            quick_actions = [
                ("📦", "Mis Pedidos", lambda: self.show_frame_with_animation(self.orders_frame)),
                ("❤️", "Favoritos", lambda: self.show_frame_with_animation(self.favorites_frame)),
                ("🛒", "Mi Carrito", lambda: self.show_frame_with_animation(self.cart_frame)),
                ("🛍️", "Seguir Comprando", lambda: self.show_frame_with_animation(self.home_frame))
            ]
            
            for i, (icon, text, command) in enumerate(quick_actions):
                btn = tk.Button(
                    quick_buttons_frame,
                    text=f"{icon}\n{text}",
                    font=self.label_font,
                    bg=self.button_color,
                    fg=self.button_text_color,
                    relief=tk.RAISED,
                    borderwidth=2,
                    padx=10,
                    pady=10,
                    command=command
                )
                
                if self.is_mobile:
                    btn.pack(fill=tk.X, pady=2)
                else:
                    btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")
                    quick_buttons_frame.grid_columnconfigure(0, weight=1)
                    quick_buttons_frame.grid_columnconfigure(1, weight=1)

        # Opciones del perfil mejoradas
        options_frame = tk.Frame(profile_content, bg=self.bg_color)
        options_frame.pack(fill=tk.X, pady=20)

        tk.Label(
            options_frame,
            text="⚙️ Configuración de Cuenta",
            font=self.button_font,
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=10)

        # Crear opciones
        if self.current_user: 
              options = [
                ("🔑", "Cambiar Contraseña", self.change_password),
                ("📧", "Cambiar Email", self.change_email),
                ("🏠", "Mis Direcciones", self.manage_addresses),
                ("💳", "Métodos de Pago", self.manage_payment_methods),
                ("🔔", "Notificaciones", self.notification_settings),
                ("📊", "Estadísticas Detalladas", self.show_detailed_stats),
                ("💾", "Exportar Mis Datos", self.export_data),
                ("🗑️", "Eliminar Cuenta", self.delete_account)
              ]
        else:
            options = [
                ("🔑", "Iniciar Sesión", lambda: self.show_frame_with_animation(self.login_frame)),
                ("📝", "Registrarse", lambda: self.show_frame_with_animation(self.register_frame)),
                ("⚙️", "Configuración General", lambda: self.show_frame_with_animation(self.settings_frame))
            ]

        for icon, text, command in options:
            self.create_profile_option(options_frame, icon, text, command)

        # Botón de cerrar sesión (solo si está logueado)
        if self.current_user:
            logout_frame = tk.Frame(profile_content, bg=self.bg_color)
            logout_frame.pack(fill=tk.X, pady=20)
            
            logout_button = tk.Button(
                logout_frame, 
                text="🚪 Cerrar Sesión", 
                font=self.button_font,
                bg="#F44336", 
                fg="white",
                relief=tk.RAISED,
                borderwidth=2,
                padx=20,
                pady=10,
                command=self.logout
            )
            logout_button.pack(pady=10)

        self.create_responsive_footer(self.profile_frame)

    def create_profile_option(self, parent, icon, text, command):
        """Crea una opción de perfil mejorada"""
        option_frame = tk.Frame(parent, bg=self.card_bg, bd=1, relief=tk.SOLID, cursor="hand2")
        option_frame.pack(fill=tk.X, pady=3, padx=5)
        
        # Contenido de la opción
        content_frame = tk.Frame(option_frame, bg=self.card_bg)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        
        icon_label = tk.Label(
            content_frame,
            text=icon,
            font=("Arial", 16),
            bg=self.card_bg,
            fg=self.fg_color
        )
        icon_label.pack(side=tk.LEFT, padx=5)
        
        text_label = tk.Label(
            content_frame,
            text=text,
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        text_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        arrow_label = tk.Label(
            content_frame,
            text="→",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        arrow_label.pack(side=tk.RIGHT, padx=5)
        
        # Hacer clickeable
        def on_click(event):
            command()
        
        for widget in [option_frame, content_frame, icon_label, text_label, arrow_label]:
            widget.bind("<Button-1>", on_click)
        
        # Efectos hover (solo desktop)
        if not self.is_mobile:
            def on_enter(event):
                option_frame.config(bg=self.highlight_color)
                content_frame.config(bg=self.highlight_color)
                for widget in [icon_label, text_label, arrow_label]:
                    widget.config(bg=self.highlight_color)
                    
            def on_leave(event):
                option_frame.config(bg=self.card_bg)
                content_frame.config(bg=self.card_bg)
                for widget in [icon_label, text_label, arrow_label]:
                    widget.config(bg=self.card_bg)
                    
            option_frame.bind("<Enter>", on_enter)
            option_frame.bind("<Leave>", on_leave)

    def setup_favorites_screen(self):
        """Configura la pantalla de favoritos"""
        header = self.create_responsive_header(self.favorites_frame, "❤️ Mis Favoritos")
        
        back_button = tk.Button(
            header,
            text="← Volver",
            font=self.label_font,
            bg=self.header_color,
            fg=self.header_text_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame_with_animation(self.profile_frame)
        )
        back_button.place(x=10, y=10)
        
        content = tk.Frame(self.favorites_frame, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Contenedor de favoritos
        self.favorites_container = tk.Frame(content, bg=self.bg_color)
        self.favorites_container.pack(fill=tk.BOTH, expand=True)
        
        self.display_favorites()
        self.create_responsive_footer(self.favorites_frame)

    def display_favorites(self):
        """Muestra los productos favoritos"""
        for widget in self.favorites_container.winfo_children():
            widget.destroy()
        
        if not self.current_user:
            login_prompt = tk.Label(
                self.favorites_container,
                text="🔑 Inicia sesión para ver tus favoritos",
                font=self.label_font,
                bg=self.bg_color,
                fg=self.fg_color
            )
            login_prompt.pack(pady=50)
            return
        
        # Obtener favoritos de la base de datos
        favorites = self.db.get_user_favorites(self.current_user.id)
        
        if not favorites:
            empty_label = tk.Label(
                self.favorites_container,
                text="❤️ No tienes productos favoritos\n\n¡Explora nuestra tienda y marca\ntus productos favoritos!",
                font=self.label_font,
                bg=self.bg_color,
                fg=self.fg_color,
                justify=tk.CENTER
            )
            empty_label.pack(pady=50)
            return
        
        # Mostrar favoritos en grid
        columns = 1 if self.is_mobile else 2
        row_frame = None
        
        for i, product in enumerate(favorites):
            if i % columns == 0:
                row_frame = tk.Frame(self.favorites_container, bg=self.bg_color)
                row_frame.pack(fill=tk.X, pady=5)
            
            self.create_favorite_card(row_frame, product, columns)

    def create_favorite_card(self, parent, product: Product, columns):
        """Crea una tarjeta de producto favorito"""
        card_width = (self.window_width - 40) if columns == 1 else (self.window_width - 60) // 2
        card_height = 200 if self.is_mobile else 250
        
        product_card = tk.Frame(parent, bg=self.card_bg, bd=2, relief=tk.SOLID, 
                               width=card_width, height=card_height)
        product_card.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        product_card.pack_propagate(False)
        
        # Imagen
        image_canvas = tk.Canvas(product_card, width=80, height=80, 
                               bg=self.card_bg, highlightthickness=0)
        image_canvas.pack(pady=10)
        self.draw_product_image(image_canvas, product.category)
        
        # Información
        info_frame = tk.Frame(product_card, bg=self.card_bg)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        name_label = tk.Label(
            info_frame,
            text=product.name,
            font=self.label_font,
            bg=self.card_bg,
            fg=self.fg_color,
            wraplength=card_width - 20
        )
        name_label.pack(pady=2)
        
        price_label = tk.Label(
            info_frame,
            text=f"$ {product.price:,.0f} ARS",
            font=self.button_font,
            bg=self.card_bg,
            fg=self.accent_color
        )
        price_label.pack(pady=2)
        
        # Botones
        buttons_frame = tk.Frame(product_card, bg=self.card_bg)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Quitar de favoritos
        remove_fav_btn = tk.Button(
            buttons_frame,
            text="💔 Quitar",
            font=self.copyright_font,
            bg=self.card_bg,
            fg="red",
            relief=tk.GROOVE,
            borderwidth=1,
            command=lambda p=product: self.remove_favorite_and_refresh(p)
        )
        remove_fav_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Añadir al carrito
        add_btn = tk.Button(
            buttons_frame,
            text="🛒 Añadir",
            font=self.copyright_font,
            bg=self.button_color,
            fg=self.button_text_color,
            relief=tk.RAISED,
            borderwidth=1,
            state=tk.NORMAL if product.stock > 0 else tk.DISABLED,
            command=lambda p=product: self.add_to_cart(p)
        )
        add_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Ver detalles
        view_btn = tk.Button(
            buttons_frame,
            text="👁️ Ver",
            font=self.copyright_font,
            bg=self.card_bg,
            fg=self.fg_color,
            relief=tk.GROOVE,
            borderwidth=1,
            command=lambda p=product: self.show_product_detail(p)
        )
        view_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

    def remove_favorite_and_refresh(self, product: Product):
        """Quita de favoritos y refresca la vista"""
        if self.db.remove_from_favorites(self.current_user.id, product.id):
            self.notifications.show_notification("Eliminado de favoritos", "info")
            self.display_favorites()
        else:
            self.notifications.show_notification("Error al eliminar favorito", "error")

    def setup_orders_screen(self):
        """Configura la pantalla de pedidos"""
        header = self.create_responsive_header(self.orders_frame, "📦 Mis Pedidos")
        
        back_button = tk.Button(
            header,
            text="← Volver",
            font=self.label_font,
            bg=self.header_color,
            fg=self.header_text_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame_with_animation(self.profile_frame)
        )
        back_button.place(x=10, y=10)
        
        content = tk.Frame(self.orders_frame, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Contenedor de pedidos
        self.orders_container = tk.Frame(content, bg=self.bg_color)
        self.orders_container.pack(fill=tk.BOTH, expand=True)
        
        self.display_orders()
        self.create_responsive_footer(self.orders_frame)

    def display_orders(self):
        """Muestra los pedidos del usuario"""
        for widget in self.orders_container.winfo_children():
            widget.destroy()
        
        if not self.current_user:
            login_prompt = tk.Label(
                self.orders_container,
                text="🔑 Inicia sesión para ver tus pedidos",
                font=self.label_font,
                bg=self.bg_color,
                fg=self.fg_color
            )
            login_prompt.pack(pady=50)
            return
        
        # Obtener pedidos de la base de datos
        orders = self.db.get_user_orders(self.current_user.id)
        
        if not orders:
            empty_label = tk.Label(
                self.orders_container,
                text="📦 No tienes pedidos aún\n\n¡Realiza tu primera compra\ny aparecerá aquí!",
                font=self.label_font,
                bg=self.bg_color,
                fg=self.fg_color,
                justify=tk.CENTER
            )
            empty_label.pack(pady=50)
            return
        
        # Mostrar pedidos
        for order in orders:
            self.create_order_card(order)

    def create_order_card(self, order):
        """Crea una tarjeta de pedido"""
        order_frame = tk.Frame(self.orders_container, bg=self.card_bg, bd=2, relief=tk.SOLID)
        order_frame.pack(fill=tk.X, pady=10, padx=5)
        
        # Header del pedido
        header_frame = tk.Frame(order_frame, bg=self.card_bg)
        header_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Número de pedido y fecha
        order_info = tk.Label(
            header_frame,
            text=f"Pedido #{order['id']} - {order['created_at'][:10]}",
            font=self.button_font,
            bg=self.card_bg,
            fg=self.fg_color
        )
        order_info.pack(side=tk.LEFT)
        
        # Estado del pedido
        status_colors = {
            'pendiente': '#FF9800',
            'procesando': '#2196F3',
            'enviado': '#9C27B0',
            'entregado': '#4CAF50',
            'cancelado': '#F44336'
        }
        
        status_texts = {
            'pendiente': 'Pendiente',
            'procesando': 'Procesando',
            'enviado': 'Enviado',
            'entregado': 'Entregado',
            'cancelado': 'Cancelado'
        }
        
        status_color = status_colors.get(order['status'], '#666666')
        status_text = status_texts.get(order['status'], order['status'])
        
        status_label = tk.Label(
            header_frame,
            text=status_text,
            font=self.label_font,
            bg=status_color,
            fg="white",
            padx=8,
            pady=2
        )
        status_label.pack(side=tk.RIGHT)
        
        # Detalles del pedido
        details_frame = tk.Frame(order_frame, bg=self.card_bg)
        details_frame.pack(fill=tk.X, padx=15, pady=5)
        
        # Items del pedido
        if order['items']:
            items_label = tk.Label(
                details_frame,
                text=f"Productos: {order['items']}",
                font=self.copyright_font,
                bg=self.card_bg,
                fg=self.fg_color,
                wraplength=self.window_width - 60,
                justify=tk.LEFT
            )
            items_label.pack(fill=tk.X, pady=2)
        
        # Total
        total_label = tk.Label(
            details_frame,
            text=f"Total: $ {order['total']:,.0f} ARS",
            font=self.label_font,
            bg=self.card_bg,
            fg=self.accent_color
        )
        total_label.pack(fill=tk.X, pady=2)
        
        # Dirección de envío
        if order['shipping_address']:
            address_label = tk.Label(
                details_frame,
                text=f"Dirección: {order['shipping_address']}",
                font=self.copyright_font,
                bg=self.card_bg,
                fg=self.fg_color,
                wraplength=self.window_width - 60,
                justify=tk.LEFT
            )
            address_label.pack(fill=tk.X, pady=2)

    def setup_settings_screen(self):
        """Configura la pantalla de configuración"""
        header = self.create_responsive_header(self.settings_frame, "⚙️ Configuración")
        
        back_button = tk.Button(
            header,
            text="← Volver",
            font=self.label_font,
            bg=self.header_color,
            fg=self.header_text_color,
            relief=tk.FLAT,
            command=lambda: self.show_frame_with_animation(self.profile_frame)
        )
        back_button.place(x=10, y=10)
        
        content = tk.Frame(self.settings_frame, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configuraciones
        settings_options = [
            ("🌙", "Tema Oscuro/Claro", self.toggle_theme),
            ("📱", "Modo Móvil", self.toggle_mobile_mode),
            ("🔔", "Notificaciones", self.toggle_notifications),
            ("💾", "Exportar Datos", self.export_data),
            ("🗑️", "Limpiar Cache", self.clear_cache),
            ("ℹ️", "Acerca de", self.show_about)
        ]
        
        for icon, text, command in settings_options:
            self.create_profile_option(content, icon, text, command)
        
        self.create_responsive_footer(self.settings_frame)

    # Métodos de funcionalidad adicional
    def change_password(self):
        """Cambia la contraseña del usuario"""
        if not self.current_user:
            self.notifications.show_notification("Debe iniciar sesión", "warning")
            return
        
        self.notifications.show_notification("Función de cambio de contraseña en desarrollo", "info")

    def change_email(self):
        """Cambia el email del usuario"""
        if not self.current_user:
            self.notifications.show_notification("Debe iniciar sesión", "warning")
            return
        
        self.notifications.show_notification("Función de cambio de email en desarrollo", "info")

    def manage_addresses(self):
        """Gestiona las direcciones del usuario"""
        self.notifications.show_notification("Función de direcciones en desarrollo", "info")

    def manage_payment_methods(self):
        """Gestiona los métodos de pago del usuario"""
        self.notifications.show_notification("Función de métodos de pago en desarrollo", "info")

    def notification_settings(self):
        """Configuración de notificaciones"""
        self.notifications.show_notification("Configuración de notificaciones", "info")

    def show_detailed_stats(self):
        """Muestra estadísticas detalladas del usuario"""
        if not self.current_user:
            self.notifications.show_notification("Debe iniciar sesión", "warning")
            return
        
        self.notifications.show_notification("Estadísticas detalladas en desarrollo", "info")

    def export_data(self):
        """Exporta los datos del usuario"""
        if not self.current_user:
            self.notifications.show_notification("Debe iniciar sesión", "warning")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                # Obtener datos del usuario
                user_data = {
                    'user': {
                        'username': self.current_user.username,
                        'email': self.current_user.email,
                        'created_at': self.current_user.created_at
                    },
                    'orders': self.db.get_user_orders(self.current_user.id),
                    'favorites': [
                        {
                            'id': p.id,
                            'name': p.name,
                            'price': p.price,
                            'category': p.category
                        }
                        for p in self.db.get_user_favorites(self.current_user.id)
                    ]
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, indent=2, ensure_ascii=False)
                
                self.notifications.show_notification("Datos exportados correctamente", "success")
        except Exception as e:
            self.notifications.show_notification(f"Error al exportar: {str(e)}", "error")

    def delete_account(self):
        """Elimina la cuenta del usuario"""
        if not self.current_user:
            self.notifications.show_notification("Debe iniciar sesión", "warning")
            return
        
        if messagebox.askyesno("Eliminar Cuenta", "¿Está seguro que desea eliminar su cuenta?\n\nEsta acción NO se puede deshacer."):
            self.notifications.show_notification("Función de eliminación de cuenta en desarrollo", "warning")

    def toggle_mobile_mode(self):
        """Alterna el modo móvil"""
        self.is_mobile = not self.is_mobile
        self.setup_responsive_fonts()
        self.notifications.show_notification(
            f"Modo {'móvil' if self.is_mobile else 'desktop'} activado", "info"
        )

    def toggle_notifications(self):
        """Alterna las notificaciones"""
        self.notifications.show_notification("Configuración de notificaciones", "info")

    def clear_cache(self):
        """Limpia el cache de la aplicación"""
        self.notifications.show_notification("Cache limpiado", "success")

    def show_about(self):
        """Muestra información sobre la aplicación"""
        about_text = """PetZone - Tienda de Mascotas
        
Versión: 2.0
Desarrollado con Python y Tkinter
Base de datos: MySQL

Características:
• Sistema de usuarios y autenticación
• Catálogo de productos con categorías
• Carrito de compras
• Sistema de favoritos
• Gestión de pedidos
• Interfaz responsive
• Tema claro/oscuro
• Notificaciones en tiempo real

© 2025 PetZone. Todos los derechos reservados."""
        
        messagebox.showinfo("Acerca de PetZone", about_text)

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = ImprovedPetZoneApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
