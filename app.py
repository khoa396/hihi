from flask import Flask, render_template, jsonify
import requests
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

# Route trang chủ
@app.route('/')
def home():
    return render_template('index.html')

# API xử lý lấy key
@app.route('/get-key', methods=['POST'])
def get_key():
    try:
        # URL gốc
        target_url = "https://tmggamecheat.fun/GETKEY/noapi.php"
        
        # Headers giả lập trình duyệt để tránh bị chặn (nếu có)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Gọi request
        response = requests.get(target_url, headers=headers, timeout=15, allow_redirects=True)
        
        # Lấy URL cuối cùng
        final_url = response.url
        
        # Phân tích URL để lấy key
        parsed_url = urlparse(final_url)
        query_params = parse_qs(parsed_url.query)
        key_value = query_params.get('key', [None])[0]
        
        if key_value:
            return jsonify({'success': True, 'key': key_value})
        else:
            # Logic dự phòng nếu key không nằm trong param (phòng khi web thay đổi)
            return jsonify({'success': False, 'error': 'Không tìm thấy key. URL trả về: ' + final_url})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Dòng này chỉ để chạy dưới local, Vercel sẽ bỏ qua dòng này và tự import app
if __name__ == '__main__':
    app.run(debug=True)