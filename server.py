#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
울산대학교 채용공고 생성기 프록시 서버
Anthropic API CORS 우회용
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.request
import sys

API_KEY = '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'

class ProxyHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # CORS 헤더 추가
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        SimpleHTTPRequestHandler.end_headers(self)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                text = data.get('text', '')
                
                # Anthropic API 호출
                request = urllib.request.Request(
                    'https://api.anthropic.com/v1/messages',
                    data=json.dumps({
                        'model': 'claude-sonnet-4-20250514',
                        'max_tokens': 1024,
                        'messages': [{
                            'role': 'user',
                            'content': f'''다음 채용공고 텍스트를 분석하여 JSON으로 추출하라.

텍스트:
{text}

JSON 형식 (정확히 이 형식으로만 출력):
{{"positionTitle":"","department":"","employmentType":"","headcount":"","startDate":"YYYY-MM-DD","deadline":"YYYY-MM-DD","position":"","salary":"","workHours":"","responsibilities":"","qualifications":"","preferences":"","documents":"","schedule":"","contact":""}}

규칙:
1. employmentType은 "정규직", "기간제", "무기계약직", "계약직" 중 하나
2. 날짜는 YYYY-MM-DD 형식
3. responsibilities, qualifications, preferences, documents, schedule 필드는 마크다운 리스트 형식으로 작성:
   - 여러 항목이 있으면 "- 항목1\\n- 항목2\\n- 항목3" 형식 사용
   - 번호가 있으면 "1. 항목1\\n2. 항목2\\n3. 항목3" 형식 사용
4. 반드시 JSON만 출력하고 다른 설명이나 마크다운 코드블록(```)을 사용하지 말 것'''
                        }]
                    }).encode('utf-8'),
                    headers={
                        'Content-Type': 'application/json',
                        'x-api-key': API_KEY,
                        'anthropic-version': '2023-06-01'
                    }
                )
                
                with urllib.request.urlopen(request) as response:
                    result = response.read()
                    
                    # 응답 로깅
                    print('API 응답:', result.decode('utf-8')[:200])
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(result)
                    
            except Exception as e:
                print('오류 발생:', str(e))
                error_response = json.dumps({
                    'error': {
                        'message': str(e),
                        'type': 'server_error'
                    }
                }).encode('utf-8')
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(error_response)
        else:
            SimpleHTTPRequestHandler.do_POST(self)

if __name__ == '__main__':
    PORT = 8000
    print('=' * 50)
    print('울산대학교 채용공고 생성기 서버 실행')
    print('=' * 50)
    print(f'\n서버 시작: http://localhost:{PORT}')
    print('\n브라우저에서 접속하세요:')
    print(f'  http://localhost:{PORT}\n')
    print('종료: Ctrl+C')
    print('=' * 50)
    
    server = HTTPServer(('', PORT), ProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n서버를 종료합니다.')
        sys.exit(0)
