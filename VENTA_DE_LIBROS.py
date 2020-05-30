import os, json

def menu():
    os.system('cls')
    print("\t \t'MENU PRINCIPAL'") #\t sirve para darle espacion a alguna titulo de ser necesario
    print("****************************************************")
    print("*  1.   'COMPRAS.'                                 *")
    print("*  2.   'INVENTARIO.'                              *")
    print("*  3.   'INGRESO DE NUEVOS CLIENTES'               *")
    print("*  4.   'VENTAS'                                   *") 
    print("*  5.   'FACTURA'                                  *")     
    print("*  6.   'SALIR.'                                   *")    
    print("****************************************************")

    op=input("Ingresa una opcion:\n")
    while op!=7:
        if op=='1':
            nuevo_producto()
        elif op=='2':
            produc_exis()
        elif op=='3':
            nuevo_cliente()            
        elif op=='4':
            nueva_venta()
        elif op=='5':
            nueva_factura()            
        elif op=='6':
            salir() 
######################################################################################################################33                    
def nuevo_cliente():
    op='si'
    while op=='si':

        data = abrir_archivo('clientes.json')
        if not data:
            data = {}
            data['clientes'] = []

        id = input('Ingrese el nit del cliente: ')        
        nombre = input('Ingrese el nombre del cliente: ')
        direccion = input('Ingrese la dirección del cliente: ')

        data['clientes'].append({
            'id': id,
            'nombre': str(nombre),
            'direccion': str(direccion)
        })            
        
        guardar_archivo('clientes.json',data)
        
        op=input("desea agregar nuevos registros?..............  si/no:   ")
    return menu()
############################################################################################################################################
def nuevo_producto():
    op='si'
    while op=='si':

        data = abrir_archivo('productos.json')
        if not data:
            data = {}
            data['productos'] = []

        id = input('Ingrese nuevo codigo: ')        
        producto = input('Ingrese nuevo producto: ')
        cantidad = input('Ingrese las unidades adquiridas : ')
        precio = input('Ingrese el precio de costo: ')
        venta = input('Ingresa el precio venta: ')

        data['productos'].append({
            'id': id,
            'producto': str(producto),
            'cantidad': int(cantidad),
            'precio': float(precio),
            'venta': float(venta)
        })            
        
        guardar_archivo('productos.json',data)
        
        op=input("desea agregar nuevos registros?..............  si/no:   ")
    return menu()
##########################################################################################################################################
def produc_exis():
    data = abrir_archivo('productos.json')
    if data:
        if data['productos']:
            for d in data['productos']:
                print("Codigo:",d['id'])
                print("Nombre:", d['producto'])
                print("Existencia:",d['cantidad'])
                print("Precio compra:",d['precio'])
                print("precio Venta:",d['venta'])
        else:
            print('No hay productos registrados.')
            
    else:
        print('El archivo no existe o se encuentra vacio.') 

    pause = input('Presione ENTER para continuar...')
    return menu()
######################################################################################################################################### 
def abrir_archivo(archivo):
    if os.path.isfile(archivo) and os.stat(archivo).st_size > 0:
        with open (archivo) as file:
            data = json.load(file)
            file.close()
        return data
    else:
        return

def guardar_archivo(archivo, data):
    if data:
        file = open(archivo, 'w')
        json.dump(data, file)
        file.close()
