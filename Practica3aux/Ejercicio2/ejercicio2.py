
import json
import os

DEFAULT_FILE = "trabajadores.json"

class Trabajador:
    def __init__(self, nombre, carnet, salario):
        self.nombre = str(nombre)
        self.carnet = int(carnet)
        self.salario = float(salario)

    def to_dict(self):
        return {"nombre": self.nombre, "carnet": self.carnet, "salario": self.salario}

    @classmethod
    def from_dict(cls, d):
        return cls(d["nombre"], d["carnet"], d["salario"])

    def __str__(self):
        return f"Trabajador(nombre={self.nombre}, carnet={self.carnet}, salario={self.salario:.2f})"

class ArchivoTrabajador:
    def __init__(self, nombreArch=DEFAULT_FILE):
        self.nombreArch = nombreArch
        # si no existe, crear archivo vacío
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
                return [Trabajador.from_dict(d) for d in data]
            except json.JSONDecodeError:
                return []

    def guardarTrabajador(self, t: Trabajador):
        lista = self.cargar_todos()
        lista.append(t)
        with open(self.nombreArch, "w", encoding="utf-8") as f:
            json.dump([x.to_dict() for x in lista], f, indent=4)
        

    def aumentaSalario(self, aumento, carnet):
     
        lista = self.cargar_todos()
        encontrado = False
        for t in lista:
            if t.carnet == int(carnet):
                t.salario += float(aumento)
                encontrado = True
                break
        if encontrado:
            with open(self.nombreArch, "w", encoding="utf-8") as f:
                json.dump([x.to_dict() for x in lista], f, indent=4)
        return encontrado

    def buscar_mayor_salario(self):
        lista = self.cargar_todos()
        if not lista:
            return None
        mayor = max(lista, key=lambda x: x.salario)
        return mayor

    def ordenar_por_salario(self, descendente=False):
        lista = self.cargar_todos()
        return sorted(lista, key=lambda x: x.salario, reverse=descendente)

# --- utilidades 
def mostrar_lista(lst):
    if not lst:
        print("  (sin trabajadores)")
    for i, t in enumerate(lst, start=1):
        print(f"{i}. {t}")

def crear_datos_ejemplo(arch: ArchivoTrabajador):
    ejemplo = [
        Trabajador("Ana Perez", 1001, 1500.0),
        Trabajador("Juan Gomez", 1002, 2000.0),
        Trabajador("Luis Diaz", 1003, 1800.0),
        Trabajador("María Ruiz", 1004, 2200.0)
    ]
    with open(arch.nombreArch, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in ejemplo], f, indent=4)
    print("Datos de ejemplo creados.")

def menu():
    arch = ArchivoTrabajador()
    while True:
        print("\n=== ArchivoTrabajador ===")
        print("1) Mostrar todos")
        print("2) Crear datos de ejemplo")
        print("3) Guardar trabajador")
        print("4) Aumentar salario de un trabajador (por carnet)")
        print("5) Buscar trabajador con mayor salario")
        print("6) Ordenar trabajadores por salario (asc)")
        print("7) Ordenar trabajadores por salario (desc)")
        print("0) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            mostrar_lista(arch.cargar_todos())
        elif op == "2":
            crear_datos_ejemplo(arch)
        elif op == "3":
            nombre = input("Nombre: ").strip()
            carnet = int(input("Carnet (int): ").strip())
            salario = float(input("Salario: ").strip())
            t = Trabajador(nombre, carnet, salario)
            arch.guardarTrabajador(t)
            print("Trabajador guardado.")
        elif op == "4":
            carnet = int(input("Carnet del trabajador: ").strip())
            aumento = float(input("Aumento (monto en la misma moneda): ").strip())
            ok = arch.aumentaSalario(aumento, carnet)
            if ok:
                print("Salario aumentado.")
            else:
                print("Trabajador no encontrado.")
        elif op == "5":
            mayor = arch.buscar_mayor_salario()
            if mayor:
                print("Trabajador con mayor salario:")
                print(mayor)
            else:
                print("No hay trabajadores.")
        elif op == "6":
            orden = arch.ordenar_por_salario(descendente=False)
            mostrar_lista(orden)
        elif op == "7":
            orden = arch.ordenar_por_salario(descendente=True)
            mostrar_lista(orden)
        elif op == "0":
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
