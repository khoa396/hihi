from flask import Flask, render_template, request, session, redirect, url_for
import requests
from urllib.parse import urlparse, parse_qs
import os

app = Flask(__name__)

# CẤU HÌNH QUAN TRỌNG
# Token bí mật để xác thực từ Link4m
SECRET_TOKEN = "chuan-men-tmg-2026" 

# Khóa bí mật để mã hóa Session (bắt buộc phải có để lưu cookie)
# Bạn có thể gõ bừa một chuỗi ký tự dài ngẫu nhiên
app.secret_key = 'chuoi-ky-tu-ngau-nhien-bao-mat-cuc-cao-tmg-tool'

@app.route('/')
def home():
    # TRƯỜNG HỢP 1: Người dùng có Session (đã vượt link trước đó)
    # Nếu trong cookie đã lưu key, hiển thị lại key đó (F5 không bị mất, không tạo mới)
    if 'saved_key' in session:
        return render_template('index.html', key=session['saved_key'])

    # TRƯỜNG HỢP 2: Người dùng mới vào từ Link Rút Gọn (có Token trên URL)
    user_token = request.args.get('auth')

    if user_token == SECRET_TOKEN:
        # Token hợp lệ -> Tiến hành lấy Key mới
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
                # LƯU KEY VÀO SESSION (COOKIE)
                session['saved_key'] = key_value
                
                # QUAN TRỌNG: Chuyển hướng về trang chủ để XÓA URL PARAM (ẩn token)
                return redirect(url_for('home'))
            else:
                return render_template('index.html', error="Lỗi: Web nguồn không trả về key.")
                
        except Exception as e:
            return render_template('index.html', error=f"Lỗi kết nối: {str(e)}")

    # TRƯỜNG HỢP 3: Truy cập trực tiếp (không có Token, không có Session)
    return render_template('index.html', error="Vui lòng truy cập qua link rút gọn để lấy Key.")

# Route phụ để Reset (nếu người dùng muốn lấy Key mới)
@app.route('/reset')
def reset_session():
    session.pop('saved_key', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
