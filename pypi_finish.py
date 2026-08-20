#!/usr/bin/env python3
"""PyPI 自动化收尾 (已实测可用, 2026-08-20):
登录(含 2FA TOTP) → 创建 API token → 存凭据 → 之后跑 publish_pypi.sh 发布.
用法: ~/quant_research/mcp_venv/bin/python pypi_finish.py
前提: 账号已注册+邮箱已验证+2FA 已启用 (TOTP_SECRET 正确).
"""
import base64, hashlib, hmac, json, os, re, struct, sys, time
import requests

CFG = json.load(open(os.path.expanduser('~/quant_research/push_config.json')))
EMAIL = CFG['user']
PW = open('/tmp/pypi_pw.txt').read().strip()
TOTP_SECRET = os.environ.get('PYPI_TOTP_SECRET', 'J6COZFJTKU74E24NBM2BJSLYIKI5TGVR')
CRED = os.path.expanduser('~/Desktop/账号凭证/pypi_credential.txt')

s = requests.Session()
s.headers['User-Agent'] = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                           'AppleWebKit/537.36 Chrome/126.0 Safari/537.36')

def totp(secret, period=30, digits=6):
    key = base64.b32decode(secret.upper() + '=' * ((8 - len(secret) % 8) % 8))
    counter = int(time.time() // period)
    h = hmac.new(key, struct.pack('>Q', counter), hashlib.sha1).digest()
    o = h[-1] & 0x0f
    code = (struct.unpack('>I', h[o:o + 4])[0] & 0x7fffffff) % (10 ** digits)
    return str(code).zfill(digits)

def absurl(loc):
    if loc.startswith('//'):
        return 'https:' + loc
    if loc.startswith('/'):
        return 'https://pypi.org' + loc
    return loc

def login(attempt=0):
    r = s.get('https://pypi.org/account/login/', allow_redirects=False)
    csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', r.text, re.S).group(1)
    r = s.post('https://pypi.org/account/login/',
               data={'csrf_token': csrf, 'username': 'imprint-pdf', 'password': PW},
               headers={'Origin': 'https://pypi.org', 'Referer': 'https://pypi.org/account/login/'},
               allow_redirects=False, timeout=40)
    loc = r.headers.get('Location', '')
    if '/account/two-factor/' in loc:
        url = absurl(loc)
        r = s.get(url, allow_redirects=False)
        m = re.search(r'<form method="post"[^>]*action="([^"]*)"[^>]*id="totp-auth-form"', r.text, re.S)
        action = m.group(1) if m else '/account/two-factor/'
        csrf2 = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', r.text, re.S).group(1)
        r = s.post(absurl(action),
                   data={'csrf_token': csrf2, 'method': 'totp',
                         'totp_value': totp(TOTP_SECRET), 'remember_device': 'true'},
                   headers={'Origin': 'https://pypi.org', 'Referer': url},
                   allow_redirects=False, timeout=40)
        loc = r.headers.get('Location', '')
        if loc:
            r = s.get(absurl(loc), allow_redirects=False)
    if '/account/login' in r.url or '/two-factor' in r.url:
        if attempt < 3:
            print('  login retry...'); time.sleep(3)
            return login(attempt + 1)
    return r

def main():
    login()
    r = s.get('https://pypi.org/manage/account/token/', allow_redirects=False)
    if r.status_code != 200:
        login()
        r = s.get('https://pypi.org/manage/account/token/', allow_redirects=False)
    assert r.status_code == 200, 'token page: %s' % r.status_code
    csrf = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', r.text, re.S).group(1)
    data = {'csrf_token': csrf, 'description': 'imprint-pdf publish', 'token_scope': 'scope:user'}
    r = s.post('https://pypi.org/manage/account/token/', data=data,
               headers={'Origin': 'https://pypi.org', 'Referer': 'https://pypi.org/manage/account/token/'},
               allow_redirects=False, timeout=40)
    if r.status_code in (301, 302, 303, 307, 308):
        r = s.get(absurl(r.headers['Location']), allow_redirects=False)
    m = re.search(r'pypi-[A-Za-z0-9_\-]{20,}', r.text)
    if not m:
        sys.exit('token not found on page')
    token = m.group(0)
    with open(CRED, 'w') as f:
        f.write(f'USER=imprint-pdf\nEMAIL={EMAIL}\nPASSWORD={PW}\nPYPI_TOKEN={token}\nTOTP_SECRET={TOTP_SECRET}\n')
    os.chmod(CRED, 0o600)
    print('凭据已存:', CRED)
    print('下一步: bash publish_pypi.sh')

if __name__ == '__main__':
    main()
