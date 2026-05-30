# train_recognizers.py

Este script lê o dataset, monta os rótulos e treina os reconhecedores faciais.

## Partes principais

- `training_path = 'dataset/'`: pasta de origem das imagens de treino.
- `get_image_data(path_train)`: percorre as subpastas do dataset, carrega as imagens e monta `ids`, `faces` e `face_names`.
- Conversão para cinza e redimensionamento: deixa todas as faces com o mesmo tamanho antes do treino.
- Gravação de `face_names.pickle`: salva o mapeamento de nome para ID.
- Treino dos classificadores:
	- `EigenFaceRecognizer`
	- `LBPHFaceRecognizer`
	- `FisherFaceRecognizer`
- Escrita dos modelos em `.yml`.

## Resultado

- Gera `face_names.pickle`.
- Gera `eigen_classifier.yml`.
- Gera `lbph_classifier.yml`.
- Gera `fisher_classifier.yml`.
