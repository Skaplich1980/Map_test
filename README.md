# Map Test Project

������������� ����� ���� ������ � ����������������������.  
������ ���������� �� **Django + DRF**, ������������ �������� ����������, ���������� �� �����������, ������ ������ � ������� **GeoJSON (RFC 7946)** � ������������ API ����� **Swagger/Redoc**.

---

## �����������
- CRUD ��� ���� (`Place`) � ���������� (`Photo`)
- ����������� ����� JWT (SimpleJWT)
- Inline-�������������� ���������� � ������� � drag-and-drop �����������
- ������ ����������� � �������
- ��������� WYSIWYG ��������� (CKEditor5) ��� ��������
- ���������� ���� �� ����������� (bbox)
- �������� `/api/places/geojson/` ��� ��������� FeatureCollection
- ������������� ����� API � ������������ (Swagger, Redoc)

---
## ��������� � ������

### 1. ������������ �����������
git clone https://github.com/Skaplich1980/Map_test.git
cd map-test
2. �������� ������������ ���������
bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
3. ��������� ������������
bash
pip install -r requirements.txt
4. ��������� ���������
������ ���� .env � ����� ������� �� ������ �������:

env
SECRET_KEY=django-insecure-...
DEBUG=True
DB_ENGINE=sqlite
DB_NAME=map
DB_USER=postgres
DB_PASSWORD=secret
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1

�� � ��������� !
db.sqlite3  
������������:root
������:admin
���� ���������, �� ���� 5-6 ����� ����������

5. ���������� ��������
bash
python manage.py migrate
6. �������� �����������������
bash
python manage.py createsuperuser
7. ������ �������
bash
python manage.py runserver
?? �������� ��������� API
JWT �����������

POST /api/token/ � �������� �����
POST /api/token/refresh/ � �������� �����
�����
GET /api/places/ � ������ ����
POST /api/places/ � ������� �����
GET /api/places/{id}/ � ��������
GET /api/places/geojson/ � ��� ����� � ������� GeoJSON
����������
GET /api/photos/ � ������ ����
POST /api/photos/ � �������� ����
������������ API
Swagger UI: http://localhost:8000/api/docs/
Redoc: http://localhost:8000/api/redoc/
JSON-�����: http://localhost:8000/api/schema/
�������
URL: http://localhost:8000/admin/

�����������:
Inline-�������������� ����������
Drag-and-drop ���������� ����
������ �����������
�������� CKEditor�5 ��� �������� ����

������� � �����
����������� �����: /static/
���������� (����������� ����): /media/

���������� �������������� ����� �����
������ �� pythonanywhere / ������ �������
���������� ������� load_place <url> ��� ������� ������

�������� �������� ������ ��� ������������

��������
MIT License

������ �������� �� 4 ���, 1 ���� �� 19,20 ���� ��������������