

import json
import os

DEFAULT_FILE = "productos.json"

class Producto:
    def __init__(self, codigo, nombre, precio):
        self.codigo = int(codigo)
        self.nombre = str(nombre)
        self.precio = float(precio)

    def to_dict(self):
        return {"codigo": self.codigo, "nombre": self.nombre, "precio": self.precio}

    @classmethod
    def from_dict(cls, d):
        return cls(d["codigo"], d["nombre"], d["precio"])

    def __str__(self):
        return f"Producto(codigo={self.codigo}, nombre={self.nombre}, precio={self.precio:.2f})"

class ArchivoProducto:
    def __init__(self, nombreArch=DEFAULT_FILE):
        self.nombreArch = nombreArch
        if not os.path.exists(self.nombreArch):
            self.crearArchivo()

    def crearArchivo(self):
        with open(self.nombreArch, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

    def cargar_todos(self):
        if not os.path.exists(self.nombreArch):
            return []
        with open(self.nombreArch, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return [Producto.from_dict(d) for d in data]
            except json.JSONDecodeError:
                return []

    def guardarProducto(self, p: Producto):
        lista = self.cargar_todos()
        # evitar duplicado por codigo: si existe se reemplaza
        for i, prod in enumerate(lista):
            if prod.codigo == p.codigo:
                lista[i] = p
                break
        else:
            lista.append(p)
        with open(self.nombreArch, "w", encoding="utf-8") as f:
            json.dump([x.to_dict() for x in lista], f, indent=4)

    def buscaProducto(self, codigo):
        lista = self.cargar_todos()
        for p in lista:
            if p.codigo == int(codigo):
                return p
        return None

    def promedio_precios(self):
        lista = self.cargar_todos()
        if not lista:
            return 0.0
        total = sum(p.precio for p in lista)
        return total / len(lista)

    def producto_mas_caro(self):
        lista = self.cargar_todos()
        if not lista:
            return None
        return max(lista, key=lambda p: p.precio)

# --- interfaz 
def mostrar_lista(lst):
    if not lst:
        print("  (sin productos)")
    for i, p in enumerate(lst, start=1):
        print(f"{i}. {p}")

def crear_datos_ejemplo(arch: ArchivoProducto):
    ejemplo = [
        Producto(1, "Cuaderno", 5.50),
        Producto(2, "Lápiz", 0.80),
        Producto(3, "Mochila", 25.00),
        Producto(4, "Calculadora", 45.99)
    ]
    with open(arch.nombreArch, "w", encoding="utf-8") as f:
        json.dump([p.to_dict() for p in ejemplo], f, indent=4)
    print("Datos de ejemplo creados.")

def menu():
    arch = ArchivoProducto()
    while True:
        print("\n=== ArchivoProducto ===")
        print("1) Mostrar todos")
        print("2) Crear datos de ejemplo")
        print("3) Guardar producto")
        print("4) Buscar producto por codigo")
        print("5) Calcular promedio de precios")
        print("6) Mostrar producto más caro")
        print("0) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            mostrar_lista(arch.cargar_todos())
        elif op == "2":
            crear_datos_ejemplo(arch)
        elif op == "3":
            codigo = int(input("Codigo (int): ").strip())
            nombre = input("Nombre: ").strip()
            precio = float(input("Precio: ").strip())
            p = Producto(codigo, nombre, precio)
            arch.guardarProducto(p)
            print("Producto guardado/actualizado.")
        elif op == "4":
            codigo = int(input("Codigo a buscar: ").strip())
            res = arch.buscaProducto(codigo)
            if res:
                print("Producto encontrado:")
                print(res)
            else:
                print("No se encontró producto con ese código.")
        elif op == "5":
            prom = arch.promedio_precios()
            print(f"Promedio de precios: {prom:.2f}")
        elif op == "6":
            caro = arch.producto_mas_caro()
            if caro:
                print("Producto más caro:")
                print(caro)
            else:
                print("No hay productos.")
        elif op == "0":
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
