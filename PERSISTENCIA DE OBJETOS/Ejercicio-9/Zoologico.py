import json

class Animal:
    def __init__(self, especie, nombre, cantidad):
        self.especie = especie
        self.nombre = nombre
        self.cantidad = cantidad
    
    def to_dict(self):
        return {
            "especie": self.especie,
            "nombre": self.nombre,
            "cantidad": self.cantidad
        }

    def getEspecie(self):
        return self.especie
    
    def getNombre(self):
        return self.nombre

    def getCantidad(self):
        return self.cantidad
    
    def setCantidad(self, nueva_cantidad):
        self.cantidad = nueva_cantidad

    def __str__(self):
        return f"Animal(Especie: {self.especie}, Nombre: {self.nombre}, Cantidad: {self.cantidad})"

class Zoologico:
    def __init__(self, id, nombre, nroAnimales, animales=None):
        self.id = id
        self.nombre = nombre
        self.animales = animales if animales is not None else {}
        self.nroAnimales = self._contar_animales()
    
    def _contar_animales(self):
        return sum(a.getCantidad() for a in self.animales.values())

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "nroAnimales": self._contar_animales(),
            "animales": [a.to_dict() for a in self.animales.values()]
        }
        
    def getId(self):
        return self.id

    def getNombre(self):
        return self.nombre

    def getNumeroAnimales(self):
        return self._contar_animales()

    def getVariedadEspecies(self):
        return len(self.animales)

    def agregar_animal(self, animal):
        self.animales[animal.getEspecie().lower()] = animal
        self.nroAnimales = self._contar_animales()

    def eliminar_animal(self, especie):
        especie_lower = especie.lower()
        animal = self.animales.pop(especie_lower, None)
        self.nroAnimales = self._contar_animales()
        return animal

    def getAnimalesPorEspecie(self, especie_x):
        especie_lower = especie_x.lower()
        return self.animales.get(especie_lower)

    def __str__(self):
        return (f"Zoo(ID: {self.id}, Nombre: {self.nombre}, "
                f"Animales Total: {self.getNumeroAnimales()}, Variedad: {self.getVariedadEspecies()})")

class ArchZoo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.zoologicos = {}
        self.cargar_archivo()

    def _guardar_en_archivo(self):
        data_to_save = [z.to_dict() for z in self.zoologicos.values()]
        try:
            with open(self.nombre, 'w') as f:
                json.dump(data_to_save, f, indent=4)
        except IOError:
            pass

    def cargar_archivo(self):
        try:
            with open(self.nombre, 'r') as f:
                data = json.load(f)
                
                self.zoologicos.clear()
                for d in data:
                    animales_dict = {}
                    for a_dict in d.get("animales", []):
                        animal = Animal(a_dict['especie'], a_dict['nombre'], a_dict['cantidad'])
                        animales_dict[animal.getEspecie().lower()] = animal

                    zoo = Zoologico(d['id'], d['nombre'], d['nroAnimales'], animales_dict)
                    self.zoologicos[zoo.getId()] = zoo
        except:
            pass

    def crearArchivo(self):
        self.zoologicos.clear()
        self._guardar_en_archivo()
        
    def get_zoo(self, id_zoo):
        return self.zoologicos.get(id_zoo)

    def adicionar(self, zoologico):
        self.zoologicos[zoologico.getId()] = zoologico
        self._guardar_en_archivo()
        
    def modificar_zoo_nombre(self, id_zoo, nuevo_nombre):
        if id_zoo in self.zoologicos:
            zoo = self.zoologicos[id_zoo]
            zoo.nombre = nuevo_nombre
            self._guardar_en_archivo()
            return True
        return False
    def eliminar_zoo(self, id_zoo):
        if id_zoo in self.zoologicos:
            del self.zoologicos[id_zoo]
            self._guardar_en_archivo()
            return True
        return False
 
    def listar_zoo_mayor_variedad(self):
        if not self.zoologicos:
            return []

        max_variedad = max(z.getVariedadEspecies() for z in self.zoologicos.values())
        
        return [z for z in self.zoologicos.values() if z.getVariedadEspecies() == max_variedad]

    def listar_y_eliminar_vacios(self):
        zoos_vacios = []
        codigos_a_eliminar = []
        
        for zoo in self.zoologicos.values():
            if zoo.getNumeroAnimales() == 0:
                zoos_vacios.append(zoo)
                codigos_a_eliminar.append(zoo.getId())

        for cod in codigos_a_eliminar:
            del self.zoologicos[cod]
            
        if codigos_a_eliminar:
            self._guardar_en_archivo()
            
        return zoos_vacios

    def animales_por_especie(self, especie_x):
        resultado = []
        for zoo in self.zoologicos.values():
            animal = zoo.getAnimalesPorEspecie(especie_x)
            if animal:
                resultado.append((animal, zoo))
        return resultado

    def mover_animales(self, id_zoo_origen, id_zoo_destino):
        zoo_x = self.zoologicos.get(id_zoo_origen)
        zoo_y = self.zoologicos.get(id_zoo_destino)
        
        if not zoo_x or not zoo_y or id_zoo_origen == id_zoo_destino:
            return 0 

        animales_a_mover = list(zoo_x.animales.values())
        movidos_count = zoo_x.getNumeroAnimales()
        
        if movidos_count == 0:
            return 0
            
        zoo_x.animales.clear()
        zoo_x.nroAnimales = 0

        for animal in animales_a_mover:
            especie_lower = animal.getEspecie().lower()
            if especie_lower in zoo_y.animales:
                animal_destino = zoo_y.animales[especie_lower]
                animal_destino.setCantidad(animal_destino.getCantidad() + animal.getCantidad())
            else:
                zoo_y.agregar_animal(animal)
            
        zoo_y.nroAnimales = zoo_y._contar_animales()
        
        self._guardar_en_archivo()
        return movidos_count

