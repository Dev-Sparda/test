# config_repository.py
import duckdb


class ConfigRepository:

    def __init__(self, ruta_db):
        self.ruta_db = ruta_db
        self.conn = None

    def __enter__(self):
        self.conn = duckdb.connect(self.ruta_db)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

    # ================================
    # INSUMO
    # ================================

    def obtener_insumo(self, id_insumo):
        return self.conn.execute("""
            SELECT ID_INSUMO, RUTA_ARCHIVO, TIPO_ARCHIVO
            FROM CAT_INSUMOS
            WHERE ID_INSUMO = ?
        """, (id_insumo,)).fetchone()

    # ================================
    # PARTES
    # ================================

    def obtener_partes(self, id_insumo):
        return self.conn.execute("""
            SELECT ID_PARTE, NUM_PARTE, NOMBRE_PARTE
            FROM INSUMOS_PARTES
            WHERE ID_INSUMO = ?
              AND ESTATUS = TRUE
            ORDER BY NUM_PARTE
        """, (id_insumo,)).fetchall()

    # ================================
    # RANGOS
    # ================================

    def obtener_rangos(self, id_parte):
        return self.conn.execute("""
            SELECT ID_RANGO, NUM_RANGO, NOMBRE_RANGO,
                   COL_INICIO, COL_FIN
            FROM INSUMOS_RANGOS
            WHERE ID_PARTE = ?
              AND ESTATUS = TRUE
            ORDER BY NUM_RANGO
        """, (id_parte,)).fetchall()

    # ================================
    # DEFINICIÓN COLUMNAS
    # ================================

    def obtener_definicion_columnas(self, id_rango):

        columnas = self.conn.execute("""
            SELECT INDEX_COL, NOMBRE_COLUMN, TIPO_DATO_SYS
            FROM DEFINICION_INSUMOS
            WHERE ID_RANGO = ?
              AND ESTATUS = TRUE
            ORDER BY INDEX_COL
        """, (id_rango,)).fetchall()

        import polars as pl

        mapeo = {
            "INT": pl.Int64,
            "STRING": pl.Utf8,
            "DATE": pl.Utf8,
            "FLOAT": pl.Float64
        }

        schema = {}
        for _, nombre, tipo in columnas:
            schema[nombre] = mapeo.get(tipo, pl.Utf8)

        return schema

    # ================================
    # VALIDACIONES SLA
    # ================================

    def obtener_validaciones_sla(self, id_insumo):
        return self.conn.execute("""
            SELECT ID_VAL,
                   VALIDACION,
                   DESCRIPCION,
                   GRUPO,
                   SECCION,
                   BANDERA
            FROM MOTOR_VAL
            WHERE ID_INSUMO = ?
              AND TIPO_VAL = 'SLA'
              AND ESTATUS = TRUE
        """, (id_insumo,)).fetchall()
