import tkinter as tk
from src.capture_coord import CapturaTela, obter_coordenadas_captura
from src.capture_window import capturar_salvar_e_extrair_texto
import threading

class AplicacaoPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        self.__configsWindow()
        self.__elementsWindow()

        self.flagThreadExtracao = False

        self.mainloop()
    
    def __configsWindow(self):
        self.title("Captura e Extração de Texto")
        self.resizable(False,False)

        largura_janela = 300
        altura_janela = 200
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        
        posicao_x = (largura_tela - largura_janela) // 2
        posicao_y = (altura_tela - altura_janela) // 2
        
        self.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")

    def __elementsWindow(self):
        self.btn_capturar = tk.Button(self, text="Capturar Coordenadas", command=self.capturar_coordenadas)
        self.btn_capturar.pack(pady=5)

        self.btn_iniciar = tk.Button(self, text="Iniciar Extração de Texto", command=self.iniciar_extracao)
        self.btn_iniciar.pack(pady=5)

        self.btn_parar = tk.Button(self, text="Parar Extração de Texto", command=self.parar_extracao,state='disabled')
        self.btn_parar.pack(pady=5)

        self.label_info_extraction = tk.Label(self,text="Info: ")
        self.label_info_extraction.pack(pady=5)

    def capturar_coordenadas(self):
        self.withdraw()  # Esconde a janela principal temporariamente
        captura = CapturaTela(self)
        captura.wait_window()  # Espera até que a janela de captura seja fechada
        self.deiconify()  # Mostra a janela principal novamente

    def iniciar_extracao(self):
        coordenadas = obter_coordenadas_captura()
        if coordenadas:
            x1, y1, x2, y2 = coordenadas
            self.withdraw()  # Esconde a janela principal
            try:
                self.btn_iniciar.config(state='disabled')
                self.flagThreadExtracao = True
                thread = threading.Thread(target=lambda:capturar_salvar_e_extrair_texto(x1, y1, x2, y2,self))
                thread.daemon = True
                thread.start()
                self.btn_parar.config(state='normal')
            except KeyboardInterrupt:
                print("Processo interrompido pelo usuário.")
            finally:
                self.deiconify()  # Mostra a janela principal novamente
        else:
            print("Por favor, capture as coordenadas primeiro.")

    def parar_extracao(self):
        self.flagThreadExtracao = False
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_parar.config(state=tk.DISABLED)