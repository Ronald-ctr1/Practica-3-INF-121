import json

class Medicamento:
    def __init__(self, nombre, codMedicamento, tipo, precio):
        self.nombre = nombre
        self.codMedicamento = codMedicamento
        self.tipo = tipo
        self.precio = precio

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "codMedicamento": self.codMedicamento,
            "tipo": self.tipo,
            "precio": self.precio
        }

    def getTipo(self):
        return self.tipo

    def getPrecio(self):
        return self.precio

    def __str__(self):
        return f"Medicamento(Cod: {self.codMedicamento}, Nombre: {self.nombre}, Tipo: {self.tipo}, Precio: {self.precio:.2f})"

class Farmacia:
    def __init__(self, nombreFarmacia, sucursal, direccion, nroMedicamentos, medicamentos=None):
        self.nombreFarmacia = nombreFarmacia
        self.sucursal = sucursal
        self.direccion = direccion
        self.medicamentos = medicamentos if medicamentos is not None else []
        self.nroMedicamentos = len(self.medicamentos)

    def to_dict(self):
        return {
            "nombreFarmacia": self.nombreFarmacia,
            "sucursal": self.sucursal,
            "direccion": self.direccion,
            "nroMedicamentos": len(self.medicamentos),
            "medicamentos": [m.to_dict() for m in self.medicamentos]
        }
        
    def getDireccion(self):
        return self.direccion

    def getSucursal(self):
        return self.sucursal
    
    def buscarMedicamento(self, nombre_med):
        nombre_lower = nombre_med.lower()
        return [
            m for m in self.medicamentos 
            if m.nombre.lower() == nombre_lower
        ]

    def __str__(self):
        return (f"Farmacia(Sucursal: {self.sucursal}, Nombre: {self.nombreFarmacia}, "
                f"Dirección: {self.direccion}, Stock: {len(self.medicamentos)} medicamentos)")
    
    def __repr__(self):
        return self.__str__()

