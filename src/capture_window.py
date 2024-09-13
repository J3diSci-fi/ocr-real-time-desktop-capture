import mss
import cv2
import numpy as np
import time
import easyocr

reader = easyocr.Reader(['pt'])  # Inicialize com os idiomas desejados

def capturar_area_retangular(sct, area):
    screenshot = sct.grab(area)
    frame = np.array(screenshot)
    return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

def extrair_texto_da_imagem(imagem):
    resultado = reader.readtext(imagem)
    texto = ' '.join([res[1] for res in resultado])
    return texto.strip()

def capturar_salvar_e_extrair_texto(x1, y1, x2, y2, master, intervalo=0.5):
    with mss.mss() as sct:
        area = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
        
        while master.flagThreadExtracao:
            inicio = time.time()
            
            frame = capturar_area_retangular(sct, area)
            nome_arquivo = f"temp/captura.png"
            cv2.imwrite(nome_arquivo, frame)
            
            print(f"Imagem {nome_arquivo} salva.")
            
            texto_extraido = extrair_texto_da_imagem(frame)
            if texto_extraido:
                print(f"Texto extraído da imagem {nome_arquivo}:")
                print(texto_extraido)
                master.label_info_extraction.config(text=f"Info: {texto_extraido}")
            else:
                print(f"Nenhum texto encontrado na imagem {nome_arquivo}.")
            
            tempo_decorrido = time.time() - inicio
            tempo_espera = max(0, intervalo - tempo_decorrido)
            time.sleep(tempo_espera)