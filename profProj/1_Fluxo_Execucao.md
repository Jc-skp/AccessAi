# Fluxo de Execução do App

Este projeto funciona com os scripts da raiz e com o helper compartilhado [helper_functions.py](helper_functions.py).

## 1. Captura de faces

Arquivo: [face_capture_webcam.py](face_capture_webcam.py)

Fluxo:
- Abre a webcam.
- Pede o RA do usuário.
- Normaliza o nome com `parse_name`.
- Cria as pastas `dataset/<ra>` e `dataset_full/<ra>`.
- Detecta o rosto usando `haarcascade` ou `ssd`.
- Quando o rosto aparece e a tecla `q` é pressionada, salva:
- a face recortada em `dataset/`
- a imagem completa em `dataset_full/`
- Repete até atingir `max_samples`.

## 2. Treinamento dos reconhecedores

Arquivo: [train_recognizers.py](train_recognizers.py)

Fluxo:
- Lê as imagens dentro de `dataset/`.
- Converte cada imagem para escala de cinza.
- Redimensiona as faces para o tamanho usado no treino.
- Cria o dicionário `face_names` com o nome de cada pasta e seu ID.
- Salva o mapeamento em `face_names.pickle`.
- Treina e salva os modelos:
- `eigen_classifier.yml`
- `lbph_classifier.yml`
- `fisher_classifier.yml`

## 3. Reconhecimento em tempo real

Arquivo: [recognition_webcam.py](recognition_webcam.py)

Fluxo:
- Carrega o modelo `lbph_classifier.yml`.
- Carrega o mapa de nomes salvo em `face_names.pickle`.
- Abre a webcam.
- Detecta o rosto com SSD.
- Redimensiona o rosto para o mesmo tamanho usado no treino.
- Faz a predição com o classificador LBPH.
- Mostra o nome reconhecido na imagem.
- Quando `q` é pressionado, grava o último reconhecimento em `meuarquivo.txt`.

## 4. Versão alternativa do reconhecimento

Arquivo: [reconhecedor-lbph.py](reconhecedor-lbph.py)

Fluxo:
- Abre a webcam.
- Detecta o rosto com Haar Cascade.
- Carrega o classificador `lbph_classifier.yml`.
- Faz a predição e exibe ID e confiança na tela.

## 5. Dependência compartilhada

Arquivo: [helper_functions.py](helper_functions.py)

Função usada pelos scripts:
- `resize_video(width, height, max_width)`

Ela ajusta a largura e a altura do vídeo mantendo a proporção original.

## Ordem de uso

1. Capturar faces com [face_capture_webcam.py](face_capture_webcam.py).
2. Treinar os modelos com [train_recognizers.py](train_recognizers.py).
3. Executar o reconhecimento com [recognition_webcam.py](recognition_webcam.py) ou [reconhecedor-lbph.py](reconhecedor-lbph.py).

---
--- 

### Nota: mais informações sobre o funcionamento estão na pasta [MD_notes](MD_notes)