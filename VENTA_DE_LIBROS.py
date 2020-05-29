import os, json

def menu():
    os.system('cls')
    print("\t \t'MENU PRINCIPAL'") #\t sirve para darle espacion a alguna titulo de ser necesario
    print("****************************************************")
    print("*  1.   'COMPRAS.'                                 *")
    print("*  2.   'INVENTARIO.'                              *")
    print("*  3.   'INGRESO DE NUEVOS CLIENTES'               *")
    print("*  4.   'VENTAS-FACTURACION'                       *") 
    print("*  5.   'SALIR.'                                   *")    
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
            salir() 

def nuevo_cliente():
    print("BIENVENIDO AL MODULO CLIENTE \n")
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
    #######################################################################################

def nuevo_producto():#Compras 
    op='si'
    print("BIENVENIDO AL MODULO COMPRAS\n")
    while op=='si':

        data = abrir_archivo('productos.json')
        if not data:
            data = {}
            data['productos'] = []

        id = input('Ingrese nuevo codigo: ')        
        producto = input('Ingrese nuevo producto: ')
        cantidad = input('Ingrese las unidades adquiridas : ')
        precio = input('Ingrese el precio costo: ')
        venta = input('Ingrese el precio de venta: ')

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
############################################################################################################
def produc_exis():#Inventario
    print("BIENVENDIDO AL MODULO INVENTARIO \n")
    data = abrir_archivo('productos.json')
    if data:
        if data['productos']:
            for d in data['productos']:
                print("Codigo:",d['id'])
                print("Nombre:", d['producto'])
                print("Existencia:",d['cantidad'])
                print("Precio Venta:",d['precio'])
        else:
            print('No hay productos registrados.')
            
    else:
        print('El archivo no existe o se encuentra vacio.') 

    pause = input('Presione ENTER para continuar...')
    return menu()
#########################################################
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
#####################################################################################################################
def nueva_venta():

    print("BIENVENIDO AL MODULO VENTA\n")

    ventas = abrir_archivo('ventas.json') #abrimos el archivo ventas desde la funcion que hemos creado para abrir archivos
    if not ventas: #si no existe el diccionario para almacenar la info lo creamos.
        ventas = {}
        ventas['ventas'] = []

    venta = '' #el no. de la venta es obligatorio asi que creamos un cliclo con while y una variable que lo controla
    while not venta:
        venta = input('Ingrese el no. de venta: ')

    #Obtenemos la información del cliente y guardamos el id en un variable
    cliente = input('Ingrese el NIT del cliente: ')
    if cliente:
        clientes = abrir_archivo('clientes.json')
        if clientes['clientes']:
            for c in clientes['clientes']:
                if cliente == c['id']:
                    #print(c['id'])
                    print('Nombre Cliente: ' + str(c['nombre']))
                    break #terminamos el ciclo pues ya tenemos la info que necesitabamos
        else:
            print('No hay clientes registrados.')

    #buscamos los productos desde inventario para la venta actual, creamos un ciclo hasta que el usuario lo termine
    op='si'
    productos_venta = [] #este arreglo nos servira para almacenar los codigos de los productos de la venta actual
    while op=='si':
        producto = input('Ingrese el codigo del producto: ')
        if producto: #comprobamos si se ingreso el codigo del producto
            productos = abrir_archivo('productos.json') #abrimos el archivo productos
            if productos['productos']: #comprobamos si existen productos guardados en inventario
                for p in productos['productos']: #recoremos los productos para encontrar el requerido
                    if producto == p['id']: #comprobamos si existe el codigo ingresado
                        print("Codigo: " ,  str(p['id'])) #imprimimos el codigo para que el usuario pueda verlo
                        print("Nombre Libro: " ,  str(p['producto'])) #imprimimos el nombre del producto
                        cantidad = input('Por favor ingrese la cantidad : ') #solicitamos ingrese la cantidad de la venta del producto solicitado
                        if cantidad: #comprobamos si se ingreso una cantidad                            
                            productos_venta.append({ #creamos un diccionario para cada producto de la venta dentro de nuestro arreglo de ventas
                                'producto_id': producto,
                                'cantidad' : cantidad
                            })
                            break #terminamos el ciclo pues ya tenemos la info que necesitabamos
            else:
                print('Producto no encontrado.')            
        op = input("¿Desea agregar otro producto a la venta?..............  si/no: ")

    ventas['ventas'].append({ #creamos nuestro arreglo y diccionarios finales antes de guardar nuestra venta el archivo ventas.json
        'venta_id': venta,
        'cliente_id': cliente,
        'productos_venta': productos_venta
    })      
    #Creamos un resumen de la venta
    print("****************************************************")
    print('VENTA NO: ' + str(venta) + ' CLIENTE: ' + str(c['nombre'])) 
    print("****************************************************")
    print('PRODUCTOS ')
    for i in productos_venta: #recorremos el arreglo de los productos que se agregaron a esta venta
        print("Codigo:" ,str(i['producto_id']))
        print("Cantidad: " ,  str(i['cantidad']))
        print("EL LIBRO VENDIDO ES: DIARIO DE ANA FRANK")
        print("TOTAL A PAGAR: Q175") 
              
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
###############################################################################################################################################

def salir():
    print("Gracias por utilizar nuestros servicios.")
    exit()

"""menu"""
menu()
nuevo_producto()
nuevo_cliente()
produc_exis()
nueva_venta()
abrir_archivo()
guardar_archivo()
salir()
