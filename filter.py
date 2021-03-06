from PIL import Image
import numpy as np
import click
from numpy import ndarray


class ImageProcessor:
    def __init__(self, image_data: ndarray, size: int, level: int):
        self.data = image_data
        self.size = ImageProcessor.validate_size(size)
        self.step = int(255 / ImageProcessor.validate_level(level))

    def process_image(self):
        """

        :return: Преобразованное изображение
        """
        height = len(self.data)
        width = len(self.data[1])
        for x in range(0, width, self.size):
            for y in range(0, height, self.size):
                average_color = self._get_average_color(x, y)
                self._set_gradation(average_color, x, y)
        return Image.fromarray(self.data)

    def _get_average_color(self, start_x, start_y):
        """
        :param start_x: Левый край блока
        :param start_y: Верхний край блока
        :return: Средний цвет блока пикселей
        """
        average_color_sum = self.data[start_x:start_x + self.size, start_y:start_y + self.size].sum() / 3
        average_color = int(average_color_sum // self.size ** 2)
        return average_color

    def _set_gradation(self, color, start_x, start_y):
        """
        Закрашивает блока пикселей, ближайшим к допустимому, серым цветом

        :param color: Цвет для поиска ближайшего серого
        :param start_x: Левый край блока
        :param start_y: Верхний край блока
        """
        self.data[start_x:start_x + self.size, start_y:start_y + self.size] = int(color // self.step) * self.step

    @staticmethod
    def validate_size(size):
        """
        Проверяет размер на корректность

        >>> ImageProcessor.validate_size(30)
        30

        >>> ImageProcessor.validate_size(-1)
        Traceback (most recent call last):
          ...
        ValueError: Size must be greater than 0.

        :param size: Размер для проверки
        :return: Корректный размер
        """
        if size <= 0:
            raise ValueError("Size must be greater than 0.")
        else:
            return size

    @staticmethod
    def validate_level(level):
        """
        Проверяет уровень на корректность

        >>> ImageProcessor.validate_level(30)
        30

        >>> ImageProcessor.validate_level(-1)
        Traceback (most recent call last):
          ...
        ValueError: Level must be greater than 0 and less than 255.

        >>> ImageProcessor.validate_level(256)
        Traceback (most recent call last):
          ...
        ValueError: Level must be greater than 0 and less than 255.

        :param level: Уровень для проверки
        :return: Корректный уровень
        """
        if level <= 0 or level > 255:
            raise ValueError("Level must be greater than 0 and less than 255.")
        else:
            return level


@click.command()
@click.option("-i", default="input.jpg", help="Input filename.")
@click.option("-o", default="output.jpg", help="Output filename.")
@click.option("--size", default=10, help="Size of mosaic.")
@click.option("--level", default=50, help="Number of colors")
def main(i, o, size, level):
    img = Image.open(i)
    image = np.array(img)

    result = ImageProcessor(image, size, level).process_image()
    result.save(o)


if __name__ == '__main__':
    main()
