# AI Interview Tag Pool | 视频访谈AI标签生成项目

## 📖 Project Introduction / 项目介绍

**English**: An end-to-end automated pipeline for YouTube interview/video subtitle processing and AI tagging. The system automatically downloads video subtitles, splits content into complete semantic segments, generates standard tags based on a fixed tag pool, and saves structured results.

**中文**: 一套端到端的 YouTube 访谈/视频字幕 AI 标签自动化处理流水线。项目可自动下载视频字幕、将内容切分为完整语义片段，基于固定标签池生成标准化标签，并持久化保存结构化结果。

## ⚙️ Core Functions / 核心功能

**English**

- Auto-download and parse YouTube subtitles

- Intelligent semantic segmentation (complete sentence-based segments, no fragmented text)

- Standard AI tagging based on fixed tag pool

- Batch processing & error retry mechanism

- Automated result storage and output

**中文**

- 自动下载、解析 YouTube 视频字幕

- 智能语义分段（基于完整句子，无残缺文本片段）

- 依托固定标签池，生成标准化 AI 标签

- 支持批量处理、异常重试机制

- 结果自动存储、结构化输出

## 🔄 Pipeline Workflow / 运行流程

**English**: The main program orchestrates three core services to complete the full processing flow:

**中文**: 主程序串联三大核心服务，完成全流程自动化处理：

`Subtitle Download → AI Segmentation & Tagging → Result Storage | 字幕下载 → AI分段打标 → 结果存储`

1. **SubtitleService**: Extract and clean original video subtitles / 提取并清洗原始视频字幕

2. **TaggingService**: Split subtitles into semantic segments and generate standard tags / 字幕语义分段、AI 智能打标

3. **StorageService**: Save tagged structured data locally / 将打标后的结构化数据落地保存

## 📁 Project Structure / 项目结构

**English**

- `main.py`: Entry file, pipeline orchestration core

- `config.py`: Global configuration, environment variables, fixed tag pool management

- `services/`: Core business service modules

- `.env`: Local private environment variables (secrets, not committed)

**中文**

- `main.py`: 项目入口文件，负责整体流水线调度

- `config.py`: 全局配置文件，管理环境变量、固定标签池

- `services/`: 核心业务服务模块目录

- `.env`: 本地私密环境变量配置（密钥、参数，禁止上传）

## 🚀 Usage / 使用方式

### Prerequisites / 前置条件

**English**: Python 3.8+ installed, complete .env configuration, and dependent libraries installed.

**中文**: 安装 Python 3.8+ 版本，配置好本地 .env 环境变量，安装项目依赖库。

### Run Command / 运行指令

**English**: Execute the script with a YouTube video URL parameter

**中文**: 传入 YouTube 视频链接参数运行脚本

```Plain Text
# Basic usage / 基础运行
python main.py <youtube_video_url>

# Example / 示例
python main.py "https://www.youtube.com/watch?v=xxxxxx"
```

## 📤 Output Description / 输出说明

**English**: After successful operation, the system outputs structured data prefixed with `tagged_segments`, including original subtitle content, semantic segments, and AI-matched standard tags.

**中文**: 程序运行成功后，会生成 `tagged_segments` 前缀的结构化结果文件，包含原始字幕、语义分段内容、AI 匹配的标准化标签。

## 🛡️ Error Handling Mechanism / 异常处理机制

**English**

- Intercept subtitle download failures and output error logs

- Catch AI tagging exceptions during batch processing

- Record and feedback file storage failures

- Built-in retry logic for unstable API requests

**中文**

- 拦截字幕下载异常，精准输出错误日志

- 捕获批量处理中 AI 打标失败异常

- 记录并反馈文件存储失败问题

- 内置接口请求重试机制，适配网络波动场景

## 📌 Features Highlights / 项目优势

**English**

- **Standardized**: Unified fixed tag pool to avoid messy custom tags

- **Semantic Priority**: Segment based on complete sentences to ensure tagging accuracy

- **Robust**: Complete error handling and batch processing logic

- **Maintainable**: Decoupled service architecture, centralized config management

**中文**

- **标准化**: 固定标签池统一输出，避免标签杂乱无序

- **语义优先**: 以完整句子为单位分段，大幅提升打标精准度

- **高稳健**: 完善的异常捕获、批量处理、重试机制

- **易维护**: 服务解耦架构，配置集中管理，便于迭代优化
> （注：文档部分内容可能由 AI 生成）
