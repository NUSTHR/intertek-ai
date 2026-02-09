# AI Questionaire (EU AI Act Compliance Mapper)

本项目包含前端问卷（Vue 3 + Vite）与后端规则引擎（FastAPI），用于依据欧盟 AI 法案（Regulation (EU) 2024/1689）执行范围判定、分类与结论生成。

## 项目结构
- frontend: `src/`（Vue 3、Pinia、Vue Router）
- backend: `backend/`（FastAPI、YAML 规则驱动）
- 规则资源：
  - 英文：`backend/app/resources/En/`
  - 中文：`backend/app/resources/Cn/`

## 环境要求
- Node.js ≥ 20.19 或 ≥ 22.12
- Python ≥ 3.10（推荐 3.11+）
- 包管理器：npm

## 后端安装与运行
1. 进入 `backend/`
2. 创建并激活虚拟环境（任选其一）：
   - Windows PowerShell：
     - `python -m venv .venv`
     - `.venv\\Scripts\\Activate.ps1`
   - macOS/Linux：
     - `python3 -m venv .venv`
     - `source .venv/bin/activate`
3. 安装依赖：
   - `pip install -r requirements.txt`
4. 启动服务（开发模式，默认端口 8000）：
   - `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000`
   - 说明：`--host 0.0.0.0` 允许局域网访问；`--reload` 热重载

## 前端安装与运行
1. 进入项目根目录
2. 安装依赖：
   - `npm install`
3. 配置后端地址（开发时建议显式设置）：
   - 在根目录创建 `.env`：
     ```
     VITE_API_BASE=http://127.0.0.1:8000
     ```
4. 启动前端（开发模式）：
   - `npm run dev`
   - 默认 Vite 在本机端口（如 5173），浏览器访问该地址即可

## 构建与预览
- 生产构建：
  - `npm run build`
- 本地预览构建产物：
  - `npm run preview`

## 语言切换与会话
- 语言持久化：`localStorage` 键 `questionnaire_lang`
- 后端接口均接受 `lang=en|cn`，由前端在请求中自动传递
- 切换语言时，题目会即时重新拉取并替换当前题目视图

## 常用脚本
- 代码检查：`npm run lint`
- 类型检查：`npm run type-check`
- 开发：`npm run dev`
- 构建：`npm run build`
- 预览：`npm run preview`

## 端口与网络
- 后端默认 `8000`
- 前端默认由 Vite 决定（如 `5173`）
- 局域网访问：后端需要 `--host 0.0.0.0`；前端开发模式如需被其它设备访问，需以 `--host 0.0.0.0` 启动（可参阅 Vite CLI 文档）

## 后端环境变量
- `REDIS_URL`：启用 Redis 会话存储（未设置则使用进程内内存）
- `LOG_LEVEL`：日志级别（默认 INFO）
- `LOG_FILE`：日志输出文件（默认 `logs/app.log`）
- `LOG_MAX_BYTES`：单个日志文件大小上限（默认 10485760）
- `LOG_BACKUP_COUNT`：日志轮转保留数量（默认 5）
- `SESSION_TTL_SECONDS`：会话存活秒数（默认 7200）
- `SESSION_CLEANUP_INTERVAL`：内存会话清理间隔秒数（默认 300）

## 规则引擎说明（简要）
- 规则通过 YAML 定义，后端加载后以数据驱动执行
- 变量类型支持：`boolean`、`string`、`list`（或 `string_list`）
- 条件表达式支持：`and`/`or`/`not`、`in`、`contains [list]`
- 结论模块（Module 9）会汇总各模块变量，生成风险等级与原因等输出

## 免责声明
本项目输出的结论仅供信息参考，不构成法律意见。最终分类须由合格专家复核。使用本项目不构成任何合同关系。
