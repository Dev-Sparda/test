def procesar_datos(contenido, columnas_totales, columnas_a_procesar=None, longitudes_interes=None):
    """
    Procesa un string con datos numéricos precedidos por signos y los clasifica
    en listas según signo, longitud y columnas seleccionadas.
    
    Args:
        contenido (str): String con los datos a procesar
        columnas_totales (int): Número total de columnas por fila
        columnas_a_procesar (list): Lista con índices de columnas a procesar (0-based)
        longitudes_interes (list): Lista con longitudes a filtrar (opcional)
    
    Returns:
        dict: Diccionario con listas organizadas por signo y longitud
    """
    
    # Valores por defecto
    if columnas_a_procesar is None:
        columnas_a_procesar = list(range(columnas_totales))
    if longitudes_interes is None:
        longitudes_interes = []
    
    # Dividir el contenido en elementos individuales
    elementos = contenido.split()
    
    # Combinar signos con sus números correspondientes
    elementos_combinados = []
    i = 0
    while i < len(elementos):
        if elementos[i] in ['+', '-'] and i + 1 < len(elementos):
            # Combinar signo con el siguiente número
            elementos_combinados.append(elementos[i] + elementos[i + 1])
            i += 2
        else:
            # Si ya está combinado o es un elemento individual
            elementos_combinados.append(elementos[i])
            i += 1
    
    # Organizar en filas según el número de columnas
    filas = []
    fila_actual = []
    
    for elemento in elementos_combinados:
        fila_actual.append(elemento)
        if len(fila_actual) == columnas_totales:
            filas.append(fila_actual)
            fila_actual = []
    
    # Si queda una fila incompleta, agregarla
    if fila_actual:
        filas.append(fila_actual)
    
    # Diccionario para almacenar los resultados
    resultados = {
        'positivos': {},
        'negativos': {}
    }
    
    # Procesar las filas y columnas seleccionadas
    for fila in filas:
        for idx_columna in columnas_a_procesar:
            if idx_columna < len(fila):
                elemento = fila[idx_columna]
                
                # Verificar si el elemento tiene signo + o -
                if elemento.startswith('+') or elemento.startswith('-'):
                    signo = elemento[0]
                    numero_str = elemento[1:].strip()
                    
                    # Solo procesar si el número no está vacío
                    if numero_str:
                        longitud = len(numero_str)
                        
                        # Filtrar por longitudes si se especificó
                        if not longitudes_interes or longitud in longitudes_interes:
                            if signo == '+':
                                if longitud not in resultados['positivos']:
                                    resultados['positivos'][longitud] = []
                                resultados['positivos'][longitud].append(numero_str)
                            elif signo == '-':
                                if longitud not in resultados['negativos']:
                                    resultados['negativos'][longitud] = []
                                resultados['negativos'][longitud].append(numero_str)
    
    return resultados

def imprimir_resultados(resultados):
    """Imprime los resultados organizados en la consola"""
    
    print("=" * 50)
    print("RESULTADOS ORGANIZADOS")
    print("=" * 50)
    
    # Imprimir positivos
    print("\nELEMENTOS POSITIVOS:")
    print("-" * 30)
    if resultados['positivos']:
        for longitud, numeros in sorted(resultados['positivos'].items()):
            print(f"Longitud {longitud}: {numeros}")
    else:
        print("No hay elementos positivos")
    
    # Imprimir negativos
    print("\nELEMENTOS NEGATIVOS:")
    print("-" * 30)
    if resultados['negativos']:
        for longitud, numeros in sorted(resultados['negativos'].items()):
            print(f"Longitud {longitud}: {numeros}")
    else:
        print("No hay elementos negativos")

# Ejemplo de uso
if __name__ == "__main__":
    # Tu variable de entrada
    contenido_str = '+ 55555 + 66666 + 658888 + 522222 + 100256852000 +101256834000  - 856482 -101256834000'
    
    print("CONTENIDO ORIGINAL:")
    print(contenido_str)
    print()
    
    # Ejemplo 1: Procesar todas las columnas (3 columnas)
    print("EJEMPLO 1: 3 columnas, todas las columnas")
    resultados1 = procesar_datos(contenido_str, columnas_totales=3)
    imprimir_resultados(resultados1)
    
    # Ejemplo 2: Procesar solo columnas 1 y 2 (0-based: [1, 2])
    print("\n" + "="*50)
    print("EJEMPLO 2: 3 columnas, solo columnas 1 y 2")
    resultados2 = procesar_datos(contenido_str, columnas_totales=3, columnas_a_procesar=[1, 2])
    imprimir_resultados(resultados2)
    
    # Ejemplo 3: Procesar solo longitudes específicas (5 y 12)
    print("\n" + "="*50)
    print("EJEMPLO 3: 3 columnas, todas las columnas, solo longitudes 5 y 12")
    resultados3 = procesar_datos(contenido_str, columnas_totales=3, longitudes_interes=[5, 12])
    imprimir_resultados(resultados3)
    
    # Ejemplo 4: Procesar con 2 columnas
    print("\n" + "="*50)
    print("EJEMPLO 4: 2 columnas, todas las columnas")
    resultados4 = procesar_datos(contenido_str, columnas_totales=2)
    imprimir_resultados(resultados4)
