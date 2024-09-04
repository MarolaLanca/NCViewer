import datetime
import tkinter as tk
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib
from tkinter import filedialog, messagebox


class NetCDFViewer:
    def __init__(self, root):

        self.root = root
        self.root.title("Visualizador de NetCDF")

        self.ds = None  # Para armazenar o dataset carregado

        # Frame de seleção de arquívo
        self.FrameSelArquivo = tk.Frame(root)
        self.FrameSelArquivo.grid(row=0, column=0, pady=10)

        self.label = tk.Label(self.FrameSelArquivo, text="Nenhum arquivo selecionado")
        self.label.grid(row=0, column=0, pady=5)

        self.select_button = tk.Button(self.FrameSelArquivo, text="Selecionar Arquivo", command=self.open_file)
        self.select_button.grid(row=1, column=0, pady=5)

        # Frame configuração
        self.FrameConfiguracao = tk.Frame(root)

        self.LabelConf = tk.Label(self.FrameConfiguracao, text="")
        self.LabelConf.grid(row=0, column=0, pady=5, columnspan=4)

        self.LabelLonConf = tk.Label(self.FrameConfiguracao, text="Longitude")
        self.LabelLonConf.grid(row=1, column=0, pady=5, padx=5)
        self.EntryLonConf = tk.Entry(self.FrameConfiguracao)
        self.EntryLonConf.grid(row=2, column = 0, pady=5, padx=5)

        self.LabelLatConf = tk.Label(self.FrameConfiguracao, text="Latitude")
        self.LabelLatConf.grid(row=1, column=1, pady=5, padx=5)
        self.EntryLatConf = tk.Entry(self.FrameConfiguracao)
        self.EntryLatConf.grid(row=2, column=1, pady=5, padx=5)

        self.LabelTimeConf = tk.Label(self.FrameConfiguracao, text="Time")
        self.LabelTimeConf.grid(row=1, column=2, pady=5, padx=5)
        self.EntryTimeConf = tk.Entry(self.FrameConfiguracao, state='disabled')
        self.EntryTimeConf.grid(row=2, column=2, pady=5, padx=5)
        self.var_entry_time = tk.BooleanVar()
        self.CheckbuttonTime = tk.Checkbutton(self.FrameConfiguracao, text="Time?", variable=self.var_entry_time,
                                          command=self.toggle_entry_time)
        self.CheckbuttonTime.grid(row=3, column=2, pady=3)

        self.LabelDepthConf = tk.Label(self.FrameConfiguracao, text="Depth")
        self.LabelDepthConf.grid(row=1, column=3, pady=5, padx=5)
        self.EntryDepthConf = tk.Entry(self.FrameConfiguracao, state="disabled")
        self.EntryDepthConf.grid(row=2, column=3, pady=5, padx=5)
        self.var_entry_depth = tk.BooleanVar()
        self.CheckbuttonDepth = tk.Checkbutton(self.FrameConfiguracao, text="Depth?", variable=self.var_entry_depth,
                                              command=self.toggle_entry_depth)
        self.CheckbuttonDepth.grid(row=3, column=3, pady=3)

        # Frame seleção variavel
        self.FrameSelVar = tk.Frame(root)

        self.variable_var = tk.StringVar(self.FrameSelVar)
        self.variable_selector = tk.OptionMenu(self.FrameSelVar, self.variable_var, "")
        self.variable_selector.grid(row=0, column=0, pady=5)

        # Frame seleção data e hora
        self.FrameDataHora = tk.Frame(root)

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

        # Frame salvar
        self.FramaSalvar = tk.Frame(root)

        self.var_save = tk.BooleanVar()
        self.check_save = tk.Checkbutton(self.FramaSalvar, text="Salvar", variable=self.var_save)
        self.check_save.grid(row=1, column=0, pady=5, padx=10)

        # Plot Button
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

            self.LabelConf.config(text=self.lista_coordenadas())
            self.FrameConfiguracao.grid(row=1, column=0, pady=10)

            self.FrameSelVar.grid(row=2, column=0, pady=10)

            self.FramaSalvar.grid(row=5, column=0, pady=10)

            self.plot_button.grid(row=6, column=0, pady=10)

    def plot_variable(self):
        coordenadas = {}
        coordenadas["lat_name"] = self.EntryLatConf.get()
        coordenadas["lon_name"] = self.EntryLonConf.get()
        if self.var_entry_time.get():
            coordenadas["time_name"] = self.EntryTimeConf.get()
        if self.var_entry_depth.get():
            coordenadas["depth_name"] = self.EntryDepthConf.get()

        for coords in coordenadas.values():
            if coords not in list(self.ds.coords):
                messagebox.showerror("Erro", f"{coords} não está na lista de coordenadas.")
                return

        if self.ds is None:
            print("Nenhum arquivo foi carregado.")
            return

        var_name = self.variable_var.get()

        if self.var_entry_time.get():
            try:
                ano = int(self.EntryAno.get())
                mes = int(self.EntryMes.get())
                dia = int(self.EntryDia.get())
                hora = int(self.EntryHora.get())
            except:
                messagebox.showerror("Erro", "Não colocado um número na data/hora.")
                return

            try:
                data = datetime.datetime(year=ano, month=mes, day=dia, hour=hora)
                self.ds = self.ds.sel({coordenadas["time_name"]: data}, method="nearest")
            except:
                messagebox.showerror("Erro", "A data selecionada não existe.")
                return

        if self.var_entry_depth.get():
            profundidade = int(self.EntryProfundidade.get())

            self.ds = self.ds.sel({coordenadas["depth_name"]: profundidade}, method="nearest")

        lat = self.ds[coordenadas["lat_name"]].values
        lon = self.ds[coordenadas["lon_name"]].values
        value = self.ds[var_name].values

        fig = plt.figure(figsize=(10, 6))
        proj = ccrs.PlateCarree()
        ax = plt.axes(projection=proj)
        cf = ax.contourf(lon, lat, value, 60, norm=None, cmap="jet", transform=ccrs.PlateCarree())
        cb = plt.colorbar(cf, extend='both', shrink=0.675, pad=0.02, orientation='vertical', fraction=0.1)
        ax.coastlines()
        plt.title("Mapa")
        plt.tight_layout()

        if self.var_save.get():
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            messagebox.showinfo("Salvo", f"Imagem salva em {save_path}")
            plt.savefig(save_path, dpi=300, transparent=False, bbox_inches='tight')

        plt.show()

    def lista_coordenadas(self):
        coordenadas = list(self.ds.coords)

        string = ""
        for i in range(len(coordenadas) - 1):
            string = string + f"{coordenadas[i]}, "
        string = string + coordenadas[-1]

        message = f"Suas coordenadas são {string}."
        return message

    def toggle_entry_time(self):
        if self.var_entry_time.get():  # Se o Checkbutton estiver selecionado
            self.EntryTimeConf.config(state='normal')
            self.FrameDataHora.grid(row=2, column=0, pady=10)
        else:  # Se o Checkbutton estiver desmarcado
            self.EntryTimeConf.config(state='disabled')
            self.FrameDataHora.grid_forget()

    def toggle_entry_depth(self):
        if self.var_entry_depth.get():  # Se o Checkbutton estiver selecionado
            self.EntryDepthConf.config(state='normal')
            self.FrameSelecaoProfundidade.grid(row=3, column=0, pady=10)
        else:  # Se o Checkbutton estiver desmarcado
            self.EntryDepthConf.config(state='disabled')
            self.FrameSelecaoProfundidade.grid_forget()



if __name__ == "__main__":
    root = tk.Tk()
    app = NetCDFViewer(root)
    root.mainloop()

