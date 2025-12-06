import json

class Persona:
    def __init__(self, nombre, apellidoPaterno, apellidoMaterno, ci):
        self.nombre = nombre
        self.apellidoPaterno = apellidoPaterno
        self.apellidoMaterno = apellidoMaterno
        self.ci = ci
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "apellidoPaterno": self.apellidoPaterno,
            "apellidoMaterno": self.apellidoMaterno,
            "ci": self.ci
        }

    def getCI(self):
        return self.ci

    def __str__(self):
        return f"Persona(CI: {self.ci}, Nombre: {self.nombre} {self.apellidoPaterno})"

class Nino(Persona):
    def __init__(self, nombre, apellidoPaterno, apellidoMaterno, ci, edad, peso, talla):
        super().__init__(nombre, apellidoPaterno, apellidoMaterno, ci)
        self.edad = edad
        self.peso = peso
        self.talla = talla
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "edad": self.edad,
            "peso": self.peso,
            "talla": self.talla
        })
        return data

    def getEdad(self):
        return self.edad

    def getPeso(self):
        return self.peso

    def getTalla(self):
        return self.talla
    
    def __str__(self):
        return (f"Niño(CI: {self.ci}, Nombre: {self.nombre} {self.apellidoPaterno}, "
                f"Edad: {self.edad} años, Peso: {self.peso}, Talla: {self.talla})")

class ArchNino:
    def __init__(self, na):
        self.na = na
        self.ninos = {}
        self.cargar_archivo()

    def _guardar_en_archivo(self):
        data_to_save = [n.to_dict() for n in self.ninos.values()]
        try:
            with open(self.na, 'w') as f:
                json.dump(data_to_save, f, indent=4)
        except IOError:
            pass

    def cargar_archivo(self):
        try:
            with open(self.na, 'r') as f:
                data = json.load(f)
                
                self.ninos.clear()
                for d in data:
                    n = Nino(
                        d['nombre'], d['apellidoPaterno'], d['apellidoMaterno'], d['ci'],
                        d['edad'], d['peso'], d['talla']
                    )
                    self.ninos[n.getCI()] = n
        except:
            pass

    def crearArchivo(self):
        self.ninos.clear()
        self._guardar_en_archivo()
        
    def adicionar(self, nino):
        self.ninos[nino.getCI()] = nino
        self._guardar_en_archivo()

    def listar(self):
        return list(self.ninos.values())



    def _es_adecuado(self, edad, peso, talla):
        
        try:
            peso_float = float(peso.replace('kg', '').strip())
            talla_float = float(talla.replace('cm', '').strip())
        except ValueError:
            return False, False

        peso_ideal = 3 * edad + 8
        peso_ok = peso_ideal * 0.9 <= peso_float <= peso_ideal * 1.1

        talla_ideal = 6 * edad + 77
        talla_ok = talla_ideal * 0.95 <= talla_float <= talla_ideal * 1.05

        return peso_ok, talla_ok

    def contar_ninos_adecuados(self):
        ninos_adecuados = 0
        for nino in self.ninos.values():
            peso_ok, talla_ok = self._es_adecuado(nino.getEdad(), nino.getPeso(), nino.getTalla())
            if peso_ok and talla_ok:
                ninos_adecuados += 1
        return ninos_adecuados

    def ninos_no_adecuados(self):
        ninos_inadecuados = []
        for nino in self.ninos.values():
            peso_ok, talla_ok = self._es_adecuado(nino.getEdad(), nino.getPeso(), nino.getTalla())
            if not peso_ok or not talla_ok:
                ninos_inadecuados.append(nino)
        return ninos_inadecuados

    def promedio_edad(self):
        if not self.ninos:
            return 0.0
        
        suma_edades = sum(n.getEdad() for n in self.ninos.values())
        return suma_edades / len(self.ninos)

    def buscar_por_ci(self, ci_x):
        return self.ninos.get(ci_x)

    def ninos_mas_altos(self):
        if not self.ninos:
            return []

        try:
            tallas = [(float(n.getTalla().replace('cm', '').strip()), n) for n in self.ninos.values()]
            max_talla = max(t for t, n in tallas)
            return [n for t, n in tallas if t == max_talla]
        except ValueError:
            return []

if __name__ == "__main__":
    
    NOMBRE_ARCHIVO = "ninos_data.json"
    print(" INICIO DEL SISTEMA DE GESTIÓN DE NIÑOS ")

    gestion = ArchNino(NOMBRE_ARCHIVO)
    gestion.crearArchivo()
    print(f"[Sistema] Archivo '{NOMBRE_ARCHIVO}' creado/reinicializado.")
    
    n1 = Nino("Carlos", "Soto", "A", 111, 4, "20.5 kg", "102 cm") 
    n2 = Nino("Laura", "Paz", "B", 222, 5, "18.0 kg", "108 cm") 
    n3 = Nino("Diego", "Cruz", "C", 333, 4, "25.0 kg", "101 cm") 
    n4 = Nino("Sofia", "Mesa", "D", 444, 6, "26.0 kg", "115 cm") 
    n5 = Nino("Pedro", "Rios", "E", 555, 6, "26.5 kg", "115 cm") 
   
    gestion.adicionar(n1)
    gestion.adicionar(n2)
    gestion.adicionar(n3)
    gestion.adicionar(n4)
    gestion.adicionar(n5)
    print("\n Operación (a) - Creación/Adición de 5 Niños ")
    
    print("\n--- a) Listado de Niños ---")
    lista_ninos = gestion.listar()
    for n in lista_ninos:
        print(f"  - {n}")

    print("\n--- b) Niños con Peso y Talla Adecuados ---")
    cont_adecuados = gestion.contar_ninos_adecuados()
    print(f"  - Número de niños con peso/talla adecuados: {cont_adecuados}")

    print("\n--- c) Niños NO Adecuados (Peso o Talla) ---")
    ninos_inadecuados = gestion.ninos_no_adecuados()
    if ninos_inadecuados:
        for n in ninos_inadecuados:
            print(f"  - {n}")
    else:
        print("  - Todos los niños tienen peso y talla adecuados según el modelo de ejemplo.")

    print("\n--- d) Promedio de Edad ---")
    promedio = gestion.promedio_edad()
    print(f"  - Promedio de edad: {promedio:.2f} años")


    ci_x = 333
    print(f"\n--- e) Buscar Niño con Carnet {ci_x} ---")
    nino_e = gestion.buscar_por_ci(ci_x)
    if nino_e:
        print(f"  - Encontrado: {nino_e}")
    else:
        print(f"  - Niño con CI {ci_x} no encontrado.")


    print("\n--- f) Niños con la Talla más Alta ---")
    ninos_f = gestion.ninos_mas_altos()
    if ninos_f:
        talla_max = ninos_f[0].getTalla()
        print(f"  - Talla Máxima Encontrada: {talla_max}")
        for n in ninos_f:
            print(f"  - {n}")
    else:
        print("  - No hay niños registrados.")

    print("\n FIN DEL SISTEMA ")