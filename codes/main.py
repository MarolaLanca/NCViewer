import datetime
import tkinter as tk
from tkinter import filedialog
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib
matplotlib.use("TkAgg")


class NetCDFViewer:
    def __init__(self, root):

        self.root = root
        self.root.title("Visualizador de NetCDF")

        self.ds = None  # Para armazenar o dataset carregado

        # Frame de seleção de arquívo
        self.FrameSelArquivo = tk.Frame(root)
        self.FrameSelArquivo.grid(row=0, column=0, pady=10)

        self.label = tk.Label(self.FrameSelArquivo, text="Nenhum arquivo selecionado")
        self.label.grid(row=0, column=0, pady=10)

        self.select_button = tk.Button(self.FrameSelArquivo, text="Selecionar Arquivo", command=self.open_file)
        self.select_button.grid(row=1, column=0, pady=10)

        # Frame seleção variavel
        self.FrameSelVar = tk.Frame(root)

        self.variable_var = tk.StringVar(self.FrameSelVar)
        self.variable_selector = tk.OptionMenu(self.FrameSelVar, self.variable_var, "")
        self.variable_selector.grid(row=0, column=0, pady=10)

        # Frame seleção data e hora
        self.FrameDataHora = tk.Frame(root)

        self.LabelTime = tk.Label(self.FrameDataHora, text="Selecione a data e a hora")
        self.LabelTime.grid(row=0, column=0, pady=10, columnspan=4)

        self.LabelAno = tk.Label(self.FrameDataHora, text="Ano")
        self.LabelAno.grid(row=1, column=0, pady=5, padx=5)
        self.EntryAno = tk.Entry(self.FrameDataHora)
        self.EntryAno.grid(row=2, column=0, pady=5, padx=5)
        self.LabelMes = tk.Label(self.FrameDataHora, text="Mês")
        self.LabelMes.grid(row=1, column=1, pady=5, padx=5)
        self.EntryMes = tk.Entry(self.FrameDataHora)
        self.EntryMes.grid(row=2, column=1, pady=5, padx=5)
        self.LabelDia = tk.Label(self.FrameDataHora, text="Dia")
        self.LabelDia.grid(row=1, column=2, pady=5, padx=5)
        self.EntryDia = tk.Entry(self.FrameDataHora)
        self.EntryDia.grid(row=2, column=2, pady=5, padx=5)
        self.LabelHora = tk.Label(self.FrameDataHora, text="Hora")
        self.LabelHora.grid(row=1, column=3, pady=5, padx=5)
        self.EntryHora = tk.Entry(self.FrameDataHora)
        self.EntryHora.grid(row=2, column=3, pady=5, padx=5)

        # Frame seleção de profundidade
        self.FrameSelecaoProfundidade = tk.Frame(root)

        self.LabelProfundidade = tk.Label(self.FrameSelecaoProfundidade, text="Digite uma profundidade")
        self.LabelProfundidade.grid(row=0, column=0, pady=5)
        self.EntryProfundidade = tk.Entry(self.FrameSelecaoProfundidade)
        self.EntryProfundidade.grid(row=1, column=0, pady=5)

        self.plot_button = tk.Button(self.root, text="Plotar Variável", command=self.plot_variable)

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("NetCDF files", "*.nc"),("NetCDF files", "*.nc4")])
        if filepath:
            self.label.config(text=filepath)
            self.ds = xr.open_dataset(filepath)

            variables = list(self.ds.data_vars.keys())
            self.variable_selector['menu'].delete(0, 'end')
            for var in variables:
                self.variable_selector['menu'].add_command(label=var, command=tk._setit(self.variable_var, var))
            self.variable_var.set(variables[0])  # Define a primeira variável como padrão

            self.FrameSelVar.grid(row=1, column=0, pady=10)
            if "time" in self.ds.variables:
                data_inicio = self.ds.isel(time=0)["time"].values
                data_final = self.ds.isel(time=-1)["time"].values
                self.FrameDataHora.grid(row=2, column=0, pady=10)
                self.LabelTime.config(text=f"Selecionar data entre {data_inicio} - {data_final}")

            if "depth" in self.ds.variables:
                profundidade_inicio = self.ds.isel(depth=0)["depth"].values
                profundidade_fim = self.ds.isel(depth=-1)["depth"].values
                self.FrameSelecaoProfundidade.grid(row=3, column=0, pady=10)
                self.LabelProfundidade.config(text=f"Selecionar profundidade entre {profundidade_inicio} - {profundidade_fim}")

            self.plot_button.grid(row=4, column=0, pady=10)
    def plot_variable(self):
        if self.ds is None:
            print("Nenhum arquivo foi carregado.")
            return

        var_name = self.variable_var.get()

        if "time" in self.ds.variables:
            ano = int(self.EntryAno.get())
            mes = int(self.EntryMes.get())
            dia = int(self.EntryDia.get())
            hora = int(self.EntryHora.get())

            data = datetime.datetime(year=ano, month=mes, day=dia, hour=hora)
            self.ds = self.ds.sel(time=data, method="nearest")
        if "depth" in self.ds.variables:
            profundidade = int(self.EntryProfundidade.get())

            self.ds = self.ds.sel(depth=profundidade, method="nearest")

        lat = self.ds.lat.values
        lon = self.ds.lon.values
        value = self.ds[var_name].values

        fig = plt.figure(figsize=(10, 6))
        proj = ccrs.PlateCarree()
        ax = plt.axes(projection=proj)
        cf = ax.contourf(lon, lat, value, 60, norm=None, cmap="jet", transform=ccrs.PlateCarree())
        cb = plt.colorbar(cf, extend='both', shrink=0.675, pad=0.02, orientation='vertical', fraction=0.1)
        ax.coastlines()
        plt.title("Mapa")
        plt.tight_layout()
        plt.show()
        print("*")


if __name__ == "__main__":
    root = tk.Tk()
    app = NetCDFViewer(root)
    root.mainloop()

