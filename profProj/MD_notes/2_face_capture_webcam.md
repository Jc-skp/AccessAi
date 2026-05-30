# face_capture_webcam.py

Este script faz a captura de faces pela webcam e salva as imagens no dataset.

## Partes principais

- `parse_name(name)`: normaliza o RA informado para usar como nome de pasta.
- `create_folders(final_path, final_path_full)`: cria as pastas de saída se não existirem.
- `detect_face(face_detector, orig_frame)`: detecta rosto com Haar Cascade e recorta a face.
- `detect_face_ssd(network, orig_frame, show_conf=True, conf_min=0.7)`: detecta rosto com SSD e recorta a face.
- Bloco de inicialização: escolhe o detector, abre a webcam e define as pastas `dataset/` e `dataset_full/`.
- Loop principal: captura frames, redimensiona com `resize_video`, mostra o rosto detectado e salva as imagens quando a tecla `q` é pressionada.

## Resultado

- Salva a face recortada em `dataset/<ra>/`.
- Salva a imagem completa em `dataset_full/<ra>/`.
- Para após atingir `max_samples`.
