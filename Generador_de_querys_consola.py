import re

def procesar_query_individual():
    """
    Procesa una query individual ingresada por el usuario
    """
    print("=== CONVERSOR DE QUERIES CM_MILES → CORTES_MILES ===")
    print("Instrucciones:")
    print("- Pegua tu query de CM_MILES")
    print("- El programa generará las queries para CORTES_MILES")
    print("- Presiona Ctrl+C para salir")
    print("-" * 50)
    
    while True:
        try:
            # Obtener query del usuario
            query_original = input("\n📝 Ingresa la query (o 'salir' para terminar): ").strip()
            
            if query_original.lower() in ['salir', 'exit', 'quit']:
                print("¡Hasta luego!")
                break
            
            if not query_original:
                continue
            
            # Procesar la query
            resultados = procesar_single_query(query_original)
            
            # Mostrar resultados
            print("\n" + "="*80)
            print("🔄 QUERY ORIGINAL:")
            print(f"   {query_original}")
            print("\n" + "="*80)
            
            for i, resultado in enumerate(resultados, 1):
                print(f"\n📊 QUERY GENERADA {i}:")
                print(f"   {resultado['query_nueva']}")
                print(f"   💡 Tipo: {resultado['tipo']}")
                print(f"   🪙 Moneda: {resultado['moneda_detectada']}")
            
            print("\n" + "="*80)
            
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Por favor, verifica la query e intenta nuevamente.")

def procesar_single_query(query_original):
    """
    Procesa una sola query y retorna los resultados
    """
    # Detectar si tiene filtro de moneda
    tiene_moneda, valor_moneda = detectar_filtro_moneda(query_original)
    
    resultados = []
    
    if tiene_moneda:
        # Solo una query con la columna correspondiente
        nueva_query = generar_query_moneda_especifica(query_original, valor_moneda)
        resultados.append({
            'query_nueva': nueva_query,
            'moneda_detectada': valor_moneda,
            'tipo': 'MONEDA_ESPECÍFICA'
        })
    else:
        # Dos queries: una para MN y otra para ME
        query_mn = generar_query_sin_moneda(query_original, 'MN')
        query_me = generar_query_sin_moneda(query_original, 'ME')
        
        resultados.extend([
            {
                'query_nueva': query_mn,
                'moneda_detectada': 14,
                'tipo': 'SIN_MONEDA → MN'
            },
            {
                'query_nueva': query_me,
                'moneda_detectada': 4,
                'tipo': 'SIN_MONEDA → ME'
            }
        ])
    
    return resultados

def detectar_filtro_moneda(query):
    """
    Detecta si la query tiene filtro AND MONEDA = X
    Retorna: (tiene_moneda, valor_moneda)
    """
    patron = r'AND\s+MONEDA\s*=\s*(\d+)'
    coincidencia = re.search(patron, query, re.IGNORECASE)
    
    if coincidencia:
        valor_moneda = int(coincidencia.group(1))
        return True, valor_moneda
    
    return False, None

def generar_query_moneda_especifica(query_original, moneda):
    """
    Genera query para cuando hay filtro de moneda específico
    """
    # Remover el filtro de moneda
    query_sin_moneda = re.sub(r'AND\s+MONEDA\s*=\s*\d+', '', query_original, flags=re.IGNORECASE)
    
    # Determinar la columna según la moneda
    columna = 'ME' if moneda == 4 else 'MN'
    
    # Reemplazar tabla y columna SUM
    nueva_query = query_sin_moneda.replace('CM_MILES', 'CORTES_MILES')
    nueva_query = re.sub(r'SUM\(\s*MONTO\s*\)', f'SUM({columna})', nueva_query, flags=re.IGNORECASE)
    
    # Limpiar espacios dobles y asegurar formato
    nueva_query = re.sub(r'\s+', ' ', nueva_query).strip()
    nueva_query = re.sub(r'WHERE\s+AND', 'WHERE', nueva_query)  # Arreglar WHERE AND
    
    return nueva_query

def generar_query_sin_moneda(query_original, columna):
    """
    Genera query para cuando NO hay filtro de moneda
    """
    # Reemplazar tabla y columna SUM
    nueva_query = query_original.replace('CM_MILES', 'CORTES_MILES')
    nueva_query = re.sub(r'SUM\(\s*MONTO\s*\)', f'SUM({columna})', nueva_query, flags=re.IGNORECASE)
    
    return nueva_query

# Función para pruebas rápidas
def prueba_rapida():
    """
    Función para hacer pruebas rápidas con ejemplos predefinidos
    """
    ejemplos = [
        "SELECT SUM(MONTO) FROM CM_MILES WHERE CONCEPTO IN ('xxxx', 'xxxx') AND FECHA_DATOS = '{FD}'",
        "SELECT SUM(MONTO) FROM CM_MILES WHERE CONCEPTO IN ('xxxx', 'xxxx') AND MONEDA = 14 AND FECHA_DATOS = '{FD}'",
        "SELECT SUM(MONTO) FROM CM_MILES WHERE CONCEPTO IN ('xxxx', 'xxxx') AND MONEDA = 4 AND FECHA_DATOS = '{FD}'"
    ]
    
    print("=== MODO PRUEBA RÁPIDA ===")
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n--- Ejemplo {i} ---")
        print(f"Original: {ejemplo}")
        resultados = procesar_single_query(ejemplo)
        for j, resultado in enumerate(resultados, 1):
            print(f"  Generada {j}: {resultado['query_nueva']}")
            print(f"    Tipo: {resultado['tipo']}")

# EJECUCIÓN PRINCIPAL
if __name__ == "__main__":
    print("Selecciona modo:")
    print("1. Modo interactivo (ingresar queries manualmente)")
    print("2. Modo prueba rápida (ver ejemplos)")
    
    opcion = input("Elige (1/2): ").strip()
    
    if opcion == "2":
        prueba_rapida()
    else:
        procesar_query_individual()
