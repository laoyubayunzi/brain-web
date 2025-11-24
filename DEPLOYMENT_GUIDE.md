# 网站部署指南

本文档详细说明如何将 SAU脑机与人工智能俱乐部 网站部署到服务器上。

## 1. 项目架构概览

- **前端**: 静态网站（HTML, CSS, JavaScript）
- **后端**: Python Flask 应用，提供RESTful API
- **数据库**: SQLite (可切换为MySQL/PostgreSQL)
- **端口配置**: 前端和后端分开部署，后端API使用8000端口

## 2. 服务器环境要求

### 2.1 必要软件

- **操作系统**: Linux (Ubuntu 20.04+/CentOS 8+ 推荐)
- **Python**: 3.8 或更高版本
- **Web服务器**: Nginx (用于静态文件和反向代理)
- **WSGI服务器**: Gunicorn (用于运行Flask应用)
- **版本控制**: Git (可选，用于代码部署)

### 2.2 防火墙配置

需要开放以下端口：
- 80 (HTTP)
- 443 (HTTPS，如果配置)
- 8000 (后端API服务，仅在内部访问)

## 3. 后端服务部署

### 3.1 安装依赖

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装Python和相关工具
sudo apt install python3 python3-pip python3-venv -y

# 安装Nginx
sudo apt install nginx -y
```

### 3.2 部署后端应用

```bash
# 创建项目目录
sudo mkdir -p /var/www/brain-web/backend
sudo chown -R $USER:$USER /var/www/brain-web

# 进入后端目录
cd /var/www/brain-web/backend

# 复制项目文件（通过Git或其他方式）
# git clone <repository-url> .  或者直接上传文件

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建环境变量文件
cp .env.example .env
# 编辑.env文件设置环境变量
# nano .env
```

### 3.3 配置Gunicorn服务

创建systemd服务文件：

```bash
sudo nano /etc/systemd/system/brain-web-backend.service
```

添加以下内容：

```ini
[Unit]
Description=SAU Brain Web Backend API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/brain-web/backend
Environment="PATH=/var/www/brain-web/backend/venv/bin"
ExecStart=/var/www/brain-web/backend/venv/bin/gunicorn --workers 3 --bind unix:/var/www/brain-web/backend/brain-web.sock production_start:app

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start brain-web-backend
sudo systemctl enable brain-web-backend
```

## 4. 前端静态文件部署

### 4.1 复制静态文件

```bash
# 创建前端目录
sudo mkdir -p /var/www/brain-web/frontend

# 复制前端文件（HTML, CSS, JS, images等）到该目录
# 确保api.js中的API_BASE_URL配置正确，指向部署的API地址
```

### 4.2 配置Nginx

创建Nginx配置文件：

```bash
sudo nano /etc/nginx/sites-available/brain-web
```

添加以下内容：

```nginx
server {
    listen 80;
    server_name example.com; # 替换为你的域名

    # 前端静态文件配置
    root /var/www/brain-web/frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理配置
    location /api {
        proxy_pass http://unix:/var/www/brain-web/backend/brain-web.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置并重启Nginx：

```bash
sudo ln -s /etc/nginx/sites-available/brain-web /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 5. 数据库配置（可选）

### 5.1 使用MySQL替代SQLite（推荐）

```bash
# 安装MySQL
sudo apt install mysql-server -y

# 创建数据库和用户
mysql -u root -p

CREATE DATABASE brainweb;
CREATE USER 'brainweb_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON brainweb.* TO 'brainweb_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

更新.env文件：

```
DATABASE_URL=mysql+pymysql://brainweb_user:your_password@localhost/brainweb
```

更新requirements.txt，添加MySQL驱动：

```
pymysql==1.0.3
```

## 6. 配置HTTPS（推荐）

使用Let's Encrypt获取免费SSL证书：

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d example.com -d www.example.com
```

## 7. 部署验证与测试

1. 检查服务状态：
   ```bash
   sudo systemctl status brain-web-backend
   sudo systemctl status nginx
   ```

2. 测试API端点：
   ```bash
   curl http://localhost/api/stats
   ```

3. 通过浏览器访问网站，测试所有功能

## 8. 部署完成后的维护

### 8.1 定期更新

```bash
# 进入项目目录
cd /var/www/brain-web/backend

# 激活虚拟环境
source venv/bin/activate

# 更新代码（如果使用Git）
git pull

# 安装更新的依赖
pip install -r requirements.txt

# 重启服务
sudo systemctl restart brain-web-backend
sudo systemctl restart nginx
```

### 8.2 日志管理

- Nginx日志：`/var/log/nginx/access.log` 和 `/var/log/nginx/error.log`
- 应用日志：使用 `sudo journalctl -u brain-web-backend` 查看

### 8.3 数据库备份

对于SQLite数据库：
```bash
cp /var/www/brain-web/backend/instance/bciai_club.db /path/to/backup/bciai_club_$(date +%Y%m%d).db
```

## 9. 故障排除

### 9.1 常见问题

1. **API连接失败**：检查Gunicorn服务状态和Nginx代理配置
2. **数据库错误**：检查数据库连接字符串和权限设置
3. **静态文件不加载**：确认Nginx配置中的root路径正确
4. **端口被占用**：使用 `netstat -tulpn` 检查端口占用情况

### 9.2 性能优化

- 增加Gunicorn工作进程数
- 配置Nginx缓存
- 考虑使用CDN分发静态资源

## 10. Docker部署（可选）

如果使用Docker部署，可以创建以下Dockerfile和docker-compose.yml文件。

---

以上是完整的部署指南。按照这些步骤，您可以成功地将网站部署到生产服务器上。