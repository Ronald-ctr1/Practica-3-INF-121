import json

class Estudiante:
    def __init__(self, ru, nombre, paterno, materno, edad):
        self.ru = ru
        self.nombre = nombre
        self.paterno = paterno
        self.materno = materno
        self.edad = edad
    
    def to_dict(self):
        return {
            "ru": self.ru,
            "nombre": self.nombre,
            "paterno": self.paterno,
            "materno": self.materno,
            "edad": self.edad
        }
    
    def __str__(self):
        return f"Estudiante(RU: {self.ru}, Nombre: {self.nombre} {self.paterno}, Edad: {self.edad})"

class Nota:
    def __init__(self, materia, notaFinal, estudiante):
        self.materia = materia
        self.notaFinal = notaFinal
        self.estudiante = estudiante
    
    def to_dict(self):
        return {
            "materia": self.materia,
            "notaFinal": self.notaFinal,
            "ru_estudiante": self.estudiante.ru 
        }
    
    def __str__(self):
        return (f"Nota(Materia: {self.materia}, Nota: {self.notaFinal:.1f}, "
                f"Estudiante: {self.estudiante.nombre} {self.estudiante.paterno})")

class ArchiNota:
    def __init__(self, nombreArchi):
        self.nombreArchi = nombreArchi
        self.notas = []
        self.estudiantes = {}
        self.cargar_archivo()

    def _guardar_en_archivo(self):
        notas_data = [n.to_dict() for n in self.notas]
        estudiantes_data = [e.to_dict() for e in self.estudiantes.values()]
        
        data_to_save = {
            "estudiantes": estudiantes_data,
            "notas": notas_data
        }
        
        try:
            with open(self.nombreArchi, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            print(f"[Sistema] Datos guardados exitosamente en '{self.nombreArchi}'.")
        except IOError:
            print(f"[Sistema] Error al escribir en el archivo '{self.nombreArchi}'.")

    def cargar_archivo(self):
        try:
            with open(self.nombreArchi, 'r') as f:
                data = json.load(f)
                
                self.estudiantes.clear()
                for d in data.get("estudiantes", []):
                    est = Estudiante(d['ru'], d['nombre'], d['paterno'], d['materno'], d['edad'])
                    self.estudiantes[est.ru] = est
                
                self.notas.clear()
                for d in data.get("notas", []):
                    ru = d['ru_estudiante']
                    estudiante_ref = self.estudiantes.get(ru)
                    if estudiante_ref:
                        self.notas.append(Nota(d['materia'], d['notaFinal'], estudiante_ref))
                
            print(f"[Sistema] Archivo '{self.nombreArchi}' cargado con {len(self.estudiantes)} estudiantes y {len(self.notas)} notas.")
        except FileNotFoundError:
            print(f"[Sistema] Archivo '{self.nombreArchi}' no encontrado. Inicializando vacío.")
        except json.JSONDecodeError:
            print(f"[Sistema] Archivo '{self.nombreArchi}' mal formado. Inicializando vacío.")

    def crearArchivo(self):
        self.estudiantes.clear()
        self.notas.clear()
        self._guardar_en_archivo()
        print(f"[Operación] Archivo '{self.nombreArchi}' creado/reinicializado.")
        
    def agregar_estudiantes(self, lista_estudiantes):
        nuevos_agregados = 0
        for est in lista_estudiantes:
            if est.ru not in self.estudiantes:
                self.estudiantes[est.ru] = est
                nuevos_agregados += 1
            else:
                print(f"[Advertencia] Estudiante con RU {est.ru} ya existe. Ignorado.")
                
        self._guardar_en_archivo()
        print(f"[Operación] Se agregaron {nuevos_agregados} nuevos estudiantes.")

    def agregar_nota(self, nota):
        if nota.estudiante.ru not in self.estudiantes:
            print(f"[Error] No se puede agregar la nota. Estudiante con RU {nota.estudiante.ru} no registrado.")
            return

        self.notas.append(nota)
        self._guardar_en_archivo()
        print(f"[Operación] Nota de {nota.materia} para {nota.estudiante.nombre} guardada.")

    def obtener_promedio_notas(self):
        print("\n--- c) Promedio de Notas ---")
        if not self.notas:
            print("[Resultado] No hay notas registradas. Promedio: 0.0")
            return 0.0
        
        suma_notas = sum(n.notaFinal for n in self.notas)
        promedio = suma_notas / len(self.notas)
        
        print(f"[Resultado] Promedio de {len(self.notas)} notas: {promedio:.2f}")
        return promedio

    def buscar_mejor_nota(self):
        print("\n--- d) Estudiante(s) con la Mejor Nota ---")
        if not self.notas:
            print("[Resultado] No hay notas para buscar la mejor.")
            return []

        max_nota_val = max(n.notaFinal for n in self.notas)
        
        mejores_estudiantes = []
        for n in self.notas:
            if n.notaFinal == max_nota_val:
                mejores_estudiantes.append(n)
        
        print(f"[Resultado] La nota más alta es {max_nota_val:.1f}. Obtenida por:")
        
        estudiantes_unicos = set(n.estudiante.ru for n in mejores_estudiantes)
        
        for ru in estudiantes_unicos:
            est = self.estudiantes.get(ru)
            print(f"  - {est} (Materia(s): {', '.join(n.materia for n in mejores_estudiantes if n.estudiante.ru == ru)})")
            
        return mejores_estudiantes

    def eliminar_por_materia(self, materia):
        print(f"\n--- e) Eliminando Notas de la Materia '{materia}' ---")
        
        materia_lower = materia.lower()
        
        notas_original_count = len(self.notas)
        
        self.notas = [
            n for n in self.notas 
            if n.materia.lower() != materia_lower
        ]
        
        eliminados = notas_original_count - len(self.notas)
        
        if eliminados > 0:
            self._guardar_en_archivo()
            print(f"[Resultado] Se eliminaron {eliminados} notas para la materia '{materia}'.")
        else:
            print(f"[Resultado] No se encontraron notas para la materia '{materia}'. No se realizó la eliminación.")


if __name__ == "__main__":
    NOMBRE_ARCHIVO = "notas_data.json"
    print("### INICIO DEL SISTEMA DE GESTIÓN DE NOTAS ###")

    gestion = ArchiNota(NOMBRE_ARCHIVO)
    gestion.crearArchivo()

    e1 = Estudiante(ru=1001, nombre="Ana", paterno="Cruz", materno="B", edad=20)
    e2 = Estudiante(ru=1002, nombre="Juan", paterno="Paz", materno="M", edad=21)
    e3 = Estudiante(ru=1003, nombre="Elsa", paterno="Sol", materno="C", edad=22)
    
    lista_estudiantes = [e1, e2, e3]

    print("\n### Ejecutando Operación (b) - Agregar Estudiantes ###")
    gestion.agregar_estudiantes(lista_estudiantes)

    n1 = Nota("Matematicas", 95.0, e1)
    n2 = Nota("Fisica", 80.0, e1)
    n3 = Nota("Matematicas", 98.0, e2) 
    n4 = Nota("Fisica", 98.0, e3) 
    n5 = Nota("Quimica", 70.0, e3)
    n6 = Nota("Matematicas", 50.0, e3) 

    gestion.agregar_nota(n1)
    gestion.agregar_nota(n2)
    gestion.agregar_nota(n3)
    gestion.agregar_nota(n4)
    gestion.agregar_nota(n5)
    gestion.agregar_nota(n6)

    gestion.obtener_promedio_notas()

    gestion.buscar_mejor_nota()

    gestion.eliminar_por_materia("Matematicas")
    
    gestion.obtener_promedio_notas() 
    gestion.buscar_mejor_nota() 

    print("\n### FIN DEL SISTEMA ###")