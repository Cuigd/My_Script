# WPS 自动化资源索引

## 官方文档
- WPS 开放平台（API / 自动化 / 集成）
- 宏编辑器 / JS API / AirScript

## GitHub 项目（可直接参考）

### 1. AirScript 脚本集合（推荐）
- https://github.com/poboll/wps_script
- MIT License
- 特点：支持签到、聚合脚本、多账号

### 2. Python 调用 WPS（RPC）
- https://github.com/timxx/pywpsrpc
- MIT License
- 特点：可通过 Python 控制 WPS 打开/编辑/保存文档

### 3. Windows 自动化（通用方案）
- https://github.com/AutoHotkey/AutoHotkey
- GPL-2.0
- 特点：通过快捷键、鼠标操作自动化任何桌面软件（包括 WPS）

## 如何选择

| 场景 | 推荐方案 |
|------|--------|
| 金山文档自动执行 | AirScript |
| Python 后端调度 | pywpsrpc |
| 桌面自动化 | AutoHotkey |

## 下一步建议

1. 选一个方向（AirScript / Python / GUI）
2. 在本仓库新增子目录
3. 把实际脚本逐步沉淀进来
