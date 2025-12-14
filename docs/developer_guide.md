# 网易云音乐下载器开发者文档

## 项目结构

```
NeteaseMusicDownloader/
├── main.py                 # 程序入口文件
├── requirements.txt        # 依赖包列表
├── README.md              # 项目说明文档
├── LICENSE                # 开源许可证
├── build.py              # 构建脚本
├── src/                  # 源代码目录
│   ├── api/             # API接口模块
│   │   └── netease_api.py
│   ├── auth/            # 认证模块
│   │   └── cookie_manager.py
│   ├── core/            # 核心下载模块
│   │   └── downloader.py
│   ├── ui/              # 用户界面模块
│   │   └── app.py
│   └── utils/           # 工具函数模块
│       └── helpers.py
└── docs/                # 文档目录
    └── usage_guide.md   # 使用说明
```

## 核心模块说明

### 1. API模块 (src/api/netease_api.py)
负责与网易云音乐API交互：
- 获取歌曲下载链接
- 获取歌曲详细信息
- 获取歌词信息
- 获取歌单详情

### 2. 认证模块 (src/auth/cookie_manager.py)
负责用户认证和Cookie管理：
- 浏览器自动登录
- Cookie保存和读取
- 登录状态检查

### 3. 核心下载模块 (src/core/downloader.py)
负责文件下载和处理：
- HTTP请求下载
- 进度跟踪
- 元数据嵌入
- 连接池优化

### 4. 用户界面模块 (src/ui/app.py)
负责图形界面展示和交互：
- Flet界面构建
- 用户事件处理
- 下载任务管理

### 5. 工具函数模块 (src/utils/helpers.py)
提供通用工具函数：
- 文件名清理
- 文件命名生成
- 已下载文件扫描
- 拼音排序

## 构建说明

### macOS构建
使用PyInstaller打包为macOS应用：
```bash
python build.py
```

构建脚本会：
1. 使用PyInstaller打包Python程序
2. 修复应用包的Info.plist
3. 处理代码签名问题
4. 创建最终发布版本

## 依赖包说明

### 核心依赖
- `flet`: 图形界面框架
- `requests`: HTTP请求库
- `pyncm`: 网易云音乐API封装
- `cryptography`: 加密库
- `mutagen`: 音频元数据处理
- `Pillow`: 图像处理
- `pypinyin`: 中文拼音转换

### 可选依赖
- `selenium`: 浏览器自动化（登录功能）

## 代码规范

### 命名规范
- 类名使用大驼峰命名法（CamelCase）
- 函数和变量使用小写字母加下划线（snake_case）
- 常量使用大写字母加下划线（UPPER_CASE）

### 注释规范
- 类和函数需要文档字符串说明
- 复杂逻辑需要行内注释
- 变量命名应具有描述性

### 错误处理
- 网络请求需要异常捕获
- 文件操作需要异常处理
- 用户输入需要验证

## 扩展开发

### 添加新功能
1. 在相应模块中添加新功能函数
2. 在UI模块中添加对应的界面元素
3. 更新requirements.txt（如有新依赖）
4. 测试功能并更新文档

### 优化建议
1. 下载速度优化
2. 内存使用优化
3. 用户体验改进
4. 错误处理完善

## 版本管理

使用语义化版本号：MAJOR.MINOR.PATCH
- MAJOR：不兼容的重大变更
- MINOR：向后兼容的功能新增
- PATCH：向后兼容的问题修复

## 贡献指南

欢迎提交Issue和Pull Request：
1. Fork项目仓库
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 许可证

本项目采用MIT许可证，详见LICENSE文件。