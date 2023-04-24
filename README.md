# Хакатон "Распознай своё место на Физтехе"

## Датасеты

### ITLP-Campus

Видео-демонстрации треков датасета (публичная часть):
- [2023-02-10-08-04-19-twilight](https://drive.google.com/file/d/1GcJ4jBFuT-Cr4MUTuZaqmX7WDgMNLLJ9/view?usp=share_link)
- [2023-02-21-07-28-58-day](https://drive.google.com/file/d/1BbbCDUx6DnWKaCIgaqZ0Vj9A4-D9WD4Q/view?usp=share_link)
- [2023-03-15-13-25-48-night](https://drive.google.com/file/d/1KiBpk1fBE6cF4BGFK0mPOmsonvB4vBtY/view?usp=share_link)

### Oxford RobotCar

todo

### NCLT

todo

## Базовое решение

### Установка

Базовое решение использует библиотеку [Open Place Recognition](https://github.com/alexmelekhin/open_place_recognition), в которой на текущий момент реализована модель MinkLoc++ и классы для работы с датасетами [Oxford RobotCar](https://robotcar-dataset.robots.ox.ac.uk/), [NCLT](http://robots.engin.umich.edu/nclt/) и **ITLP-Campus**.

Предлагаемые варианты установки зависимостей для работы с кодом:
- Воспользоваться предложенным ноутбуком, в котором продемонстрирован процесс установки зависимостей в Google Colab;
- Воспользоваться docker-образом и инструкциями из [репозитория библиотеки Open Place Recognition](https://github.com/alexmelekhin/open_place_recognition).
- Установить зависимости в свое окружение вручную, воспользовавшись рекомендациями ниже.

#### Ручная установка

Код базового решения разрабатывался и тестировался на Ubuntu 20.04 с CUDA 11.6, PyTorch 1.13.1 и MinkowskiEngine ...

1. Установите PyTorch, воспользовавшись [официальными инструкциями](https://pytorch.org/get-started/previous-versions/)
2. Установите MinkowskiEngine (https://github.com/NVIDIA/MinkowskiEngine):
   ```bash
   # необходимые библиотеки
   sudo apt install build-essential python3-dev libopenblas-dev
   pip install ninja

   # Библиотека MinkowskiEngine должна собираться из исходников с github:
   pip install -U git+https://github.com/NVIDIA/MinkowskiEngine -v --no-deps \
                          --install-option="--force_cuda" \
                          --install-option="--blas=openblas"
   ```
   Если последняя команда возвращает ошибку, то у вас новая версия pip, где `--install-option` переименовали в `--global-option`:
   ```bash
   pip install -U git+https://github.com/NVIDIA/MinkowskiEngine -v --no-deps \
                          --global-option="--force_cuda" \
                          --global-option="--blas=openblas"
   ```

3. Склонируйте и установите [Open Place Recognition](https://github.com/alexmelekhin/open_place_recognition):
   ```bash
   git clone https://github.com/alexmelekhin/open_place_recognition
   cd open_place_recognition
   pip install -e .  # флаг -e необходим для возможности редактировать код уже установленной библиотеки
   ```

После этого вам станет доступен импорт кода из библиотеки `opr`:
```python
from opr.models import minkloc_multimodal

baseline_model = minkloc_multimodal(weights="path_to_checkpoint")
```
