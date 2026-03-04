# validador_sla.py
import duckdb
import json
from datetime import datetime
from pathlib import Path


class ValidadorSLA:

    def __init__(self,
                 id_insumo,
                 id_parte,
                 id_rango,
                 df,
                 validaciones,
                 base_log_path):

        self.id_insumo = id_insumo
        self.id_parte = id_parte
        self.id_rango = id_rango
        self.df = df
        self.validaciones = validaciones
        self.base_log_path = Path(base_log_path)

        self.conn = None

        self.resultado = {
            "id_insumo": id_insumo,
            "id_parte": id_parte,
            "id_rango": id_rango,
            "fecha_proceso": datetime.now(),
            "estructura_ok": True,
            "reglas": []
        }

        self.total_reglas = 0
        self.reglas_con_error = 0
        self.total_errores = 0

    def __enter__(self):
        self.conn = duckdb.connect(":memory:")
        self.conn.register("datos", self.df.to_arrow())
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

    # ==========================================
    # EJECUCIÓN SLA
    # ==========================================

    def procesar(self):

        for regla in self.validaciones:

            id_val, query, descripcion, grupo, seccion, bandera = regla

            self.total_reglas += 1

            resultado = self.conn.execute(query).pl()
            total = resultado.height

            if total > 0:

                self.reglas_con_error += 1
                self.total_errores += total

                # 🔹 Guardar parquet completo
                self._guardar_parquet(id_val, resultado)

                # 🔹 Guardar muestra en JSON
                muestra = resultado.head(10).to_dicts()

                self.resultado["reglas"].append({
                    "id_val": id_val,
                    "descripcion": descripcion,
                    "grupo": grupo,
                    "seccion": seccion,
                    "bandera": bandera,
                    "total_errores": total,
                    "muestra": muestra
                })

        self.resultado["resumen"] = {
            "total_reglas": self.total_reglas,
            "reglas_con_error": self.reglas_con_error,
            "total_errores_detectados": self.total_errores
        }

        return self.resultado

    # ==========================================
    # PARQUET
    # ==========================================

    def _guardar_parquet(self, id_val, df):

        ruta = (self.base_log_path /
                f"parte_{self.id_parte}" /
                f"rango_{self.id_rango}")

        ruta.mkdir(parents=True, exist_ok=True)

        archivo = ruta / f"regla_{id_val}.parquet"

        df.write_parquet(
            archivo,
            compression="zstd"
        )
