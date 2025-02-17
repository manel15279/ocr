import easyocr
from PIL import Image, ImageEnhance
import cv2
import numpy as np

class OCR():
    def __init__(self, contrast_ths=0.1, adjust_contrast=0.35):
        self.reader = easyocr.Reader(["ar", 'en'])
        self.contrast_ths = contrast_ths
        self.adjust_contrast = adjust_contrast

    # def concatenate_ocr_results(self, result):
    #     """Concatenates recognized text from OCR result in one variable"""
    #     for detection in result:
    #         text = detection[1]
    #         all_text += text + "\n" 
    #         return all_text.strip()


    def extract_text(self, image_path):
        """Extracts text from an image using EasyOCR"""
        img = cv2.imread(image_path)
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Contrast(pil_img)
        enhanced_img = enhancer.enhance(2.0)
        enhanced_img_cv = cv2.cvtColor(np.array(enhanced_img), cv2.COLOR_RGB2BGR)

        result = self.reader.readtext(enhanced_img_cv, contrast_ths=self.contrast_ths, adjust_contrast=self.adjust_contrast, paragraph=True)
        
        # Extract text from the OCR result
        text = "\n".join([item[1] for item in result])  # item[1] contains the recognized text
        
        return text
