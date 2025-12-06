

import json
import os
from collections import defaultdict

LIBROS_FILE = "libros.json"
PRESTAMOS_FILE = "prestamos.json"
CLIENTES_FILE = "clientes.json"

class Libro:
    def __init__(self, codLibro, titulo, precio):
        self.codLibro = int(codLibro)
        self.titulo = str(titulo)
        self.precio = float(precio)

    def to_dict(self):
        return {"codLibro": self.codLibro, "titulo": self.titulo, "precio": self.precio}

    @classmethod
    def from_dict(cls, d):
        return cls(d["codLibro"], d["titulo"], d["precio"])

    def __str__(self):
        return f"{self.codLibro} - {self.titulo} (${self.precio:.2f})"

class Prestamo:
    def __init__(self, codCliente, codLibro, fechaPrestamo, cantidad):
        self.codCliente = int(codCliente)
        self.codLibro = int(codLibro)
        self.fechaPrestamo = str(fechaPrestamo)
        self.cantidad = int(cantidad)

    def to_dict(self):
        return {"codCliente": self.codCliente, "codLibro": self.codLibro,
                "fechaPrestamo": self.fechaPrestamo, "cantidad": self.cantidad}

    @classmethod
    def from_dict(cls, d):
        return cls(d["codCliente"], d["codLibro"], d["fechaPrestamo"], d["cantidad"])

    def __str__(self):
        return f"Cliente {self.codCliente} - Libro {self.codLibro} - {self.cantidad} uds ({self.fechaPrestamo})"

class Cliente:
    def __init__(self, codCliente, nombre, apellido):
        self.codCliente = int(codCliente)
        self.nombre = str(nombre)
        self.apellido = str(apellido)

    def to_dict(self):
        return {"codCliente": self.codCliente, "nombre": self.nombre, "apellido": self.apellido}

    @classmethod
    def from_dict(cls, d):
        return cls(d["codCliente"], d["nombre"], d["apellido"])

    def __str__(self):
        return f"{self.codCliente} - {self.nombre} {self.apellido}"

