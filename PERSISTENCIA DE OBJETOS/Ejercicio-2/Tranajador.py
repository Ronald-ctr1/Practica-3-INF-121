import json

class Trabajador:
    def __init__(self, nombre: str, carnet: int, salario: float):
        self.nombre = nombre
        self.carnet = carnet
        self.salario = salario
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "carnet": self.carnet,
            "salario": self.salario
        }

    def __str__(self):
        return f"Trabajador(Nombre: {self.nombre}, Carnet: {self.carnet}, Salario: {self.salario:.2f})"
    
    def __repr__(self):
        return self.__str__()

class ArchivoTrabajador:
    def __init__(self, nombreArch: str):
        self.nombreArch = nombreArch
        self.trabajadores = [] 
        self.cargar_archivo() 

    def _guardar_en_archivo(self):
        data_to_save = [t.to_dict() for t in self.trabajadores]
        try:
            with open(self.nombreArch, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            print(f"[Sistema] Datos guardados exitosamente en '{self.nombreArch}'.")
        except IOError:
            print(f"[Sistema] Error al escribir en el archivo '{self.nombreArch}'.")

    def cargar_archivo(self):
        try:
            with open(self.nombreArch, 'r') as f:
                data = json.load(f)
                self.trabajadores = [
                    Trabajador(d['nombre'], d['carnet'], d['salario']) for d in data
                ]
            print(f"[Sistema] Archivo '{self.nombreArch}' cargado con {len(self.trabajadores)} trabajadores.")
        except FileNotFoundError:
            print(f"[Sistema] Archivo '{self.nombreArch}' no encontrado. Se inicializará vacío.")
        except json.JSONDecodeError:
            print(f"[Sistema] El archivo '{self.nombreArch}' está vacío o mal formado. Se inicializará vacío.")
        except Exception as e:
            print(f"[Sistema] Ocurrió un error al cargar el archivo: {e}")

    def crearArchivo(self):
        self.trabajadores = [] 
        self._guardar_en_archivo()
        print(f"Archivo '{self.nombreArch}' creado/reinicializado.")

    def guardarTrabajador(self, trabajador):
        if any(t.carnet == trabajador.carnet for t in self.trabajadores):
            print(f"Error: Ya existe un trabajador con carnet {trabajador.carnet}. No se guardó.")
            return

        self.trabajadores.append(trabajador)
        self._guardar_en_archivo()
        print(f" Trabajador '{trabajador.nombre}' guardado.")

    def aumentaSalario(self, aumento_porcentaje, carnet):
        encontrado = False
        for t in self.trabajadores:
            if t.carnet == carnet:
                aumento = t.salario * (aumento_porcentaje / 100)
                t.salario += aumento
                encontrado = True
                print(f" Salario de {t.nombre} (Carnet: {carnet}) aumentado en {aumento_porcentaje}%. Nuevo salario: {t.salario:.2f}")
                break
        
        if encontrado:
            self._guardar_en_archivo()
        else:
            print(f" Error: Trabajador con carnet {carnet} no encontrado para aumentar salario.")

    def buscar_mayor_salario(self): 
        if not self.trabajadores:
            print(" La lista de trabajadores está vacía.")
            return None

        trabajador_max = max(self.trabajadores, key=lambda t: t.salario)
        
        print("\n--- d) Trabajador con el Mayor Salario ---")
        print(trabajador_max)
        return trabajador_max

    def ordenar_por_salario(self):
        if not self.trabajadores:
            print(" La lista de trabajadores está vacía.")
            return []

        lista_ordenada = sorted(self.trabajadores, key=lambda t: t.salario)
        
        print("\n--- e) Trabajadores Ordenados por Salario (Ascendente) ---")
        for t in lista_ordenada:
            print(t)
            
        return lista_ordenada

    def listar_todos(self):
        print(f"\n--- Listado Actual de Trabajadores ({len(self.trabajadores)} en total) ---")
        if self.trabajadores:
            for t in self.trabajadores:
                print(t)
        else:
            print("(Lista vacía)")


if __name__ == "__main__":
    NOMBRE_ARCHIVO = "trabajadores_data.json"
    print(f" INICIO DEL SISTEMA DE GESTIÓN DE TRABAJADORES ")
    
    gestion = ArchivoTrabajador(NOMBRE_ARCHIVO)
    gestion.crearArchivo()

    print("\ Ejecutando Operaciones de Guardado (b)")
    
    t1 = Trabajador("Ana Lopez", 101, 3500.00)
    t2 = Trabajador("Boris Mamani", 102, 5000.00)
    t3 = Trabajador("Carlos Perez", 103, 3000.00)

    gestion.guardarTrabajador(t1)
    gestion.guardarTrabajador(t2)
    gestion.guardarTrabajador(t3)
    
    gestion.listar_todos()

    print("\n Ejecutando Aumento de Salario (c) ")
    gestion.aumentaSalario(aumento_porcentaje=15, carnet=102) 
    gestion.aumentaSalario(aumento_porcentaje=10, carnet=101) 
    
    gestion.listar_todos()

    gestion.buscar_mayor_salario()

    gestion.ordenar_por_salario()
    
    print("\n FIN DEL SISTEMA ")