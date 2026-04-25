def mostrar_info(self):
        print(self.df.info())
        print(self.df.describe())

def graficar(self):
        print("Columnas disponibles:")
        print(self.df.select_dtypes(include='number').columns)

        col = input("Elija columna: ")

        if col not in self.df.columns:
            print("Columna inválida")
            return

        fig, ax = plt.subplots(1, 3, figsize=(12,4))

        self.df[col].plot(ax=ax[0], title="Plot")
        self.df[col].plot(kind='box', ax=ax[1], title="Boxplot")
        self.df[col].plot(kind='hist', ax=ax[2], title="Hist")
        
        ax[0].set_xlabel("Tiempo")
        ax[0].set_ylabel("Valor")

        ax[1].set_ylabel("Valor")

        ax[2].set_xlabel("Valor")
        ax[2].set_ylabel("Frecuencia")

        plt.tight_layout()
        plt.savefig("siata_graficos.png")
        plt.show(block=False)
        plt.pause(3)
        plt.close()

def operaciones(self):
        print(self.df.select_dtypes(include='number').columns)
        c1 = input("Columna 1: ")
        c2 = input("Columna 2: ")

        if c1 not in self.df.columns or c2 not in self.df.columns:
            print("Columnas inválidas")
            return

        self.df['apply'] = self.df[c1].apply(lambda x: x*2)
        self.df['map'] = self.df[c1].map(lambda x: x/2)
        self.df['suma'] = self.df[c1] + self.df[c2]

        print(self.df[[c1,c2,'apply','map','suma']].head())

def remuestreo(self):
        print(self.df.select_dtypes(include='number').columns)
        col = input("Columna: ")

        if col not in self.df.columns:
            print("Columna inválida")
            return

        d = self.df[col].resample('D').mean()
        m = self.df[col].resample('M').mean()
        t = self.df[col].resample('Q').mean()

        plt.plot(d, label="Diario")
        plt.plot(m, label="Mensual")
        plt.plot(t, label="Trimestral")
        plt.legend()
        plt.savefig("remuestreo.png")
        plt.show()
