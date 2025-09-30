import pandas as pd
import re

def procesar_queries_moneda(df, columna_queries='query'):
    """
    Procesa las queries de CM_MILES y genera las correspondientes para CORTES_MILES
    según las reglas de moneda (4 → ME, 14 → MN)
    """
    
    queries_resultado = []
    
    for idx, query_original in enumerate(df[columna_queries]):
        query_original = str(query_original).strip()
        
        # Detectar si tiene filtro de moneda
        tiene_moneda, valor_moneda = detectar_filtro_moneda(query_original)
        
        # Generar las queries según corresponda
        if tiene_moneda:
            # Solo una query con la columna correspondiente
            nueva_query = generar_query_moneda_especifica(query_original, valor_moneda)
            queries_resultado.append({
                'query_original': query_original,
                'query_nueva': nueva_query,
                'moneda_detectada': valor_moneda,
                'tipo': 'moneda_especifica'
            })
        else:
            # Dos queries: una para MN y otra para ME
            query_mn = generar_query_sin_moneda(query_original, 'MN')
            query_me = generar_query_sin_moneda(query_original, 'ME')
            
            queries_resultado.extend([
                {
                    'query_original': query_original,
                    'query_nueva': query_mn,
                    'moneda_detectada': 14,
                    'tipo': 'sin_moneda_MN'
                },
                {
                    'query_original': query_original,
                    'query_nueva': query_me,
                    'moneda_detectada': 4,
                    'tipo': 'sin_moneda_ME'
                }
            ])
    
    return pd.DataFrame(queries_resultado)

def detectar_filtro_moneda(query):
    """
    Detecta si la query tiene filtro AND MONEDA = X
    Retorna: (tiene_moneda, valor_moneda)
    """
    # Patrón para buscar AND MONEDA = número
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
    
    # Limpiar espacios dobles
    nueva_query = re.sub(r'\s+', ' ', nueva_query).strip()
    
    return nueva_query

def generar_query_sin_moneda(query_original, columna):
    """
    Genera query para cuando NO hay filtro de moneda
    """
    # Reemplazar tabla y columna SUM (sin remover filtros de moneda)
    nueva_query = query_original.replace('CM_MILES', 'CORTES_MILES')
    nueva_query = re.sub(r'SUM\(\s*MONTO\s*\)', f'SUM({columna})', nueva_query, flags=re.IGNORECASE)
    
    return nueva_query

# USO COMPLETO DEL SCRIPT
def procesar_excel_queries(archivo_entrada, archivo_salida, columna_queries='query'):
    """
    Función principal para procesar el Excel completo
    """
    # Leer el Excel
    df_original = pd.read_excel(archivo_entrada)
    
    # Procesar las queries
    df_resultado = procesar_queries_moneda(df_original, columna_queries)
    
    # Guardar resultados
    df_resultado.to_excel(archivo_salida, index=False)
    
    print(f"Procesamiento completado!")
    print(f"Queries originales: {len(df_original)}")
    print(f"Queries generadas: {len(df_resultado)}")
    
    return df_resultado

# EJEMPLO DE USO
if __name__ == "__main__":
    # Configuración
    archivo_entrada = r'C:\Users\thede\OneDrive\Escritorio\queries_originales.xlsx'
    archivo_salida = r'C:\Users\thede\OneDrive\Escritorio\queries_generadas.xlsx'
    columna_con_queries = 'querys'  # Cambia por el nombre de tu columna
    
    # Procesar
    resultado = procesar_excel_queries(archivo_entrada, archivo_salida, columna_con_queries)
    
    # Mostrar ejemplos
    print("\n--- Ejemplos de conversión ---")
    for i, row in resultado.head(4).iterrows():
        print(f"\nOriginal: {row['query_original'][:80]}...")
        print(f"Nueva: {row['query_nueva']}")
        print(f"Tipo: {row['tipo']}")
