from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient,VipClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce
path = "path/to/your/files"
path, _ = os.path.split(os.path.abspath(__file__))

# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    
    def validar_dni_ecuador(self, dni):
        if len(dni) != 10 or not dni.isdigit():
            return False

        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        total = sum(int(digit) * coef for digit, coef in zip(dni[:-1], coeficientes))
        verificador = (total % 10) if total % 10 == 0 else 10 - (total % 10)
        return verificador == int(dni[-1])

    def create(self):
        borrarPantalla()
        print('\033c', end='')
        print(green_color+"*"*90+reset_color)
        print(blue_color+"Registro de Cliente")
        print(blue_color+Company.get_business_name())
        print(purple_color+"Seleccione el tipo de cliente:")
        print("1) Cliente Regular")
        print("2) Cliente VIP")
        tipo_cliente = input("Seleccione una opción: ")
        
        if tipo_cliente == "1":
            print("Cliente Regular")
            nombre = input("Ingrese el nombre del cliente: ")
            apellido = input("Ingrese el apellido del cliente: ")
            dni = input("Ingrese el DNI del cliente: ")

            if not self.validar_dni_ecuador(dni):
                print("DNI inválido para Ecuador.")
                time.sleep(2)
                return

            card = input("¿El cliente tiene tarjeta de descuento? (s/n): ").lower() == "s"
            new_client = RegularClient(nombre, apellido, dni, card)
        elif tipo_cliente == "2":
            print("Cliente VIP")
            nombre = input("Ingrese el nombre del cliente: ")
            apellido = input("Ingrese el apellido del cliente: ")
            dni = input("Ingrese el DNI del cliente: ")

            if not self.validar_dni_ecuador(dni):
                print("DNI inválido para Ecuador.")
                time.sleep(2)
                return

            new_client = VipClient(nombre, apellido, dni)
        else:
            print("Opción inválida")
            return
        
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.read()
        clients.append(new_client.getJson())
        json_file.save(clients)
        print("Cliente registrado exitosamente!")
        time.sleep(2)

    def update(self):
        borrarPantalla()
        print('\033c', end='')
        print(green_color + "*" * 90 + reset_color)
        print(blue_color + "Actualización de Cliente")
        print(blue_color + Company.get_business_name())
        dni = input("Ingrese el DNI del cliente que desea actualizar: ")
        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()

        found = False
        updated_clients = []
        for client in clients:
            if client['dni'] == dni:
                found = True
                print("Cliente encontrado:")
                print(f"Nombre: {client['nombre']}")
                print(f"Apellido: {client['apellido']}")
                print(f"DNI: {client['dni']}")
                print()
                new_nombre = input("Ingrese el nuevo nombre del cliente (deje en blanco para mantener el mismo): ")
                new_apellido = input("Ingrese el nuevo apellido del cliente (deje en blanco para mantener el mismo): ")
                if new_nombre:
                    client['nombre'] = new_nombre
                if new_apellido:
                    client['apellido'] = new_apellido
            updated_clients.append(client)

        if found:
            json_file.save(updated_clients)
            print("Cliente actualizado exitosamente!")
        else:
            print("Cliente no encontrado.")
        time.sleep(2)

    def delete(self):
        borrarPantalla()
        print('\033c', end='')
        print(green_color+"*"*90+reset_color)
        print(blue_color+"Eliminación de Cliente")
        print(blue_color+Company.get_business_name())
        dni = input("Ingrese el DNI del cliente que desea eliminar: ")
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.read()
        
        filtered_clients = [client for client in clients if client['dni'] != dni]
        
        if len(filtered_clients) < len(clients):
            json_file.save(filtered_clients)
            print("Cliente eliminado exitosamente!")
        else:
            print("Cliente no encontrado.")
        time.sleep(2)

    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Cliente"+" "*35+"██")
        gotoxy(2,4);dni = input("Ingrese DNI del cliente: ")
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.find("dni", dni)
        
        if clients:
            client = clients[0]
            print(f"Nombre: {client['nombre']}")
            print(f"Apellido: {client['apellido']}")
            print(f"DNI: {client['dni']}")
        else:
            print("Cliente no encontrado.")
        input("Presione una tecla para continuar...")   

