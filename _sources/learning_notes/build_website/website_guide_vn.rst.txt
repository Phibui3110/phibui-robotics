Hướng Dẫn Sử Dụng Website Documentation
=======================================

Tài liệu này giải thích cách **sử dụng, bảo trì và đóng góp** cho website documentation của Phibui Robotics Lab.

Nội dung bao gồm:

- Cấu trúc repository
- Cấu trúc documentation
- Workflow viết tài liệu
- Hướng dẫn reStructuredText
- Build và deploy
- Best practices
- Các lỗi thường gặp cần tránh


====================================================================
1. MỤC ĐÍCH CỦA WEBSITE
====================================================================

Website này đóng vai trò là **cổng documentation kỹ thuật** cho các dự án robotics được phát triển trong Phibui Robotics Lab.

Mục tiêu chính:

• Documentation cho các robotics project  
• Ghi lại quá trình học robotics  
• Cung cấp tutorial về ROS2 / Ubuntu / Robotics  
• Lưu trữ documentation kỹ thuật cho dự án xe tự hành  

Website được xây dựng bằng:

Sphinx + reStructuredText + GitHub Pages.


====================================================================
2. CẤU TRÚC REPOSITORY
====================================================================

Repository được tổ chức như sau:

phibui-robotics

├── docs
│
├── ros2_ws
├── firmware
├── hardware
├── simulations
├── scripts
│
├── .github
│   └── workflows
│
├── README.md
├── LICENSE
└── .gitignore


Giải thích:

docs
    Source code của website documentation

ros2_ws
    ROS2 workspace cho software robotics

firmware
    Firmware cho STM32

hardware
    Thiết kế phần cứng, wiring diagram, CAD

simulations
    Môi trường simulation

scripts
    Các script hỗ trợ development


Toàn bộ website documentation nằm trong:

docs/


====================================================================
3. CẤU TRÚC DOCUMENTATION
====================================================================

docs/source

├── index.rst
│
├── projects
│   ├── index.rst
│   └── autonomous_vehicle
│       ├── index.rst
│       ├── overview.rst
│       ├── system_architecture.rst
│       ├── hardware.rst
│       ├── software.rst
│       ├── ros2_workspace.rst
│       ├── sensors.rst
│       ├── perception.rst
│       ├── control.rst
│       ├── simulation.rst
│       └── experiments.rst
│
├── system
│   ├── index.rst
│   ├── hardware
│   ├── software
│   ├── perception
│   ├── control
│   └── simulation
│
├── tutorials
│   └── index.rst
│
├── learning_notes
│   └── index.rst
│
└── blog
└── index.rst

Ý nghĩa của từng section:

projects
    Documentation cho các robotics project.

system
    Documentation về kiến trúc kỹ thuật của hệ thống.

tutorials
    Các hướng dẫn từng bước.

learning_notes
    Ghi chú cá nhân trong quá trình học robotics.

blog
    Nhật ký phát triển project.


====================================================================
1. WORKFLOW VIẾT TÀI LIỆU
====================================================================

Workflow thông thường:

Sửa file .rst
↓
git add
↓
git commit
↓
git push
↓
GitHub Actions build documentation
↓
GitHub Pages deploy website


Workflow phát triển local:

1) Chỉnh sửa tài liệu

Ví dụ:

docs/source/projects/autonomous_vehicle/overview.rst


2) Build documentation local

cd docs
make html


3) Mở website đã build

docs/build/html/index.html


4) Commit thay đổi

git add .
git commit -m "update documentation"
git push


====================================================================
5. RESTRUCTUREDTEXT (RST) CƠ BẢN
====================================================================

Toàn bộ documentation được viết bằng reStructuredText (.rst).


--------------------------------------------------------------------
5.1 Tiêu đề
--------------------------------------------------------------------

Tiêu đề dùng ký tự gạch dưới.

Ví dụ:

Autonomous Vehicle Overview
===========================

Hardware Architecture
---------------------


--------------------------------------------------------------------
5.2 Đoạn văn
--------------------------------------------------------------------

Viết văn bản bình thường.

Ví dụ:

Tài liệu này mô tả kiến trúc phần cứng
của nền tảng xe tự hành.


--------------------------------------------------------------------
5.3 Danh sách
--------------------------------------------------------------------

Ví dụ:

- Raspberry Pi 5
- STM32 Nucleo
- IMU
- Camera


--------------------------------------------------------------------
5.4 Code Block
--------------------------------------------------------------------

Ví dụ:

.. code-block:: bash

   ros2 topic list


--------------------------------------------------------------------
5.5 Chèn hình ảnh
--------------------------------------------------------------------

Ví dụ:

.. .. image:: images/vehicle.jpg
..    :width: 600px
..    :align: center


====================================================================
6. TOCTREE
====================================================================

Navigation của website được quản lý bởi toctree.

Ví dụ:

.. .. toctree::
..    :maxdepth: 2

..    overview
..    hardware
..    software


Quy tắc:

• Path là relative với file hiện tại  
• Không ghi .rst  
• Mỗi document phải có title  


====================================================================
7. THÊM MỘT TRANG MỚI
====================================================================

Ví dụ: thêm trang perception.

Bước 1

Tạo file:

projects/autonomous_vehicle/perception_pipeline.rst


Bước 2

Thêm tiêu đề:

Perception Pipeline
===================


Bước 3

Thêm vào toctree:

projects/autonomous_vehicle/index.rst


.. .. toctree::
..    :maxdepth: 1

..    overview
..    perception_pipeline


====================================================================
8. QUÁ TRÌNH DEPLOY
====================================================================

Deployment hoàn toàn tự động.

Khi push code lên GitHub:

GitHub Actions sẽ:

1) Cài dependencies  
2) Build Sphinx documentation  
3) Deploy lên GitHub Pages  


Website public:

https://phibui3110.github.io/phibui-robotics


====================================================================
9. BEST PRACTICES
====================================================================

Đặt tiêu đề rõ ràng

Ví dụ:

Control System
==============

thay vì

Control


Mỗi document chỉ nên tập trung vào một chủ đề.


Sử dụng diagram khi có thể.

Architecture diagram giúp hiểu hệ thống nhanh hơn.


Mirror cấu trúc repository

Ví dụ:

ros2_ws → ROS2 documentation  
hardware → hardware documentation  


====================================================================
10. CÁC LỖI THƯỜNG GẶP
====================================================================

Thiếu title

Mỗi file .rst phải bắt đầu bằng title.


Sai path trong toctree

Sai:

projects/autonomous_vehicle/overview

Đúng:

overview


File chưa được thêm vào toctree

Nếu file không nằm trong toctree,
nó sẽ không xuất hiện trong navigation.


Quên build lại

Luôn chạy:

make html

trước khi commit.


====================================================================
11. MÔI TRƯỜNG PHÁT TRIỂN
====================================================================

Python virtual environment:

docs-env


Activate environment:

source docs-env/bin/activate


Cài dependencies:

pip install sphinx
pip install sphinx_rtd_theme


Build documentation:

cd docs
make html


====================================================================
12. HƯỚNG PHÁT TRIỂN TƯƠNG LAI
====================================================================

Các extension có thể thêm sau:

sphinx-mermaid
    Vẽ architecture diagram

sphinx-copybutton
    Copy code button

sphinx-design
    UI component đẹp hơn


====================================================================
KẾT THÚC TÀI LIỆU
====================================================================