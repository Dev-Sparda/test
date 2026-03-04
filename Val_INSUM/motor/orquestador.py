# orquestador.py
from datetime import datetime
from pathlib import Path
import json

from config_repository import ConfigRepository
from file_loader_factory import FileLoaderFactory
from validador_sla import ValidadorSLA


class OrquestadorInsumo:

    def __init__(self, id_insumo, ruta_db):
        self.id_insumo = id_insumo
        self.ruta_db = ruta_db

    def procesar(self):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_log_path = Path("logs") / f"insumo_{self.id_insumo}_{timestamp}"
        base_log_path.mkdir(parents=True, exist_ok=True)

        resultados_globales = []

        with ConfigRepository(self.ruta_db) as repo:

            insumo = repo.obtener_insumo(self.id_insumo)
            partes = repo.obtener_partes(self.id_insumo)
            validaciones = repo.obtener_validaciones_sla(self.id_insumo)

            for parte in partes:

                id_parte = parte[0]
                hoja = parte[2]

                rangos = repo.obtener_rangos(id_parte)

                for rango in rangos:

                    id_rango, _, _, col_ini, col_fin = rango

                    schema = repo.obtener_definicion_columnas(id_rango)

                    df = FileLoaderFactory.cargar(
                        ruta=insumo[1],
                        tipo_archivo=insumo[2],
                        schema=schema,
                        hoja=hoja
                    )

                    df_rango = df[:, col_ini:col_fin + 1]

                    with ValidadorSLA(
                        self.id_insumo,
                        id_parte,
                        id_rango,
                        df_rango,
                        validaciones,
                        base_log_path
                    ) as val:

                        resultado = val.procesar()
                        resultados_globales.append(resultado)

        # 🔹 Guardar JSON general
        with open(base_log_path / "log.json", "w", encoding="utf-8") as f:
            json.dump(resultados_globales, f, indent=4, default=str)

        print("✔ Proceso finalizado")
