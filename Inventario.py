inventario = []
pedidos = []

# ---------- FUNCIONES DE INVENTARIO ----------

def registrar_producto():
    """Permite registrar un nuevo producto en el inventario con nombre, cantidad y precio."""
    nombre_producto = input("Ingresar el nombre del producto que se va a registrar: ")
    cantidad_producto = int(input("Ingresar la cantidad del producto: "))
    precio_producto = float(input("Ingresar el precio del producto: "))

    producto = { "nombre": nombre_producto, "cantidad": cantidad_producto, "precio": precio_producto}
    inventario.append(producto)
    print(f"El producto {nombre_producto} se registro de manera correcta.")

def mostrar_inventario():
    """Muestra todos los productos disponibles en el inventario con su cantidad y precio."""
    if inventario == []:
        print("No hay ningun producto registrado en el inventario ")
    else:
        print("\nInventario Del Sistema")
        for producto in inventario:
            print(f"{producto['nombre']} - Cantidad: {producto['cantidad']} - Precio: {producto['precio']}")

def actualizar_producto():
    """Permite modificar los datos de un producto existente (nombre, cantidad, precio)."""
    mostrar_inventario()
    if inventario:
        index = int(input("Ingrese el número del producto a actualizar: ")) - 1
        if 0 <= index < len(inventario):
            nuevo_nombre = input("Nuevo nombre (dejar vacío si no desea cambiar): ")
            nueva_cantidad = input("Nueva cantidad (dejar vacío si no desea cambiar): ")
            nuevo_precio = input("Nuevo precio (dejar vacío si no desea cambiar): ")

            if nuevo_nombre:
                inventario[index]["nombre"] = nuevo_nombre
            if nueva_cantidad:
                inventario[index]["cantidad"] = int(nueva_cantidad)
            if nuevo_precio:
                inventario[index]["precio"] = float(nuevo_precio)

            print("Producto actualizado correctamente.")
        else:
            print("Opción o campo inválido.")

def eliminar_producto():
    """Elimina un producto del inventario y lo elimina de la lista."""
    mostrar_inventario()
    if inventario:
        index = int(input("Ingrese el número del producto a eliminar (El primer prodcuto que se ingresa se le asigna el 1 y asi con los demas va aumentando): ")) - 1
        if 0 <= index < len(inventario):
            inventario.pop(index)
            print("El producto se elimino de manera correcta.")
        else:
            print("Opción inválida.")

# ---------- FUNCIONES DE PEDIDOS ----------

def registrar_pedido():
    """Permite crear un pedido con uno o varios productos, ajustando el inventario y calculando el total."""
    if inventario == []:
        print("No hay productos disponibles para generar pedidos.")
        return

    pedido = {"productos": [], "total": 0}

    while True:
        mostrar_inventario()
        try:
            producto_idx = int(input("Seleccione el número del producto para agregar al pedido (0 para terminar): ")) - 1
        except ValueError:
            print("Entrada inválida.")
            continue

        if producto_idx == -1:
            break
        if 0 <= producto_idx < len(inventario):
            try:
                cantidad = int(input("Ingrese la cantidad: "))
            except ValueError:
                print("Cantidad inválida.")
                continue

            if cantidad <= 0:
                print("Cantidad debe ser mayor a 0.")
                continue

            if cantidad > inventario[producto_idx]["cantidad"]:
                print("No hay suficiente stock disponible.")
                continue

            producto_seleccionado = {
                "nombre": inventario[producto_idx]["nombre"],
                "cantidad": cantidad,
                "total": cantidad * inventario[producto_idx]["precio"]
            }

            pedido["productos"].append(producto_seleccionado)
            pedido["total"] += producto_seleccionado["total"]
            inventario[producto_idx]["cantidad"] -= cantidad
            print(f"Producto '{producto_seleccionado['nombre']}' agregado al pedido.")
        else:
            print("Producto inválido.")

    if pedido["productos"]:
        pedidos.append(pedido)
        print(f"\nPedido registrado con {len(pedido['productos'])} productos. Total: ${pedido['total']:.2f}")
        mostrar_pedido(pedido)
    else:
        print("No se agregó ningún producto al pedido.")

def mostrar_pedidos():
    """Muestra todos los pedidos registrados con sus productos y total de cada uno."""
    if pedidos == []:
        print("No hay pedidos registrados.")
        return

    print("\nPedidos actuales:")
    for i, ped in enumerate(pedidos, start=1):
        print(f"\nPedido {i} - Total: ${ped['total']:.2f}")
        for prod in ped["productos"]:
            print(f"  - {prod['nombre']} x{prod['cantidad']} = ${prod['total']:.2f}")