##############################################################################################################################################
def nueva_venta():

    ventas = abrir_archivo('ventas.json') #abrimos el archivo ventas desde la funcion que hemos creado para abrir archivos
    if not ventas: #si no existe el diccionario para almacenar la info lo creamos.
        ventas = {}
        ventas['ventas'] = []

    venta = '' #el no. de la venta es obligatorio asi que creamos un cliclo con while y una variable que lo controla
    while not venta: #siempre y cuando la variable se encuentre vacía el ciclo se seguira ejecutando
        venta = input('Ingrese el no. de venta: ')
        if venta: #comprobamos que se haya ingresado algo
            for v in ventas['ventas']: #recorremos las ventas actuales para verificar el no. de venta
                if venta == v['venta_id']: #evaluamos si el no. de venta ya existe
                    print('El no. de venta ya esta en uso, por favor use otro no. ...')
                    venta = '' #dejamos la variable en blanco para que el ciclo while siga corriendo hasta que se ingrese un no. valido.

    #Obtenemos la información del cliente y guardamos el id en un variable
    cliente = input('Ingrese el codigo/Nit del cliente: ')
    if cliente:
        clientes = abrir_archivo('clientes.json')
        if clientes['clientes']:
            for c in clientes['clientes']:
                if cliente == c['id']:
                    print(c['id'])
                    print(c['nombre'])
                    break #terminamos el ciclo pues ya tenemos la info que necesitabamos
        else:
            print('No hay clientes registrados.')

    #buscamos los productos desde inventario para la venta actual, creamos un ciclo hasta que el usuario lo termine
    op='si'
    total = 0 #guardamos el total de la venta
    productos_venta = [] #este arreglo nos servira para almacenar los codigos de los productos de la venta actual
    while op=='si':
        producto = input('Ingrese el codigo del producto: ')
        if producto: #comprobamos si se ingreso el codigo del producto
            productos = abrir_archivo('productos.json') #abrimos el archivo productos
            if productos['productos']: #comprobamos si existen productos guardados en inventario
                for p in productos['productos']: #recoremos los productos para encontrar el requerido
                    if producto == p['id']: #comprobamos si existe el codigo ingresado
                        print(p['id']) #imprimimos el codigo para que el usuario pueda verlo
                        print(p['producto']) #imprimimos el nombre del producto
                        cantidad = input('Por favor ingrese la cantidad : ') #solicitamos ingrese la cantidad de la venta del producto solicitado
                        if cantidad: #comprobamos si se ingreso una cantidad                            
                            productos_venta.append({ #creamos un diccionario para cada producto de la venta dentro de nuestro arreglo de ventas
                                'producto_id': producto,
                                'producto_nombre' : p['producto'],
                                'cantidad' : cantidad,
                                'precio' : p['precio'],
                                'subtotal' : int(cantidad) * float(p['precio'])
                            })
                            total = total + int(cantidad) * float(p['precio'])
                            break #terminamos el ciclo pues ya tenemos la info que necesitabamos
            else:
                print('Producto no encontrado.')            
        op = input("¿Desea agregar otro producto a la venta?..............  si/no: ")

    ventas['ventas'].append({ #creamos nuestro arreglo y diccionarios finales antes de guardar nuestra venta el archivo ventas.json
        'venta_id': venta, #guardamos el no. de venta
        'cliente_id': cliente, # el nit o id del cliente
        'cliente_nombre': str(c['nombre']), #el nombre del cliente
        'productos_venta': productos_venta, #los productos de la venta estos van en una lista nueva
        'total' : float(total), #guardamos el total de la venta
        'estado' : 'no facturado' #el estado de la venta -'no facturado' al momento de facturarlo pasa a ser 'facturado' para que no se cobre 2 veces 
    })      
    #Creamos un resumen de la venta
    print("****************************************************")
    print('VENTA NO: ' + str(venta) + ' CLIENTE: ' + str(c['nombre'])) 
    print("****************************************************")
    print('PRODUCTOS ')
    for i in productos_venta: #recorremos el arreglo de los productos que se agregaron a esta venta
        print("código:" , str(i['producto_id']))
        print("Libro vendido:", str(p['producto']))
        print("Cantidad vendida: ", str(i['cantidad']))
        print("Precio: ", str(i['precio']))
        print("Sub Total: ", str(i['subtotal'])) #imprimimos         
    print("****************************************************")
    print('TOTAL: ' + str(total))
    print("****************************************************")
    verifique = input('Por favor verifique los datos de la venta, ¿es correto?.... si/no: ') #le pedimos al usuario que verifique la venta antes de guardar

    if verifique == 'si':
        guardar_archivo('ventas.json',ventas) #guardamos la info usando nuestra funcion guardar.

        #DESCARGAREMOS LOS PRODUCTOS DEL INVENTARIO
        for i in productos_venta: #recorremos el arreglo de los productos que se agregaron a esta venta
            for p in productos['productos']: #recoremos los productos para encontrar el requerido
                if i['producto_id'] == p['id']: #comprobamos si los productos coinciden
                    p.update({'cantidad': int(p['cantidad']) - int(i['cantidad'])}) #actualizamos el diccionario de inventario
                    break #terminamos el ciclo actual

        guardar_archivo('productos.json',productos) #guardamos la info usando nuestra funcion guardar.
    else:
        print('La venta no fue guardada, puede iniciar de nuevo el proceso...')
    return menu()

