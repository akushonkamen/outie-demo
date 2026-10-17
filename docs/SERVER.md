# 服务器与部署清单（OurVerse / OUTIE）

> 2026-10-17 核对。含服务器 IP 与路径，勿公开传播；密钥本体不入库。

## 服务器
- **IP**：`150.109.197.231`（腾讯云境外节点）
- **SSH**：`ssh root@150.109.197.231`（本机已配密钥免密）
- **调试隧道**（跨境链路抖动时）：`ssh -f -N -L 1443:127.0.0.1:443 root@150.109.197.231` → 浏览器访问 `https://127.0.0.1:1443`

## 域名 / 接入
- `our-verse.com` / `www.our-verse.com`，GoDaddy 注册（已续费），A 记录 → 150.109.197.231，无 IPv6
- nginx 站点配置：`/etc/nginx/sites-enabled/ourverse`，80 跳 443，`/api` 反代 → `127.0.0.1:8444`
- nginx 日志：`/var/log/nginx/`；错误排查 `tail /var/log/nginx/error.log`

## 应用（OurVerse 仓库，服务器端）
- **目录**：`/home/ubuntu/OurVerse`（git 仓库）
- **前端**：`web/index.html` ← 本地 `~/projects/Outie/outie-live.html`
  - 部署 = `scp` 上去 + `md5sum` 校验
  - 改前先跑语法门：`bash ~/projects/Outie/deploy-check.sh`
- **后端**：`backend/`（Node），pm2 进程名 `ourverse`，属主 `ubuntu`，监听 `127.0.0.1:8444`
- **重启**：`sudo -u ubuntu HOME=/home/ubuntu pm2 restart ourverse --update-env`（或 `bash ourverse.sh`）
- **环境变量**：`backend/.env` —— `PORT=8444`、`NODE_ENV=production`、`RATE_LIMIT_MAX_REQUESTS`（生产 100，压测临时 3000）、`MAX_DISTANCE_VERIFICATION=50`、`AMAP_WEB_API_KEY / AMAP_REST_API_KEY / AMAP_SECURITY_CODE`（高德三件套）、`GITHUB_CLIENT_ID/SECRET/CALLBACK`（OAuth）、`MONGODB_URI`
- **日志**：`sudo -u ubuntu HOME=/home/ubuntu pm2 logs ourverse --lines 50 --nostream`

## 数据库
- Docker 容器 `ourverse-mongodb`（mongo:6.0），27017 仅本机监听
- 库名 `ourverse`，账号 `ourverse`，authSource `admin`
- 密码：`grep MONGODB_URI /home/ubuntu/OurVerse/backend/.env`
- 查询模板：
  `docker exec ourverse-mongodb mongosh -u ourverse -p <密码> --authenticationDatabase admin ourverse --quiet --eval '...'`

## 小程序
- 服务器：`/home/ubuntu/OurVerse/miniprogram`；本地副本：`~/projects/Outie/miniprogram`
- AppID：`wxdff88255ea6ab7ff`（小程序类型；旧值 `wxeb8d477e2a091679` 为小游戏类型已弃用，见 commit bd90f66）
- API 指向：`https://www.our-verse.com/api`

## 待办（安全）
- [ ] `JWT_SECRET` 仍为占位符（`your...` 开头）——有真实用户前换随机长串并重启
- [ ] `GITHUB_TOKEN`（PAT）与 `GITHUB_CLIENT_SECRET` 明文在 `.env`——若机器曾有人接触，去 GitHub 轮换 token
