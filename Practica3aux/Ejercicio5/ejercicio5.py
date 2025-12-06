
import json
import os

DEFAULT_FILE = "farmacias.json"

class Medicamento:
    def __init__(self, nombre, codMedicamento, tipo, precio):
        self.nombre = str(nombre)
        self.codMedicamento = int(codMedicamento)
        self.tipo = str(tipo)   # ej. "tos", "dolor", "antibiotico"
        self.precio = float(precio)

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "codMedicamento": self.codMedicamento,
            "tipo": self.tipo,
            "precio": self.precio
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["nombre"], d["codMedicamento"], d["tipo"], d["precio"])

    def __str__(self):
        return f"{self.nombre} (cod:{self.codMedicamento}, tipo:{self.tipo}, ${self.precio:.2f})"

class Farmacia:
    def __init__(self, nombreFarmacia, sucursal, direccion, medicamentos=None):
        self.nombreFarmacia = str(nombreFarmacia)
        self.sucursal = int(sucursal)
        self.direccion = str(direccion)
        self.medicamentos = medicamentos if medicamentos is not None else []

    def to_dict(self):
        return {
            "nombreFarmacia": self.nombreFarmacia,
            "sucursal": self.sucursal,
            "direccion": self.direccion,
            "medicamentos": [m.to_dict() for m in self.medicamentos]
        }

    @classmethod
    def from_dict(cls, d):
        meds = [Medicamento.from_dict(m) for m in d.get("medicamentos", [])]
        return cls(d["nombreFarmacia"], d["sucursal"], d["direccion"], meds)

    def __str__(self):
        return f"{self.nombreFarmacia} - Sucursal {self.sucursal} - {self.direccion} (meds: {len(self.medicamentos)})"

class ArchFarmacia:
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
                return [Farmacia.from_dict(d) for d in data]
            except json.JSONDecodeError:
                return []

    def guardar_todos(self, lista_farmacias):
        with open(self.nombreArch, "w", encoding="utf-8") as f:
            json.dump([f_.to_dict() for f_ in lista_farmacias], f, indent=4, ensure_ascii=False)

    def agregar_farmacia(self, farmacia: Farmacia):
        lista = self.cargar_todos()
        
        for i, f_ in enumerate(lista):
            if f_.sucursal == farmacia.sucursal:
                lista[i] = farmacia
                break
        else:
            lista.append(farmacia)
        self.guardar_todos(lista)

    # a) Mostrar los medicamentos para la tos, de la Sucursal número X
    def mostrarMedicamentosTos(self, sucursal):
        lista = self.cargar_todos()
        for f in lista:
            if f.sucursal == int(sucursal):
                return [m for m in f.medicamentos if m.tipo.strip().lower() == "tos"]
        return []  # si no existe sucursal o no hay meds de tos

    # b) Mostrar el número de sucursal y su dirección que tienen el medicamento "Tapsin"
    def buscarTapsin(self):
        lista = self.cargar_todos()
        res = []
        for f in lista:
            for m in f.medicamentos:
                if m.nombre.strip().lower() == "tapsin":
                    res.append((f.sucursal, f.direccion))
                    break
        return res  # lista de tuplas (sucursal, direccion)

    # c) Buscar medicamentos por tipo
    def buscar_por_tipo(self, tipo_buscar):
        tipo_buscar = tipo_buscar.strip().lower()
        lista = self.cargar_todos()
        encontrados = []
        for f in lista:
            for m in f.medicamentos:
                if m.tipo.strip().lower() == tipo_buscar:
                    encontrados.append((f.sucursal, f.nombreFarmacia, m))
        return encontrados  # lista de (sucursal, nombreFarmacia, Medicamento)

    # d) Ordenar las farmacias según su dirección en orden alfabético.
    def ordenar_por_direccion(self):
        lista = self.cargar_todos()
        ordenadas = sorted(lista, key=lambda x: x.direccion.lower())
        return ordenadas

    # e) Mover los medicamentos de tipo x de la farmacia origen 
    def mover_medicamentos_tipo(self, suc_origen, suc_destino, tipo):
        lista = self.cargar_todos()
        origen = None
        destino = None
        for f in lista:
            if f.sucursal == int(suc_origen):
                origen = f
            if f.sucursal == int(suc_destino):
                destino = f
        if origen is None or destino is None:
            return 0  # no se pudo hacer no existe
        tipo_l = tipo.strip().lower()
        a_mover = [m for m in origen.medicamentos if m.tipo.strip().lower() == tipo_l]
        if not a_mover:
            return 0
        # quitar de origen
        origen.medicamentos = [m for m in origen.medicamentos if m.tipo.strip().lower() != tipo_l]
        # agregar a destino (mantener codigos, nombres, precios)
        destino.medicamentos.extend(a_mover)
        # guardar cambios
        self.guardar_todos(lista)
        return len(a_mover)

# ---------------- interfaz ----------------
def mostrar_lista_meds(meds):
    if not meds:
        print("  (sin medicamentos)")
        return
    for i, m in enumerate(meds, start=1):
        print(f"{i}. {m}")