def mostrar_pedido(pedido):
    """Muestra los detalles de un solo pedido, incluyendo productos, cantidades y total."""
    print("\nDetalle del pedido:")
    for prod in pedido["productos"]:
        print(f"  - {prod['nombre']} - Cantidad: {prod['cantidad']} = ${prod['total']:.2f}")
    print(f"Total del pedido: ${pedido['total']:.2f}")

def actualizar_pedido():
    """Permite modificar un pedido existente: cambiar cantidades de productos y agregar nuevos productos."""
    mostrar_pedidos()
    if pedidos:
        index = int(input("Ingrese el número del pedido a actualizar: ")) - 1
        if 0 <= index < len(pedidos):
            pedido = pedidos[index]
            print("\nPedido seleccionado:")
            mostrar_pedido(pedido)

            for i, prod in enumerate(pedido["productos"], start=1):
                print(f"\nProducto {i}: {prod['nombre']} - Cantidad actual: {prod['cantidad']} - Total: ${prod['total']:.2f}")
                nueva_cantidad = input("Nueva cantidad (dejar vacío para mantener la actual): ")
                if nueva_cantidad:
                    nueva_cantidad = int(nueva_cantidad)
                    if nueva_cantidad <= 0:
                        print("Cantidad inválida, se mantiene la original.")
                        continue
                    diferencia = nueva_cantidad - prod["cantidad"]
                    for item in inventario:
                        if item["nombre"] == prod["nombre"]:
                            if diferencia > item["cantidad"]:
                                print("No hay suficiente stock disponible, se mantiene la cantidad original.")
                                nueva_cantidad = prod["cantidad"]
                                diferencia = 0
                            item["cantidad"] -= diferencia
                            break
                    prod["cantidad"] = nueva_cantidad
                    prod["total"] = nueva_cantidad * next(item["precio"] for item in inventario if item["nombre"] == prod["nombre"])
            
            while True:
                agregar = input("\n¿Desea agregar un nuevo producto al pedido? (s/n): ").lower()
                if agregar == "s":
                    mostrar_inventario()
                    producto_idx = int(input("Seleccione el número del producto para agregar: ")) - 1
                    if 0 <= producto_idx < len(inventario):
                        cantidad = int(input("Ingrese la cantidad: "))
                        if cantidad <= 0 or cantidad > inventario[producto_idx]["cantidad"]:
                            print("Cantidad inválida o no disponible.")
                            continue
                        producto_seleccionado = {
                            "nombre": inventario[producto_idx]["nombre"],
                            "cantidad": cantidad,
                            "total": cantidad * inventario[producto_idx]["precio"]
                        }
                        pedido["productos"].append(producto_seleccionado)
                        inventario[producto_idx]["cantidad"] -= cantidad
                        print(f"Producto '{producto_seleccionado['nombre']}' agregado al pedido.")
                    else:
                        print("Producto inválido.")
                elif agregar == "n":
                    break
                else:
                    print("Opción inválida.")

            pedido["total"] = sum(p["total"] for p in pedido["productos"])
            print("\nPedido actualizado correctamente.")
            mostrar_pedido(pedido)
        else:
            print("Opción inválida.")

def eliminar_pedido():
    """Elimina un pedido existente y devuelve los productos al inventario."""
    mostrar_pedidos()
    if pedidos:
        index = int(input("Ingrese el número del pedido a eliminar: ")) - 1
        if 0 <= index < len(pedidos):
            for prod in pedidos[index]["productos"]:
                for item in inventario:
                    if item["nombre"] == prod["nombre"]:
                        item["cantidad"] += prod["cantidad"]
                        break
            pedidos.pop(index)
            print("Pedido eliminado con éxito.")
        else:
            print("Opción inválida.")

# ---------- MENÚ PRINCIPAL ----------

def main():
    """Menú principal del sistema, permite acceder a todas las funcionalidades de inventario y pedidos."""
    while True:
        print("\n========= MENÚ PRINCIPAL =========")
        print("1. Registrar producto")
        print("2. Mostrar inventario")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Registrar pedido")
        print("6. Mostrar pedidos")
        print("7. Actualizar pedido")
        print("8. Eliminar pedido")
        print("9. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            mostrar_inventario()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            registrar_pedido()
        elif opcion == "6":
            mostrar_pedidos()
        elif opcion == "7":
            actualizar_pedido()
        elif opcion == "8":
            eliminar_pedido()
        elif opcion == "9":
            print("Saliendo del sistema. Hasta luego.")
            break
        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    main()
