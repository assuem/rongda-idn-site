#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""站点自检：HTML 解析 / JSON-LD 合法 + FAQ 正文一致 / sitemap 与文件对应 / 站内链接存活。
用法：python3 tools/check_site.py   （CI 与本地提交前均可跑）"""
import re, json, sys, glob, os, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []

def err(msg):
    errors.append(msg)
    print('FAIL', msg)

def ok(msg):
    print(' ok ', msg)

# 1. HTML 可解析 + JSON-LD 合法 + FAQ 正文与 schema 一致
html_files = ['index.html', 'onepager.html', 'brochure.html'] + sorted(glob.glob('id/*.html'))
for f in html_files:
    p = os.path.join(ROOT, f)
    if not os.path.exists(p):
        err(f'{f} 不存在')
        continue
    h = open(p, encoding='utf-8').read()
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    for b in blocks:
        try:
            d = json.loads(b)
        except Exception as e:
            err(f'{f} JSON-LD 解析失败: {e}')
            continue
        for n in d.get('@graph', [d]):
            if n.get('@type') == 'FAQPage':
                for q in n.get('mainEntity', []):
                    if q['name'] not in h or q['acceptedAnswer']['text'] not in h:
                        err(f"{f} FAQ schema 与正文不一致: {q['name'][:40]}")
    ok(f'{f} 解析通过（{len(blocks)} 块 JSON-LD）')

# 2. sitemap 里的 URL 必须有对应文件
sm = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
for loc in re.findall(r'<loc>(.*?)</loc>', sm):
    path = urllib.parse.urlparse(loc).path.lstrip('/') or 'index.html'
    if not os.path.exists(os.path.join(ROOT, path)):
        err(f'sitemap URL 无对应文件: {loc}')
ok('sitemap.xml 与文件对应')

# 3. 站内链接（id/、media/、.html）全部存活
for f in html_files:
    h = open(os.path.join(ROOT, f), encoding='utf-8').read()
    base = os.path.dirname(os.path.join(ROOT, f))
    for href in re.findall(r'href="([^"#]+?)"', h):
        if href.startswith(('http', 'mailto:', 'data:', 'tel:')):
            continue
        target = os.path.normpath(os.path.join(base, href))
        if not os.path.exists(target):
            err(f'{f} 死链: {href}')
ok('站内链接检查完毕')

# 4. 域名口径：不得出现坏域名（www.jxrdxf.top 属国内站；id.jxrdxf.top 是笔误）
for f in html_files + ['robots.txt', 'sitemap.xml', 'llms.txt']:
    t = open(os.path.join(ROOT, f), encoding='utf-8').read()
    if 'www.jxrdxf.top' in t or re.search(r'(?<!idn\.)id\.jxrdxf\.top', t):
        err(f'{f} 出现坏域名（应统一 idn.jxrdxf.top）')
ok('域名口径检查完毕')

print()
if errors:
    print(f'{len(errors)} 个错误')
    sys.exit(1)
print('全部检查通过')
