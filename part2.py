class ProcesadorSIATA:
    def __init__(self, ruta):
        try:
            data = sio.loadmat(ruta)
        except FileNotFoundError:
            print(" Error: No encontramos el archivo. Verifica que la ruta sea correcta.")

        self.df = pd.read_csv(ruta)
        self.nombre = os.path.basename(ruta)

        for col in self.df.columns:
            if "fecha" in col.lower() or "date" in col.lower():
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                self.df.set_index(col, inplace=True)
                break

