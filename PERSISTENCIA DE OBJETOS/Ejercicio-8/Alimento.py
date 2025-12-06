import json
from datetime import datetime

class Alimento:
    def __init__(self, nombre, fechaVencimiento, cantidad):
        self.nombre = nombre
        self.fechaVencimiento = fechaVencimiento
        self.cantidad = cantidad
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "fechaVencimiento": self.fechaVencimiento,
            "cantidad": self.cantidad
        }

    def getNombre(self):
        return self.nombre

    def getFechaVencimiento(self):
        return self.fechaVencimiento

    def getCantidad(self):
        return self.cantidad
    
    def setCantidad(self, nueva_cantidad):
        self.cantidad = nueva_cantidad

    def __str__(self):
        return (f"Alimento(Nombre: {self.nombre}, Vencimiento: {self.fechaVencimiento}, "
                f"Cantidad: {self.cantidad})")

class ArchRefri:
    def __init__(self, nombre):
        self.nombre = nombre
        self.alimentos = {}
        self.cargar_archivo()

    def _guardar_en_archivo(self):
        data_to_save = [a.to_dict() for a in self.alimentos.values()]
        try:
            with open(self.nombre, 'w') as f:
                json.dump(data_to_save, f, indent=4)
        except IOError:
            pass

    def cargar_archivo(self):
        try:
            with open(self.nombre, 'r') as f:
                data = json.load(f)
                
                self.alimentos.clear()
                for d in data:
                    a = Alimento(d['nombre'], d['fechaVencimiento'], d['cantidad'])
                    self.alimentos[a.getNombre().lower()] = a
        except:
            pass

    def crearArchivo(self):
        self.alimentos.clear()
        self._guardar_en_archivo()
        
    def listar(self):
        return list(self.alimentos.values())


    def adicionar(self, alimento):
        self.alimentos[alimento.getNombre().lower()] = alimento
        self._guardar_en_archivo()

    def modificar_por_nombre(self, nombre_alimento, nueva_cantidad=None, nueva_fecha=None):
        nombre_lower = nombre_alimento.lower()
        if nombre_lower in self.alimentos:
            alimento = self.alimentos[nombre_lower]
            if nueva_cantidad is not None:
                alimento.setCantidad(nueva_cantidad)
            if nueva_fecha is not None:
                alimento.fechaVencimiento = nueva_fecha
            self._guardar_en_archivo()
            return True
        return False

    def eliminar_por_nombre(self, nombre_alimento):
        nombre_lower = nombre_alimento.lower()
        if nombre_lower in self.alimentos:
            del self.alimentos[nombre_lower]
            self._guardar_en_archivo()
            return True
        return False

    def caducados_antes_de(self, fecha_x_str):
        alimentos_caducados = []
        try:
            fecha_x = datetime.strptime(fecha_x_str, '%Y-%m-%d').date()
        except ValueError:
            return []
            
        for alimento in self.alimentos.values():
            try:
                fecha_vencimiento = datetime.strptime(alimento.getFechaVencimiento(), '%Y-%m-%d').date()
                if fecha_vencimiento < fecha_x:
                    alimentos_caducados.append(alimento)
            except ValueError:
                pass
                
        return alimentos_caducados
    def eliminar_cantidad_cero(self):
        nombres_a_eliminar = [
            nombre for nombre, alimento in self.alimentos.items() 
            if alimento.getCantidad() == 0
        ]
        
        eliminados = 0
        for nombre in nombres_a_eliminar:
            del self.alimentos[nombre]
            eliminados += 1
            
        if eliminados > 0:
            self._guardar_en_archivo()
            
        return eliminados

    def buscar_alimentos_s(self):
        hoy = datetime.now().date()
        alimentos_s = []
        
        for alimento in self.alimentos.values():
            try:
                fecha_vencimiento = datetime.strptime(alimento.getFechaVencimiento(), '%Y-%m-%d').date()
                if fecha_vencimiento < hoy:
                    alimentos_s.append(alimento)
            except ValueError:
                pass
                
        return alimentos_s

    def alimento_con_mas_cantidad(self):
        if not self.alimentos:
            return None
        
        alimento_max = None
        max_cantidad = -1
        
        for alimento in self.alimentos.values():
            if alimento.getCantidad() > max_cantidad:
                max_cantidad = alimento.getCantidad()
                alimento_max = alimento
            
        return alimento_max



if __name__ == "__main__":
    
    NOMBRE_ARCHIVO = "refri_data.json"
    HOY_PRUEBA = "2025-12-06"
    print(" INICIO DEL SISTEMA DE GESTIÓN DE REFRIGERADOR ")

    gestion = ArchRefri(NOMBRE_ARCHIVO)
    gestion.crearArchivo()
    print(f"[Sistema] Archivo '{NOMBRE_ARCHIVO}' creado/reinicializado.")
    
    a1 = Alimento("Leche", "2025-12-10", 3)
    a2 = Alimento("Yogur", "2025-12-01", 5)   
    a3 = Alimento("Queso", "2026-01-20", 0)   
    a4 = Alimento("Jugo", "2025-12-05", 10)    
    a5 = Alimento("Huevo", "2026-03-01", 12)

    gestion.adicionar(a1)
    gestion.adicionar(a2)
    gestion.adicionar(a3)
    gestion.adicionar(a4)
    gestion.adicionar(a5)

    print("\n--- a) Creación de 5 Alimentos ---")
    
    print("\n--- a) Modificar 'Yogur' (cantidad a 2, fecha a 2025-12-15) ---")
    gestion.modificar_por_nombre("Yogur", nueva_cantidad=2, nueva_fecha="2025-12-15")
    
    print("\n--- a) Eliminar 'Leche' ---")
    gestion.eliminar_por_nombre("Leche")

    print("\n--- Listado Actual de Alimentos ---")
    for a in gestion.listar():
        print(f"  - {a}")

    fecha_limite = "2025-12-10"
    print(f"\n--- b) Alimentos caducados antes de {fecha_limite} ---")
    caducados_antes = gestion.caducados_antes_de(fecha_limite)
    if caducados_antes:
        for a in caducados_antes:
            print(f"  - {a}")
    else:
        print("  - Ningún alimento caducó antes de la fecha límite.")

    print("\n--- c) Eliminando alimentos con cantidad 0 ('Queso') ---")
    eliminados_cero = gestion.eliminar_cantidad_cero()
    print(f"  - Alimentos eliminados por cantidad 0: {eliminados_cero}")

    print("\n--- Listado Después de Eliminación por Cantidad ---")
    for a in gestion.listar():
        print(f"  - {a}")
    print(f"\n--- d) Alimentos ya s (Hoy: {HOY_PRUEBA}) ---")
    s = gestion.buscar_alimentos_s()
    if s:
        for a in s:
            print(f"  - {a}")
    else:
        print("  - Ningún alimento está .")

    print("\n--- e) Alimento con más cantidad en el refri ---")
    alimento_max_cant = gestion.alimento_con_mas_cantidad()
    if alimento_max_cant:
        print(f"  - Alimento: {alimento_max_cant}")
    else:
        print("  - El refrigerador está vacío.")
        
    print("\n FIN DEL SISTEMA ")