from flask import Flask, render_template, request
import requests
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

# Danh sách các domain được phép
ALLOWED_DOMAINS = ['link4m.com', 'layma.net']

@app.route('/')
def home():
    # 1. Lấy thông tin Referer từ Header
    referer = request.headers.get('Referer', '')
    
    # 2. Kiểm tra xem Referer có chứa domain hợp lệ không
    # Logic: Nếu referer trống hoặc không chứa từ khóa trong whitelist -> Chặn
    is_valid_source = any(domain in referer for domain in ALLOWED_DOMAINS)
    
    # DEBUG: Nếu bạn muốn test trực tiếp mà không cần qua link rút gọn, 
    # hãy comment dòng if bên dưới lại. Khi deploy nhớ mở ra.
    if not is_valid_source:
         return render_template('index.html', error="Truy cập không hợp lệ! Vui lòng truy cập từ Link4M hoặc Layma.")

    # 3. Nếu hợp lệ, tiến hành lấy Key
    try:
        target_url = "https://tmggamecheat.fun/GETKEY/noapi.php"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Gọi link để lấy redirect
        response = requests.get(target_url, headers=headers, timeout=15, allow_redirects=True)
        final_url = response.url
        
        # Phân tích URL để lấy param 'key'
        parsed_url = urlparse(final_url)
        query_params = parse_qs(parsed_url.query)
        key_value = query_params.get('key', [None])[0]
        
        if key_value:
            # Trả về giao diện cùng với Key
            return render_template('index.html', key=key_value)
        else:
            return render_template('index.html', error="Không lấy được key từ hệ thống nguồn.")
            
    except Exception as e:
        return render_template('index.html', error=f"Lỗi hệ thống: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
