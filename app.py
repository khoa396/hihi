from flask import Flask, render_template, request
import requests
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

# Đặt một mã bí mật của riêng bạn
SECRET_TOKEN = "chuan-men-tmg-2026"

@app.route('/')
def home():
    # 1. Kiểm tra Token trên URL thay vì Referer
    # Người dùng phải truy cập: domain.vercel.app/?auth=chuan-men-tmg-2026
    user_token = request.args.get('auth')

    # Nếu token không khớp, hiển thị lỗi và hướng dẫn debug
    if user_token != SECRET_TOKEN:
         # Lấy thử referer để bạn xem tại sao cách cũ không chạy (chỉ để hiển thị lỗi)
         debug_referer = request.headers.get('Referer', 'Không có Referer')
         return render_template(
             'index.html', 
             error=f"Truy cập bị từ chối! Token không hợp lệ.<br>Debug Referer nhận được: {debug_referer}"
         )

    # 2. Nếu Token đúng, tiến hành lấy Key ngay lập tức
    try:
        target_url = "https://tmggamecheat.fun/GETKEY/noapi.php"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(target_url, headers=headers, timeout=15, allow_redirects=True)
        final_url = response.url
        
        parsed_url = urlparse(final_url)
        query_params = parse_qs(parsed_url.query)
        key_value = query_params.get('key', [None])[0]
        
        if key_value:
            return render_template('index.html', key=key_value)
        else:
            return render_template('index.html', error="Web nguồn không trả về key.")
            
    except Exception as e:
        return render_template('index.html', error=f"Lỗi backend: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
