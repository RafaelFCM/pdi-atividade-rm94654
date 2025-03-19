# Aluno: Rafael Fiel Cruz Miranda
# RM: 94654 = soma 24 = soma 6 -> vídeo q1B.mp4
# Turma: 3SIR

import cv2
import numpy as np

# Função para verificar se dois retângulos colidem
def colisao(x1, y1, w1, h1, x2, y2, w2, h2):
    # Verifica se há sobreposição entre os retângulos
    return (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2)

# Função para verificar se uma forma ultrapassou a barreira
def passou_barreira(y1, h1, y2):
    # Verifica se a forma 2 ultrapassou a forma 1
    return y2 > y1 + h1

# Função principal para processar o vídeo
def processar_video(video_path):
    # Abre o vídeo
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    # Variável para controlar se a colisão já ocorreu
    colisao_ocorreu = False

    # Ajusta o tempo de espera para acelerar o vídeo
    fps = cap.get(cv2.CAP_PROP_FPS)
    tempo_espera = int(1000 / fps)  # Tempo original por frame
    tempo_espera = int(tempo_espera / 10)  # Ajuste para 10x de velocidade

    while True:
        # Lê o próximo frame do vídeo
        ret, frame = cap.read()

        if not ret:
            print("Fim do vídeo ou erro ao ler o frame.")
            break

        # Redimensiona o frame para melhorar a performance
        frame = cv2.resize(frame, (1200, 700))

        # Converte o frame para o espaço de cores HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define os intervalos de cores para azul e creme
        # Azul
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])

        # Creme
        lower_cream = np.array([10, 100, 100])
        upper_cream = np.array([25, 255, 255])

        # Cria máscaras para as cores azul e creme
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_cream = cv2.inRange(hsv, lower_cream, upper_cream)

        # Encontra os contornos das formas azuis
        contornos_azul, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Encontra os contornos das formas creme
        contornos_creme, _ = cv2.findContours(mask_cream, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Variáveis para armazenar os maiores contornos
        maior_contorno_azul = None
        maior_area_azul = 0
        maior_contorno_creme = None
        maior_area_creme = 0

        # Encontra o maior contorno azul
        for contorno in contornos_azul:
            area = cv2.contourArea(contorno)
            if area > maior_area_azul:
                maior_area_azul = area
                maior_contorno_azul = contorno

        # Encontra o maior contorno creme
        for contorno in contornos_creme:
            area = cv2.contourArea(contorno)
            if area > maior_area_creme:
                maior_area_creme = area
                maior_contorno_creme = contorno

        # Desenha retângulos ao redor das formas detectadas
        if maior_contorno_azul is not None:
            x_azul, y_azul, w_azul, h_azul = cv2.boundingRect(maior_contorno_azul)
            cv2.rectangle(frame, (x_azul, y_azul), (x_azul + w_azul, y_azul + h_azul), (0, 255, 0), 2)

        if maior_contorno_creme is not None:
            x_creme, y_creme, w_creme, h_creme = cv2.boundingRect(maior_contorno_creme)
            cv2.rectangle(frame, (x_creme, y_creme), (x_creme + w_creme, y_creme + h_creme), (0, 165, 255), 2)

            # Verifica se houve colisão entre as formas
            if maior_contorno_azul is not None:
                if colisao(x_azul, y_azul, w_azul, h_azul, x_creme, y_creme, w_creme, h_creme):
                    cv2.putText(frame, "COLISAO DETECTADA", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    colisao_ocorreu = True

                # Verifica se a forma creme ultrapassou a barreira após a colisão
                if colisao_ocorreu and passou_barreira(y_azul, h_azul, y_creme):
                    cv2.putText(frame, "PASSOU BARREIRA", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Exibe o frame processado
        cv2.imshow("Video Processado", frame)

        # Verifica se a tecla 'ESC' foi pressionada para sair
        key = cv2.waitKey(tempo_espera) & 0xFF
        if key == 27:
            break

    # Libera os recursos
    cap.release()
    cv2.destroyAllWindows()

# Caminho do vídeo
video_path = "q1/q1B.mp4"
processar_video(video_path)