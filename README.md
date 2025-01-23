# Landscape Lab 风景园林实训室数据管理平台

## 项目简介
本项目是为风景园林专业实训室开发的综合数据管理平台，采用模块化架构设计，整合了植物/建材数据库管理、三维模型解析、项目数据分析等核心功能。

## 目录结构
```
landscape_lab/
├── models/              # 数据模型层
│   ├── plant.py         # 植物数据模型
│   ├── material.py      # 建材数据模型
│   ├── project.py       # 项目数据模型
│   └── user.py          # 用户数据模型
├── controllers/         # 业务逻辑层
│   ├── plant_controller.py    # 植物管理逻辑
│   ├── material_controller.py # 建材管理逻辑
│   └── project_controller.py  # 项目管理逻辑
├── views/               # 视图展示层
│   ├── plant_view.py    # 植物数据可视化
│   ├── material_view.py # 建材数据可视化
│   └── project_view.py  # 项目三维展示
├── utils/               # 工具模块
│   ├── file_utils.py    # 文件处理工具
│   ├── analysis_utils.py# 数据分析工具
│   └── security.py      # 安全验证模块
├── database/            # 数据库管理
│   └── db.py            # SQLite数据库连接
├── static/              # 静态资源
│   ├── css/             # 样式表
│   └── js/              # 前端脚本 
├── templates/           # 网页模板
└── requirements.txt     # 依赖库列表
```

## 核心功能进展
### ✅ 已实现功能
1. **基础数据管理**
   - 植物/建材数据库（SQLite）
   - 自动生成缩略图（Pillow集成）
   - CSV/Excel数据导入导出

2. **三维模型解析**
   - FBX/OBJ模型文件解析
   - 植物坐标/尺寸参数提取
   - 材质信息分析

3. **基础分析工具**
   - 植物分布统计报表
   - 日照阴影模拟（Three.js集成）
   - 项目版本对比功能

4. **用户权限系统**
   - JWT令牌认证
   - 角色分级权限控制
   - 操作日志记录

## 安装与使用
```bash
# 克隆仓库
git clone https://github.com/yourrepo/landscape_lab.git

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python database/db.py --init

# 启动系统
python main.py
```

## 未来改进方向
### 近期规划
1. **性能优化**
   - 大文件加载分块处理
   - 模型解析缓存机制
   - 异步任务队列支持

2. **功能扩展**
   - BIM模型兼容性增强
   - 雨水径流模拟模块
   - 植物生长预测算法

3. **协作功能**
   - 多用户协同标注
   - 版本合并冲突解决
   - 实时评论系统

### 长期愿景
- 集成AR实景预览
- 接入GIS地理信息系统
- 开发移动端配套应用
