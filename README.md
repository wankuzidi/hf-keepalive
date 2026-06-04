# HF Spaces Keepalive

通过 GitHub Actions 定时 ping Hugging Face Spaces，防止因长时间无访问被休眠。

## 快速上手

### 1. Fork / Clone 本仓库

### 2. 配置要保活的 Space URL

**方式 A（推荐）：GitHub Variables**

在仓库 → Settings → Variables → Actions 中添加：

| Name | Value |
|------|-------|
| `HF_SPACES` | 逗号分隔的 Space URL，例如 `https://your-name-space1.hf.space,https://your-name-space2.hf.space` |

**方式 B：`spaces.txt` 文件**

直接编辑仓库根目录的 `spaces.txt`，每行填一个 URL。

### 3. （可选）配置 HF Token

如果你的 Space 设置为私有，需要在 Settings → Secrets → Actions 中添加：

| Name | Value |
|------|-------|
| `HF_TOKEN` | 你的 Hugging Face Access Token |

### 4. 启用 Workflow

进入 Actions 标签页，点击 **Enable** 启用工作流。

默认每 5 分钟运行一次，你也可以在 Actions 页面手动触发。

## 配置调度频率

编辑 `.github/workflows/keep-alive.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: "*/5 * * * *"   # 每 5 分钟
  # - cron: "0 * * * *"   # 每小时
  # - cron: "*/30 * * * *" # 每 30 分钟
```

> **注意**：GitHub Actions 免费额度对公开仓库无限制；私有仓库每月有 2000 分钟免费额度。