if __name__ == "__main__":
    
    NOMBRE_ARCHIVO = "zoos_data.json"
    print(" INICIO DEL SISTEMA DE GESTIÓN DE ZOOLÓGICOS ")

    gestion = ArchZoo(NOMBRE_ARCHIVO)
    gestion.crearArchivo()
    print(f"[Sistema] Archivo '{NOMBRE_ARCHIVO}' creado/reinicializado.")
    

    a1 = Animal("León", "Felino ", 2)
    a2 = Animal("Tigre", "Felino ", 1)
    a3 = Animal("Oso", "Mamifero", 3)
    a4 = Animal("Cebra", "Herbívoro", 5)
    a5 = Animal("Jirafa", "Herbívoro", 2)
    a6 = Animal("Perezoso", "Mamifero", 1)
    

    z1_animales = {a1.getEspecie().lower(): a1, a2.getEspecie().lower(): a2}  
    z2_animales = {a3.getEspecie().lower(): a3, a4.getEspecie().lower(): a4, a5.getEspecie().lower(): a5} 
    z3_animales = {}  
    
    z1 = Zoologico(1, "Zoo ", 3, z1_animales)
    z2 = Zoologico(2, "Ecologi ", 10, z2_animales)
    z3 = Zoologico(3, "Reserva Natural", 0, z3_animales)
    z4 = Zoologico(4, "Zoombrio", 0)
 
    gestion.adicionar(z1)
    gestion.adicionar(z2)
    gestion.adicionar(z3)
    gestion.adicionar(z4)
    print("\n--- a) Creación de 4 Zoológicos ---")

    gestion.modificar_zoo_nombre(id_zoo=4, nuevo_nombre="Zoo Modificado")
    print("\n--- a) Modificación del nombre del Zoo 4 ---")

    gestion.eliminar_zoo(4)
    print("\n--- a) Eliminación del Zoo 4 ---")
    
    print("\n--- Listado Actual de Zoológicos ---")
    for z in gestion.zoologicos.values():
        print(f"  - {z}")

    print("\n--- b) Zoológicos con Mayor Variedad de Especies ---")
    mayor_variedad = gestion.listar_zoo_mayor_variedad()
    if mayor_variedad:
        max_v = mayor_variedad[0].getVariedadEspecies()
        print(f"  - Máxima Variedad de Especies: {max_v}")
        for z in mayor_variedad:
            print(f"  - {z}")
    else:
        print("  - No hay zoológicos registrados.")

    print("\n--- c) Listar y Eliminar Zoológicos Vacíos (Zoo 3) ---")
    vacios_eliminados = gestion.listar_y_eliminar_vacios()
    if vacios_eliminados:
        print(f"  - Zoológicos eliminados ({len(vacios_eliminados)}):")
        for z in vacios_eliminados:
            print(f"    * Eliminado: {z.nombre} (ID: {z.getId()})")
    else:
        print("  - No se encontraron zoológicos vacíos.")

    print("\n--- Listado Después de la Eliminación de Vacíos ---")
    for z in gestion.zoologicos.values():
        print(f"  - {z}")

    especie_x = "León"
    print(f"\n--- d) Animales de la especie '{especie_x}' ---")
    animales_especie = gestion.animales_por_especie(especie_x)
    if animales_especie:
        for animal, zoo in animales_especie:
            print(f"  - {animal} (En Zoo: {zoo.nombre})")
    else:
        print(f"  - No se encontraron animales de la especie '{especie_x}'.")
        
    cod_origen = 1
    cod_destino = 2
    print(f"\n--- e) Mover todos los animales del Zoo {cod_origen} al Zoo {cod_destino} ---")
    movidos = gestion.mover_animales(cod_origen, cod_destino)
    
    if movidos > 0:
        print(f"  - Movimiento exitoso. Se movieron {movidos} animales (en total).")
        zoo_o = gestion.get_zoo(cod_origen)
        zoo_d = gestion.get_zoo(cod_destino)
        if zoo_o and zoo_d:
            print(f"    * Origen ({zoo_o.nombre}): Nuevo Stock: {zoo_o.getNumeroAnimales()}")
            print(f"    * Destino ({zoo_d.nombre}): Nuevo Stock: {zoo_d.getNumeroAnimales()}")
    else:
        print("  - No se realizó el movimiento (origen vacío o códigos inválidos).")

    print("\n FIN DEL SISTEMA ")