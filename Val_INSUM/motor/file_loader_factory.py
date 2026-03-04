# file_loader_factory.py
import polars as pl


class FileLoaderFactory:

    @staticmethod
    def cargar(ruta, tipo_archivo, schema=None, hoja=None):

        if tipo_archivo == "CSV":
            return pl.read_csv(ruta, schema=schema)

        elif tipo_archivo == "TXT":
            return pl.read_csv(ruta, separator="\t", schema=schema)

        elif tipo_archivo == "EXCEL":
            return pl.read_excel(
                ruta,
                sheet_name=hoja,
                schema=schema
            )

        else:
            raise ValueError("Tipo de archivo no soportado")
