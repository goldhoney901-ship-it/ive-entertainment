#!/usr/bin/env python3
"""IVE 홈페이지 페이지 생성기.
src/master.html(전체 내용을 담은 원본)을 고친 뒤 `python3 src/build.py`를 실행하면
index.html / company.html / apply.html / business.html / contact.html 이 다시 만들어진다."""
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = open(os.path.join(ROOT, 'src/master.html'), encoding='utf-8').read()
SITE = 'https://ive-entertainment.com/'

MARKS = ['<!-- NAV -->','<!-- HERO -->','<!-- STATS -->','<!-- VIDEO -->','<!-- ABOUT -->','<!-- PROCESS -->',
         '<!-- PLATFORMS -->','<!-- CREATORS -->','<!-- ROUTE -->','<!-- APPLY -->','<!-- BUSINESS -->','<!-- CONTACT -->','<!-- FOOTER -->']
pos = []
for m in MARKS:
    assert M.count(m) == 1, m
    pos.append(M.index(m))
assert pos == sorted(pos)
head = M[:pos[0]]
seg = {MARKS[i][5:-4]: M[pos[i]:pos[i+1]] for i in range(len(MARKS)-1)}
tail = M[pos[-1]:]

NAV_LINKS = '''<button class="nav-burger" type="button" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
  <ul class="nav-links">
    <li><a href="company.html"{a_company}>Company</a></li>
    <li><a href="/#creators">Creators</a></li>
    <li class="has-sub"><a href="apply.html"{a_apply}>Apply</a>
      <ul class="sub"><li><a href="apply.html">Creator · 크리에이터 지원</a></li><li><a href="business.html">Business · 제휴 문의</a></li></ul>
    </li>
    <li><a href="news.html"{a_news}>News</a></li>
    <li><a href="contact.html"{a_contact}>Contact</a></li>
    <li><a href="apply.html" class="nav-cta">지원하기</a></li>
  </ul>'''

def nav(active):
    n = seg['NAV']
    n = re.sub(r'<ul class="nav-links">.*?</ul>', lambda _: NAV_LINKS.format(**{k: (' aria-current="page"' if k == 'a_'+active else '') for k in ['a_company','a_apply','a_news','a_contact']}), n, count=1, flags=re.S)
    return n.replace('<a href="#" class="nav-logo">', '<a href="/" class="nav-logo">')

def links(t):
    for k, v in {'#apply':'apply.html','#business':'business.html','#contact':'contact.html','#about':'company.html#about',
                 '#process':'company.html#process','#support':'company.html#support','#platforms':'company.html#platforms','#creators':'/#creators'}.items():
        t = t.replace('href="%s"' % k, 'href="%s"' % v)
    return t.replace('<a href="#" class="footer-logo">', '<a href="/" class="footer-logo">')

def page_head(en, ko, desc):
    return f'''<!-- PAGE HEAD -->
<section class="page-head">
  <div class="page-head-inner">
    <div class="page-head-en">{en}</div>
    <h1 class="page-head-ko">{ko}</h1>
    <p class="page-head-desc">{desc}</p>
  </div>
</section>

'''

def meta(h, title, desc, path):
    h = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', h, count=1)
    h = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1)+desc, h, count=1)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1)+title, h, count=1)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1)+desc, h, count=1)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1)+SITE+path, h, count=1)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1)+SITE+path, h, count=1)
    return h

BRAND = '아이브 엔터테인먼트 IVE Entertainment'
PAGES = {
 'index.html': dict(active='', path='', title=None, desc=None, head=None,
    body=['HERO','STATS','CREATORS','ROUTE']),
 'company.html': dict(active='company', path='company.html', title='회사 소개 | '+BRAND,
    desc='아이브 엔터테인먼트 회사 소개 — 비고라이브·틱톡 라이브 전문 에이전시의 매니지먼트 과정과 크리에이터 지원 내용, 활동 플랫폼을 안내합니다.',
    head=('Company','회사 소개','2019년부터 비고라이브·틱톡 라이브 크리에이터와 함께해 온 IVE를 소개합니다.'),
    body=['ABOUT','PROCESS','PLATFORMS']),
 'apply.html': dict(active='apply', path='apply.html', title='크리에이터 지원하기 | '+BRAND,
    desc='아이브 엔터테인먼트 크리에이터 지원서 — 비고라이브·틱톡 라이브 방송을 시작하고 싶은 분은 지원서를 남겨 주세요. 방송 경험이 없어도 지원할 수 있습니다.',
    head=('Creator','크리에이터 지원','지원서를 남겨 주시면 담당자가 확인 후 연락드립니다.'),
    body=['APPLY']),
 'business.html': dict(active='apply', path='business.html', title='제휴·협업 문의 | '+BRAND,
    desc='아이브 엔터테인먼트 제휴·협업 문의 — 브랜드 협찬, 광고, 에이전시 제휴, 공동 이벤트 제안을 받습니다.',
    head=('Business','제휴 · 협업 문의','브랜드 협찬, 광고, 에이전시 제휴 제안을 기다립니다.'),
    body=['BUSINESS']),
 'news.html': dict(active='news', path='news.html', title='소식 | '+BRAND,
    desc='아이브 엔터테인먼트 소식 — 강남역 미디어월, 압구정 신웅빌딩 광고 등 IVE 크리에이터가 함께한 비고라이브 광고 영상과 새로운 소식을 전합니다.',
    head=('News','소식','IVE 크리에이터와 함께한 광고 영상과 새로운 소식'),
    body=['VIDEO']),
 'contact.html': dict(active='contact', path='contact.html', title='문의하기 | '+BRAND,
    desc='아이브 엔터테인먼트 연락처 — 전화, 이메일, 카카오톡 오픈채팅, 인스타그램으로 문의하실 수 있습니다.',
    head=('Contact','문의하기','편한 방법으로 연락 주세요.'),
    body=['CONTACT']),
}
for fn, p in PAGES.items():
    h = head if not p['title'] else meta(head, p['title'], p['desc'], p['path'])
    out = h + nav(p['active']) + (page_head(*p['head']) if p['head'] else '')
    out += ''.join(seg[k] for k in p['body']) + tail
    out = links(out)
    open(os.path.join(ROOT, fn), 'w', encoding='utf-8').write(out)
    print(fn, len(out)//1024, 'KB')
