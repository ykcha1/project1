# download_docs.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
from collections import deque

base_url = "https://modelon-impact-client.readthedocs.io/en/stable/"
output_dir = "modelon_docs"

# 폴더 생성
os.makedirs(output_dir, exist_ok=True)

# BFS로 모든 페이지 다운로드
visited_urls = set()
queue = deque([base_url])
base_domain = urlparse(base_url).netloc
total_count = 0

while queue:
    url = queue.popleft()

    # 이미 방문한 URL은 건너뛰기
    if url in visited_urls:
        continue

    visited_urls.add(url)
    total_count += 1

    try:
        print(f"[{total_count}] 다운로드 중: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # HTML 파일 저장
        filename = urlparse(url).path.split('/')[-1]
        if not filename or not filename.endswith('.html'):
            filename = f"page_{total_count}.html"

        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)

        # 현재 페이지에서 새로운 링크 추출
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            new_url = urljoin(url, link['href'])
            new_url_without_fragment = new_url.split('#')[0]
            parsed = urlparse(new_url_without_fragment)

            # 같은 도메인의 HTML 링크만 큐에 추가
            if (parsed.netloc == base_domain and
                new_url_without_fragment.endswith('.html') and
                new_url_without_fragment not in visited_urls):
                queue.append(new_url_without_fragment)

    except Exception as e:
        print(f"오류: {url} - {e}")

print(f"완료! 총 {len(visited_urls)}개 페이지 다운로드됨")