def nueva_factura():
    ventas = abrir_archivo('ventas.json')
    if ventas:
        for v in ventas['ventas']:
            if v['estado'] == 'no facturado':
                print('No.:' + str(v['venta_id']) + ' - Cliente: ' + str(v['cliente_nombre']) + ' - Total: '+ str(v['total'])) #imprimimos

        factura = '' #el no. de la factura es obligatorio asi que creamos un cliclo con while y una variable que lo controla
        venta_valida = '' #en esta variable almacenamos posteriormente si la venta es valida para ser procesada
        while not factura: #siempre y cuando la variable se encuentre vacía el ciclo se seguira ejecutando
            factura = input('Ingrese el no. de venta a facturar: ')
            if factura: #comprobamos que se haya ingresado algo
                for v in ventas['ventas']: #recorremos las ventas actuales para verificar el no. de venta
                    if factura == v['venta_id']: #evaluamos si el no. de venta existe
                        print("****************************************************")
                        print('VENTA NO: ' + str(v['venta_id']) + ' CLIENTE: ' + str(v['cliente_nombre'])) 
                        print("****************************************************")
                        print('PRODUCTOS ')
                        for i in v['productos_venta']: #recorremos el arreglo de los productos que se agregaron a esta venta
                            print(str(i['producto_id']) + ' '+ str(i['producto_nombre']) + ' ' + str(i['cantidad']) + ' ' + str(i['precio'])+ ' ' + str(i['subtotal'])) #imprimimos                                     
                        print("****************************************************")
                        print('TOTAL: ' + str(v['total']))
                        print("****************************************************")
                        venta_valida = 'valida'
                        break #finalizamos el cliclo actual pues ya tenemos la info
                if venta_valida == 'valida': #verificamos si la venta ingresada era valida
                    pago = input('Por favor ingrese el monto a cancelar: ')
                else:
                    print('La venta no es válida por favor revise el no. ingresado.')
                    factura = ''

    return menu()

def nuevo_producto():
    op='si'
    while op=='si':

        data = abrir_archivo('productos.json')
        if not data:
            data = {}
            data['productos'] = []

        id = input('Ingrese nuevo codigo: ')        
        producto = input('Ingrese nuevo producto: ')
        cantidad = input('Ingrese las unidades adquiridas : ')
        precio = input('Ingrese el precio de costo: ')
        venta = input('Ingresa el precio venta: ')

        data['productos'].append({
            'id': id,
            'producto': str(producto),
            'cantidad': int(cantidad),
            'precio': float(precio),
            'venta': float(venta)
        })            
        
        guardar_archivo('productos.json',data)
        
        op=input("desea agregar nuevos registros?..............  si/no:   ")
    return menu()

def nuevo_cliente():
    op='si'
    while op=='si':

        data = abrir_archivo('clientes.json')
        if not data:
            data = {}
            data['clientes'] = []

        id = input('Ingrese el nit del cliente: ')        
        nombre = input('Ingrese el nombre del cliente: ')
        direccion = input('Ingrese la dirección del cliente: ')

        data['clientes'].append({
            'id': id,
            'nombre': str(nombre),
            'direccion': str(direccion)
        })            
        
        guardar_archivo('clientes.json',data)
        
        op=input("desea agregar nuevos registros?..............  si/no:   ")
    return menu()

def produc_exis():
    data = abrir_archivo('productos.json')
    if data:
        if data['productos']:
            for d in data['productos']:
                print("Codigo:",d['id'])
                print("Nombre:", d['producto'])
                print("Existencia:",d['cantidad'])
                print("Precio compra:",d['precio'])
                print("precio Venta:",d['venta'])
        else:
            print('No hay productos registrados.')
            
    else:
        print('El archivo no existe o se encuentra vacio.') 

    pause = input('Presione ENTER para continuar...')
    return menu()

def salir():
    print("Gracias por utilizar nuestros servicios.")
    exit()

"""menu"""
menu()
nuevo_producto()
nuevo_cliente()
produc_exis()
nueva_venta()
nueva_factura()
abrir_archivo()
guardar_archivo()
salir()   
