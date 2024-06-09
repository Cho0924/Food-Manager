#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
import time
from math import sqrt
from matplotlib import pyplot as plt

import os
from PIL import Image
import pyocr

#組み込み方説明
# process関数以外は全てOCR処理の各ステップを定義した関数で、気にしなくていい
# 一番下のprocess関数は、引数のimage_pathにカメラから取った画像のパスを入れる
# vegetabel_databaseには野菜のデータベースのリストを入れる。
# process関数の返り値としては、抽出した野菜の名前が入ったリストが返ってくる。
# １４３行目と１４６行目のパスには,ダウロードしたtesseractのフォルダのパスとtesseract.exeのパスをそれぞれ入れる


def sub_color(img, K):
    #画像を一次元の配列に変換して各ピクセルのBGR値をfloat32型で取得（後でk-means法で減色処理をするための前準備）
    pixels = img.reshape(-1, 3).astype(np.float32)
    #k-means法に関する設定
    criteria = cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 10, 1.0
    attempts = 10
    flags = cv2.KMEANS_RANDOM_CENTERS
    #k-means法で減色を実行し、減色後の画像を作成
    _, labels, centers = cv2.kmeans(pixels, K, None, criteria, attempts, flags)
    sub_color_img = centers[labels].reshape(img.shape).astype(np.uint8)
    #処理結果を表示
    # plot_orig_img(sub_color_img)
    return sub_color_img

def plot_histgram(img):
    #ヒストグラムを計算
    hist = cv2.calcHist([img], [0], None, [256], [0,256])
    #histgramを描画
    # plt.figure()
    # plt.bar([i for i in range(0,256)], hist.ravel())
    # plt.show()

def binarize(img):
    #グレースケール（RGB値を画像から取り除き、明るさの値だけにする）
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold = np.unique(np.array(gray_img).ravel())[-2] -1  # 白側から2色の位置で閾値を置く
    # plot_orig_img(gray_img)
    #白黒の二値画像に変換（閾値を決め、グレー画像の各ピクセルについて、明るさの値が閾値以上だったら白、未満だったら黒とする）
    _, binary_img = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY)
    # plot_orig_img(binary_img)
    return gray_img, binary_img


def find_contours(img):
    #二値画像から輪郭を判断する（返り値は、輪郭の各点の座標値が入ったリスト）
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def approximate_contours(img, contours):
    height, width, _ = img.shape
    img_size = height * width
    approx_contours = []
    for i, cnt in enumerate(contours):
        #輪郭に囲まれた部分の周長と面積
        arclen = cv2.arcLength(cnt, True)
        area = cv2.contourArea(cnt)
        #周長が0でなく、かつ面積が画像の面積の2～90％以内の時、近似処理を行う。
        if arclen != 0 and img_size*0.02 < area < img_size*0.9:
            #ダグラスペッカー法を使って、多角形を四角形に近似（矯正）している。近似の為の許容誤差はepsilon(周長の1％)
            approx_contour = cv2.approxPolyDP(cnt, epsilon=0.01*arclen, closed=True)
            # print('approx_contour')
            # print(approx_contour)
            if len(approx_contour) == 4:  # 四角形として検知できていない場合は無視する
                approx_contours.append(approx_contour)
    return approx_contours


def draw_contours(img, contours):
    draw_contours_file = cv2.drawContours(img.copy(), contours, -1, (0, 0, 255, 255), 10)
    #輪郭を画像上に表示
    # plot_orig_img(draw_contours_file)


def plot_orig_img(img):
    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()
    #cv2.imwrite('./{}.png'.format(time.time()), img)

def save_crop_img(img, contours):
    # 輪郭に囲まれた領域を切り取って保存する
    x, y, w, h = cv2.boundingRect(contours[0])
    crop_img = img[y:y+h, x:x+w]
    # cv2.imwrite('output.jpg', crop_img)
    #一応pythonの方でも表示させておく
    # plot_orig_img(crop_img)
    # plt.imshow(cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))
    # plt.show()

