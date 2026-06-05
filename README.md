# pb 部署备忘

## 启动/停止

```bash
# 后台启动
cd ~/pb && docker-compose up -d

# 停止
cd ~/pb && docker-compose down

# 查看状态
docker ps --filter "name=pb-"
```

## 服务端口

| 服务 | 端口 |
|------|------|
| pb | 10002 |
| MongoDB | 27017（内部）|

## 踩坑记录

### 网络
- Docker Hub 不通 → 手动从 `docker.1ms.run` 拉镜像再 `docker tag`
- PyPI 超时 → 阿里云镜像（apk + pip）

### 依赖兼容
- `pymongo==3.7.2` → `4.6.3`（Python 3.11 C 扩展不兼容）
- `docutils==0.14` → `0.20.1`（`rU` 模式已移除）
- `requirements.txt` 开头有 BOM 字符，已清除
- `setup.py` 读依赖时带换行符，已修复
- 构建前预装 `setuptools-scm`

### 已修改的文件
- `Dockerfile`：预装 setuptools-scm、升级 pip
- `requirements.txt`：升级 pymongo 和 docutils
- `setup.py`：修复依赖解析

## 相关链接

- [Issue #257](https://github.com/ptpb/pb/issues/257)
- [PR #258](https://github.com/ptpb/pb/pull/258)