# ---------- funciones de persistencia ----------
def load_json_list(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_json_list(filename, lista):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

def load_libros():
    data = load_json_list(LIBROS_FILE)
    return [Libro.from_dict(d) for d in data]

def save_libros(libros):
    save_json_list(LIBROS_FILE, [l.to_dict() for l in libros])

def load_prestamos():
    data = load_json_list(PRESTAMOS_FILE)
    return [Prestamo.from_dict(d) for d in data]

def save_prestamos(prestamos):
    save_json_list(PRESTAMOS_FILE, [p.to_dict() for p in prestamos])

def load_clientes():
    data = load_json_list(CLIENTES_FILE)
    return [Cliente.from_dict(d) for d in data]

def save_clientes(clientes):
    save_json_list(CLIENTES_FILE, [c.to_dict() for c in clientes])


# a) Listar los libros cuyo precio estén entre 2 valores (x y y).
def libros_en_rango(x, y):
    libros = load_libros()
    x = float(x); y = float(y)
    menor, mayor = min(x,y), max(x,y)
    return [l for l in libros if menor <= l.precio <= mayor]

# b) Calcular el ingreso total generado por un libro específico.
#    Sumamos (cantidad * precio del libro) sobre todos los prestamos de ese libro.
def ingreso_total_por_libro(codLibro):
    libros = {l.codLibro: l for l in load_libros()}
    prestamos = load_prestamos()
    total = 0.0
    for p in prestamos:
        if p.codLibro == int(codLibro):
            libro = libros.get(p.codLibro)
            if libro:
                total += p.cantidad * libro.precio
    return total

# c) Mostrar la lista de libros que nunca fueron vendidos (prestados).
def libros_no_vendidos():
    libros = {l.codLibro: l for l in load_libros()}
    prestamos = load_prestamos()
    vendidos = set(p.codLibro for p in prestamos)
    return [libros[c] for c in libros if c not in vendidos]

# d) Mostrar a todos los clientes que compraron/solicitaron un libro especifico (por codigo).
def clientes_que_compraron_libro(codLibro):
    clientes = {c.codCliente: c for c in load_clientes()}
    prestamos = load_prestamos()
    cod = int(codLibro)
    cods_clientes = set(p.codCliente for p in prestamos if p.codLibro == cod)
    return [clientes[c] for c in cods_clientes if c in clientes]

# e) Definir  el libro más prestado (por cantidad total).
def libro_mas_prestado():
    prestamos = load_prestamos()
    if not prestamos:
        return None, 0
    cont = defaultdict(int)  
    for p in prestamos:
        cont[p.codLibro] += p.cantidad
    cod_max = max(cont, key=lambda k: cont[k])
    libros = {l.codLibro: l for l in load_libros()}
    return libros.get(cod_max), cont[cod_max]

# f) Mostrar el cliente que tuvo más préstamos (sumando cantidad).
def cliente_con_mas_prestamos():
    prestamos = load_prestamos()
    if not prestamos:
        return None, 0
    cont = defaultdict(int)  # codCliente -> total cantidad
    for p in prestamos:
        cont[p.codCliente] += p.cantidad
    cod_max = max(cont, key=lambda k: cont[k])
    clientes = {c.codCliente: c for c in load_clientes()}
    return clientes.get(cod_max), cont[cod_max]

# ---------- menu ----------
def crear_datos_ejemplo():
    libros = [
        Libro(1, "Programacion I", 30.0),
        Libro(2, "Matematicas Basicas", 20.0),
        Libro(3, "Algoritmos", 45.5),
        Libro(4, "Estructuras de Datos", 50.0),
        Libro(5, "Ingles Tecnico", 15.0)
    ]
    clientes = [
        Cliente(101, "Ana", "Perez"),
        Cliente(102, "Juan", "Gomez"),
        Cliente(103, "Luis", "Diaz"),
        Cliente(104, "Marta", "Quispe")
    ]
    prestamos = [
        Prestamo(101, 1, "2025-03-01", 1),
        Prestamo(102, 1, "2025-03-02", 2),
        Prestamo(103, 3, "2025-03-05", 1),
        Prestamo(101, 3, "2025-03-10", 1),
        Prestamo(104, 4, "2025-03-11", 3),
        Prestamo(102, 2, "2025-03-12", 1)
    ]
    save_libros(libros)
    save_clientes(clientes)
    save_prestamos(prestamos)
    print("Datos de ejemplo creados: libros.json, clientes.json, prestamos.json")

def mostrar_lista(lst):
    if not lst:
        print("  (sin resultados)")
        return
    for i, e in enumerate(lst, start=1):
        print(f"{i}. {e}")

def menu():
    while True:
        print("\n=== Ejercicio 6: Libros / Prestamos / Clientes ===")
        print("1) Crear datos de ejemplo (sobrescribe archivos)")
        print("2) Listar todos los libros")
        print("3) Listar libros por rango de precio (a)")
        print("4) Ingreso total generado por un libro (b)")
        print("5) Listar libros que nunca fueron prestados (c)")
        print("6) Mostrar clientes que prestaron un libro (d)")
        print("7) Libro más prestado (e)")
        print("8) Cliente con más préstamos (f)")
        print("9) Agregar libro manual")
        print("10) Agregar cliente manual")
        print("11) Agregar préstamo manual")
        print("0) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            crear_datos_ejemplo()
        elif op == "2":
            mostrar_lista(load_libros())
        elif op == "3":
            try:
                x = float(input("Precio mínimo (x): ").strip())
                y = float(input("Precio máximo (y): ").strip())
            except ValueError:
                print("Valor inválido.")
                continue
            res = libros_en_rango(x, y)
            print(f"Libros con precio entre {x} y {y}:")
            mostrar_lista(res)
        elif op == "4":
            try:
                cod = int(input("Código del libro: ").strip())
            except ValueError:
                print("Código inválido.")
                continue
            total = ingreso_total_por_libro(cod)
            print(f"Ingreso total generado por el libro {cod}: ${total:.2f}")
        elif op == "5":
            res = libros_no_vendidos()
            print("Libros que nunca fueron prestados:")
            mostrar_lista(res)
        elif op == "6":
            try:
                cod = int(input("Código del libro: ").strip())
            except ValueError:
                print("Código inválido.")
                continue
            res = clientes_que_compraron_libro(cod)
            print(f"Clientes que participaron en préstamos del libro {cod}:")
            mostrar_lista(res)
        elif op == "7":
            libro, cnt = libro_mas_prestado()
            if libro:
                print(f"Libro más prestado: {libro} - Total unidades prestadas: {cnt}")
            else:
                print("No hay préstamos registrados.")
        elif op == "8":
            cliente, cnt = cliente_con_mas_prestamos()
            if cliente:
                print(f"Cliente con más préstamos: {cliente} - Total unidades prestadas: {cnt}")
            else:
                print("No hay préstamos registrados.")
        elif op == "9":
            try:
                cod = int(input("Código libro: ").strip())
                titulo = input("Título: ").strip()
                precio = float(input("Precio: ").strip())
            except ValueError:
                print("Datos inválidos.")
                continue
            libros = load_libros()
            libros.append(Libro(cod, titulo, precio))
            save_libros(libros)
            print("Libro guardado.")
        elif op == "10":
            try:
                cod = int(input("Código cliente: ").strip())
                nombre = input("Nombre: ").strip()
                apellido = input("Apellido: ").strip()
            except ValueError:
                print("Datos inválidos.")
                continue
            clientes = load_clientes()
            clientes.append(Cliente(cod, nombre, apellido))
            save_clientes(clientes)
            print("Cliente guardado.")
        elif op == "11":
            try:
                codC = int(input("Código cliente: ").strip())
                codL = int(input("Código libro: ").strip())
                fecha = input("Fecha (YYYY-MM-DD): ").strip()
                cantidad = int(input("Cantidad (int): ").strip())
            except ValueError:
                print("Datos inválidos.")
                continue
            prestamos = load_prestamos()
            prestamos.append(Prestamo(codC, codL, fecha, cantidad))
            save_prestamos(prestamos)
            print("Préstamo guardado.")
        elif op == "0":
            print("Saliendo.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
