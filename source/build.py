import sys,os,shutil,datetime
src='src/'
site='--site' in sys.argv
files=['data.js','engine.js','model.js','photo.js','scene.js','ui.js','views.js','io.js']+(['site.js'] if site else [])+['main.js']
js='\n'.join(open(src+f,encoding='utf-8').read() for f in files)
css=open(src+'style.css',encoding='utf-8').read()
assert '</script' not in js.lower() and '</style' not in css.lower()
html=open(src+'index.tpl.html',encoding='utf-8').read().replace('/*CSS*/',css).replace('/*JS*/','(function(){"use strict";\n'+js+'\n})();' if '--iife' in sys.argv else js)
if not site:
    open('dist/konstruktor-fotozon.html','w',encoding='utf-8').write(html)
    print('built',len(html),'bytes')
else:
    # the stand-alone site (GitHub Pages): a full document with the home-screen icon, manifest and offline cache
    out='site/';build=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M')
    if os.path.isdir(out):
        for n in os.listdir(out):
            if n!='.git':
                pth=os.path.join(out,n);shutil.rmtree(pth) if os.path.isdir(pth) else os.remove(pth)
    os.makedirs(out,exist_ok=True)
    head=('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
      '<meta name="theme-color" content="#2A2C2F">\n<meta name="description" content="Konfetti Deco — конструктор фотозон: сцена, смета, чертежи и предложение клиенту">\n'
      '<link rel="manifest" href="manifest.webmanifest">\n<link rel="icon" type="image/png" href="icons/favicon-64.png">\n<link rel="apple-touch-icon" href="icons/icon-180.png">\n'
      '<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
      '<meta name="apple-mobile-web-app-title" content="Konfetti Deco">\n')
    i=html.index('<title>');j=html.index('</title>')+8
    doc=head+html[i:j]+'\n'+html[j:].replace('<div class="ws" id="ws">','</head>\n<body>\n<div class="ws" id="ws">',1)+'\n</body>\n</html>\n'
    open(out+'index.html','w',encoding='utf-8').write(doc)
    shutil.copytree('site_src/icons',out+'icons')
    os.makedirs(out+'.github/workflows',exist_ok=True);shutil.copy('site_src/.github/workflows/deploy.yml',out+'.github/workflows/deploy.yml')
    for f in ['manifest.webmanifest','README.md']:
        if os.path.exists('site_src/'+f):shutil.copy('site_src/'+f,out+f)
    open(out+'sw.js','w',encoding='utf-8').write(open('site_src/sw.js',encoding='utf-8').read().replace('__BUILD__',build))
    open(out+'.nojekyll','w').write('')
    # the sources travel with the site, so the next change can be built from them
    shutil.copytree('src',out+'source/src');shutil.copy('build.py',out+'source/build.py');shutil.copytree('site_src',out+'source/site_src')
    print('site built',len(doc),'bytes, build',build)