class CrudProducts(ICrud):
    
    def create(self):
        # Función para crear un nuevo producto
        borrarPantalla()
        print('\033c', end='')
        print(green_color+"*"*90+reset_color)
        print(blue_color+"Registro de Producto")
        print(purple_color+"Ingrese los datos del nuevo producto:")
        id = input("ID del producto: ")
        descrip = input("Descripción del producto: ")
        preci = input("Precio del producto: ")
        stock = input("Stock del producto: ")

        # Validar que se ingresen valores numéricos para precio y stock
        try:
            preci = float(preci)
            stock = int(stock)
        except ValueError:
            print(red_color+"Error: El precio y el stock deben ser valores numéricos."+reset_color)
            time.sleep(2)
            return
        # Crear el nuevo producto
        new_product = Product(id, descrip, preci, stock)
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        products.append(new_product.getJson())
        json_file.save(products)
        print("Producto registrado exitosamente!")
        time.sleep(2)
    
    def update(self):
        # Función para actualizar un producto existente
        borrarPantalla()
        print('\033c', end='')
        print(green_color + "*" * 90 + reset_color)
        print(blue_color + "Actualización de Producto")
        print(purple_color + "Ingrese el ID del producto que desea actualizar:")
        id = input("ID del producto: ")
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        # Buscar el producto por su ID
        found = False
        updated_products = []
        for product in products:
            if product['id'] == id:
                found = True
                # Si se encuentra el producto, mostrar los datos para modificarlos
                print("Producto encontrado:")
                print(f"Descripción: {product['descripcion']}")
                print(f"Precio: {product['precio']}")

                print(f"Stock: {product['stock']}")
                print()
                # Solicitar nueva información para el producto
                new_descrip = input("Ingrese la nueva descripción del producto (deje en blanco para mantener el mismo): ")
                new_preci = input("Ingrese el nuevo precio del producto (deje en blanco para mantener el mismo): ")
                new_stock = input("Ingrese el nuevo stock del producto (deje en blanco para mantener el mismo): ")
                # Actualizar la información si se proporcionó
                if new_descrip:
                    product['descrip'] = new_descrip
                if new_preci:
                    product['preci'] = float(new_preci)
                if new_stock:
                    product['stock'] = int(new_stock)
            updated_products.append(product)
        if found:
            # Guardar los cambios en el archivo JSON
            json_file.save(updated_products)
            print("Producto actualizado exitosamente!")
        else:
            print("Producto no encontrado.")
        time.sleep(2)

    def delete(self):
        # Función para eliminar un producto existente
        borrarPantalla()
        print('\033c', end='')
        print(green_color+"*"*90+reset_color)
        print(blue_color+"Eliminación de Producto")
        print(purple_color+"Ingrese el ID del producto que desea eliminar (deje en blanco para mostrar todos los productos):")
        id = input("ID del producto: ")
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        
        if not id:
            # Si no se proporciona un ID, mostrar todos los productos
            print("Listado de Productos:")
            print("{:<5} {:<20} {:<10} {:<10}".format("ID", "Descripción", "Precio", "Stock"))
            for product in products:
                print("{:<5} {:<20} {:<10} {:<10}".format(product['id'], product['descrip'], product['preci'], product['stock']))
        else:
            # Eliminar el producto con el ID proporcionado
            filtered_products = [product for product in products if product['id'] != id]
            if len(filtered_products) < len(products):
                json_file.save(filtered_products)
                print("Producto eliminado exitosamente!")
            else:
                print("Producto no encontrado.")
        time.sleep(2)

    def consult(self):
        # Función para consultar un producto por su ID o mostrar todos los productos
        borrarPantalla()
        print('\033c', end='')
        print(green_color + "*" * 90 + reset_color)
        print(blue_color + "Consulta de Producto")
        print(purple_color + "Ingrese el ID del producto que desea consultar (deje en blanco para mostrar todos los productos):")
        id = input("ID del producto: ")
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        if not id:
            # Mostrar todos los productos si no se proporciona un ID
            print("Listado de Productos:")
            print("{:<5} {:<20} {:<10} {:<10}".format("ID", "Descripción", "Precio", "Stock"))
            for product in products:
                print("{:<5} {:<20} {:<10} {:<10}".format(product.get('id', ''), product.get('descripcion', 'Descripción no disponible'), product.get('precio', ''), product.get('stock', '')))
        else:
            # Mostrar el producto con el ID proporcionado
            found_product = next((product for product in products if product.get('id') == id), None)
            if found_product:
                print("{:<5} {:<20} {:<10} {:<10}".format("ID", "Descripción", "Precio", "Stock"))
                print("{:<5} {:<20} {:<10} {:<10}".format(found_product.get('id', ''), found_product.get('descripcion', 'Descripción no disponible'), found_product.get('precio', ''), found_product.get('stock', '')))
            else:
                print("Producto no encontrado.")
        time.sleep(3)