def projective_transformation(img_path, contours):
    r1 = sqrt((contours[0][0][0][0])**2 + (contours[0][0][0][1])**2)
    r2 = sqrt((contours[0][1][0][0])**2 + (contours[0][1][0][1])**2)
    r3 = sqrt((contours[0][2][0][0])**2 + (contours[0][2][0][1])**2)
    r4 = sqrt((contours[0][3][0][0])**2 + (contours[0][3][0][1])**2)
    r = [r1, r2, r3, r4]
    numr = r.index(max(r))
    point = []
    point.append(contours[0][(numr+1)%4][0])
    point.append(contours[0][(numr+2)%4][0])
    point.append(contours[0][(numr+3)%4][0])
    point.append(contours[0][numr%4][0])

    side1 = sqrt((point[0][0]- point[1][0])**2 + (point[0][1] - point[1][1])**2)
    side2 = sqrt((point[1][0]- point[2][0])**2 + (point[1][1] - point[2][1])**2)
    side3 = sqrt((point[2][0]- point[3][0])**2 + (point[2][1] - point[3][1])**2)
    side4 = sqrt((point[3][0]- point[0][0])**2 + (point[3][1] - point[0][1])**2)
    width = int((side1 + side3) / 2)
    height = int((side2 + side4) / 2)
    #pts1はカードの4辺、pts2は変換後の座標
    pts1 = np.float32([point[1], point[0], point[2], point[3]])
    pts2 = np.float32([[0,0], [width,0], [0,height], [width,height]])
    #射影変換を実施
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img_path, M, (width, height))
    #ファイル書き出し
    output_image_path = "output_image.jpg"
    cv2.imwrite(output_image_path, dst)
    #pythonでの表示
    plot_orig_img(dst)
    return output_image_path
    

#def get_receipt_contours(img, K):
# sub_color_img = sub_color(img, K)
# gray_img, binary_img = binarize(sub_color_img)
# contours = find_contours(binary_img)
# plot_histgram(gray_img)
# approx_contours = approximate_contours(img, contours)
# draw_contours(img, approx_contours)



#Tesseract-OCRをダウンロードする必要がある

# path = "/Users/debunhiroto/opt/anaconda3/pkgs/tesseract-5.2.0-he9d5cce_0"#@山下　ここには、Tesseract-OCRファイルのダウンロード先のパスを入れる
# os.environ['PATH'] = os.environ['PATH'] + path

# pyocr.tesseract.TESSERACT_CMD = "/Users/debunhiroto/opt/anaconda3/pkgs/tesseract-5.2.0-he9d5cce_0/bin/tesseract" #@山下　ここには、Tesseract-OCRの中にあるtesseract.exeのパスを入れる
tools = pyocr.get_available_tools()
tool = tools[0]
# print(tool)

#読み取り精度の設定（tesseract_layoutで設定できる）
builder = pyocr.builders.TextBuilder(tesseract_layout=6)

#OCRをする関数 引数には画像のパスを入れる。文字列を返す
def ocr(img_path):
    #画像ファイルパスの指定
    img = Image.open(img_path)
    #文字を読み取る
    text = tool.image_to_string(img, lang="jpn", builder=builder)
    return text

#OCRで読み取った文字列の中から、データベースに登録してある野菜の名前を抜き出して、リストとして返す

def read_food_name(database, receipt_data):
    food_list = []
    #databaseの各単語について、レシートの中にあるかどうか確認する
    for i in range(len(database)):
        word_len = len(database[i])
        #もしdatabaseの単語の最初の文字がreceiptデータのなかにあるならば。。。
        idx = 0
        idx2 = 0
        if database[i][0] in receipt_data:
            while True:
                #今確かめている単語の最初の文字は、receipt_dataの方では何番目の要素か
                idx2 = idx
                idx = receipt_data.find(database[i][0], idx2+1)
                if idx == -1:
                    break
                #1文字ずつ、databaseの単語とreceiptの文字を比較し、同じでないものが出たらflagをfalseにする
                flag = True
                x = 0           #receipt_data を走査
                y = 0           #database を走査
                while True:
                    if y >= word_len:
                        break
                    if (idx+word_len) > len(receipt_data):
                        flag = False
                        break
                    if database[i][y] != receipt_data[idx+x]:
                        if receipt_data[idx+x] != ' ':
                            flag = False
                            break    
                    else :
                        y +=1
                    x +=1
                if flag == True:
                    food_list.append(i)

    return food_list

def process(image_path, vegetable_database):
    input_file = cv2.imread(image_path)
    plt.imshow(cv2.cvtColor(input_file, cv2.COLOR_BGR2RGB))
    plt.show()
    sub_color_img = sub_color(input_file, 5)
    gray_img, binary_img = binarize(sub_color_img)
    contours = find_contours(binary_img)
    # print(contours)
    plot_histgram(gray_img)
    approx_contours = approximate_contours(input_file, contours)
    print(approx_contours)
    draw_contours(input_file, approx_contours)
    # save_crop_img(input_file, approx_contours)
    output_image_path = projective_transformation(input_file,approx_contours)
    receipt_data = ocr(output_image_path) #output_iamge_nameは同じディレクトリの画像パスにする（画像の名前）
    print(receipt_data)
    food_list = read_food_name(vegetable_database, receipt_data)
    return food_list



