# recognition_webcam.py

Este script faz o reconhecimento em tempo real pela webcam usando o modelo treinado.

## Partes principais

- `load_recognizer(option, training_data)`: carrega o classificador escolhido, neste caso o LBPH.
- Leitura de `face_names.pickle`: recupera o nome associado a cada ID treinado.
- `grava(id)`: grava o identificador reconhecido junto com a data e hora em `meuarquivo.txt`.
- `recognize_faces(network, face_classifier, orig_frame, face_names, threshold, conf_min=0.9)`: detecta o rosto com SSD, recorta a face, faz a predição e monta o texto exibido.
- Bloco de inicialização: abre o modelo `lbph_classifier.yml`, carrega o SSD e prepara a webcam.
- Loop principal: captura frames, redimensiona com `resize_video`, mostra o resultado e grava a última identificação ao pressionar `q`.

## Resultado

- Exibe o nome reconhecido na tela.
- Salva o último reconhecimento em `meuarquivo.txt`.
