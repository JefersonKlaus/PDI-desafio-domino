import numpy as np
from copy import copy


def find_objects(img):
    """
    Percorre a imagem e rotarna posicao dos objetos encontrados e sua area
    :param img:
    :return:
    """
    to_result = []
    _img = copy(img)

    for row in range(0, len(_img)):
        for col in range(0, len(_img[row])):
            if _img[row][col] == 255:
                continue
            else:
                to_result.append(_get_object(_img, row, col))

    return to_result


def _get_object(_img, row, col, _object=None):
    """
    Pega o objeto e o remove da imagem original
    :param _img:
    :param row:
    :param col:
    :param _object:
    :return:
    """
    size = _img.shape

    if row < 0:
        return None
    if col < 0:
        return None
    if row >= size[0]:
        return None
    if col >= size[1]:
        return None

    if not _object:
        object_to_result = {
            "area": 0,
            "square": {
                "top": size[0],
                "down": 0,
                "left": size[1],
                "right": 0
            }
        }
    else:
        object_to_result = _object

    if _img[row][col] == 0:
        object_to_result["area"] += 1
        object_to_result["square"]["top"] = row if row < object_to_result["square"]["top"] else \
            object_to_result["square"]["top"]

        object_to_result["square"]["down"] = row if row > object_to_result["square"]["down"] else \
            object_to_result["square"]["down"]

        object_to_result["square"]["left"] = col if col < object_to_result["square"]["left"] else \
            object_to_result["square"]["left"]

        object_to_result["square"]["right"] = col if col > object_to_result["square"]["right"] else \
            object_to_result["square"]["right"]

        _img[row][col] = 255

    else:
        return None

    _get_object(_img, row + 1, col, object_to_result)
    _get_object(_img, row, col + 1, object_to_result)
    _get_object(_img, row - 1, col, object_to_result)
    _get_object(_img, row, col - 1, object_to_result)

    return object_to_result


def sobel_operator(img):
    container = np.copy(img)
    size = container.shape

    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            gx = (img[row - 1][col - 1] + 2 * img[row][col - 1] + img[row + 1][col - 1]) - \
                 (img[row - 1][col + 1] + 2 * img[row][col + 1] + img[row + 1][col + 1])

            gy = (img[row - 1][col - 1] + 2 * img[row - 1][col] + img[row - 1][col + 1]) - \
                 (img[row + 1][col - 1] + 2 * img[row + 1][col] + img[row + 1][col + 1])
            container[row][col] = min(255, np.sqrt(gx ** 2 + gy ** 2))
    return container


def remove_lines(img, size):
    """
    Remove linhas e retorna instancia nova
    :param img:
    :param size: largura maxima da linha a ser removida
    :return:
    """
    _img = np.copy(img)
    # eh processado duas vezes para remover "esquinas"
    for row in range(0, len(_img)):
        for col in range(0, len(_img[row])):
            _img[row][col] = 255 if _is_col(_img, row, col, size) else _img[row][col]

    for row in range(0, len(_img)):
        for col in range(0, len(_img[row])):
            _img[row][col] = 255 if _is_row(_img, row, col, size) else _img[row][col]
    return _img


def _is_row(img, row, col, limit):
    """
    Retorna se o pixel eh uma linha (apenas utilizar este metodo em ambiente controlado)
    :param img: Imagem
    :param row:
    :param col:
    :param limit: considera apenas se for menor que LIMIT
    :return:
    """
    _limit = limit - 1
    _up = 1
    _down = 1

    # valida altura menor que SIZE
    try:
        while img[row + _up][col] == 0:
            _limit -= 1
            _up += 1

            if _limit < 0:
                return False
    except:
        pass

    try:
        while img[row - _down][col] == 0:
            _limit -= 1
            _down += 1

            if _limit < 0:
                return False
    except:
        pass

    try:
        if img[row][col - 1] == 255:
            left = False
        else:
            left = True
    except:
        left = False

    try:
        if img[row][col + 1] == 255:
            right = False
        else:
            right = True
    except:
        right = False

    return (left or right) or (not left and not right)


def _is_col(img, row, col, limit):
    """
    Retorna se o pixel eh uma coluna (apenas utilizar este metodo em ambiente controlado)
    :param img: Imagem
    :param row:
    :param col:
    :param limit: considera apenas se for menor que LIMIT
    :return:
    """
    _limit = limit - 1
    _up = 1
    _down = 1

    # valida altura menor que SIZE
    try:
        while img[row][col + _up] == 0:
            _limit -= 1
            _up += 1

            if _limit < 0:
                return False
    except:
        pass

    try:
        while img[row][col - _down] == 0:
            _limit -= 1
            _down += 1

            if _limit < 0:
                return False
    except:
        pass

    try:
        if img[row - 1][col] == 255:
            left = False
        else:
            left = True
    except:
        left = False

    try:
        if img[row + 1][col] == 255:
            right = False
        else:
            right = True
    except:
        right = False

    return (left or right) or (not left and not right)
