# 荣达印尼官网（idn.jxrdxf.top）

PT Rongda Internasional 印尼双语官网源码。纯静态站，无构建步骤，改完即传。

## 目录

| 路径 | 说明 |
|---|---|
| `index.html` | 官网首页（印尼语主、中文辅，全部版块） |
| `onepager.html` | A4 一页式网页版 |
| `brochure.html` | 宣传册翻页版 |
| `id/` | 11 个独立页面：6 服务页 + 4 项目页 + FAQ（纯印尼语，GEO 可引用） |
| `robots.txt` `sitemap.xml` `llms.txt` | 搜索引擎与 AI 爬虫入口 |
| `media/` | 图片与二维码（wa-qr / web-qr / 宣传册页图） |
| `tools/check_site.py` | 站点自检脚本（改完必跑） |
| `.github/workflows/` | CI 自检 + COS 部署模板 |

## 日常更新三种操作

**1. 改数字 / 联系方式 / 文案**
改 `index.html`（有时还要同步 `onepager.html`、`llms.txt`），然后：

```bash
python3 tools/check_site.py   # 自检必须通过
git add -A && git commit -m "说明" && git push
```

**2. 加一个新项目 / 新服务页**
复制 `id/` 里最像的一个页面改内容；注意：
- 页面底部 CTA、页脚 NAP（地址/电话/WhatsApp）保持不动
- JSON-LD 里 `@id`、`url`、canonical 改成新路径
- 首页对应版块加一张卡片并链接过去
- 把新 URL 加进 `sitemap.xml` 和 `llms.txt`

**3. 换联系人 / 电话 / 二维码**
全局搜索旧号码，至少覆盖：`index.html`、`onepager.html`、`id/` 全部页面、`llms.txt`、
`media/wa-qr.png`（用 qrcode 重新生成）、宣传册与 A4 的 `.page` 源文件。改完跑自检。

## 铁律（改任何东西前看）

- 域名只能出现 `idn.jxrdxf.top`（`www.` 是国内站，`id.` 是历史笔误——自检脚本会拦）
- 资质口径：ISO 三证 / 高新 / 专精特新是**集团持有**，子公司不得写成自有
- 2GW 项目 = **单晶硅片（wafer，拉棒+切片）**，不是电池片（cell）
- 合同金额不上站；指定隐去的甲方名（如佳文）全站不得出现
- FAQ 的可见正文与 JSON-LD 必须逐字一致（改了答案两边一起改）

## 部署

- **EdgeOne Pages（推荐）**：控制台关联本仓库 main 分支，无构建命令，输出目录 `/`
- **COS**：启用 `.github/workflows/deploy-cos.yml`（按文件头注释配 4 个 Secrets）
- 推送到 main 即自动部署；部署后到 GSC/Bing 重新提交 `https://idn.jxrdxf.top/sitemap.xml`
