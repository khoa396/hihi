from flask import Flask, render_template, jsonify
from urllib.parse import quote

app = Flask(__name__)

# CẤU HÌNH API KEY (Giấu ở đây, không lộ ra HTML)
LINK4M_API = "67fe08df2741353b9475dd73"
LAYMA_TOKEN = "b8b60726e4ebf47ffe41df8a8d96c869"
TARGET_URL = "https://tmggamecheat.fun/GETKEY/noapi.php"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-link', methods=['POST'])
def generate_link():
    try:
        # --- BƯỚC 1: TẠO LINK LỚP TRONG (LINK4M) ---
        # Mã hóa target url để nó trở thành 1 tham số an toàn
        # Ví dụ: https://... trở thành https%3A%2F%2F...
        target_encoded = quote(TARGET_URL)
        
        # Tạo link Link4m hoàn chỉnh
        # Link4m Quick Link format: https://link4m.co/st?api={API}&url={TARGET}
        link4m_url = f"https://link4m.co/st?api={LINK4M_API}&url={target_encoded}"

        # --- BƯỚC 2: TẠO LINK LỚP NGOÀI (LAYMA) ---
        # Bây giờ link4m_url lại đóng vai trò là "target" của Layma
        # Nên ta phải mã hóa link4m_url một lần nữa
        link4m_encoded = quote(link4m_url)

        # Tạo link Layma hoàn chỉnh
        # Layma Quick Link format: https://api.layma.net/.../quicklink?tokenUser={TOKEN}&url={LINK4M_ENCODED}
        final_link = f"https://api.layma.net/api/admin/shortlink/quicklink?tokenUser={LAYMA_TOKEN}&url={link4m_encoded}"

        return jsonify({'success': True, 'url': final_link})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
