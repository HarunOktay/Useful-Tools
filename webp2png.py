import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PIL import Image

class ImageConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Bir .webp dosyası seçin ve .png'ye dönüştürün.", self)
        layout.addWidget(self.label)

        self.btn_select = QPushButton('Resim Seç', self)
        self.btn_select.clicked.connect(self.select_image)
        layout.addWidget(self.btn_select)

        self.setLayout(layout)
        self.setWindowTitle('WebP to PNG Converter')
        self.setGeometry(300, 300, 300, 150)
    
    def select_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Bir .webp dosyası seçin", "", "WebP Files (*.webp);;All Files (*)", options=options)
        
        if file_path:
            self.convert_to_png(file_path)
    
    def convert_to_png(self, webp_image_path):
        try:
            img = Image.open(webp_image_path)
            png_image_path = webp_image_path.rsplit('.', 1)[0] + '.png'
            img.save(png_image_path, 'PNG')
            self.label.setText(f"Dönüştürüldü: {png_image_path}")
        except Exception as e:
            self.label.setText(f"Hata: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageConverter()
    ex.show()
    sys.exit(app.exec_())
