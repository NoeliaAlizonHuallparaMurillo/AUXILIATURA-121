class Persona:
    def __init__(self, nombre, apellido_paterno, apellido_materno, c1):
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.c1 = c1
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

class Niño(Persona):
    def __init__(self, nombre, apellido_paterno, apellido_materno, c1, edad, peso, talla):
        super().__init__(nombre, apellido_paterno, apellido_materno, c1)
        self.edad = edad
        self.peso = peso  # en kg
        self.talla = talla  # en cm
    
    def mostrar(self):
        print(f"Carnet: {self.c1}")
        print(f"Nombre: {self.nombre} {self.apellido_paterno} {self.apellido_materno}")
        print(f"Edad: {self.edad} años")
        print(f"Peso: {self.peso} kg")
        print(f"Talla: {self.talla} cm")
        print("-" * 30)
    
    def peso_adecuado(self):
        """Determina si el peso es adecuado según edad y talla"""
       
        if self.edad <= 2:
            peso_ideal = 10 + (self.edad * 2.5)
        elif self.edad <= 5:
            peso_ideal = 15 + (self.edad - 2) * 2
        elif self.edad <= 10:
            peso_ideal = 23 + (self.edad - 5) * 2.5
        else:
            peso_ideal = 35 + (self.edad - 10) * 3
        
        # Ajuste por talla
        talla_ideal = 75 + (self.edad * 6)  # Talla promedio por edad
        
        # Margen del 15% para considerar adecuado
        peso_min = peso_ideal * 0.85
        peso_max = peso_ideal * 1.15
        
        return peso_min <= self.peso <= peso_max
    
    def talla_adecuada(self):
        """Determina si la talla es adecuada según la edad"""
        talla_ideal = 75 + (self.edad * 6)
        # Margen del 10% para considerar adecuado
        talla_min = talla_ideal * 0.9
        talla_max = talla_ideal * 1.1
        
        return talla_min <= self.talla <= talla_max

class SistemaNiños:
    def __init__(self):
        self.niños = []
    
    # a) CRUD operations
    def crear_niño(self):
        print("\n--- CREAR NUEVO NIÑO ---")
        c1 = int(input("Carnet (c1): "))
        
        # Verificar si ya existe
        for niño in self.niños:
            if niño.c1 == c1:
                print("¡Error! Ya existe un niño con ese carnet.")
                return
        
        nombre = input("Nombre: ")
        apellido_paterno = input("Apellido Paterno: ")
        apellido_materno = input("Apellido Materno: ")
        edad = int(input("Edad (años): "))
        peso = float(input("Peso (kg): "))
        talla = float(input("Talla (cm): "))
        
        nuevo_niño = Niño(nombre, apellido_paterno, apellido_materno, c1, edad, peso, talla)
        self.niños.append(nuevo_niño)
        print("¡Niño creado exitosamente!")
    
    def leer_niño(self, c1):
        for niño in self.niños:
            if niño.c1 == c1:
                return niño
        return None
    
    def listar_niños(self):
        if not self.niños:
            print("\nNo hay niños registrados.")
            return
        
        print("\n--- LISTA DE NIÑOS ---")
        for i, niño in enumerate(self.niños, 1):
            print(f"{i}. Carnet {niño.c1}: {niño.nombre} {niño.apellido_paterno}")
    
    def mostrar_niño(self, c1):
        niño = self.leer_niño(c1)
        if niño:
            print("\n--- INFORMACIÓN DEL NIÑO ---")
            niño.mostrar()
        else:
            print("No se encontró un niño con ese carnet.")
    
    def mostrar_todos(self):
        if not self.niños:
            print("\nNo hay niños registrados.")
            return
        
        print("\n--- INFORMACIÓN DE TODOS LOS NIÑOS ---")
        for niño in self.niños:
            niño.mostrar()
    
    # b) Niños con peso adecuado
    def contar_peso_adecuado(self):
        count = 0
        print("\n--- NIÑOS CON PESO ADECUADO ---")
        for niño in self.niños:
            if niño.peso_adecuado():
                count += 1
                print(f"- {niño.nombre} {niño.apellido_paterno}: {niño.peso} kg (Adecuado)")
            else:
                print(f"- {niño.nombre} {niño.apellido_paterno}: {niño.peso} kg (No adecuado)")
        
        print(f"\nTotal de niños con peso adecuado: {count}")
        return count
    
    # c) Niños con problemas de peso o talla
    def niños_con_problemas(self):
        print("\n--- NIÑOS CON PESO O TALLA INADECUADA ---")
        problemas = []
        
        for niño in self.niños:
            peso_ok = niño.peso_adecuado()
            talla_ok = niño.talla_adecuada()
            
            if not peso_ok or not talla_ok:
                problemas.append(niño)
                print(f"- {niño.nombre} {niño.apellido_paterno} ({niño.edad} años):")
                if not peso_ok:
                    print(f"  Peso inadecuado: {niño.peso} kg")
                if not talla_ok:
                    print(f"  Talla inadecuada: {niño.talla} cm")
                print()
        
        if not problemas:
            print("Todos los niños tienen peso y talla adecuados.")
        
        return problemas
    
    # d) Promedio de edad
    def promedio_edad(self):
        if not self.niños:
            return 0
        
        total_edad = sum(niño.edad for niño in self.niños)
        promedio = total_edad / len(self.niños)
        
        print(f"\n--- PROMEDIO DE EDAD ---")
        print(f"Total niños: {len(self.niños)}")
        print(f"Suma de edades: {total_edad} años")
        print(f"Promedio de edad: {promedio:.2f} años")
        
        return promedio
    
    # e) Buscar niño por carnet
    def buscar_por_carnet(self, c1):
        niño = self.leer_niño(c1)
        if niño:
            print(f"\n--- NIÑO ENCONTRADO CON CARNET {c1} ---")
            niño.mostrar()
            return niño
        else:
            print(f"No se encontró ningún niño con carnet {c1}")
            return None
    
    # f) Niños con la talla más alta
    def niños_talla_mas_alta(self):
        if not self.niños:
            print("\nNo hay niños registrados.")
            return []
        
        # Encontrar la talla máxima
        max_talla = max(niño.talla for niño in self.niños)
        
        # Encontrar todos los niños con esa talla
        mas_altos = [niño for niño in self.niños if niño.talla == max_talla]
        
        print(f"\n--- NIÑOS CON LA TALLA MÁS ALTA ({max_talla} cm) ---")
        for niño in mas_altos:
            print(f"- {niño.nombre} {niño.apellido_paterno}: {niño.edad} años, {niño.peso} kg")
        
        return mas_altos

