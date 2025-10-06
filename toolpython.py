"""
Streamlit Python Toolkit — English deploy-ready single-file app

This file bundles many utilities. Save as streamlit_python_toolkit.py and run with:
    streamlit run streamlit_python_toolkit.py

"""

import streamlit as st
import base64
import hashlib
import uuid
import random
import string
import json
import math
import io
from datetime import datetime, date, timedelta

# Optional imports
_missing_libs = []
try:
    import qrcode
except Exception:
    qrcode = None
    _missing_libs.append('qrcode')
try:
    from PIL import Image, ImageOps, ImageFilter
except Exception:
    Image = None
    ImageOps = None
    ImageFilter = None
    _missing_libs.append('Pillow')
try:
    import pandas as pd
except Exception:
    pd = None
    _missing_libs.append('pandas')
try:
    from faker import Faker
    _faker = Faker()
except Exception:
    _faker = None
    _missing_libs.append('faker')
try:
    import PyPDF2
except Exception:
    PyPDF2 = None
    _missing_libs.append('PyPDF2')
try:
    import requests
except Exception:
    requests = None
    _missing_libs.append('requests')

st.set_page_config(page_title='Python Toolkit', layout='wide')
st.title('Python Toolkit — All-in-One')

if _missing_libs:
    st.sidebar.warning('Optional libraries missing: ' + ', '.join(_missing_libs))

menu = [
    'Overview', 'Calculator', 'Units', 'Random', 'Encode/Hash', 'Text',
    'Files', 'QR & Image', 'PDF', 'HTTP', 'Dates', 'Colors', 'Faker', 'Deploy'
]
choice = st.sidebar.selectbox('Choose', menu)

# Safe evaluator
def safe_eval(expr: str):
    # allow only a small set of safe characters (digits, operators, parentheses, decimal point, spaces and e/E)
    allowed_chars = set('0123456789+-*/()., eE')
    if not expr:
        return 'Empty expression'
    try:
        # remove newline and carriage return characters using chr() to avoid embedding escape sequences
        cleaned = expr.replace(chr(10), '').replace(chr(13), '')
        if any(ch not in allowed_chars for ch in cleaned):
            return 'Disallowed character in expression'
        return eval(cleaned, {'__builtins__': {}}, {'math': math})
    except Exception as e:
        return f'Error: {e}'

# Overview
if choice == 'Overview':
    st.header('Overview')
    st.write('This app collects many small utilities into one file. Use the left menu to explore the tools.')

# Calculator
if choice == 'Calculator':
    st.header('Calculator')
    expr = st.text_input('Arithmetic expression', '2*(3+4)/7')
    if st.button('Compute'):
        st.write(safe_eval(expr))

# Units
if choice == 'Units':
    st.header('Unit converter')
    category = st.selectbox('Category', ['Length','Weight','Temperature','Speed'])
    if category == 'Length':
        units = {'m':1, 'km':1000, 'cm':0.01, 'mm':0.001, 'inch':0.0254, 'ft':0.3048}
    elif category == 'Weight':
        units = {'kg':1, 'g':0.001, 'lb':0.45359237, 'oz':0.0283495231}
    elif category == 'Speed':
        units = {'m/s':1, 'km/h':1000/3600, 'mph':0.44704}
    val = st.number_input('Value', value=1.0)
    src = st.selectbox('From', list(units.keys()))
    dst = st.selectbox('To', list(units.keys()))
    if st.button('Convert'):
        st.write(f'{val} {src} = {val * units[src] / units[dst]} {dst}')

    if category == 'Temperature':
        val = st.number_input('Value (temp)', value=25.0, key='temp')
        src_t = st.selectbox('From (temp)', ['C','F','K'], key='t_from')
        dst_t = st.selectbox('To (temp)', ['C','F','K'], key='t_to')
        def tconv(v,s,d):
            if s == d:
                return v
            if s == 'C':
                c = v
            elif s == 'F':
                c = (v - 32) * 5/9
            else:
                c = v - 273.15
            if d == 'C':
                return c
            if d == 'F':
                return c * 9/5 + 32
            return c + 273.15
        if st.button('Convert Temperature'):
            st.write(tconv(val, src_t, dst_t))

