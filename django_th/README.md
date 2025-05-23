<!-- Tạo một dự án Python mới tên là django_th. Thư mục này sẽ chứa mã nguồn và file cấu hình của Poetry (pyproject.toml). -->
poetry new django_th
cd django_th
<!-- Cài đặt Django vào môi trường ảo được quản lý bởi Poetry. -->
poetry add django
<!-- Tạo một Django project tên là config bên trong thư mục src/ (đây là cấu trúc phổ biến để tách biệt mã nguồn khỏi root dự án). -->
poetry run django-admin startproject config src/
<!-- Thư mục src/ chứa manage.py và thư mục cấu hình config/. -->
cd src
<!-- Tạo một app nội bộ tên là core, nơi bạn sẽ viết model, view, và các xử lý nghiệp vụ. -->
poetry run python manage.py startapp core
<!-- Tạo một tài khoản superuser để đăng nhập vào trang quản trị tại /admin. -->
poetry run python manage.py createsuperuser
<!-- Chạy chongw trình, Mở trình duyệt truy cập: -->
poetry run python manage.py runserver
<!-- Tạo migration và migrate -->
poetry run python manage.py makemigrations
poetry run python manage.py migrate

<!-- Nếu có trước db thì sử dụng: -->
poetry add mysqlclient //Mysql
poetry add psycopg2-binary //PostgreSqlSql
<!-- Chạy lệnh inspectdb  -->
poetry run python manage.py inspectdb > your_app/models.py







