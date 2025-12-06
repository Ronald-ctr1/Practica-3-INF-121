import json

ARCHIVO = "charangos.json"

class Charango:
    def __init__(self, material, nroCuerdas, cuerdas):
        self.material = material
        self.nroCuerdas = nroCuerdas
        self.cuerdas = cuerdas 

    def contar_cuerdas_rotas(self):
        return self.cuerdas.count(False)

    def to_dict(self):
        """Convierte el objeto a un diccionario para guardarlo en JSON."""
        return {
            "material": self.material,
            "nroCuerdas": self.nroCuerdas,
            "cuerdas": self.cuerdas
        }

    @staticmethod
    def from_dict(data):
        """Reconstruye un Charango desde un diccionario."""
        return Charango(
            data["material"],
            data["nroCuerdas"],
            data["cuerdas"]
        )

    def __str__(self):
        return f"Material: {self.material}, Cuerdas: {self.nroCuerdas}, Estado: {self.cuerdas}"


def cargar_todos():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Charango.from_dict(d) for d in data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def guardar_lista(lista):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump([c.to_dict() for c in lista], f, indent=4)


def guardar_charango(charango):
    lista = cargar_todos()
    lista.append(charango)
    guardar_lista(lista)


def eliminar_charangos():
    lista = cargar_todos()
    lista_filtrada = [c for c in lista if c.contar_cuerdas_rotas() <= 6]
    guardar_lista(lista_filtrada)
    print("Charangos defectuosos eliminados.")


def listar(material):
    lista = cargar_todos()
    resultado = [c for c in lista if c.material.lower() == material.lower()]
    for c in resultado:
        print(c)
    return resultado


def buscar():
    lista = cargar_todos()
    resultado = [c for c in lista if c.nroCuerdas == 10]
    for c in resultado:
        print(c)
    return resultado



def ordenar():
    lista = cargar_todos()
    lista.sort(key=lambda c: c.material.lower())
    guardar_lista(lista)
    print("Archivo ordenado por material.")



if __name__ == "__main__":

    # Crear charangos de ejemplo
    c1 = Charango("Madera", 10, [True, True, True, False, True, True, True, True, False, True])
    c2 = Charango("Metal", 8,  [True]*8 + [False]*2)
    c3 = Charango("Plástico", 10, [False]*7 + [True]*3)

    guardar_charango(c1)
    guardar_charango(c2)
    guardar_charango(c3)

    print("== Eliminando defectuosos ==")
    eliminar_charangos()

    print("\n== Charangos de material 'Madera' ==")
    listar("Madera")

    print("\n== Charangos con 10 cuerdas ==")
    buscar()

    print("\n== Ordenando por material ==")
    ordenar()
