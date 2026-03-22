@echo off
chcp 65001 > nul
echo =====================================
echo  울산대학교 채용공고 생성기 서버 실행
echo =====================================
echo.
echo AI 기능을 사용하려면 이 서버가 필요합니다.
echo.
echo 브라우저에서 다음 주소로 접속하세요:
echo http://localhost:8000
echo.
echo 종료하려면 Ctrl+C를 누르세요.
echo =====================================
echo.

python server.py

pause
