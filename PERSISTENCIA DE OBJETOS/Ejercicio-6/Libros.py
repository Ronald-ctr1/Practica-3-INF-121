import json

class Libro:
    def __init__(self, codLibro, titulo, precio):
        self.codLibro = codLibro
        self.titulo = titulo
        self.precio = precio
    
    def to_dict(self):
        return {
            "codLibro": self.codLibro,
            "titulo": self.titulo,
            "precio": self.precio
        }

    def __str__(self):
        return f"Libro(Cod: {self.codLibro}, Titulo: {self.titulo}, Precio: {self.precio:.2f})"

class Cliente:
    def __init__(self, codCliente, ci, nombre, apellido):
        self.codCliente = codCliente
        self.ci = ci
        self.nombre = nombre
        self.apellido = apellido
    
    def to_dict(self):
        return {
            "codCliente": self.codCliente,
            "ci": self.ci,
            "nombre": self.nombre,
            "apellido": self.apellido
        }

    def __str__(self):
        return f"Cliente(Cod: {self.codCliente}, CI: {self.ci}, Nombre: {self.nombre} {self.apellido})"

class Prestamo:
    def __init__(self, codCliente, codLibro, fechaPrestamo, cantidad):
        self.codCliente = codCliente
        self.codLibro = codLibro
        self.fechaPrestamo = fechaPrestamo
        self.cantidad = cantidad
    
    def to_dict(self):
        return {
            "codCliente": self.codCliente,
            "codLibro": self.codLibro,
            "fechaPrestamo": self.fechaPrestamo,
            "cantidad": self.cantidad
        }

    def __str__(self):
        return (f"Prestamo(Cliente: {self.codCliente}, Libro: {self.codLibro}, "
                f"Fecha: {self.fechaPrestamo}, Cantidad: {self.cantidad})")

class ArchivoBase:
    def __init__(self, nomArch, coleccion):
        self.nomArch = nomArch
        self.coleccion = coleccion
        self.cargar_archivo()

    def _guardar_en_archivo(self):
        data_to_save = [item.to_dict() for item in self.coleccion.values()]
        try:
            with open(self.nomArch, 'w') as f:
                json.dump(data_to_save, f, indent=4)
        except IOError:
            pass

    def cargar_archivo(self):
        try:
            with open(self.nomArch, 'r') as f:
                data = json.load(f)
                self.coleccion.clear()
                self._reconstruir_objetos(data)
        except:
            pass
            
    def _reconstruir_objetos(self, data):
        pass

    def crearArchivo(self):
        self.coleccion.clear()
        self._guardar_en_archivo()

class ArchLibro(ArchivoBase):
    def __init__(self, nomArch):
        self.libros = {}
        super().__init__(nomArch, self.libros)

    def _reconstruir_objetos(self, data):
        for d in data:
            libro = Libro(d['codLibro'], d['titulo'], d['precio'])
            self.libros[libro.codLibro] = libro

    def guardaLibro(self, libro):
        self.libros[libro.codLibro] = libro
        self._guardar_en_archivo()

class ArchCliente(ArchivoBase):
    def __init__(self, nomArch):
        self.clientes = {}
        super().__init__(nomArch, self.clientes)

    def _reconstruir_objetos(self, data):
        for d in data:
            cliente = Cliente(d['codCliente'], d['ci'], d['nombre'], d['apellido'])
            self.clientes[cliente.codCliente] = cliente

    def guardaCliente(self, cliente):
        self.clientes[cliente.codCliente] = cliente
        self._guardar_en_archivo()

