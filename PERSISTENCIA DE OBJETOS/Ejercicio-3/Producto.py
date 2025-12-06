import json

class Producto:
    def __init__(self, codigo: int, nombre: str, precio: float):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
    
    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio
        }
    
    def __str__(self):
        return f"Producto(Código: {self.codigo}, Nombre: {self.nombre}, Precio: {self.precio:.2f})"
    
    def __repr__(self):
        return self.__str__()

class ArchivoProducto:
    def __init__(self, noma: str):
        self.noma = noma
        self.productos = [] 
        self.cargar_archivo()


    def _guardar_en_archivo(self):
        data_to_save = [p.to_dict() for p in self.productos]
        try:
            with open(self.noma, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            print(f"[Sistema] Datos guardados exitosamente en '{self.noma}'.")
        except IOError:
            print(f"[Sistema] Error al escribir en el archivo '{self.noma}'.")

    def cargar_archivo(self):
        try:
            with open(self.noma, 'r') as f:
                data = json.load(f)
                self.productos = [
                    Producto(d['codigo'], d['nombre'], d['precio']) for d in data
                ]
            print(f"[Sistema] Archivo '{self.noma}' cargado con {len(self.productos)} productos.")
        except FileNotFoundError:
            print(f"[Sistema] Archivo '{self.noma}' no encontrado. Se inicializará vacío.")
        except json.JSONDecodeError:
            print(f"[Sistema] El archivo '{self.noma}' está vacío o mal formado. Se inicializará vacío.")
        except Exception as e:
            print(f"[Sistema] Ocurrió un error al cargar el archivo: {e}")


    def crearArchivo(self):
        self.productos = [] 
        self._guardar_en_archivo()
        print(f"[Operación] Archivo '{self.noma}' creado/reinicializado.")

    def guardaProducto(self, producto):
        if any(p.codigo == producto.codigo for p in self.productos):
            print(f"[Error] Ya existe un producto con código {producto.codigo}. No se guardó.")
            return

        self.productos.append(producto)
        self._guardar_en_archivo()
        print(f"[Operación] Producto '{producto.nombre}' guardado.")

    def buscaProducto(self, codigo: int):
        print(f"\n--- c) Buscando Producto con código {codigo} ---")
        
        for p in self.productos:
            if p.codigo == codigo:
                print(f"[Resultado] Producto encontrado: {p}")
                return p
        
        print(f"[Resultado] Producto con código {codigo} no encontrado.")
        return None

    def calcular_promedio_precios(self):
        print("\n--- d) Calculando Promedio de Precios ---")
        
        if not self.productos:
            print("[Resultado] No hay productos para calcular el promedio. Retornando 0.0")
            return 0.0

        suma_precios = sum(p.precio for p in self.productos)
        promedio = suma_precios / len(self.productos)
        
        print(f"[Resultado] El promedio de precios de {len(self.productos)} productos es: {promedio:.2f}")
        return promedio

    def mostrar_producto_mas_caro(self):
        print("\n--- e) Mostrando Producto Más Caro ---")
        
        if not self.productos:
            print("[Resultado] La lista de productos está vacía.")
            return None

        producto_max = max(self.productos, key=lambda p: p.precio)
        
        print(f"[Resultado] El producto más caro es: {producto_max}")
        return producto_max

    def listar_todos(self):
        print(f"\n--- Listado Actual de Productos ({len(self.productos)} en total) ---")
        if self.productos:
            for p in self.productos:
                print(p)
        else:
            print("(Lista vacía)")


# --- BLOQUE DE PRUEBA Y EJECUCIÓN ---
if __name__ == "__main__":
    NOMBRE_ARCHIVO = "productos_data.json"
    print(f" INICIO DEL SISTEMA DE GESTIÓN DE PRODUCTOS ")

    gestion = ArchivoProducto(NOMBRE_ARCHIVO)
    gestion.crearArchivo()

    print("\n Ejecutando Operaciones de Guardado (b) ")
    
    p1 = Producto(10, "Laptop ", 1500.50)
    p2 = Producto(20, "Mouse ", 25.00)
    p3 = Producto(30, "Monitor ", 450.99)
    p4 = Producto(40, "Teclado ", 80.00)
    
    gestion.guardaProducto(p1)
    gestion.guardaProducto(p2)
    gestion.guardaProducto(p3)
    gestion.guardaProducto(p4)
    
    gestion.listar_todos()

    print("\n Ejecutando Búsqueda de Producto (c) ")
    gestion.buscaProducto(codigo=30)
    gestion.buscaProducto(codigo=99) 

    print("\n Ejecutando Cálculo del Promedio (d) ")
    gestion.calcular_promedio_precios()

    print("\n Ejecutando Mostrar Más Caro (e) ")
    gestion.mostrar_producto_mas_caro()
    
    print("\n FIN DEL SISTEMA ")