# Random
if choice == 'Random':
    st.header('Random generators')
    kind = st.selectbox('Kind', ['Password','UUID','Token','String'])
    if kind == 'Password':
        length = st.slider('Length', 6, 128, 16)
        use_upper = st.checkbox('Uppercase', True)
        use_digits = st.checkbox('Digits', True)
        use_symbols = st.checkbox('Symbols', True)
        if st.button('Generate password'):
            pool = string.ascii_lowercase
            if use_upper:
                pool += string.ascii_uppercase
            if use_digits:
                pool += string.digits
            if use_symbols:
                pool += '!@#$%^&*()'
            st.code(''.join(random.choice(pool) for _ in range(length)))
    if kind == 'UUID':
        if st.button('Generate UUID4'):
            st.write(str(uuid.uuid4()))
    if kind == 'Token':
        n = st.number_input('Bytes', 8, 256, 32)
        if st.button('Generate token'):
            try:
                data = random.randbytes(n) if hasattr(random, 'randbytes') else bytes(random.getrandbits(8) for _ in range(n))
                st.code(base64.urlsafe_b64encode(data).rstrip(b'=').decode())
            except Exception as e:
                st.error(e)
    if kind == 'String':
        length = st.number_input('Length', 1, 500, 12)
        charset = st.text_input('Charset', value=string.ascii_letters + string.digits)
        if st.button('Generate string'):
            st.write(''.join(random.choice(charset) for _ in range(int(length))))

# Encode/Hash
if choice == 'Encode/Hash':
    st.header('Base64 and Hash')
    part = st.selectbox('Choose', ['Base64','Hash'])
    if part == 'Base64':
        text = st.text_area('Text')
        action = st.radio('Action', ['encode','decode'])
        if st.button('Run'):
            try:
                if action == 'encode':
                    st.text(base64.b64encode(text.encode()).decode())
                else:
                    st.text(base64.b64decode(text).decode())
            except Exception as e:
                st.error(e)
    else:
        text = st.text_input('Text to hash')
        algo = st.selectbox('Algorithm', ['md5','sha1','sha256'])
        if st.button('Hash'):
            h = getattr(hashlib, algo)(text.encode()).hexdigest()
            st.code(h)