def mostrar_farmacias(lst):
    if not lst:
        print("  (sin farmacias)")
        return
    for i, f in enumerate(lst, start=1):
        print(f"{i}. {f}")
        mostrar_lista_meds(f.medicamentos)
        print("-"*30)

def crear_datos_ejemplo(arch: ArchFarmacia):
    f1 = Farmacia("Farmacia Salud", 1, "Av. Bolivia 123", [
        Medicamento("Tapsin", 101, "tos", 12.50),
        Medicamento("BroncoStop", 102, "tos", 10.00),
        Medicamento("DolorFast", 201, "dolor", 8.00)
    ])
    f2 = Farmacia("Farmacenter", 2, "Calle Real 45", [
        Medicamento("Tapsin", 103, "tos", 13.00),
        Medicamento("Antibiocil", 301, "antibiotico", 25.00)
    ])
    f3 = Farmacia("Botica Central", 3, "Av. Independencia 8", [
        Medicamento("Calmaton", 401, "dolor", 9.50),
        Medicamento("JarabeX", 402, "tos", 11.00)
    ])
    arch.guardar_todos([f1, f2, f3])
    print("Datos de ejemplo creados en", arch.nombreArch)

def menu():
    arch = ArchFarmacia()
    while True:
        print("\n=== Archivo Farmacias ===")
        print("1) Mostrar todas las farmacias y sus medicamentos")
        print("2) Crear datos de ejemplo (sobrescribe)")
        print("3) Mostrar los medicamentos para la tos de la sucursal X (a)")
        print("4) Mostrar sucursal y direccion que tienen el medicamento 'Tapsin' (b)")
        print("5) Buscar medicamentos por tipo (c)")
        print("6) Ordenar farmacias por direccion y mostrar (d)")
        print("7) Mover medicamentos de tipo X de sucursal A a sucursal Z (e)")
        print("8) Agregar/actualizar una farmacia manualmente")
        print("0) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            mostrar_farmacias(arch.cargar_todos())
        elif op == "2":
            crear_datos_ejemplo(arch)
        elif op == "3":
            try:
                suc = int(input("Ingresa número de sucursal: ").strip())
            except ValueError:
                print("Número inválido.")
                continue
            meds = arch.mostrarMedicamentosTos(suc)
            print(f"Medicamentos para la tos en sucursal {suc}:")
            mostrar_lista_meds(meds)
        elif op == "4":
            res = arch.buscarTapsin()
            if not res:
                print("No se encontró 'Tapsin' en ninguna sucursal.")
            else:
                for suc, dirc in res:
                    print(f"Sucursal {suc} - Dirección: {dirc}")
        elif op == "5":
            tipo = input("Tipo a buscar (ej. tos, dolor): ").strip()
            encontrados = arch.buscar_por_tipo(tipo)
            if not encontrados:
                print("No se encontraron medicamentos de ese tipo.")
            else:
                print(f"Medicamentos de tipo '{tipo}':")
                for suc, nombreFarm, med in encontrados:
                    print(f"Sucursal {suc} - {nombreFarm} -> {med}")
        elif op == "6":
            orden = arch.ordenar_por_direccion()
            print("Farmacias ordenadas por dirección (alfabético):")
            mostrar_farmacias(orden)
        elif op == "7":
            try:
                origen = int(input("Sucursal origen (A): ").strip())
                destino = int(input("Sucursal destino (Z): ").strip())
            except ValueError:
                print("Sucursal inválida.")
                continue
            tipo = input("Tipo de medicamentos a mover (ej. tos): ").strip()
            moved = arch.mover_medicamentos_tipo(origen, destino, tipo)
            if moved == 0:
                print("No se movió nada. Revisa que las sucursales existan y que haya medicamentos de ese tipo.")
            else:
                print(f"Se movieron {moved} medicamento(s) del tipo '{tipo}' de sucursal {origen} a {destino}.")
        elif op == "8":
            nombre = input("Nombre farmacia: ").strip()
            try:
                suc = int(input("Numero sucursal (int): ").strip())
            except ValueError:
                print("Sucursal inválida.")
                continue
            direccion = input("Dirección: ").strip()
            meds = []
            agregar = input("¿Agregar medicamentos ahora? (s/n): ").strip().lower()
            if agregar == "s":
                try:
                    k = int(input("¿Cuántos medicamentos?: ").strip())
                except ValueError:
                    k = 0
                for i in range(k):
                    print(f"Medicamento {i+1}:")
                    nombreM = input("  Nombre: ").strip()
                    try:
                        cod = int(input("  Codigo (int): ").strip())
                    except ValueError:
                        cod = 0
                    tipo = input("  Tipo: ").strip()
                    try:
                        precio = float(input("  Precio: ").strip())
                    except ValueError:
                        precio = 0.0
                    meds.append(Medicamento(nombreM, cod, tipo, precio))
            f = Farmacia(nombre, suc, direccion, meds)
            arch.agregar_farmacia(f)
            print("Farmacia agregada/actualizada.")
        elif op == "0":
            print("Saliendo.")
            break
        else:
            print("Opción no válida. Intenta otra vez.")

if __name__ == "__main__":
    menu()