class ArchFarmacia:
    def __init__(self, na):
        self.na = na
        self.farmacias = {}
        self.cargar_archivo()

    def _guardar_en_archivo(self):
        data_to_save = [f.to_dict() for f in self.farmacias.values()]
        try:
            with open(self.na, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            print(f"[Sistema] Datos guardados exitosamente en '{self.na}'.")
        except IOError:
            print(f"[Sistema] Error al escribir en el archivo '{self.na}'.")

    def cargar_archivo(self):
        try:
            with open(self.na, 'r') as f:
                data = json.load(f)
                
                self.farmacias.clear()
                for d in data:
                    medicamentos_list = [
                        Medicamento(m['nombre'], m['codMedicamento'], m['tipo'], m['precio']) 
                        for m in d.get("medicamentos", [])
                    ]
                    farm = Farmacia(
                        d['nombreFarmacia'], 
                        d['sucursal'], 
                        d['direccion'], 
                        d['nroMedicamentos'], 
                        medicamentos_list
                    )
                    self.farmacias[farm.sucursal] = farm
                
            print(f"[Sistema] Archivo '{self.na}' cargado con {len(self.farmacias)} sucursales.")
        except FileNotFoundError:
            print(f"[Sistema] Archivo '{self.na}' no encontrado. Inicializando vacío.")
        except json.JSONDecodeError:
            print(f"[Sistema] Archivo '{self.na}' mal formado. Inicializando vacío.")

    def crearArchivo(self):
        self.farmacias.clear()
        self._guardar_en_archivo()
        print(f"[Operación] Archivo '{self.na}' creado/reinicializado.")
        
    def adicionar(self, farmacia):
        if farmacia.sucursal in self.farmacias:
            print(f"[Advertencia] Sucursal {farmacia.sucursal} ya existe. Sobrescribiendo.")
        
        self.farmacias[farmacia.sucursal] = farmacia
        self._guardar_en_archivo()
        print(f"[Operación] Farmacia '{farmacia.nombreFarmacia} - {farmacia.sucursal}' guardada.")


    def mostrar_medicamentos_tos_sucursal(self, sucursal_x):
        print(f"\n--- a) Medicamentos para la Tos en Sucursal {sucursal_x} ---")
        
        farmacia = self.farmacias.get(sucursal_x)
        if not farmacia:
            print(f"[Resultado] Sucursal {sucursal_x} no encontrada.")
            return

        medicamentos_tos = [
            m for m in farmacia.medicamentos 
            if m.getTipo().lower() == "tos"
        ]

        if medicamentos_tos:
            print(f"[Resultado] Farmacia: {farmacia.nombreFarmacia} - {farmacia.direccion}")
            for m in medicamentos_tos:
                print(f"  - {m}")
        else:
            print(f"[Resultado] No hay medicamentos de tipo 'tos' en la Sucursal {sucursal_x}.")

    def buscar_farmacias_por_medicamento(self, nombre_med):
        print(f"\n--- b) Sucursales que tienen el medicamento '{nombre_med}' ---")
        
        sucursales_encontradas = []
        
        for farmacia in self.farmacias.values():
            if farmacia.buscarMedicamento(nombre_med):
                sucursales_encontradas.append(farmacia)
                
        if sucursales_encontradas:
            for f in sucursales_encontradas:
                print(f"[Resultado] Sucursal N°{f.getSucursal()} en: {f.getDireccion()}")
        else:
            print(f"[Resultado] Ninguna sucursal tiene el medicamento '{nombre_med}'.")

    def buscar_medicamentos_por_tipo(self, tipo_med):
        print(f"\n--- c) Buscando medicamentos de tipo '{tipo_med}' ---")
        
        tipo_lower = tipo_med.lower()
        encontrados = []
        
        for farmacia in self.farmacias.values():
            for m in farmacia.medicamentos:
                if m.getTipo().lower() == tipo_lower:
                    encontrados.append((m, farmacia.sucursal))

        if encontrados:
            for m, sucursal in encontrados:
                print(f"[Resultado] {m} (En Sucursal: {sucursal})")
        else:
            print(f"[Resultado] No se encontraron medicamentos de tipo '{tipo_med}' en ninguna sucursal.")
            
    def ordenar_farmacias_por_direccion(self):
        print("\n--- d) Farmacias Ordenadas por Dirección ---")
        
        if not self.farmacias:
            print("[Resultado] No hay farmacias para ordenar.")
            return []

        lista_ordenada = sorted(
            self.farmacias.values(), 
            key=lambda f: f.getDireccion().lower()
        )
        
        for f in lista_ordenada:
            print(f"[Resultado] Sucursal N°{f.sucursal}: {f.getDireccion()}")
            
        return lista_ordenada

    def mover_medicamentos(self, tipo_med, sucursal_origen, sucursal_destino):
        print(f"\n--- e) Moviendo medicamentos tipo '{tipo_med}' de Suc. {sucursal_origen} a Suc. {sucursal_destino} ---")
        
        farmacia_y = self.farmacias.get(sucursal_origen)
        farmacia_z = self.farmacias.get(sucursal_destino)
        tipo_lower = tipo_med.lower()

        if not farmacia_y:
            print(f"[Error] Farmacia origen (Sucursal {sucursal_origen}) no encontrada.")
            return
        if not farmacia_z:
            print(f"[Error] Farmacia destino (Sucursal {sucursal_destino}) no encontrada.")
            return
            
        if sucursal_origen == sucursal_destino:
            print("[Error] Las sucursales de origen y destino son las mismas. No se realiza el movimiento.")
            return

        medicamentos_a_mover = []
        medicamentos_restantes = []
        movidos_count = 0
        
        for m in farmacia_y.medicamentos:
            if m.getTipo().lower() == tipo_lower:
                medicamentos_a_mover.append(m)
                movidos_count += 1
            else:
                medicamentos_restantes.append(m)

        farmacia_y.medicamentos = medicamentos_restantes
        farmacia_y.nroMedicamentos = len(medicamentos_restantes)

        farmacia_z.medicamentos.extend(medicamentos_a_mover)
        farmacia_z.nroMedicamentos = len(farmacia_z.medicamentos)
        
        if movidos_count > 0:
            self._guardar_en_archivo()
            print(f"[Resultado] Movimiento exitoso. Se movieron {movidos_count} medicamentos de tipo '{tipo_med}'.")
            print(f"  - Origen (Suc.{sucursal_origen}): Nuevo stock {len(farmacia_y.medicamentos)}")
            print(f"  - Destino (Suc.{sucursal_destino}): Nuevo stock {len(farmacia_z.medicamentos)}")
        else:
            print(f"[Resultado] No se encontraron medicamentos de tipo '{tipo_med}' en la farmacia origen.")
            
    def listar_farmacias(self):
        print(f"\n--- Listado Actual de Farmacias ({len(self.farmacias)} en total) ---")
        for f in self.farmacias.values():
            print(f)


if __name__ == "__main__":
    NOMBRE_ARCHIVO = "farmacias_data.json"
    print(" INICIO DEL SISTEMA DE GESTIÓN DE FARMACIAS ")

    gestion = ArchFarmacia(NOMBRE_ARCHIVO)
    gestion.crearArchivo()

    m1 = Medicamento("Tapsin", 101, "Resfrio", 5.50)
    m2 = Medicamento("Jarabe P", 102, "Tos", 12.00)
    m3 = Medicamento("Aspirina", 103, "Dolor", 2.00)
    farm1 = Farmacia("Farmacia Central", 1, "Calle A 100", 3, [m1, m2, m3])

    m4 = Medicamento("Tapsin", 201, "Resfrio", 6.00)
    m5 = Medicamento("Jarabe Q", 202, "Tos", 15.00)
    m6 = Medicamento("Ibuprofeno", 203, "Dolor", 8.50)
    farm2 = Farmacia("Farmacia Sur", 2, "Avenida B 50", 3, [m4, m5, m6])

    m7 = Medicamento("Diclofenaco", 301, "Dolor", 7.00)
    m8 = Medicamento("Jarabe R", 302, "Tos", 10.00)
    farm3 = Farmacia("Farmacia Norte", 3, "Plaza C 20", 2, [m7, m8])
    
    gestion.adicionar(farm1)
    gestion.adicionar(farm2)
    gestion.adicionar(farm3)
    
    gestion.listar_farmacias()
    print("\n Ejecutando Operaciones Solicitadas ")
    gestion.mostrar_medicamentos_tos_sucursal(sucursal_x=2)
    gestion.buscar_farmacias_por_medicamento(nombre_med="Tapsin")
    gestion.buscar_medicamentos_por_tipo(tipo_med="Dolor")
    gestion.ordenar_farmacias_por_direccion()
    gestion.mover_medicamentos(tipo_med="Tos", sucursal_origen=2, sucursal_destino=1)
    gestion.listar_farmacias()

    print("\n FIN DEL SISTEMA ")