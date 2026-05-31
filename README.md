# AccessAI — Sistema de Controle de Acesso por Reconhecimento Facial

O **AccessAI** é um sistema de segurança e controle de portaria que utiliza visão computacional e inteligência artificial para autenticar usuários em tempo real. Integrando captura de biometria facial e o classificador LBPH, o projeto oferece uma portaria digital desktop moderna e intuitiva.

## Links do Projeto
* **Repositório Git:** [https://github.com/Jc-skp/AccessAi]
* **Documentação Completa:** Consulte o arquivo `AccessAI - Plano de Desenvolvimento.docx` na raiz do projeto.

---

## Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Interface Gráfica (GUI):** `customtkinter` e `Pillow` (PIL)
* **Visão Computacional:** `OpenCV` (`cv2` e `cv2.face`)
* **Detecção Facial:** Haar Cascade (`haarcascade_frontalface_default.xml`)
* **Modelo de IA:** Algoritmo **LBPH** (*Local Binary Patterns Histograms*)

---

## Estrutura de Arquivos

```text
├── dataset/                    # Fotos recortadas da face (90x120px) organizadas por RA
├── dataset_full/               # Capturas do frame completo da webcam para auditoria
├── app_interface.py            # Software Principal (Interface GUI e loop de vídeo)
├── train_recognizers.py        # Script de treino que gera os arquivos .yml e .pickle
├── haarcascade_frontalface_default.xml # Arquivo de mapeamento do OpenCV para detecção
├── face_names.pickle           # Dicionário serializado que vincula o RA ao ID da IA
├── lbph_classifier.yml         # Arquivo de IA com os histogramas faciais treinados
└── meuarquivo.txt              # Histórico persistente de acessos autorizados (Log de Portaria)
