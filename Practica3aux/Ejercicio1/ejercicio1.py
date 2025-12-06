
import json
import os

DATA_FILE = "charangos.json"  # archivo json

class Charango:
    def __init__(self, material, nroCuerdas, cuerdas):
        """
        cuerdas: lista de 10 booleanos (True/False)
        nroCuerdas: int (puede coincidir con sum(cuerdas) o ser independiente)
        """
        self.material = material
        self.nroCuerdas = int(nroCuerdas)
        if len(cuerdas) != 10:
            raise ValueError("La lista 'cuerdas' debe tener exactamente 10 elementos.")
        self.cuerdas = [bool(x) for x in cuerdas]

    def to_dict(self):
        return {
            "material": self.material,
            "nroCuerdas": self.nroCuerdas,
            "cuerdas": self.cuerdas
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["material"], d["nroCuerdas"], d["cuerdas"])

    def __str__(self):
        return f"Charango(material={self.material}, nroCuerdas={self.nroCuerdas}, cuerdas={self.cuerdas})"
#funciones persis
def load_charangos(filename=DATA_FILE):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return [Charango.from_dict(d) for d in data]
        except json.JSONDecodeError:
            return []

def save_charangos(charangos, filename=DATA_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([c.to_dict() for c in charangos], f, indent=4, ensure_ascii=False)

# ------ operaciones
def eliminar_charangos_malas(charangos):
    """
    b) Eliminar a los charangos cuyas cuerdas en estado False sean > 6.
    Devuelve la nueva lista (no modifica el archivo directamente).
    """
    nueva = []
    for c in charangos:
        falses = sum(1 for estado in c.cuerdas if not estado)
        if falses <= 6:
            nueva.append(c)
    return nueva

def listar_por_material(charangos, material_x):
    """
    c) Listar a los charangos de material x (case-insensitive)
    """
    m = material_x.strip().lower()
    return [c for c in charangos if c.material.strip().lower() == m]

def buscar_con_10_cuerdas(charangos):
    """
    d) Buscar charangos con 10 cuerdas (nroCuerdas == 10)
    """
    return [c for c in charangos if c.nroCuerdas == 10]

def ordenar_por_material(charangos):
    """
    e) Ordenar los charangos por material en orden alfabético.
    Devuelve una nueva lista ordenada.
    """
    return sorted(charangos, key=lambda c: c.material.lower())
#datos de ejemplo crear
def crear_datos_ejemplo():
    ejemplo = [
        Charango("Madera", 10, [True]*10),
        Charango("Plastico", 8, [True, True, False, False, True, False, False, False, True, False]),
        Charango("Madera", 6, [False, False, False, False, False, False, True, True, True, True]),
        Charango("Metal", 10, [True]*10),
        Charango("Madera", 9, [True, True, True, True, True, True, True, True, True, False]),
        Charango("Fibra", 4, [False, False, False, False, False, False, False, True, True, True])
    ]
    save_charangos(ejemplo)
    print("Datos de ejemplo creados y guardados en", DATA_FILE)

# -- interfaz  por consola 
def mostrar_lista(lst):
    if not lst:
        print("  (sin resultados)")
    for i, c in enumerate(lst, start=1):
        print(f"{i}. {c}")

def menu():
    print("=== Practica: Charangos (persistencia JSON) ===")
    charangos = load_charangos()
    while True:
        print("\nOpciones:")
        print("1) Mostrar todos")
        print("2) Crear datos de ejemplo (sobrescribe/crea archivo)")
        print("3) Eliminar charangos con >6 cuerdas en false (y guardar)")
        print("4) Listar charangos por material")
        print("5) Buscar charangos con 10 cuerdas")
        print("6) Ordenar por material (y mostrar)")
        print("7) Agregar un charango manualmente")
        print("0) Salir")
        opcion = input("Elige opción: ").strip()
        if opcion == "1":
            mostrar_lista(charangos)
        elif opcion == "2":
            crear_datos_ejemplo()
            charangos = load_charangos()
        elif opcion == "3":
            antes = len(charangos)
            charangos = eliminar_charangos_malas(charangos)
            save_charangos(charangos)
            print(f"Se eliminaron {antes - len(charangos)} charango(s). Guardado en {DATA_FILE}.")
        elif opcion == "4":
            mat = input("Ingresa material a buscar: ")
            res = listar_por_material(charangos, mat)
            mostrar_lista(res)
        elif opcion == "5":
            res = buscar_con_10_cuerdas(charangos)
            mostrar_lista(res)
        elif opcion == "6":
            ordenados = ordenar_por_material(charangos)
            mostrar_lista(ordenados)
            # si quieres guardar el orden:
            guardar = input("¿Guardar este orden en el archivo? (s/n): ").strip().lower()
            if guardar == "s":
                save_charangos(ordenados)
                charangos = ordenados
                print("Orden guardado.")
        elif opcion == "7":
            mat = input("Material: ").strip()
            nro = int(input("Numero de cuerdas (int): ").strip())
            print("Ingresa 10 valores para las cuerdas (1 para True, 0 para False).")
            cuerdas = []
            for i in range(10):
                v = input(f"Cuerda {i+1} (1/0): ").strip()
                cuerdas.append(v == "1")
            nuevo = Charango(mat, nro, cuerdas)
            charangos.append(nuevo)
            save_charangos(charangos)
            print("Charango agregado y guardado.")
        elif opcion == "0":
            print("Saliendo. ¡Chao!")
            break
        else:
            print("Opción no válida. Intenta otra vez.")

if __name__ == "__main__":
    menu()
