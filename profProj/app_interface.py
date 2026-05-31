import tkinter as tk
import customtkinter as ctk
import cv2
import threading
import os
import pickle
from PIL import Image, ImageTk

# Configuração global de aparência do CustomTkinter
ctk.set_appearance_mode("dark")  # Modo Escuro permanente
ctk.set_default_color_theme("blue")  # Tema de cor dos botões e destaques

class AccessAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AccessAI - Access and Recognition AI")
        self.geometry("1100x600")
        self.configure(fg_color="#1a1c23") # Fundo grafite escuro igual à imagem

        # Variáveis de controle do estado da Webcam e Modelos
        self.camera = None
        self.camera_rodando = False
        self.modo_atual = "Identificar" # Pode ser "Identificar" ou "Cadastrar"
        self.contagem_fotos = 0
        self.ra_cadastro = ""

        # Carregar classificadores do seu projeto
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.reconhecedor = cv2.face.LBPHFaceRecognizer_create()
        
        if os.path.exists("lbph_classifier.yml"):
            self.reconhecedor.read("lbph_classifier.yml")
        
        self.nomes_usuarios = {}
        if os.path.exists("face_names.pickle"):
            with open("face_names.pickle", "rb") as f:
                self.nomes_usuarios = pickle.load(f)

        self.criar_layout()
        self.iniciar_webcam()

    def criar_layout(self):
        # --- TOPO: Cabeçalho ---
        lbl_titulo = ctk.CTkLabel(self, text="AccessAI | Access and Recognition AI", font=ctk.CTkFont(size=20, weight="bold"), text_color="#e2e8f0")
        lbl_titulo.pack(pady=15, anchor="w", padx=20)

        # --- CONTAINER PRINCIPAL (Split em Esquerda e Direita) ---
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        # ---------------- COLUNA DA ESQUERDA (WEBCAM) ----------------
        frame_esquerda = ctk.CTkFrame(container, fg_color="#242630", corner_radius=15)
        frame_esquerda.pack(side="left", fill="both", expand=True, padx=(0, 10))

        lbl_video_tag = ctk.CTkLabel(frame_esquerda, text="Webcam em Tempo Real", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_video_tag.pack(pady=10, anchor="w", padx=15)

        # Onde o feed de vídeo do OpenCV será renderizado
        self.lbl_video = tk.Label(frame_esquerda, bg="#101114")
        self.lbl_video.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Painel inferior de controle do modo da câmera
        frame_botoes_cam = ctk.CTkFrame(frame_esquerda, fg_color="transparent")
        frame_botoes_cam.pack(fill="x", pady=(0, 15), padx=15)

        self.btn_modo_identificar = ctk.CTkButton(frame_botoes_cam, text="Modo: Identificar Portaria", fg_color="#3b82f6", command=self.ativar_modo_identificar)
        self.btn_modo_identificar.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_modo_cadastrar = ctk.CTkButton(frame_botoes_cam, text="Modo: Capturar Rosto", fg_color="#4b5563", command=self.ativar_modo_cadastrar)
        self.btn_modo_cadastrar.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # ---------------- COLUNA DA DIREITA (PAINEL DE CADASTRO / LOG) ----------------
        frame_direita = ctk.CTkFrame(container, fg_color="#242630", width=400, corner_radius=15)
        frame_direita.pack(side="right", fill="both", padx=(10, 0))
        frame_direita.pack_propagate(False)

        lbl_painel_tag = ctk.CTkLabel(frame_direita, text="Controle do Porteiro Digital", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_painel_tag.pack(pady=15, anchor="w", padx=20)

        # Campos de entrada de texto para novo cadastro
        lbl_ra = ctk.CTkLabel(frame_direita, text="RA / Código do Aluno:")
        lbl_ra.pack(anchor="w", padx=20, pady=(5, 2))
        self.input_ra = ctk.CTkEntry(frame_direita, placeholder_text="Ex: 12345678", width=360)
        self.input_ra.pack(padx=20, pady=(0, 10))

        lbl_nome = ctk.CTkLabel(frame_direita, text="Nome Completo:")
        lbl_nome.pack(anchor="w", padx=20, pady=(5, 2))
        self.input_nome = ctk.CTkEntry(frame_direita, placeholder_text="Ex: Amanda Aluno", width=360)
        self.input_nome.pack(padx=20, pady=(0, 15))

        # Botões de Ação
        self.btn_registrar = ctk.CTkButton(frame_direita, text="Iniciar Fluxo de Registro", fg_color="#10b981", hover_color="#059669", width=360, height=40, command=self.fluxo_registro)
        self.btn_registrar.pack(padx=20, pady=10)

        self.btn_treinar = ctk.CTkButton(frame_direita, text="Sincronizar Banco / Treinar IA", fg_color="#f59e0b", text_color="#101114", hover_color="#d97706", width=360, height=40, command=self.fluxo_treinamento)
        self.btn_treinar.pack(padx=20, pady=10)

        # Painel de Status do Sistema
        self.frame_status = ctk.CTkFrame(frame_direita, fg_color="#1a1c23", height=100)
        self.frame_status.pack(fill="x", padx=20, pady=20, side="bottom")
        
        self.lbl_status = ctk.CTkLabel(self.frame_status, text="SISTEMA PRONTO: Identificando...", font=ctk.CTkFont(size=13, weight="bold"), text_color="#10b981")
        self.lbl_status.pack(pady=15)

    # --- LÓGICA DE MODOS DA WEB CAM ---
    def ativar_modo_identificar(self):
        self.modo_atual = "Identificar"
        self.btn_modo_identificar.configure(fg_color="#3b82f6")
        self.btn_modo_cadastrar.configure(fg_color="#4b5563")
        self.lbl_status.configure(text="SISTEMA PRONTO: Identificando...", text_color="#10b981")

    def ativar_modo_cadastrar(self):
        self.modo_atual = "Cadastrar"
        self.btn_modo_identificar.configure(fg_color="#4b5563")
        self.btn_modo_cadastrar.configure(fg_color="#3b82f6")
        self.lbl_status.configure(text="MODO CADASTRO SELECIONADO.\nPreencha os campos ao lado e clique em Registrar.", text_color="#3b82f6")

    # --- FLUXO DE CAPTURA DE FOTOS ---
    def fluxo_registro(self):
        ra = self.input_ra.get().strip()
        nome = self.input_nome.get().strip()

        if not ra or not nome:
            self.lbl_status.configure(text="ERRO: Digite o RA e o Nome antes!", text_color="#ef4444")
            return

        # Criar a pasta de fotos do aluno se não existir
        self.caminho_salvamento = f"dataset/{ra}"
        os.makedirs(self.caminho_salvamento, exist_ok=True)
        
        self.ra_cadastro = ra
        self.contagem_fotos = 0
        self.ativar_modo_cadastrar()
        self.lbl_status.configure(text=f"Olhe para a câmera!\nCapturando 20 fotos para o RA {ra}...", text_color="#f59e0b")

    # --- FLUXO DE TREINAMENTO (Chama o seu script original em Background) ---
    def fluxo_treinamento(self):
        self.lbl_status.configure(text="Treinando IA... Por favor aguarde.", text_color="#f59e0b")
        
        def rodar_treino():
            # Executa o seu script original de treinamento
            os.system("python train_recognizers.py")
            
            # Recarrega as configurações atualizadas geradas pelo seu script
            if os.path.exists("lbph_classifier.yml"):
                self.reconhecedor.read("lbph_classifier.yml")
            if os.path.exists("face_names.pickle"):
                with open("face_names.pickle", "rb") as f:
                    self.nomes_usuarios = pickle.load(f)
                    
            self.lbl_status.configure(text="IA Treinada com Sucesso!\nNovos usuários integrados.", text_color="#10b981")
            self.ativar_modo_identificar()

        threading.Thread(target=rodar_treino).start()

    # --- RENDERIZAÇÃO E PROCESSAMENTO DO FRAME DA WEBCAM ---
    def iniciar_webcam(self):
        self.camera = cv2.VideoCapture(0)
        self.camera_rodando = True
        
        def loop_video():
            while self.camera_rodando:
                ret, frame = self.camera.read()
                if not ret:
                    continue

                # Espelhar para ficar natural
                frame = cv2.flip(frame, 1)
                cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(cinza, 1.3, 5)

                for (x, y, w, h) in faces:
                    # Desenhar quadrado ao redor do rosto (Estilo Target Verde da imagem)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 150), 2)

                    # Se estiver no modo IDENTIFICAR, tenta predizer quem é
                    if self.modo_atual == "Identificar" and len(self.nomes_usuarios) > 0:
                        face_roi = cv2.resize(cinza[y:y+h, x:x+w], (90, 120))
                        try:
                            id_previsto, confianca = self.reconhecedor.predict(face_roi)
                            
                            # Encontrar o Nome invertendo o dicionário face_names
                            nome_detectado = "Desconhecido"
                            for nome_chave, id_val in self.nomes_usuarios.items():
                                if id_val == id_previsto:
                                    nome_detectado = nome_chave
                                    break

                            # Se a confiança for aceitável (Ajuste o threshold conforme seu projeto)
                            if confianca < 90: 
                                texto = f"{nome_detectado} ({id_previsto})"
                                cv2.putText(frame, texto, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 150), 2)
                            else:
                                cv2.putText(frame, "Nao Identificado", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                        except:
                            pass

                    # Se estiver no modo CADASTRAR e um processo de registro foi disparado
                    elif self.modo_atual == "Cadastrar" and self.contagem_fotos < 20 and self.ra_cadastro != "":
                        self.contagem_fotos += 1
                        face_roi = cv2.resize(cinza[y:y+h, x:x+w], (90, 120))
                        
                        # Salva o arquivo de foto respeitando a nomenclatura padrão
                        nome_arquivo = f"{self.caminho_salvamento}/{self.ra_cadastro}.{self.contagem_fotos}.jpg"
                        cv2.imwrite(nome_arquivo, face_roi)
                        
                        # Alerta visual na tela do número de capturas
                        cv2.putText(frame, f"Capturando: {self.contagem_fotos}/20", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

                        if self.contagem_fotos >= 20:
                            self.ra_cadastro = ""
                            self.lbl_status.configure(text="Captura Concluída!\nClique em 'Sincronizar Banco / Treinar IA'.", text_color="#f59e0b")

                # Converter o frame do OpenCV (BGR) para formato que o Tkinter aceita (RGB)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(frame_rgb)
                
                # Redimensiona para caber bonito no painel da tela
                img_pil = img_pil.resize((640, 400))
                img_tk = ImageTk.PhotoImage(image=img_pil)

                # Atualiza a imagem na Interface Gráfica
                try:
                    self.lbl_video.img_tk = img_tk
                    self.lbl_video.configure(image=img_tk)
                except:
                    break

        # Executa a captura do OpenCV em uma linha separada para não travar os botões da tela
        threading.Thread(target=loop_video, daemon=True).start()

    def destroy(self):
        # Garante o fechamento limpo da webcam ao fechar a janela
        self.camera_rodando = False
        if self.camera:
            self.camera.release()
        super().destroy()

if __name__ == "__main__":
    app = AccessAIApp()
    app.mainloop()