#!/usr/bin/env python3
"""IVE 홈페이지 페이지 생성기.
src/master.html(전체 내용을 담은 원본)을 고친 뒤 `python3 src/build.py`를 실행하면
index.html / company.html / apply.html / business.html / contact.html 이 다시 만들어진다."""
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = open(os.path.join(ROOT, 'src/master.html'), encoding='utf-8').read()
SITE = 'https://ive-entertainment.com/'

MARKS = ['<!-- NAV -->','<!-- HERO -->','<!-- STATS -->','<!-- VIDEO -->','<!-- NEWSCARDS -->','<!-- COMPARE -->','<!-- INTRO -->','<!-- ABOUT -->','<!-- PROCESS -->',
         '<!-- PLATFORMS -->','<!-- CREATORS -->','<!-- ROUTE -->','<!-- APPLY -->','<!-- BUSINESS -->','<!-- GUIDE -->','<!-- GUIDETT -->','<!-- CONTACTCARDS -->','<!-- CONTACT -->','<!-- FOOTER -->']
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
    <li><a href="creators.html"{a_creators}>Creators</a></li>
    <li class="has-sub"><a href="apply.html"{a_apply}>Apply</a>
      <ul class="sub"><li><a href="apply.html">Creator · 크리에이터 지원</a></li><li><a href="bigolive-agency.html">Guide · 비고라이브 소속사 가이드</a></li><li><a href="tiktok-live-agency.html">Guide · 틱톡 라이브 소속사 가이드</a></li><li><a href="business.html">Business · 제휴 문의</a></li></ul>
    </li>
    <li><a href="news.html"{a_news}>News</a></li>
    <li><a href="contact.html"{a_contact}>Contact</a></li>
    <li><a href="apply.html" class="nav-cta">지원하기</a></li>
  </ul>'''

def nav(active):
    n = seg['NAV']
    n = re.sub(r'<ul class="nav-links">.*?</ul>', lambda _: NAV_LINKS.format(**{k: (' aria-current="page"' if k == 'a_'+active else '') for k in ['a_company','a_creators','a_apply','a_news','a_contact']}), n, count=1, flags=re.S)
    return n.replace('<a href="#" class="nav-logo">', '<a href="/" class="nav-logo">')

def links(t):
    for k, v in {'#apply':'apply.html','#business':'business.html','#contact':'contact.html','#about':'company.html#about',
                 '#process':'company.html#process','#support':'company.html#support','#platforms':'company.html#platforms','#creators':'creators.html'}.items():
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
    body=['HERO']),
 'company.html': dict(active='company', path='company.html', title='회사 소개 | '+BRAND,
    desc='아이브 엔터테인먼트 회사 소개 — 비고라이브·틱톡 라이브 전문 에이전시의 매니지먼트 과정과 크리에이터 지원 내용, 활동 플랫폼을 안내합니다.',
    head=('Company','회사 소개','2014년 설립, 라이브 방송 크리에이터와 함께 성장해 온 IVE를 소개합니다.'),
    body=['INTRO','ABOUT','PROCESS','PLATFORMS']),
 'creators.html': dict(active='creators', path='creators.html', title='크리에이터 | '+BRAND,
    desc='아이브 엔터테인먼트와 함께 활동 중인 비고라이브·틱톡 라이브 크리에이터를 소개합니다. 현재 222명 이상의 크리에이터가 IVE와 함께하고 있습니다.',
    head=('Creators','크리에이터','지금 IVE와 함께 방송하고 있는 크리에이터들'),
    body=['CREATORS']),
 'apply.html': dict(active='apply', path='apply.html', title='크리에이터 지원하기 | '+BRAND,
    desc='아이브 엔터테인먼트 크리에이터 지원서 — 비고라이브·틱톡 라이브 방송을 시작하고 싶은 분은 지원서를 남겨 주세요. 방송 경험이 없어도 지원할 수 있습니다.',
    head=('Creator','크리에이터 지원','지원서를 남겨 주시면 담당자가 확인 후 연락드립니다.'),
    body=['APPLY']),
 'business.html': dict(active='apply', path='business.html', title='제휴·협업 문의 | '+BRAND,
    desc='아이브 엔터테인먼트 제휴·협업 문의 — 브랜드 협찬, 광고, 에이전시 제휴, 공동 이벤트 제안을 받습니다.',
    head=('Business','제휴 · 협업 문의','브랜드 협찬, 광고, 에이전시 제휴 제안을 기다립니다.'),
    body=['BUSINESS']),
 'bigolive-agency.html': dict(active='apply', path='bigolive-agency.html', title='비고라이브 소속사(에이전시) 가입 가이드 | 비고라이브 공식 에이전시 아이브 엔터테인먼트',
    desc='비고라이브 소속사(공식 에이전시)란 무엇인지, 소속사에 들어가면 좋은 점, 가입 절차, 소속사 고르는 체크리스트와 자주 묻는 질문을 정리했습니다. 비고라이브 공식 에이전시 아이브 엔터테인먼트.',
    head=('Guide','비고라이브 소속사 가이드','비고라이브 공식 에이전시 가입 방법과 소속사 고르는 법'),
    body=['GUIDE']),
 'tiktok-live-agency.html': dict(active='apply', path='tiktok-live-agency.html', title='틱톡 라이브 소속사(에이전시) 가입 가이드 | 틱톡 라이브 전문 에이전시 아이브 엔터테인먼트',
    desc='틱톡 라이브 소속사(에이전시)란 무엇인지, 소속사에 들어가면 좋은 점, 가입 절차, 소속사 고르는 체크리스트와 자주 묻는 질문을 정리했습니다. 틱톡 라이브 전문 에이전시 아이브 엔터테인먼트.',
    head=('Guide','틱톡 라이브 소속사 가이드','틱톡 라이브 에이전시 가입 방법과 소속사 고르는 법'),
    body=['GUIDETT']),
 'news.html': dict(active='news', path='news.html', title='소식 | '+BRAND,
    desc='아이브 엔터테인먼트 소식 — 강남역 미디어월, 압구정 신웅빌딩 광고 등 IVE 크리에이터가 함께한 비고라이브 광고 영상과 새로운 소식을 전합니다.',
    head=('News','소식','IVE 크리에이터와 함께한 광고 영상과 새로운 소식'),
    body=['VIDEO','NEWSCARDS']),
 'news-tiktok-vs-bigo.html': dict(active='news', path='news-tiktok-vs-bigo.html', title='틱톡 라이브 vs 비고 라이브 비교 — 수수료·환전율·라이브 조건 | '+BRAND,
    desc='틱톡 라이브와 비고 라이브의 차이를 한눈에 비교했습니다. 라이브 조건, 노출 구조, 수익·지원금 구조, 환전율, 수수료와 지급 방식까지 정리. 두 플랫폼 모두 아이브 엔터테인먼트에서 시작할 수 있습니다.',
    head=('News','틱톡 라이브 vs 비고 라이브','어디서 방송할지 고민될 때 보는 플랫폼 비교'),
    body=['COMPARE']),
 'contact.html': dict(active='contact', path='contact.html', title='문의하기 | '+BRAND,
    desc='아이브 엔터테인먼트 연락처 — 전화, 이메일, 카카오톡 오픈채팅, 인스타그램으로 문의하실 수 있습니다.',
    head=('Contact','문의하기','편한 방법으로 연락 주세요.'),
    body=['CONTACT']),
}
for fn, p in PAGES.items():
    h = head if not p['title'] else meta(head, p['title'], p['desc'], p['path'])
    out = h + nav(p['active']) + (page_head(*p['head']) if p['head'] else '')
    out += ''.join(seg[k] for k in p['body']) + tail
    if fn == 'index.html':
        out = out.replace('</body>', '''<script>
(function(){var h=document.querySelector('.hero'),f=document.querySelector('footer');if(!h||!f)return;
function fit(){var need=0;h.querySelectorAll('.hs').forEach(function(x){var c=x.firstElementChild;if(c)need=Math.max(need,c.offsetHeight+110);});h.style.height=Math.max(520,window.innerHeight-f.offsetHeight,need)+'px';h.style.minHeight='0';}
fit();window.addEventListener('resize',fit);window.addEventListener('load',fit);if(document.fonts)document.fonts.ready.then(fit);})();
</script>
</body>''', 1)
    if fn in ('bigolive-agency.html','tiktok-live-agency.html'):
        import json as _j
        faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
          {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>',out)]}
        out=out.replace('</head>','<script type="application/ld+json">'+_j.dumps(faq,ensure_ascii=False)+'</script>\n</head>',1)
    out = links(out)
    open(os.path.join(ROOT, fn), 'w', encoding='utf-8').write(out)
    print(fn, len(out)//1024, 'KB')
