# download_docs.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

base_url = "https://modelon-impact-client.readthedocs.io/en/stable/"
output_dir = "modelon_docs"

# 폴더 생성
os.makedirs(output_dir, exist_ok=True)

# 메인 페이지에서 모든 링크 추출
try:
    response = requests.get(base_url, timeout=10)
    response.raise_for_status()
except Exception as e:
    print(f"초기 페이지 로드 실패: {e}")
    exit(1)

soup = BeautifulSoup(response.content, 'html.parser')

# 문서 내의 모든 링크 찾기
links = set()
base_domain = urlparse(base_url).netloc
for link in soup.find_all('a', href=True):
    url = urljoin(base_url, link['href'])
    url_without_fragment = url.split('#')[0]
    parsed = urlparse(url_without_fragment)

    if parsed.netloc == base_domain and url_without_fragment.endswith('.html'):
        links.add(url_without_fragment)

# 각 페이지 다운로드
links = sorted(list(links))
for i, url in enumerate(links):
    try:
        print(f"[{i+1}/{len(links)}] 다운로드 중: {url}")
        page = requests.get(url, timeout=10)
        page.raise_for_status()

        filename = urlparse(url).path.split('/')[-1]
        if not filename:
            filename = f"page_{i}.html"

        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page.text)
    except Exception as e:
        print(f"오류: {url} - {e}")

print("완료!")
