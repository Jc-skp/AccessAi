# reconhecedor-lbph.py

Este é um exemplo alternativo de reconhecimento facial usando Haar Cascade e LBPH.

## Partes principais

- `detectorFace = cv2.CascadeClassifier(...)`: carrega o detector Haar.
- `reconhecedor = cv2.face.LBPHFaceRecognizer_create()`: cria o reconhecedor LBPH.
- `reconhecedor.read("lbph_classifier.yml")`: carrega o modelo treinado.
- Leitura da webcam: captura os frames em tempo real.
- Detecção de rosto: usa `detectMultiScale` para localizar a face.
- Previsão: chama `predict` na face redimensionada para obter ID e confiança.
- Exibição: desenha o retângulo e escreve o ID e a confiança sobre a imagem.

## Resultado

- Mostra o nome/ID previsto na janela da webcam.
- Encerra ao pressionar `q`.
