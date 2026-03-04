import polars as pl


class CargadorInsumo:

    def cargar(self, ruta_archivo, layout_columnas, has_header, delimiter):

        df = pl.read_csv(
            ruta_archivo,
            has_header=has_header,
            separator=delimiter
        )

        #  Normalización por índice a nombre interno
        mapa_renombre = {
            df.columns[num_col]: nombre
            for num_col, nombre in layout_columnas
            if num_col < len(df.columns)
        }

        df = df.rename(mapa_renombre)

        return df
