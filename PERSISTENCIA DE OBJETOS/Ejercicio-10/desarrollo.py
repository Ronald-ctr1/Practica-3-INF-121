import json
import os

NOMBRE_ARCHIVO = "jugadores.txt"

class Jugador:
    def __init__(self, nombre: str, nivel: int, puntaje: int):
        self.nombre = nombre
        self.nivel = nivel
        self.puntaje = puntaje

    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "nivel": self.nivel,
            "puntaje": self.puntaje
        }

    def __str__(self) -> str:
        return f"Nombre: {self.nombre} | Nivel: {self.nivel} | Puntaje: {self.puntaje}"

class GestorJugadores:
    def __init__(self):
        self.jugadores: dict[str, Jugador] = {}
        self._cargar_jugadores()

    def _cargar_jugadores(self):
        """Carga los datos de jugadores desde el archivo 'jugadores.txt'."""
        if os.path.exists(NOMBRE_ARCHIVO):
            try:
                with open(NOMBRE_ARCHIVO, 'r') as f:
                    data = json.load(f)
                    for item in data:
                        jugador = Jugador(
                            item['nombre'],
                            item['nivel'],
                            item['puntaje']
                        )
                        self.jugadores[jugador.nombre.lower()] = jugador
                print(f"[Sistema] {len(self.jugadores)} jugadores cargados exitosamente.")
            except (IOError, json.JSONDecodeError):
                print("[Sistema] Error al leer o decodificar el archivo. Inicializando vacío.")
        else:
            print("[Sistema] Archivo de jugadores no encontrado. Inicializando vacío.")

    def _guardar_jugadores(self):
        """Guarda todos los jugadores en el archivo 'jugadores.txt'."""
        data_to_save = [j.to_dict() for j in self.jugadores.values()]
        try:
            with open(NOMBRE_ARCHIVO, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            print("[Sistema] Datos guardados.")
        except IOError:
            print("[Sistema] Error al escribir en el archivo.")

    def agregar_jugador(self, nombre: str, nivel: int, puntaje: int):
        """Crea y guarda un nuevo jugador."""
        nombre_lower = nombre.lower()
        if nombre_lower in self.jugadores:
            print(f"Error: El jugador '{nombre}' ya existe.")
            return

        nuevo_jugador = Jugador(nombre, nivel, puntaje)
        self.jugadores[nombre_lower] = nuevo_jugador
        self._guardar_jugadores()
        print(f"¡Jugador '{nombre}' agregado!")

    def listar_jugadores(self):
        """Muestra la información de todos los jugadores."""
        if not self.jugadores:
            print("No hay jugadores registrados.")
            return

        print("\n--- LISTA DE JUGADORES ---")
        for jugador in self.jugadores.values():
            print(f"- {jugador}")
        print("--------------------------")

    def buscar_jugador(self, nombre: str) -> Jugador | None:
        """Busca y devuelve un jugador por nombre."""
        nombre_lower = nombre.lower()
        jugador_encontrado = self.jugadores.get(nombre_lower)
        
        if jugador_encontrado:
            print("\n--- JUGADOR ENCONTRADO ---")
            print(f"{jugador_encontrado}")
            print("--------------------------")
            return jugador_encontrado
        else:
            print(f"Error: Jugador '{nombre}' no encontrado.")
            return None

# --- FUNCIÓN PRINCIPAL Y MENÚ ---
def menu_principal():
    """Ejecuta el menú principal del programa."""
    gestor = GestorJugadores()
    
    while True:
        print("\n=== MENÚ DEL VIDEOJUEGO ===")
        print("1. Agregar nuevo jugador")
        print("2. Mostrar todos los jugadores")
        print("3. Buscar jugador por nombre")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            nombre = input("Nombre del jugador: ").strip()
            
            try:
                nivel = int(input("Nivel: "))
                if nivel < 1: raise ValueError
            except ValueError:
                print("El nivel debe ser un número entero positivo.")
                continue

            try:
                puntaje = int(input("Puntaje: "))
                if puntaje < 0: raise ValueError
            except ValueError:
                print("El puntaje debe ser un número entero no negativo.")
                continue
                
            if nombre:
                gestor.agregar_jugador(nombre, nivel, puntaje)
            else:
                print("El nombre no puede estar vacío.")

        elif opcion == '2':
            gestor.listar_jugadores()
            
        elif opcion == '3':
            nombre = input("Ingrese el nombre del jugador a buscar: ").strip()
            if nombre:
                gestor.buscar_jugador(nombre)
            else:
                print("El nombre no puede estar vacío.")

        elif opcion == '4':
            print("¡Gracias por usar el gestor de jugadores! ¡Adiós!")
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()