class ArchPrestamo(ArchivoBase):
    def __init__(self, nomArch):
        self.prestamos = []
        super().__init__(nomArch, self.prestamos)

    def cargar_archivo(self):
        try:
            with open(self.nomArch, 'r') as f:
                data = json.load(f)
                self.prestamos.clear()
                self._reconstruir_objetos(data)
        except:
            pass

    def _guardar_en_archivo(self):
        data_to_save = [item.to_dict() for item in self.prestamos]
        try:
            with open(self.nomArch, 'w') as f:
                json.dump(data_to_save, f, indent=4)
        except IOError:
            pass
            
    def _reconstruir_objetos(self, data):
        for d in data:
            prestamo = Prestamo(d['codCliente'], d['codLibro'], d['fechaPrestamo'], d['cantidad'])
            self.prestamos.append(prestamo)

    def guardaPrestamo(self, prestamo):
        self.prestamos.append(prestamo)
        self._guardar_en_archivo()


class GestorBiblioteca:
    def __init__(self, al, ac, ap):
        self.archLibro = al
        self.archCliente = ac
        self.archPrestamo = ap

    def listar_libros_por_precio(self, x, y):
        libros_filtrados = []
        for libro in self.archLibro.libros.values():
            if x <= libro.precio <= y:
                libros_filtrados.append(libro)
        return libros_filtrados

    def calcular_ingreso_total_por_libro(self, codLibro):
        ingreso_total = 0.0
        libro_referencia = self.archLibro.libros.get(codLibro)

        if not libro_referencia:
            return 0.0

        for prestamo in self.archPrestamo.prestamos:
            if prestamo.codLibro == codLibro:
                ingreso_total += prestamo.cantidad * libro_referencia.precio
        
        return ingreso_total

    def mostrar_libros_no_vendidos(self):
        codigos_vendidos = {p.codLibro for p in self.archPrestamo.prestamos}
        libros_no_vendidos = []
        
        for cod, libro in self.archLibro.libros.items():
            if cod not in codigos_vendidos:
                libros_no_vendidos.append(libro)
                
        return libros_no_vendidos

    def mostrar_clientes_por_libro(self, codLibro):
        codigos_clientes = set()
        
        for prestamo in self.archPrestamo.prestamos:
            if prestamo.codLibro == codLibro:
                codigos_clientes.add(prestamo.codCliente)
                
        clientes_compradores = [
            self.archCliente.clientes[cod] 
            for cod in codigos_clientes 
            if cod in self.archCliente.clientes
        ]
        return clientes_compradores

    def definir_libro_mas_prestado(self):
        conteo_prestamos = {}
        for prestamo in self.archPrestamo.prestamos:
            conteo_prestamos[prestamo.codLibro] = conteo_prestamos.get(prestamo.codLibro, 0) + prestamo.cantidad
            
        if not conteo_prestamos:
            return None
            
        cod_mas_prestado = max(conteo_prestamos, key=conteo_prestamos.get)
        
        libro = self.archLibro.libros.get(cod_mas_prestado)
        cantidad = conteo_prestamos[cod_mas_prestado]

        return (libro, cantidad)

    def mostrar_cliente_con_mas_prestamos(self):
        conteo_clientes = {}
        for prestamo in self.archPrestamo.prestamos:
            conteo_clientes[prestamo.codCliente] = conteo_clientes.get(prestamo.codCliente, 0) + 1
            
        if not conteo_clientes:
            return None
            
        cod_cliente_mas_prestamos = max(conteo_clientes, key=conteo_clientes.get)
        
        cliente = self.archCliente.clientes.get(cod_cliente_mas_prestamos)
        cantidad = conteo_clientes[cod_cliente_mas_prestamos]

        return (cliente, cantidad)

