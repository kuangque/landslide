import cv2
import os

def vertical_flip_image(image):
    """
    对图像进行垂直翻转
    """
    return cv2.flip(image, 0)  # 0表示垂直翻转

def vertical_flip_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        img = cv2.imread(file_path)
        if img is None:
            print(f"跳过非图像文件: {filename}")
            continue

        flipped_img = vertical_flip_image(img)

        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_folder, f"{name}_flipV{ext}")

        success = cv2.imwrite(output_path, flipped_img)
        if success:
            print(f"{filename} 垂直翻转并保存至 {output_path}")
        else:
            print(f"保存失败: {output_path}")

if __name__ == "__main__":
    input_folder = r"input"       # 原图路径
    output_folder = r"output"      # 输出路径
    vertical_flip_images_in_folder(input_folder, output_folder)
