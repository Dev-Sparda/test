import duckdb


class DbConfig:

    def __init__(self, ruta_db):
        self.con = duckdb.connect(ruta_db)

    def obtener_config_insumo(self, id_insumo):
        return self.con.execute("""
            SELECT HAS_HEADER, DELIMITER
            FROM INSUMOS
            WHERE ID_INSUMO = ?
        """, [id_insumo]).fetchone()

    def obtener_layout_columnas(self, id_insumo):
        return self.con.execute("""
            SELECT NUM_COLUMNA, NOMBRE_INTERNO
            FROM INSUMO_COLUMNAS
            WHERE ID_INSUMO = ?
            ORDER BY NUM_COLUMNA
        """, [id_insumo]).fetchall()

    def obtener_validaciones(self, id_insumo):
        return self.con.execute("""
            SELECT *
            FROM VALIDACIONES
            WHERE ID_INSUMO = ?
        """, [id_insumo]).fetchdf().to_dicts()