if __name__ == "__main__":
    
    FILE_LIBROS = "libros.json"
    FILE_CLIENTES = "clientes.json"
    FILE_PRESTAMOS = "prestamos.json"
    
    print(" INICIO DEL SISTEMA DE GESTIÓN DE BIBLIOTECA ")

    archLibro = ArchLibro(FILE_LIBROS)
    archCliente = ArchCliente(FILE_CLIENTES)
    archPrestamo = ArchPrestamo(FILE_PRESTAMOS)

    archLibro.crearArchivo()
    archCliente.crearArchivo()
    archPrestamo.crearArchivo()

    l1 = Libro(10, "Python", 50.0)
    l2 = Libro(20, "Diseño X", 25.5)
    l3 = Libro(30, "Base de Pie ", 75.0)
    l4 = Libro(40, "Web Dev", 15.0) 

    c1 = Cliente(100, 1234, "Ana", "Gomez")
    c2 = Cliente(200, 5678, "Luis", "Perez")
    c3 = Cliente(300, 9012, "Marta", "Rojas")

    p1 = Prestamo(100, 10, "2025-01-10", 2)
    p2 = Prestamo(100, 20, "2025-01-15", 1) 
    p3 = Prestamo(200, 10, "2025-01-20", 3)
    p4 = Prestamo(200, 30, "2025-01-25", 1)
    p5 = Prestamo(300, 20, "2025-02-01", 1)
    p6 = Prestamo(200, 20, "2025-02-05", 2)

    archLibro.guardaLibro(l1)
    archLibro.guardaLibro(l2)
    archLibro.guardaLibro(l3)
    archLibro.guardaLibro(l4)

    archCliente.guardaCliente(c1)
    archCliente.guardaCliente(c2)
    archCliente.guardaCliente(c3)

    archPrestamo.guardaPrestamo(p1)
    archPrestamo.guardaPrestamo(p2)
    archPrestamo.guardaPrestamo(p3)
    archPrestamo.guardaPrestamo(p4)
    archPrestamo.guardaPrestamo(p5)
    archPrestamo.guardaPrestamo(p6)

    gestor = GestorBiblioteca(archLibro, archCliente, archPrestamo)

    x_precio, y_precio = 20.0, 60.0
    print(f"\n--- a) Libros con precio entre {x_precio:.2f} y {y_precio:.2f} ---")
    libros_rango = gestor.listar_libros_por_precio(x_precio, y_precio)
    if libros_rango:
        for l in libros_rango:
            print(f"  - {l}")
    else:
        print("  - No se encontraron libros en ese rango de precio.")
    cod_esp = 20
    print(f"\n--- b) Ingreso total generado por el libro Cod {cod_esp} ('{l2.titulo}') ---")
    ingreso = gestor.calcular_ingreso_total_por_libro(cod_esp)
    print(f"  - Ingreso Total: {ingreso:.2f}")

    print("\n--- c) Libros que nunca fueron vendidos ---")
    libros_no_vendidos = gestor.mostrar_libros_no_vendidos()
    if libros_no_vendidos:
        for l in libros_no_vendidos:
            print(f"  - {l}")
    else:
        print("  - Todos los libros han sido vendidos/prestados.")

    cod_libro_cliente = 10
    print(f"\n--- d) Clientes que compraron el libro Cod {cod_libro_cliente} ('{l1.titulo}') ---")
    clientes_libro = gestor.mostrar_clientes_por_libro(cod_libro_cliente)
    if clientes_libro:
        for c in clientes_libro:
            print(f"  - {c}")
    else:
        print("  - Ningún cliente compró este libro.")

    print("\n--- e) Libro más prestado (por cantidad) ---")
    resultado_e = gestor.definir_libro_mas_prestado()
    if resultado_e:
        libro_mas_prestado, cantidad_total = resultado_e
        print(f"  - Libro: {libro_mas_prestado}")
        print(f"  - Cantidad Total Prestada: {cantidad_total}")
    else:
        print("  - No hay préstamos registrados.")

    print("\n--- f) Cliente con más préstamos (por registro de préstamo) ---")
    resultado_f = gestor.mostrar_cliente_con_mas_prestamos()
    if resultado_f:
        cliente_mas_prestamos, conteo_prestamos = resultado_f
        print(f"  - Cliente: {cliente_mas_prestamos}")
        print(f"  - Número de Préstamos: {conteo_prestamos}")
    else:
        print("  - No hay préstamos registrados.")
        
    print("\n FIN DEL SISTEMA ")