
import json
import os

DEFAULT_FILE = "notas.json"

class Estudiante:
    def __init__(self, ru, nombre, paterno, materno, edad):
        self.ru = int(ru)
        self.nombre = str(nombre)
        self.paterno = str(paterno)
        self.materno = str(materno)
        self.edad = int(edad)

    def to_dict(self):
        return {
            "ru": self.ru,
            "nombre": self.nombre,
            "paterno": self.paterno,
            "materno": self.materno,
            "edad": self.edad
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["ru"], d["nombre"], d["paterno"], d["materno"], d["edad"])

    def __str__(self):
        return f"{self.ru} - {self.nombre} {self.paterno} {self.materno} (edad {self.edad})"

class Nota:
    def __init__(self, materia, notaFinal, estudiante: Estudiante):
        self.materia = str(materia)
        self.notaFinal = float(notaFinal)
        self.estudiante = estudiante

    def to_dict(self):
        return {
            "materia": self.materia,
            "notaFinal": self.notaFinal,
            "estudiante": self.estudiante.to_dict()
        }

    @classmethod
    def from_dict(cls, d):
        est = Estudiante.from_dict(d["estudiante"])
        return cls(d["materia"], d["notaFinal"], est)

    def __str__(self):
        return f"[{self.materia}] {self.estudiante} -> Nota: {self.notaFinal:.2f}"

class ArchiNota:
    def __init__(self, nombreArchi=DEFAULT_FILE):
        self.nombreArchi = nombreArchi
        if not os.path.exists(self.nombreArchi):
            self._crear_archivo_vacio()

    def _crear_archivo_vacio(self):
        with open(self.nombreArchi, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

    def cargar_todos(self):
        if not os.path.exists(self.nombreArchi):
            return []
        with open(self.nombreArchi, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return [Nota.from_dict(d) for d in data]
            except json.JSONDecodeError:
                return []

    def guardar_notas(self, lista_notas):
        with open(self.nombreArchi, "w", encoding="utf-8") as f:
            json.dump([n.to_dict() for n in lista_notas], f, indent=4, ensure_ascii=False)

    # b) Agregar varios estudiantes (recibe lista de objetos Nota)
    def agregar_varios(self, lista_notas):
        actuales = self.cargar_todos()
        actuales.extend(lista_notas)
        self.guardar_notas(actuales)
        return len(lista_notas)  # cuántas se agregaron

    # c) Promedio de notas de todos los estudiantes
    def promedio_general(self):
        lista = self.cargar_todos()
        if not lista:
            return 0.0
        total = sum(n.notaFinal for n in lista)
        return total / len(lista)

    # d) Buscar los estudiantes con la mejor nota
    def mejores(self):
        lista = self.cargar_todos()
        if not lista:
            return []
        max_nota = max(n.notaFinal for n in lista)
        return [n for n in lista if abs(n.notaFinal - max_nota) < 1e-9 or n.notaFinal == max_nota]

    # e) Eliminar todos los estudiantes de una determinada materia
    def eliminar_por_materia(self, materia):
        materia = materia.strip().lower()
        lista = self.cargar_todos()
        nueva = [n for n in lista if n.materia.strip().lower() != materia]
        eliminados = len(lista) - len(nueva)
        self.guardar_notas(nueva)
        return eliminados

# ----------------  interfaz ----------------
def mostrar_lista(lst):
    if not lst:
        print("  (sin resultados)")
        return
    for i, n in enumerate(lst, start=1):
        print(f"{i}. {n}")

def crear_datos_ejemplo(arch: ArchiNota):
    e1 = Estudiante(1001, "Ana", "Perez", "Lopez", 19)
    e2 = Estudiante(1002, "Luis", "Garcia", "Sanchez", 20)
    e3 = Estudiante(1003, "Marta", "Diaz", "Quispe", 21)
    ejemplo = [
        Nota("Matematica", 18.5, e1),
        Nota("Programacion", 17.0, e1),
        Nota("Matematica", 19.0, e2),
        Nota("Programacion", 20.0, e3),
        Nota("Fisica", 16.5, e2)
    ]
    arch.guardar_notas(ejemplo)
    print("Datos de ejemplo creados en", arch.nombreArchi)

def menu():
    arch = ArchiNota()
    while True:
        print("\n=== Archivo de Notas ===")
        print("1) Mostrar todas las notas")
        print("2) Crear datos de ejemplo (sobrescribe)")
        print("3) Agregar varios estudiantes (varias notas)")
        print("4) Obtener promedio general de notas")
        print("5) Buscar estudiante(s) con mejor nota")
        print("6) Eliminar todos los estudiantes de una materia")
        print("0) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            mostrar_lista(arch.cargar_todos())
        elif op == "2":
            crear_datos_ejemplo(arch)
        elif op == "3":
            print("Agregar varias notas. Primero ingresa cuántas notas vas a agregar.")
            try:
                k = int(input("Cantidad: ").strip())
            except ValueError:
                print("Número inválido.")
                continue
            nuevas = []
            for i in range(k):
                print(f"\nNota {i+1}:")
                materia = input(" Materia: ").strip()
                try:
                    notaFinal = float(input(" Nota final (ej. 17.5): ").strip())
                except ValueError:
                    print(" Nota inválida, se toma 0.0")
                    notaFinal = 0.0
                try:
                    ru = int(input(" RU del estudiante (int): ").strip())
                except ValueError:
                    print(" RU inválido, se toma 0")
                    ru = 0
                nombre = input(" Nombre: ").strip()
                paterno = input(" Paterno: ").strip()
                materno = input(" Materno: ").strip()
                try:
                    edad = int(input(" Edad: ").strip())
                except ValueError:
                    edad = 0
                est = Estudiante(ru, nombre, paterno, materno, edad)
                nuevas.append(Nota(materia, notaFinal, est))
            cont = arch.agregar_varios(nuevas)
            print(f"Se agregaron {cont} notas.")
        elif op == "4":
            prom = arch.promedio_general()
            print(f"Promedio general de notas: {prom:.2f}")
        elif op == "5":
            mejores = arch.mejores()
            if not mejores:
                print("No hay notas registradas.")
            else:
                maxn = mejores[0].notaFinal
                print(f"Mejor nota: {maxn:.2f}. Estudiante(s):")
                mostrar_lista(mejores)
        elif op == "6":
            mat = input("Ingresa la materia a eliminar (ej. Matematica): ").strip()
            eliminado = arch.eliminar_por_materia(mat)
            print(f"Se eliminaron {eliminado} nota(s) de la materia '{mat}'.")
        elif op == "0":
            print("Saliendo.")
            break
        else:
            print("Opción no válida. Intenta otra vez.")

if __name__ == "__main__":
    menu()