# Text
if choice == 'Text':
    st.header('Text utilities')
    txt = st.text_area('Text', height=200)
    if st.button('Upper'):
        st.write(txt.upper())
    if st.button('Lower'):
        st.write(txt.lower())
    if st.button('Trim blank lines'):
        st.write('
'.join([l for l in txt.splitlines() if l.strip()]))
    if st.button('Word/Char count'):
        words = len(txt.split())
        chars = len(txt)
        st.write('Words:', words, 'Chars:', chars)

# Files
if choice == 'Files':
    st.header('JSON / CSV / Excel')
    file = st.file_uploader('Upload CSV, JSON or Excel', type=['csv','json','xlsx'])
    if file is not None:
        name = file.name
        content = file.read()
        if name.endswith('.csv'):
            if pd is None:
                st.warning('pandas required')
            else:
                df = pd.read_csv(io.BytesIO(content))
                st.dataframe(df)
                st.download_button('Download JSON', data=df.to_json(orient='records', force_ascii=False), file_name=name.replace('.csv', '.json'))
        elif name.endswith('.xlsx'):
            if pd is None:
                st.warning('pandas required')
            else:
                df = pd.read_excel(io.BytesIO(content))
                st.dataframe(df)
                st.download_button('Download CSV', data=df.to_csv(index=False).encode('utf-8'), file_name=name.replace('.xlsx', '.csv'))
        else:
            try:
                obj = json.loads(content.decode())
                st.json(obj)
            except Exception:
                st.error('Invalid JSON')

# QR & Image
if choice == 'QR & Image':
    st.header('QR and Image')
    action = st.selectbox('Action', ['QR','Image preview','Image to ASCII'])
    if action == 'QR':
        data = st.text_area('Data', value='https://example.com')
        if st.button('Generate QR'):
            if qrcode is None:
                st.error('Install qrcode')
            else:
                qr = qrcode.make(data)
                buf = io.BytesIO()
                qr.save(buf, format='PNG')
                buf.seek(0)
                st.image(buf)
                st.download_button('Download', data=buf, file_name='qrcode.png')
    elif action == 'Image preview':
        up = st.file_uploader('Upload image', type=['png','jpg','jpeg','gif'])
        if up is not None:
            if Image is None:
                st.error('Install Pillow')
            else:
                img = Image.open(up)
                st.image(img, use_column_width=True)
    else:
        up = st.file_uploader('Upload image', type=['png','jpg','jpeg'])
        width = st.slider('Width', 40, 200, 80)
        if up is not None:
            if Image is None:
                st.error('Install Pillow')
            else:
                img = Image.open(up).convert('L')
                aspect = img.height / img.width
                new_w = width
                new_h = int(aspect * new_w * 0.55)
                img = img.resize((new_w, new_h))
                chars = "@%#*+=-:. "
                pixels = list(img.getdata())
                txt = ''.join(chars[pixel * len(chars) // 256] for pixel in pixels)
                ascii_img = '
'.join(txt[i:i+new_w] for i in range(0, len(txt), new_w))
                st.text(ascii_img)

# PDF
if choice == 'PDF':
    st.header('PDF extract')
    up = st.file_uploader('Upload PDF', type=['pdf'])
    if up is not None:
        if PyPDF2 is None:
            st.error('Install PyPDF2')
        else:
            try:
                reader = PyPDF2.PdfReader(io.BytesIO(up.read()))
                pages = [p.extract_text() or '' for p in reader.pages]
                st.text('

'.join(pages))
            except Exception as e:
                st.error(e)

# HTTP
if choice == 'HTTP':
    st.header('HTTP GET')
    url = st.text_input('URL', value='https://httpbin.org/get')
    if st.button('Send'):
        if requests is None:
            st.error('Install requests')
        else:
            try:
                r = requests.get(url, timeout=10)
                st.write('Status', r.status_code)
                st.code(r.text[:5000])
            except Exception as e:
                st.error(e)

# Dates
if choice == 'Dates':
    st.header('Date calculator')
    d1 = st.date_input('Date A', date.today())
    d2 = st.date_input('Date B', date.today())
    if st.button('Difference'):
        st.write('Days difference:', (d2 - d1).days)

# Colors
if choice == 'Colors':
    st.header('Color conversions')
    hexv = st.text_input('HEX', '#ff8800')
    if st.button('HEX to RGB'):
        h = hexv.lstrip('#')
        if len(h) == 6:
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            st.write('RGB:', r, g, b)
        else:
            st.error('HEX must be 6 chars')

# Faker
if choice == 'Faker':
    st.header('Fake data generator')
    if _faker is None:
        st.warning('Install faker')
    else:
        n = st.number_input('Rows', 1, 200, 5)
        fields = st.multiselect('Fields', ['name','email','address','phone'])
        if st.button('Generate'):
            rows = []
            for _ in range(n):
                r = {}
                if 'name' in fields:
                    r['name'] = _faker.name()
                if 'email' in fields:
                    r['email'] = _faker.email()
                if 'address' in fields:
                    r['address'] = _faker.address()
                if 'phone' in fields:
                    r['phone'] = _faker.phone_number()
                rows.append(r)
            st.json(rows)

# Deploy
if choice == 'Deploy':
    st.header('Deployment helpers')
    st.write('Generate requirements.txt and a basic Dockerfile for deployment.')
    reqs = ['streamlit', 'qrcode[pil]', 'Pillow', 'pandas', 'faker', 'PyPDF2', 'requests']
    if st.button('Download requirements.txt'):
        txt = '
'.join(reqs) + '
'
        st.download_button('Download', data=txt.encode('utf-8'), file_name='requirements.txt')
    docker = (
        'FROM python:3.10-slim
'
        'WORKDIR /app
'
        'COPY . /app
'
        'RUN pip install --no-cache-dir -r requirements.txt
'
        'EXPOSE 8501
'
        'CMD ["streamlit","run","streamlit_python_toolkit.py","--server.port","8501","--server.address","0.0.0.0"]
'
    )
    if st.button('Download Dockerfile'):
        st.download_button('Download Dockerfile', data=docker.encode('utf-8'), file_name='Dockerfile')

st.markdown('---')
st.caption('Ask me to add more features and I will update the file with deployment notes.')