class CrudSales(ICrud):
    
    def create(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line);
            id=str(validar.solo_numeros("Error: Solo numeros",15,9+line))  # Convertir el ID a string
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip.ljust(20))  # Alinear y limitar a 20 caracteres
                gotoxy(38,9+line);print(str(product.preci).ljust(10))  # Alinear y limitar a 10 caracteres
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(str(product.preci*qyt).ljust(10))  # Alinear y limitar a 10 caracteres
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            if invoices:
                ult_invoices = invoices[-1]["factura"]+1
            else:
                ult_invoices = 1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)


    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        gotoxy(2,4);invoice_number = input("Ingrese Factura (deje en blanco para mostrar todas): ")
        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices = json_file.read()
        
        if invoice_number:
            # Consultar una factura específica
            try:
                invoice_number = int(invoice_number)
                invoice = next((invoice for invoice in invoices if invoice.get('factura') == invoice_number), None)
                if invoice:
                    print("Factura    Fecha      Cliente         Subtotal   Descuento  IVA        Total")
                    print("{:<10} {:<10} {:<15} {:<10.2f} {:<10.2f} {:<10.2f} {:<10.2f}".format(invoice.get('factura', ''), invoice.get('Fecha', ''), invoice.get('cliente', ''), invoice.get('subtotal', 0), invoice.get('descuento', 0), invoice.get('iva', 0), invoice.get('total', 0)))
                    print("Detalles de la factura:")
                    for detalle in invoice.get('detalle', []):
                        print(f"   - Producto: {detalle.get('poducto')}, Precio: {detalle.get('precio'):.2f}, Cantidad: {detalle.get('cantidad')}, Subtotal: {detalle.get('precio') * detalle.get('cantidad'):.2f}")
                else:
                    print("Factura no encontrada.")
            except ValueError:
                print("Error: Por favor ingrese un número válido de factura.")
        else:
            # Mostrar todas las facturas
            print("Consulta de Facturas")
            print("{:<10} {:<10} {:<15} {:<10} {:<10} {:<10} {:<10}".format("Factura", "Fecha", "Cliente", "Subtotal", "Descuento", "IVA", "Total"))
            for fac in invoices:
                print("{:<10} {:<10} {:<15} {:<10.2f} {:<10.2f} {:<10.2f} {:<10.2f}".format(fac.get('factura', ''), fac.get('Fecha', ''), fac.get('cliente', ''), fac.get('subtotal', 0), fac.get('descuento', 0), fac.get('iva', 0), fac.get('total', 0)))
            
            suma = reduce(lambda total, invoice: round(total+ float(invoice.get('total', 0)),2), invoices,0)
            totales_map = list(map(lambda invoice: float(invoice.get('total', 0)), invoices))
            total_client = list(filter(lambda invoice: invoice.get('cliente') == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice:.2f}")
            print(f"              min Factura:{min_invoice:.2f}")
            print(f"              sum Factura:{tot_invoices:.2f}")
            print(f"              reduce Facturas:{suma:.2f}")
        x=input("presione una tecla para continuar...")


    def update(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Actualizar Factura"+" "*35+"██")
        invoice_number = input("Ingrese Factura a actualizar: ")

        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices = json_file.find("factura", int(invoice_number))
        if not invoices:
            print(f"Factura {invoice_number} no encontrada.")
            x = input("presione una tecla para continuar...")
            return

        invoice = invoices[0]
        print(f"Factura encontrada: {invoice['factura']}, Cliente: {invoice['cliente']}, Total: {invoice['total']}")

        while True:
            print("\n1. Eliminar producto")
            print("2. Agregar producto")
            print("3. Modificar cantidad de producto")
            print("4. Volver al menú principal")
            option = input("Seleccione una opción: ")

            if option == "1":
                # Eliminar producto
                product_index = input("Ingrese el número de producto a eliminar: ")
                try:
                    product_index = int(product_index)
                    if product_index > 0 and product_index <= len(invoice['detalle']):
                        deleted_product = invoice['detalle'].pop(product_index - 1)
                        print(f"Producto eliminado: {deleted_product.get('producto')}")

                        # Actualizar el total de la factura
                        invoice['total'] -= deleted_product['precio'] * deleted_product['cantidad']
                    else:
                        print("Índice de producto no válido.")
                except ValueError:
                    print("Error: Por favor ingrese un número válido de producto.")

            elif option == "2":
                # Agregar producto
                id_producto = input("Ingrese el ID del producto a agregar: ")
                cantidad = input("Ingrese la cantidad del producto a agregar: ")
                try:
                    id_producto = int(id_producto)
                    cantidad = int(cantidad)

                    # Buscar el producto en la lista de productos
                    json_file = JsonFile(path+'/archivos/products.json')
                    products = json_file.read()
                    product = next((product for product in products if product.get('id') == id_producto), None)

                    if product:
                        subtotal = product['precio'] * cantidad
                        new_product = {'producto': product['descripcion'], 'precio': product['precio'], 'cantidad': cantidad, 'subtotal': subtotal}
                        invoice['detalle'].append(new_product)
                        invoice['total'] += subtotal
                        print(f"Producto agregado: {new_product.get('producto')}, Cantidad: {new_product.get('cantidad')}, Subtotal: {new_product.get('subtotal')}")
                    else:
                        print("Producto no encontrado.")
                except ValueError:
                    print("Error: Por favor ingrese valores numéricos válidos.")

            elif option == "3":
                # Modificar cantidad de producto
                product_index = input("Ingrese el número de producto a modificar: ")
                new_quantity = input("Ingrese la nueva cantidad del producto: ")
                try:
                    product_index = int(product_index)
                    new_quantity = int(new_quantity)

                    if product_index > 0 and product_index <= len(invoice['detalle']):
                        product = invoice['detalle'][product_index - 1]
                        old_quantity = product['cantidad']
                        product['cantidad'] = new_quantity
                        product['subtotal'] = product['precio'] * new_quantity

                        # Actualizar el total de la factura
                        invoice['total'] += (new_quantity - old_quantity) * product['precio']
                    else:
                        print("Índice de producto no válido.")
                except ValueError:
                    print("Error: Por favor ingrese valores numéricos válidos.")

            elif option == "4":
                break  # Volver al menú principal

        json_file.save(invoices)
        print("\nFactura actualizada correctamente.")
        x = input("presione una tecla para continuar...")


    def delete(self):
        # Implementa la lógica para eliminar una factura
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*37+"Eliminar Factura"+" "*37+"██")
        invoice_number = input("Ingrese Factura a eliminar: ")

        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices = json_file.find("factura", int(invoice_number))
        if not invoices:
            print(f"Factura {invoice_number} no encontrada.")
            x = input("presione una tecla para continuar...")
            return

        invoice = invoices[0]
        print(f"Factura encontrada: {invoice['factura']}, Cliente: {invoice['cliente']}, Total: {invoice['total']}")
        
        confirmacion = input("¿Está seguro de eliminar la factura? (s/n): ")
        if confirmacion.lower() == "s":
            invoices.remove(invoice)
            json_file.save(invoices)
            print("\nFactura eliminada correctamente.")
        else:
            print("\nEliminación de factura cancelada.")

        x = input("presione una tecla para continuar...")


# Menu Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()    
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                crud_clients = CrudClients()
                crud_clients.create()
            elif opc1 == "2":
                crud_clients = CrudClients()
                crud_clients.update()
            elif opc1 == "3":
                crud_clients = CrudClients()
                crud_clients.delete()
            elif opc1 == "4":
                crud_clients = CrudClients()
                crud_clients.consult()
            print("Regresando al menu Clientes...")
            time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()    
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                crud_products = CrudProducts()
                crud_products.create()
            elif opc2 == "2":
                crud_products = CrudProducts()
                crud_products.update()
            elif opc2 == "3":
                crud_products = CrudProducts()
                crud_products.delete()
            elif opc2 == "4":
                crud_products = CrudProducts()
                crud_products.consult()
            print("Regresando al menu Productos...")
            time.sleep(2)            
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                crud_sales = CrudSales()
                crud_sales.create()
            elif opc3 == "2":
                crud_sales = CrudSales()
                crud_sales.consult()
            elif opc3 == "3":
                crud_sales = CrudSales()
                crud_sales.update()
            elif opc3 == "4":
                crud_sales = CrudSales()
                crud_sales.delete()
            print("Regresando al menu Ventas...")
            time.sleep(2)            
    print("Regresando al menu Principal...")
    time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()
