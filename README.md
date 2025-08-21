# Text Editor - Python 3.13

Một trình soạn thảo văn bản mạnh mẽ và hiện đại được phát triển bằng Python với giao diện Tkinter.

<img width="746" height="745" alt="Image" src="https://github.com/user-attachments/assets/5d3cb2ed-9989-4ee4-8601-0b0f7c34ede8" />


<img width="1914" height="1079" alt="Image" src="https://github.com/user-attachments/assets/cb5739a3-6003-4cf0-8b0c-c63b6f1112fc" />

## Tính năng chính

### 📝 Chỉnh sửa văn bản
- Hỗ trợ nhiều tab để làm việc với nhiều tài liệu cùng lúc
- Hiển thị số dòng tự động
- Tính năng Undo/Redo không giới hạn
- Tìm kiếm và thay thế văn bản
- Tự động phát hiện encoding của file

### 🎨 Syntax Highlighting
Hỗ trợ tô sáng cú pháp cho các ngôn ngữ:
- Python (.py)
- JavaScript (.js)
- HTML (.html, .htm)
- CSS (.css)
- Plain Text (.txt)

### 🎯 Giao diện người dùng
- 4 theme màu: Sáng, Tối, Xanh dương, Xanh lá
- Toolbar với các chức năng thường dùng
- Statusbar hiển thị thông tin chi tiết
- Hỗ trợ zoom in/out
- Chế độ toàn màn hình (F11)

### 🔧 Công cụ chuyển đổi
Tích hợp bộ chuyển đổi dữ liệu với các tính năng:
- **URL Encoding/Decoding**
- **Base64 Encoding/Decoding**
- **Chuyển đổi định dạng chữ**: UPPERCASE, lowercase, Title Case, camelCase, snake_case
- **Chuyển đổi encoding**: UTF-8, UTF-16, ASCII, Latin-1, Windows-1252, ISO-8859-1
- **Chuyển đổi định dạng dữ liệu**: CSV ↔ JSON ↔ XML ↔ YAML

### ⚙️ Tùy chỉnh
- Lựa chọn font chữ và kích cỡ
- Thay đổi màu chữ và màu nền
- Lưu và khôi phục cài đặt tự động
- Danh sách file đã mở gần đây

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Tkinter (thường có sẵn với Python)
- PyYAML (cho chuyển đổi YAML)

## Cài đặt


2. Cài đặt dependencies:
```bash
pip install pyyaml
```

3. Chạy ứng dụng:
```bash
python main.py
```

## Cấu trúc dự án

```
text-editor-python/
├── main.py                 # File chính để chạy ứng dụng
├── config.py              # Quản lý cấu hình và settings
├── main_window.py         # Cửa sổ chính của ứng dụng
├── tab_manager.py         # Quản lý tabs và text widgets
├── themes.py              # Hệ thống theme và màu sắc
├── syntax_highlighter.py  # Tô sáng cú pháp
├── file_operations.py     # Thao tác với file
├── toolbar.py             # Thanh công cụ
├── menubar.py             # Menu bar
├── statusbar.py           # Thanh trạng thái
├── find_dialog.py         # Hộp thoại tìm kiếm
├── settings_dialog.py     # Hộp thoại cài đặt
├── converter.py           # Engine chuyển đổi dữ liệu
└── converter_dialog.py    # Giao diện chuyển đổi dữ liệu
```

## Phím tắt

### File
- `Ctrl+N` - Tạo tài liệu mới
- `Ctrl+O` - Mở file
- `Ctrl+S` - Lưu file
- `Ctrl+Shift+S` - Lưu với tên khác
- `Ctrl+W` - Đóng tab hiện tại
- `Ctrl+Q` - Thoát ứng dụng

### Chỉnh sửa
- `Ctrl+Z` - Hoàn tác
- `Ctrl+Y` - Làm lại
- `Ctrl+X` - Cắt
- `Ctrl+C` - Sao chép
- `Ctrl+V` - Dán
- `Ctrl+A` - Chọn tất cả
- `Ctrl+F` - Tìm kiếm

### Zoom
- `Ctrl++` - Phóng to
- `Ctrl+-` - Thu nhỏ
- `Ctrl+0` - Kích thước gốc

### Khác
- `F11` - Chế độ toàn màn hình

## Tính năng nổi bật

### Syntax Highlighting thông minh
- Tự động phát hiện ngôn ngữ dựa trên phần mở rộng file
- Tô sáng keywords, strings, comments, numbers
- Hỗ trợ HTML tags và CSS properties

### Quản lý Tab hiệu quả
- Mở nhiều file cùng lúc
- Đánh dấu file đã chỉnh sửa với dấu *
- Context menu click chuột phải
- Tự động tạo tab mới khi cần

### Bộ chuyển đổi dữ liệu mạnh mẽ
- Giao diện tab riêng biệt cho từng loại chuyển đổi
- Tích hợp với editor chính
- Hỗ trợ lấy dữ liệu từ/đưa về editor


**Text Editor - Python 3.13** - Trình soạn thảo văn bản hiện đại cho developers và người dùng thông thường.
