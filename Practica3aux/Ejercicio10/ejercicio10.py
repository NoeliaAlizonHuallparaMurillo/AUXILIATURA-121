import base64
import os


#   CLASE USUARIO


class Usuario:
    def __init__(self, nombre, password):
        self.nombre = nombre
        self.password = password

    # Cifrado simple (XOR + base64)
    def cifrar(self, texto):
        key = 12
        cifrado = "".join(chr(ord(c) ^ key) for c in texto)
        return base64.b64encode(cifrado.encode()).decode()

    def descifrar(self, texto):
        key = 12
        decodificado = base64.b64decode(texto.encode()).decode()
        return "".join(chr(ord(c) ^ key) for c in decodificado)

    def to_line(self):
        return f"{self.cifrar(self.nombre)}|{self.cifrar(self.password)}\n"

    @staticmethod
    def from_line(linea):
        nombre_cif, pass_cif = linea.strip().split("|")
        temp = Usuario("", "")
        nombre = temp.descifrar(nombre_cif)
        password = temp.descifrar(pass_cif)
        return Usuario(nombre, password)



#   CLASE GESTORA


class GestorUsuarios:
    archivo = "usuarios_seguro.txt"

    @staticmethod
    def guardar(usuario):
        with open(GestorUsuarios.archivo, "a") as f:
            f.write(usuario.to_line())

    @staticmethod
    def leer_todos():
        if not os.path.exists(GestorUsuarios.archivo):
            return []

        usuarios = []
        with open(GestorUsuarios.archivo, "r") as f:
            for linea in f:
                usuarios.append(Usuario.from_line(linea))
        return usuarios

    @staticmethod
    def buscar(nombre):
        usuarios = GestorUsuarios.leer_todos()
        for u in usuarios:
            if u.nombre.lower() == nombre.lower():
                return u
        return None



#   MENÚ PRINCIPAL


def menu():
    while True:
        print("\n===== SISTEMA SEGURO DE USUARIOS =====")
        print("1. Registrar usuario")
        print("2. Mostrar todos los usuarios")
        print("3. Buscar usuario por nombre")
        print("4. Salir")

        op = input("Opción: ")

        if op == "1":
            nombre = input("Nombre de usuario: ")
            password = input("Contraseña: ")
            u = Usuario(nombre, password)
            GestorUsuarios.guardar(u)
            print("Usuario guardado correctamente.")

        elif op == "2":
            lista = GestorUsuarios.leer_todos()
            print("\n--- REGISTROS ---")
            for u in lista:
                print(f"Usuario: {u.nombre} | Contraseña: {u.password}")

        elif op == "3":
            nombre = input("Nombre a buscar: ")
            u = GestorUsuarios.buscar(nombre)
            if u:
                print(f"Encontrado → Usuario: {u.nombre} | Contraseña: {u.password}")
            else:
                print("No existe ese usuario.")

        elif op == "4":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")





menu()