def menu():
    sistema = SistemaNiños()
    
    
    # Agregamos algunos niños de ejemplo
    sistema.niños.append(Niño("Jose", "Pérez", "Gómez", 101, 5, 18.5, 110))
    sistema.niños.append(Niño("María", "López", "Santos", 102, 7, 25.0, 125))
    sistema.niños.append(Niño("Ronald", "García", "Ruiz", 103, 3, 14.0, 95))
    sistema.niños.append(Niño("Anahi", "Martínez", "Díaz", 104, 8, 28.0, 130))
    sistema.niños.append(Niño("Pablo", "Hernández", "Vega", 105, 6, 22.0, 115))
    
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE REGISTRO DE NIÑOS")
        print("="*50)
        print("a) Crear, leer, listar y mostrar")
        print("b) Niños con peso adecuado")
        print("c) Niños con problemas de peso/talla")
        print("d) Promedio de edad")
        print("e) Buscar niño por carnet")
        print("f) Niños con talla más alta")
        print("g) Mostrar todos los niños")
        print("h) Salir")
        print("="*50)
        
        opcion = input("Seleccione una opción: ").lower()
        
        if opcion == 'a':
            print("\nSubopciones:")
            print("1. Crear niño")
            print("2. Listar niños")
            print("3. Mostrar niño específico")
            subop = input("Seleccione: ")
            
            if subop == '1':
                sistema.crear_niño()
            elif subop == '2':
                sistema.listar_niños()
            elif subop == '3':
                c1 = int(input("Ingrese carnet del niño: "))
                sistema.mostrar_niño(c1)
        
        elif opcion == 'b':
            sistema.contar_peso_adecuado()
        
        elif opcion == 'c':
            sistema.niños_con_problemas()
        
        elif opcion == 'd':
            sistema.promedio_edad()
        
        elif opcion == 'e':
            c1 = int(input("Ingrese el carnet a buscar: "))
            sistema.buscar_por_carnet(c1)
        
        elif opcion == 'f':
            sistema.niños_talla_mas_alta()
        
        elif opcion == 'g':
            sistema.mostrar_todos()
        
        elif opcion == 'h':
            print("\n¡Gracias por usar el sistema!")
            break
        
        else:
            print("\nOpción no válida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")

# main
if __name__ == "__main__":
    menu()