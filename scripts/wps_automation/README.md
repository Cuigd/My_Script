# WPS 自动化资源整理

这个目录用于集中整理 **WPS / 金山文档 自动化执行** 相关资源，方便后续在你的脚本仓库中统一管理与调用。

## 推荐路线

### 1. AirScript / 金山文档在线脚本
适合：
- 在金山文档、在线表格环境中执行自动化
- 做签到、表格处理、定时任务
- 多账号与推送类场景

优先参考：
- 官方 WPS 开放平台：宏编辑器、AirScript、加载项、自定义函数文档
- `poboll/wps_script`（MIT）：适用于金山文档 AirScript 自动化执行的签到脚本集合

## 2. Python 调用 WPS（RPC）
适合：
- 想从 Python 脚本侧控制 WPS
- 做批量打开、处理、保存、转换文档
- 偏 Linux / 二次开发场景

优先参考：
- `timxx/pywpsrpc`（MIT）：Python bindings for WPS Office RPC

## 3. Windows GUI 自动化
适合：
- 没有开放接口时，用桌面自动化方式操作 WPS 客户端
- 快捷键、按钮点击、窗口激活、批量重复任务

优先参考：
- `AutoHotkey/AutoHotkey`（GPL-2.0）：Windows 桌面自动化基础工具

## 目录说明

- `resources.md`：整理可复用的开源仓库与官方入口
- `python_rpc_example.py`：Python 侧的 WPS 自动化示例骨架
- `ahk/wps_hotkeys_example.ahk`：Windows 下的 AutoHotkey 调用示例

## 建议使用方式

### 场景 A：你想在“金山文档”里跑自动化
先看 `resources.md` 里的 AirScript 资源，再把目标脚本迁移到你自己的文档环境中执行。

### 场景 B：你想用 Python 统一管理 API / 自动化脚本
先从 `python_rpc_example.py` 改起，把你的业务逻辑包装成命令行参数或者函数调用。

### 场景 C：你只是想在 Windows 桌面上自动操作 WPS 客户端
直接用 `ahk/wps_hotkeys_example.ahk` 作为起点。

## 注意事项

1. 外部仓库代码请优先查看许可证后再决定是否完整引入。
2. 本仓库当前主要先做“资源索引 + 调用模板”，避免直接复制大段第三方代码。
3. 后续可以把你常用的 WPS 自动化任务继续拆分为：
   - `signin/`
   - `excel_tasks/`
   - `doc_convert/`
   - `gui_automation/`
