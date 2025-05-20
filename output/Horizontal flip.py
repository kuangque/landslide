import cv2
import os

def horizontal_flip_image(image):
    """
    对图像进行水平翻转
    """
    return cv2.flip(image, 1)  # 1表示水平翻转

def horizontal_flip_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        img = cv2.imread(file_path)
        if img is None:
            print(f"跳过非图像文件: {filename}")
            continue

        flipped_img = horizontal_flip_image(img)

        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_folder, f"{name}_flipH{ext}")

        success = cv2.imwrite(output_path, flipped_img)
        if success:
            print(f"{filename} 水平翻转并保存至 {output_path}")
        else:
            print(f"保存失败: {output_path}")

if __name__ == "__main__":
    input_folder = r"input"       # 原图路径
    output_folder = r"output"      # 输出路径

    horizontal_flip_images_in_folder(input_folder, output_folder)
