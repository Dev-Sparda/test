"""
Gestor de conexiones a bases de datos
"""
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
from config import DB_VALIDACION, DB_ENVIOS


class DBManager:
    
    def __init__(self):
        self.db_validacion = None
        self.db_envios = None
    
    def conectar_validacion(self):
        if self.db_validacion is None:
            DB_VALIDACION.parent.mkdir(parents=True, exist_ok=True)
            self.db_validacion = sqlite3.connect(str(DB_VALIDACION))
            self.db_validacion.row_factory = sqlite3.Row
        return self.db_validacion
    
    def conectar_envios(self):
        if self.db_envios is None:
            if not DB_ENVIOS.exists():
                raise FileNotFoundError(f"DB_Envios no encontrada: {DB_ENVIOS}")
            self.db_envios = sqlite3.connect(f"file:{DB_ENVIOS}?mode=ro", uri=True)
            self.db_envios.row_factory = sqlite3.Row
        return self.db_envios
    
    def desconectar(self):
        if self.db_validacion:
            self.db_validacion.close()
            self.db_validacion = None
        if self.db_envios:
            self.db_envios.close()
            self.db_envios = None
    
    def obtener_configuraciones_activas(self) -> List[Dict]:
        conn = self.conectar_validacion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ID_CONFIG, ID_TIPO, NOMBRE_LOGICO, RUTA_BASE,
                   ID_PAQUETE, ID_SECCION, FECHA_INICIO_VALIDACION, PATRON_ARCHIVO
            FROM CONFIG_VALIDACIONES
            WHERE ESTATUS = 1
            ORDER BY ID_TIPO, NOMBRE_LOGICO
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    def obtener_excepcion_aplicable(self, id_config: int, fecha_datos: str) -> Optional[Dict]:
        conn = self.conectar_validacion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.ID_TIPO_EXCEPCION, e.PARAMETRO_NUMERICO
            FROM EXCEPCIONES_VALIDACION e
            WHERE e.ID_CONFIG = ?
              AND e.ESTATUS = 1
              AND (e.FECHA_DATOS_EXCEPCION = ? OR e.FECHA_DATOS_EXCEPCION IS NULL)
            ORDER BY CASE WHEN e.FECHA_DATOS_EXCEPCION IS NOT NULL THEN 1 ELSE 2 END
            LIMIT 1
        """, (id_config, fecha_datos))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def obtener_acuses(self, id_paquete: int, id_seccion: int, fecha_inicio: str) -> List[Dict]:
        conn = self.conectar_envios()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT FECHA_DATOS, Transmision
            FROM TB_ACUSES_SECCIONES
            WHERE ID_PAQUETE = ? AND ID_SECCION = ? AND FECHA_DATOS >= ?
            ORDER BY FECHA_DATOS DESC
        """, (id_paquete, id_seccion, fecha_inicio))
        return [dict(row) for row in cursor.fetchall()]
    
    def guardar_resultado_estructura(self, resultado: Dict):
        conn = self.conectar_validacion()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO RESULTADOS_ESTRUCTURA (
                ID_CONFIG, TIPO_VALIDACION, RUTA_RELATIVA_CARPETA,
                PATRON_ERROR, CANTIDAD_ARCHIVOS_AFECTADOS,
                EJEMPLO_ARCHIVO, INCONSISTENCIA
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            resultado['ID_CONFIG'],
            resultado['TIPO_VALIDACION'],
            resultado['RUTA_RELATIVA_CARPETA'],
            resultado['PATRON_ERROR'],
            resultado['CANTIDAD_ARCHIVOS_AFECTADOS'],
            resultado['EJEMPLO_ARCHIVO'],
            resultado['INCONSISTENCIA']
        ))
        conn.commit()
    
    def guardar_resultado_transmision(self, resultado: Dict):
        conn = self.conectar_validacion()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO RESULTADOS_TRANSMISIONES (
                ID_CONFIG, FECHA_DATOS_ACUSE, TRANSMISIONES_ESPERADAS,
                TRANSMISIONES_ESPERADAS_AJUSTADAS, PATRON_ARCHIVO_APLICADO,
                ARCHIVOS_ENCONTRADOS, ARCHIVOS_VALIDOS, INCONSISTENCIA
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            resultado['ID_CONFIG'],
            resultado['FECHA_DATOS_ACUSE'],
            resultado['TRANSMISIONES_ESPERADAS'],
            resultado['TRANSMISIONES_ESPERADAS_AJUSTADAS'],
            resultado['PATRON_ARCHIVO_APLICADO'],
            resultado['ARCHIVOS_ENCONTRADOS'],
            resultado['ARCHIVOS_VALIDOS'],
            resultado['INCONSISTENCIA']
        ))
        conn.commit()
