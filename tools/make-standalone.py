#!/usr/bin/env python3
"""Generate standalone HTML files with all local images embedded as base64 data URIs.
Output files go to dist/ directory, ready for single-file upload."""

import base64, re, os, sys, mimetypes

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(SRC_DIR, 'dist')

FILES_TO_PROCESS = [
    'FoneSquare-PRD-v2.html',
    'fonesquare-login.html',
    'fonesquare-kyc.html',
]

def img_to_base64(filepath):
    mt = mimetypes.guess_type(filepath)[0] or 'image/png'
    with open(filepath, 'rb') as f:
        return f'data:{mt};base64,{base64.b64encode(f.read()).decode()}'

def process_html(filename):
    filepath = os.path.join(SRC_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    replaced = 0

    def replace_local_ref(m):
        nonlocal replaced
        attr = m.group(1)   # src or href
        quote = m.group(2)  # " or '
        path = m.group(3)   # the path
        
        if path.startswith(('http://', 'https://', 'data:', '#', 'javascript:')):
            return m.group(0)
        
        full_path = os.path.join(SRC_DIR, path)
        if not os.path.isfile(full_path):
            return m.group(0)
        
        ext = os.path.splitext(path)[1].lower()
        if ext in ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico'):
            b64 = img_to_base64(full_path)
            replaced += 1
            return f'{attr}={quote}{b64}{quote}'
        
        return m.group(0)

    html = re.sub(
        r'(src|href)=(["\'])([^"\']+)\2',
        replace_local_ref,
        html
    )

    out_path = os.path.join(DIST_DIR, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    size_kb = os.path.getsize(out_path) / 1024
    print(f"  ✅ {filename} → dist/{filename}  ({size_kb:.0f} KB, {replaced} images embedded)")
    return replaced

def main():
    os.makedirs(DIST_DIR, exist_ok=True)
    
    print("🔧 生成独立 HTML 文件...\n")
    
    total_images = 0
    for f in FILES_TO_PROCESS:
        src = os.path.join(SRC_DIR, f)
        if not os.path.isfile(src):
            print(f"  ⚠️  {f} 不存在，跳过")
            continue
        total_images += process_html(f)
    
    print(f"\n📦 输出目录: dist/")
    print(f"   共内嵌 {total_images} 张图片")
    
    print("\n📋 上传说明:")
    print("   • 每个 HTML 文件都是完全独立的，可以单独上传")
    print("   • 图片已内嵌为 base64，无需额外上传 assets/")
    print("   • 外部 CDN（Google Fonts、Mermaid.js）需要网络访问")
    print("   • 三个文件之间的跳转链接仅在同目录上传时有效\n")

if __name__ == '__main__':
    main()
