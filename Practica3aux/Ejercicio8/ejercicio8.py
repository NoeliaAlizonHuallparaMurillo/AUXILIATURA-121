
import json
import os
from datetime import datetime

DEFAULT_FILE = "refrigerador.json"
DATE_FORMAT = "%Y-%m-%d"  #formto fecha

class Alimento:
    def __init__(self, nombre, fechaVencimiento, cantidad):
        self.nombre = str(nombre)
        # guardamos la fecha como string pero validamos formato
        try:
            datetime.strptime(fechaVencimiento, DATE_FORMAT)
        except Exception:
            raise ValueError(f"fechaVencimiento debe tener formato YYYY-MM-DD, se recibió: {fechaVencimiento}")
        self.fechaVencimiento = fechaVencimiento
        self.cantidad = int(cantidad)

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "fechaVencimiento": self.fechaVencimiento,
            "cantidad": self.cantidad
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["nombre"], d["fechaVencimiento"], d["cantidad"])

    def __str__(self):
        return f"{self.nombre} - Vence: {self.fechaVencimiento} - Cantidad: {self.cantidad}"

class ArchRefri:
    def __init__(self, nombre="refrigerador", filename=DEFAULT_FILE):
        self.nombre = nombre
        self.filename = filename
        if not os.path.exists(self.filename):
            self.crear()  # crea archivo vacío

    def crear(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        # print("Archivo creado:", self.filename)

    def cargar_todos(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return [Alimento.from_dict(d) for d in data]
            except json.JSONDecodeError:
                return []

    def guardar_todos(self, lista_alimentos):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([a.to_dict() for a in lista_alimentos], f, indent=4, ensure_ascii=False)

    # ---------- a) Crear, Modificar por nombre, Eliminar por nombre ----------
    def crear_alimento(self, alimento: Alimento):
        lista = self.cargar_todos()
        # si ya existe un alimento con el mismo nombre (case-insensitive), lo actualizamos sumando cantidad
        for i, a in enumerate(lista):
            if a.nombre.strip().lower() == alimento.nombre.strip().lower():
                # decisión de estudiante: si existe, sumamos cantidades y actualizamos fecha si es más lejana
                lista[i].cantidad += alimento.cantidad
                # actualizamos fecha si la nueva fecha es posterior (más lejana) o menor? 
                # Aquí mantengo la fecha de vencimiento más cercana (la menor) para seguridad:
                fecha_actual = datetime.strptime(lista[i].fechaVencimiento, DATE_FORMAT)
                fecha_nueva = datetime.strptime(alimento.fechaVencimiento, DATE_FORMAT)
                if fecha_nueva < fecha_actual:
                    lista[i].fechaVencimiento = alimento.fechaVencimiento
                self.guardar_todos(lista)
                return "sumada"  # se sumó a existente
        # si no existe, agregar nuevo
        lista.append(alimento)
        self.guardar_todos(lista)
        return "creado"

    def modificar_por_nombre(self, nombre, nuevos_campos: dict):
        """
        nuevos_campos puede contener claves: nombre, fechaVencimiento, cantidad
        Retorna True si modificó algo, False si no encontró.
        """
        lista = self.cargar_todos()
        modificado = False
        for i, a in enumerate(lista):
            if a.nombre.strip().lower() == nombre.strip().lower():
                if "nombre" in nuevos_campos:
                    lista[i].nombre = str(nuevos_campos["nombre"])
                if "fechaVencimiento" in nuevos_campos:
                    # validar formato
                    datetime.strptime(nuevos_campos["fechaVencimiento"], DATE_FORMAT)
                    lista[i].fechaVencimiento = nuevos_campos["fechaVencimiento"]
                if "cantidad" in nuevos_campos:
                    lista[i].cantidad = int(nuevos_campos["cantidad"])
                modificado = True
                break
        if modificado:
            self.guardar_todos(lista)
        return modificado

    def eliminar_por_nombre(self, nombre):
        lista = self.cargar_todos()
        nueva = [a for a in lista if a.nombre.strip().lower() != nombre.strip().lower()]
        eliminados = len(lista) - len(nueva)
        if eliminados > 0:
            self.guardar_todos(nueva)
        return eliminados

    # ---------- b) Mostrar los alimentos que caducaron antes de una fecha dada X ----------
    def mostrar_vencidos_antes(self, fechaX):
        """
        fechaX: string "YYYY-MM-DD"
        devuelve lista de Alimento con fechaVencimiento < fechaX
        """
        try:
            fecha_lim = datetime.strptime(fechaX, DATE_FORMAT)
        except Exception:
            raise ValueError("fechaX debe tener formato YYYY-MM-DD")
        lista = self.cargar_todos()
        vencidos = []
        for a in lista:
            f = datetime.strptime(a.fechaVencimiento, DATE_FORMAT)
            if f < fecha_lim:
                vencidos.append(a)
        return vencidos

    # ---------- c) Eliminar los alimentos que tengan cantidad 0 ----------
    def eliminar_cantidad_cero(self):
        lista = self.cargar_todos()
        nueva = [a for a in lista if a.cantidad != 0]
        eliminados = len(lista) - len(nueva)
        if eliminados > 0:
            self.guardar_todos(nueva)
        return eliminados

    # ---------- d) Buscar los alimentos ya vencidos ----------
    def listar_vencidos(self, hoy=None):
        
        if hoy is None:
            hoy_dt = datetime.now()
        else:
            hoy_dt = datetime.strptime(hoy, DATE_FORMAT)
        lista = self.cargar_todos()
        vencidos = [a for a in lista if datetime.strptime(a.fechaVencimiento, DATE_FORMAT) < hoy_dt]
        return vencidos

    # ---------- e) Mostrar el alimento que tenga más cantidad ----------
    def alimento_mayor_cantidad(self):
        lista = self.cargar_todos()
        if not lista:
            return None
        mayor = max(lista, key=lambda x: x.cantidad)
        return mayor

# ---------- interfaz ----------------
def mostrar_lista(lista):
    if not lista:
        print("  (sin resultados)")
        return
    for i, a in enumerate(lista, start=1):
        print(f"{i}. {a}")

def crear_datos_ejemplo(arch: ArchRefri):
    datos = [
        Alimento("Leche", "2025-04-15", 2),
        Alimento("Yogurt", "2025-03-20", 0),
        Alimento("Queso", "2025-05-01", 1),
        Alimento("Mantequilla", "2024-12-30", 3),
        Alimento("Jugo", "2025-02-10", 5)
    ]
    arch.guardar_todos(datos)
    print("Datos de ejemplo guardados en", arch.filename)

def menu():
    arch = ArchRefri()
    while True:
        print("\n=== Archivo: Refrigerador (Alimentos) ===")
        print("1) Mostrar todos los alimentos")
        print("2) Crear datos de ejemplo (sobrescribe archivo)")
        print("3) Crear/Agregar un alimento (si existe suma cantidad)")
        print("4) Modificar alimento por nombre")
        print("5) Eliminar alimento por nombre")
        print("6) Mostrar alimentos vencidos antes de una fecha X (a)")
        print("7) Eliminar alimentos con cantidad 0 (c)")
        print("8) Mostrar alimentos ya vencidos (hoy) (d)")
        print("9) Mostrar alimento con mayor cantidad (e)")
        print("0) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            mostrar_lista(arch.cargar_todos())
        elif op == "2":
            crear_datos_ejemplo(arch)
        elif op == "3":
            nombre = input("Nombre: ").strip()
            fecha = input("Fecha de Vencimiento (YYYY-MM-DD): ").strip()
            try:
                cantidad = int(input("Cantidad (int): ").strip())
            except ValueError:
                print("Cantidad inválida, se toma 0.")
                cantidad = 0
            try:
                res = arch.crear_alimento(Alimento(nombre, fecha, cantidad))
                if res == "creado":
                    print("Alimento creado.")
                else:
                    print("Alimento existente: cantidad sumada y fecha actualizada si corresponde.")
            except Exception as e:
                print("Error:", e)
        elif op == "4":
            nombre = input("Nombre del alimento a modificar: ").strip()
            campos = {}
            nuevo_nombre = input("  Nuevo nombre (enter para omitir): ").strip()
            if nuevo_nombre:
                campos["nombre"] = nuevo_nombre
            nueva_fecha = input("  Nueva fecha Vencimiento (YYYY-MM-DD) (enter para omitir): ").strip()
            if nueva_fecha:
                campos["fechaVencimiento"] = nueva_fecha
            nueva_cant = input("  Nueva cantidad (enter para omitir): ").strip()
            if nueva_cant:
                try:
                    campos["cantidad"] = int(nueva_cant)
                except ValueError:
                    print("Cantidad inválida, se omite campo.")
            if not campos:
                print("No se ingresaron cambios.")
            else:
                try:
                    ok = arch.modificar_por_nombre(nombre, campos)
                    if ok:
                        print("Modificado correctamente.")
                    else:
                        print("No se encontró alimento con ese nombre.")
                except Exception as e:
                    print("Error:", e)
        elif op == "5":
            nombre = input("Nombre del alimento a eliminar: ").strip()
            elim = arch.eliminar_por_nombre(nombre)
            print(f"Se eliminaron {elim} registro(s).")
        elif op == "6":
            fechaX = input("Fecha X (YYYY-MM-DD): ").strip()
            try:
                venc = arch.mostrar_vencidos_antes(fechaX)
                print(f"Alimentos vencidos antes de {fechaX}:")
                mostrar_lista(venc)
            except Exception as e:
                print("Error:", e)
        elif op == "7":
            elim = arch.eliminar_cantidad_cero()
            print(f"Se eliminaron {elim} alimento(s) con cantidad 0.")
        elif op == "8":
            hoy = None
            usar_fecha = input("¿Usar otra fecha que no sea hoy? (s/n): ").strip().lower()
            if usar_fecha == "s":
                hoy = input("Ingresa fecha (YYYY-MM-DD): ").strip()
            try:
                venc = arch.listar_vencidos(hoy)
                print("Alimentos vencidos respecto a la fecha indicada:")
                mostrar_lista(venc)
            except Exception as e:
                print("Error:", e)
        elif op == "9":
            mayor = arch.alimento_mayor_cantidad()
            if mayor:
                print("Alimento con mayor cantidad:")
                print(mayor)
            else:
                print("No hay alimentos registrados.")
        elif op == "0":
            print("Saliendo.")
            break
        else:
            print("Opción no válida. Intenta otra vez.")

if __name__ == "__main__":
    menu()
