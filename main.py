import cv2
import numpy as np


def get_image_data_from(path, show=False):
    """
    Retornara se possui circulos e quadrados e a quantidade de cada m em relacao ao domino
    :param show: mostrar imagens em uma janela
    :param path: endereco da imagem
    :return:  has_circle (bool), has_square (bool), up_count (int), down_count (int)
    """
    has_circle = False
    has_square = False
    up_count = 0
    down_count = 0

    # gambiarra para desenhar em cima
    empty = cv2.imread("imgs/Domino-empty.jpg")

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img_height = img.shape[0] * 0.95  # TODO: remover isso quando conseguir cortar a imagem

    _, threshold = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    # suave = cv2.GaussianBlur(img, (1, 1), 0)
    # canny1 = cv2.Canny(suave, 20, 120)
    # contours_1, ref = cv2.findContours(canny1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_1, ref = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours_1:
        # TODO: estudar como cortar a imagem no retangulo maior
        # area = cv2.contourArea(cnt)
        # x, y, w, h = cv2.boundingRect(cnt)
        #
        # if area > 0:
        #     print(area, x, y, w, h)
        #
        #     # Retângulos ao redor de cada formato
        #     cv2.rectangle(copia, (x, y), (x + w, y + h), (0, 0, 255), 3)
        #     mostrar_imagem_cv(copia)
        #
        #     # Grab Cut
        #     rect = (x, y, w, h)
        #     cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        #
        #     mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        #     gc = img.copy() * mask2[:, :, np.newaxis]
        #     mostrar_imagem_cv(gc)
        #
        area = cv2.contourArea(cnt)
        # remove os grandes ou pequenos emais para serrem os circulo ou quadrados
        if area > 500 or area < 100:
            continue

        # TODO: implementar esse aqui
        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if y <= img_height / 2:
            up_count += 1
        else:
            down_count += 1

        if len(approx) == 4:
            # Quadrado
            has_square = True
        else:
            # Circulo
            has_circle = True

        cv2.drawContours(empty, [approx], 0, 0, 1)

    if show:
        print("Tem circulos: %s \n"
              "Tem quadrados: %s \n"
              "N. topo: %s \n"
              "N. base: %s " %
              (
                  ("Sim" if has_circle else "Nao"),
                  ("Sim" if has_square else "Nao"),
                  str(up_count),
                  str(down_count)
              )
              )
        cv2.imshow("shapes", empty)
        # # cv2.imshow("Threshold", threshold)
        # # cv2.imshow("canny1", canny1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return has_circle, has_square, up_count, down_count


if __name__ == '__main__':
    # print(get_image_data_from(
    #     "imgs/Domino-bonus.png",
    #     show=True)
    # )

    print(get_image_data_from(
        "imgs/Domino2.png",
        show=True)
    )
