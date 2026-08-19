#!/usr/bin/env python3
"""PyPI 收尾自动化: 账号注册后(用户已点完 hCaptcha) 跑这个脚本.
1) IMAP 收 PyPI 验证邮件并点链接  2) 登录  3) 创建 API token  4) 存凭据
然后运行 publish_pypi.sh 完成发布.
用法: ~/quant_research/mcp_venv/bin/python pypi_finish.py
"""
import json, os, re, sys, time, imaplib, email

CFG = json.load(open(os.path.expanduser('~/quant_research/push_config.json')))
EMAIL = CFG['user']; AUTH = CFG['auth_code']
CRED = os.path.expanduser('~/Desktop/账号凭证/pypi_credential.txt')
PW = open('/tmp/pypi_pw.txt').read().strip()

import requests
s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36'

def get_csrf(url):
    r = s.get(url, timeout=30)
    m = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', r.text, re.S)
    return m.group(1) if m else None

def fetch_verify_link(timeout=180):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            M = imaplib.IMAP4_SSL('imap.qq.com', 993)
            M.login(EMAIL, AUTH); M.select('INBOX')
            typ, data = M.search(None, 'ALL')
            for i in reversed(data[0].split()[-15:]):
                typ, msg = M.fetch(i, '(RFC822)')
                m = email.message_from_bytes(msg[0][1])
                if 'pypi' not in (m.get('From','') or '').lower():
                    continue
                body = ''
                if m.is_multipart():
                    for part in m.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True).decode(errors='ignore'); break
                else:
                    body = m.get_payload(decode=True).decode(errors='ignore')
                urls = re.findall(r'https://pypi\.org/account/[a-z0-9/_-]+', body)
                if urls:
                    M.logout(); return urls[0]
            M.logout()
        except Exception as e:
            print('imap:', repr(e)[:100])
        time.sleep(6)
    return None

link = fetch_verify_link()
if not link:
    print('未找到验证邮件 (确认账号已创建; 若刚点提交请等1-2分钟再跑)')
    sys.exit(1)
print('验证链接:', link)
r = s.get(link, timeout=30)
print('验证状态:', r.status_code)

# 登录
csrf = get_csrf('https://pypi.org/account/login/')
r = s.post('https://pypi.org/account/login/',
           data={'csrf_token': csrf, 'username': 'imprint-pdf', 'password': PW},
           allow_redirects=True, timeout=40)
print('登录状态:', r.status_code)

def create_token(scope, project=None):
    csrf = get_csrf('https://pypi.org/manage/account/token/')
    data = {'csrf_token': csrf, 'name': 'imprint-pdf publish', 'scope': scope}
    if project:
        data['project'] = project
    r = s.post('https://pypi.org/manage/account/token/', data=data, allow_redirects=True, timeout=40)
    m = re.search(r'pypi-[A-Za-z0-9_\-]+', r.text)
    return m.group(0) if m else None

token = create_token('project', 'imprint-pdf') or create_token('all-projects')
if not token:
    print('token 创建失败'); sys.exit(1)
with open(CRED, 'w') as f:
    f.write(f'USER=imprint-pdf\nEMAIL={EMAIL}\nPASSWORD={PW}\nPYPI_TOKEN={token}\n')
os.chmod(CRED, 0o600)
print('凭据已存:', CRED)
print('下一步: bash publish_pypi.sh')
