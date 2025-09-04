import tkinter as tk
from tkinter import ttk, font, messagebox, simpledialog
from datetime import datetime
import mysql.connector
from mysql.connector import Error


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",         # tu usuario MySQL
                password="",         # tu contraseña MySQL
                database="marcket"   # tu base de datos
            )
            if self.connection.is_connected():
                print("✅ Conexión establecida con MySQL")
        except Error as e:
            print(f"❌ Error al conectar: {e}")
            messagebox.showerror("Error BD", f"No se pudo conectar: {e}")

    def execute(self, query, params=None, fetch=False):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
        except Error as e:
            print(f"Error SQL: {e}")
            return [] if fetch else False


class MarketplaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Marketplace de Ropa")

      
        self.app_width = 380
        self.app_height = 680
        self.root.geometry(f"{self.app_width}x{self.app_height}")
        self.root.resizable(False, False)

        
        self.colors = {
            'primary': '#8B1538',
            'secondary': '#A0153E',
            'accent': '#C73659',
            'background': '#FFFFFF',
            'card': '#FEFEFE',
            'text': '#2c3e50',
            'text_light': '#7f8c8d',
            'border': '#E8E8E8',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c'
        }

      
        self.title_font = font.Font(family="Arial", size=16, weight="bold")
        self.nav_font = font.Font(family="Arial", size=12)
        self.product_font = font.Font(family="Arial", size=10)
        self.price_font = font.Font(family="Arial", size=12, weight="bold")
        self.button_font = font.Font(family="Arial", size=11, weight="bold")
        self.small_font = font.Font(family="Arial", size=9)

       
        self.db = DatabaseManager()

        self.current_user = None
        self.cart_items = []
        self.current_category = "Todos"

        self.create_main_interface()
        self.show_auth_screen()

    
    def show_auth_screen(self):
        self.clear_main_container()

        auth_container = tk.Frame(self.main_container, bg=self.colors['background'])
        auth_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        title = tk.Label(auth_container, text="👗 Marketplace\nde Ropa",
                         font=self.title_font, fg=self.colors['primary'], bg=self.colors['background'])
        title.pack(pady=30)

        tk.Label(auth_container, text="Usuario:", font=self.nav_font,
                 bg=self.colors['background'], fg=self.colors['text']).pack(pady=(20, 5))
        self.username_entry = tk.Entry(auth_container, font=self.nav_font)
        self.username_entry.pack(pady=5)

        tk.Label(auth_container, text="Contraseña:", font=self.nav_font,
                 bg=self.colors['background'], fg=self.colors['text']).pack(pady=(10, 5))
        self.password_entry = tk.Entry(auth_container, font=self.nav_font, show="*")
        self.password_entry.pack(pady=5)

        login_btn = tk.Button(auth_container, text="Iniciar Sesión", font=self.button_font,
                              bg=self.colors['primary'], fg="white", command=self.login)
        login_btn.pack(pady=15)

        register_btn = tk.Button(auth_container, text="Registrarse", font=self.nav_font,
                                 fg=self.colors['primary'], bg=self.colors['background'], command=self.register)
        register_btn.pack()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Complete todos los campos")
            return

        result = self.db.execute(
            "SELECT * FROM usuarios WHERE username=%s AND password_hash=%s",
            (username, password),
            fetch=True
        )

        if result:
            self.current_user = result[0]
            messagebox.showinfo("Bienvenido", f"Hola {username}")
            self.show_home_screen()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Complete todos los campos")
            return

        exists = self.db.execute("SELECT * FROM usuarios WHERE username=%s", (username,), fetch=True)
        if exists:
            messagebox.showerror("Error", "El usuario ya existe")
            return

        self.db.execute(
            "INSERT INTO usuarios (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, f"{username}@mail.com", password)
        )
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")

   
    def create_main_interface(self):
        self.main_container = tk.Frame(self.root, bg=self.colors['background'])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.nav_frame = tk.Frame(self.root, bg=self.colors['card'], height=60, relief=tk.RAISED)
        self.nav_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.nav_frame.pack_propagate(False)

        nav_buttons = [
            ("🏠", "Inicio", self.show_home_screen),
            ("🔍", "Buscar", self.show_search_screen),
            ("➕", "Vender", self.show_sell_screen),
            ("💬", "Mensajes", self.show_messages_screen),
            ("🛒", "Carrito", self.show_cart_screen)
        ]

        for i, (icon, text, cmd) in enumerate(nav_buttons):
            btn = tk.Button(self.nav_frame, text=f"{icon}\n{text}", font=self.small_font,
                            bg=self.colors['card'], fg=self.colors['text'], command=cmd)
            btn.place(x=i*76, y=5, width=76, height=50)

    def clear_main_container(self):
        for w in self.main_container.winfo_children():
            w.destroy()

  
    def show_home_screen(self):
        self.clear_main_container()

        header = tk.Frame(self.main_container, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X)
        tk.Label(header, text="👗 Marketplace", font=self.title_font, bg=self.colors['primary'], fg="white").pack(pady=20)

        
        productos = self.db.execute("SELECT * FROM productos WHERE activo=1", fetch=True)

        if not productos:
            tk.Label(self.main_container, text="No hay productos disponibles", bg="white").pack(pady=50)
            return

        for p in productos:
            tk.Label(self.main_container,
                     text=f"{p['titulo']} - ${p['precio']}",
                     font=self.nav_font, bg="white").pack(anchor="w", padx=10, pady=5)

    def show_search_screen(self):
        self.clear_main_container()
        tk.Label(self.main_container, text="Buscar productos...", bg="white").pack()

    def show_sell_screen(self):
        self.clear_main_container()
        tk.Label(self.main_container, text="Publicar producto", bg="white").pack()

   
    def show_messages_screen(self):
        self.clear_main_container()
        tk.Label(self.main_container, text="Mensajes", bg="white").pack()

   
    def show_cart_screen(self):
        self.clear_main_container()
        tk.Label(self.main_container, text="Carrito", bg="white").pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = MarketplaceApp(root)
    root.mainloop()
