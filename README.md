# Хакатон "Распознай своё место на Физтехе"

## Датасеты

### ITLP-Campus

Датасет записан на робототехнической платформе Husky на территории кампуса МФТИ и состоит из 5 треков, записанных в разное время суток (день/сумерки/ночь) и разные времена года (зима/весна).

Для обучения предлагается использовать зимние треки (день/сумерки/ночь), а весенние (день/ночь) будут выданы для финального тестирования.

Данные разделены по трекам, длина одного трека порядка 3 км, каждый трек включает в себя порядка $600$ фреймов. Расстояние между соседними фреймами ~5 м. Каждый фрейм включает в себя:

- LiDAR -ный скан
- RGB изобрадения для 2х камер (front/back)
- Семантические маски для изображений каждой камеры
- Текстовое описание для изображений каждой камеры
- 6 DoF позу робота

Подробнее про формат данных и структуру датасета см. [itlp_campus_dataset.md](docs/itlp_campus_dataset.md).

Данные можно найти/использовать на следующих ресурсах:
- [Яндекс.Диск](https://disk.yandex.ru/d/AIAHtZkuRf08TQ)
- [Kaggle](https://www.kaggle.com/datasets/creatorofuniverses/itlp-campus-dataset-public)
- [Google Drive]()

sha256: `f59cf87bb0ea380431c9dc889cc49d32dd1e985b8c4700b7155629cca34d5da6` public.zip

Видео-демонстрации треков датасета (публичная часть):
- [2023-02-10-08-04-19-twilight](https://drive.google.com/file/d/1GcJ4jBFuT-Cr4MUTuZaqmX7WDgMNLLJ9/view?usp=share_link)
- [2023-02-21-07-28-58-day](https://drive.google.com/file/d/1BbbCDUx6DnWKaCIgaqZ0Vj9A4-D9WD4Q/view?usp=share_link)
- [2023-03-15-13-25-48-night](https://drive.google.com/file/d/1KiBpk1fBE6cF4BGFK0mPOmsonvB4vBtY/view?usp=share_link)

### Oxford RobotCar


Данные можно найти/использовать на следующих ресурсах:
- [Яндекс.Диск](https://disk.yandex.ru/d/0qq9cnrhlzU8Qg)
- [Kaggle](https://www.kaggle.com/datasets/creatorofuniverses/oxfordrobotcar-iprofi-hack-23)
- [Google Drive]()

sha256: `25c45eed9ce77a3a4ab9828754fb1945c358c34d67cc241d47ea0c61d236a620` pnvlad_oxford_robotcar.zip

todo

### NCLT

Данные можно найти/использовать на следующих ресурсах:
- [Яндекс.Диск](https://disk.yandex.ru/d/9wjyWKkWXe0vDQ)
- [Kaggle](https://www.kaggle.com/datasets/creatorofuniverses/nclt-iprofi-hack-23)
- [Google Drive]()

sha256: `6ca5dc27d4928b1cbe6c1959b87a539f1dd9bc1764220c53b6d5e406e8cef310` NCLT_preprocessed_small.zip

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
