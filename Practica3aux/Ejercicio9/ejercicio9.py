import json
import os



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

class Zoologico:
    def __init__(self, id, nombre, animales=None):
        self.id = id
        self.nombre = nombre
        self.animales = animales if animales else []

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "animales": [a.to_dict() for a in self.animales]
        }


class ArchZoo:
    archivo = "zoologicos.json"

    @staticmethod
    def cargar():
        if not os.path.exists(ArchZoo.archivo):
            return []
        with open(ArchZoo.archivo, "r") as f:
            datos = json.load(f)
        lista = []
        for z in datos:
            animales = [
                Animal(a["especie"], a["nombre"], a["cantidad"])
                for a in z["animales"]
            ]
            lista.append(Zoologico(z["id"], z["nombre"], animales))
        return lista

    @staticmethod
    def guardar(lista):
        datos = [z.to_dict() for z in lista]
        with open(ArchZoo.archivo, "w") as f:
            json.dump(datos, f, indent=4)

    @staticmethod
    def crear(zoo):
        lista = ArchZoo.cargar()
        lista.append(zoo)
        ArchZoo.guardar(lista)

    @staticmethod
    def modificar(zoo_mod):
        lista = ArchZoo.cargar()
        for i, z in enumerate(lista):
            if z.id == zoo_mod.id:
                lista[i] = zoo_mod
        ArchZoo.guardar(lista)

    @staticmethod
    def eliminar(id_zoo):
        lista = ArchZoo.cargar()
        lista = [z for z in lista if z.id != id_zoo]
        ArchZoo.guardar(lista)


# b) Zoológicos con mayor variedad
def listar_mayor_variedad():
    lista = ArchZoo.cargar()
    if not lista:
        print("No hay zoológicos registrados.")
        return
    max_var = max(len(z.animales) for z in lista)
    print(f"Zoológicos con mayor variedad ({max_var} especies):")
    for z in lista:
        if len(z.animales) == max_var:
            print(f"- [{z.id}] {z.nombre}")

# c) Listar y eliminar zoológicos vacíos
def eliminar_vacios():
    lista = ArchZoo.cargar()
    vacios = [z for z in lista if len(z.animales) == 0]
    if not vacios:
        print("No existen zoológicos vacíos.")
        return
    print("Zoológicos eliminados por estar vacíos:")
    for z in vacios:
        print(f"- {z.nombre}")
    lista = [z for z in lista if len(z.animales) > 0]
    ArchZoo.guardar(lista)

# d) Mostrar animales de especie X
def mostrar_especie(especie):
    lista = ArchZoo.cargar()
    print(f"Animales de la especie '{especie}':")
    for z in lista:
        encontrados = [a for a in z.animales if a.especie == especie]
        if encontrados:
            print(f"\nEn {z.nombre}:")
            for a in encontrados:
                print(f" - {a.nombre} ({a.cantidad})")

# NUEVA FUNCIÓN 
def listar_todos_los_animales():
    lista = ArchZoo.cargar()
    print("\n===== ANIMALES REGISTRADOS =====")
    hay_animales = False

    for z in lista:
        if z.animales:
            hay_animales = True
            print(f"\nZoológico: {z.nombre}")
            for a in z.animales:
                print(f" - Especie: {a.especie} | Nombre: {a.nombre} | Cantidad: {a.cantidad}")

    if not hay_animales:
        print("No hay animales registrados en ningún zoológico.")

# e) Mover animales del zoo X al zoo Y
def mover_animales(id_x, id_y):
    lista = ArchZoo.cargar()

    zx = next((z for z in lista if z.id == id_x), None)
    zy = next((z for z in lista if z.id == id_y), None)

    if not zx or not zy:
        print("Uno de los zoológicos no existe.")
        return

    print(f"Moviendo animales desde {zx.nombre} hacia {zy.nombre}...")

    for a in zx.animales:
        zy.animales.append(a)
    zx.animales = []

    ArchZoo.modificar(zx)
    ArchZoo.modificar(zy)

    print("Movimiento completado.")



def menu():
    while True:
        print("\n===== SISTEMA DE ZOOLÓGICOS =====")
        print("1. Crear zoológico")
        print("2. Modificar zoológico")
        print("3. Eliminar zoológico")
        print("4. Zoológicos con mayor variedad")
        print("5. Eliminar zoológicos vacíos")
        print("6. Mostrar animales de especie X")
        print("7. Mover animales entre zoológicos")
        print("8. Salir")
        print("9. Ver todos los animales") 

        op = input("Opción: ")

        if op == "1":
            id = int(input("ID: "))
            nombre = input("Nombre: ")
            zoo = Zoologico(id, nombre)
            ArchZoo.crear(zoo)
            print("Zoológico creado.")

        elif op == "2":
            id = int(input("ID del zoológico a modificar: "))
            lista = ArchZoo.cargar()
            zoo = next((z for z in lista if z.id == id), None)
            if not zoo:
                print("No existe ese zoológico.")
                continue

            nuevo_nombre = input("Nuevo nombre: ")
            zoo.nombre = nuevo_nombre
            ArchZoo.modificar(zoo)
            print("Modificado.")

        elif op == "3":
            id = int(input("ID del zoológico a eliminar: "))
            ArchZoo.eliminar(id)
            print("Zoológico eliminado.")

        elif op == "4":
            listar_mayor_variedad()

        elif op == "5":
            eliminar_vacios()

        elif op == "6":
            especie = input("Especie: ")
            mostrar_especie(especie)

        elif op == "7":
            x = int(input("ID origen: "))
            y = int(input("ID destino: "))
            mover_animales(x, y)

        elif op == "8":
            print("Saliendo...")
            break

        elif op == "9":
            listar_todos_los_animales()

        else:
            print("Opción inválida")


menu()
