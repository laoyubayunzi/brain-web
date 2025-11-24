# HTTPS配置指南

## 概述

本指南提供了为SAU脑机与人工智能俱乐部网站配置HTTPS的详细步骤。HTTPS通过SSL/TLS协议加密网站流量，保护用户数据安全，同时提升网站的搜索引擎排名和用户信任度。

## 目录

1. [获取SSL证书](#获取ssl证书)
2. [在Nginx中配置HTTPS](#在nginx中配置https)
3. [更新Docker配置](#更新docker配置)
4. [自动续期SSL证书](#自动续期ssl证书)
5. [验证HTTPS配置](#验证https配置)

## 获取SSL证书

### 使用Let's Encrypt（推荐）

Let's Encrypt提供免费的SSL证书，适合大多数网站使用。

#### 在Linux服务器上安装Certbot

```bash
# Ubuntu/Debian系统
apt update
apt install certbot python3-certbot-nginx -y

# CentOS/RHEL系统
dnf install epel-release -y
dnf install certbot python3-certbot-nginx -y
```

#### 获取证书

```bash
# 自动配置Nginx
certbot --nginx -d example.com -d www.example.com

# 仅获取证书，手动配置
certbot certonly --nginx -d example.com -d www.example.com
```

### 使用其他证书颁发机构

如果需要更高级别的证书（如EV证书），可以考虑付费的证书颁发机构如DigiCert、Comodo等。

## 在Nginx中配置HTTPS

### 基本HTTPS配置

将以下配置添加到Nginx配置文件中（替换现有的HTTP服务器块）：

```nginx
# 重定向HTTP到HTTPS
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$host$request_uri;
}

# HTTPS服务器配置
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    # SSL证书配置
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    # SSL优化配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    
    # HSTS配置
    add_header Strict-Transport-Security "max-age=63072000" always;
    
    # 前端静态文件配置
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # 后端API反向代理
    location /api {
        proxy_pass http://backend:8000/api;
        # 其他代理配置...
    }
    
    # 其他配置...
}
```

## 更新Docker配置

### 修改docker-compose.yml

更新docker-compose.yml以支持HTTPS：

```yaml
# 修改nginx服务部分
nginx:
  image: nginx:alpine
  container_name: brainweb-nginx
  restart: always
  ports:
    - "80:80"
    - "443:443"  # 添加HTTPS端口
  volumes:
    - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    - ./:/var/www/html:ro
    - /etc/letsencrypt:/etc/letsencrypt:ro  # 挂载证书目录
  depends_on:
    - backend
  networks:
    - brainweb-network
```

### 使用Docker Compose进行部署

```bash
docker-compose down
docker-compose up -d
```

## 自动续期SSL证书

Let's Encrypt证书的有效期为90天，需要定期续期。可以设置自动续期：

### 创建定时任务

```bash
# 编辑crontab
crontab -e

# 添加以下行（每天凌晨2点检查证书是否需要续期）
0 2 * * * certbot renew --nginx --quiet && systemctl reload nginx
```

对于Docker环境，可以创建一个专用的续期容器或在宿主机上执行续期。

## 验证HTTPS配置

部署完成后，使用以下方法验证HTTPS配置：

1. **浏览器访问**：在浏览器中访问`https://example.com`，检查地址栏是否显示锁图标
2. **SSL Labs测试**：访问[SSL Labs](https://www.ssllabs.com/ssltest/)，输入您的域名进行全面测试
3. **手动检查**：使用curl测试证书

```bash
curl -I https://example.com
```

## 常见问题排查

1. **证书不被信任**：确保使用了完整的证书链（fullchain.pem）
2. **配置错误**：检查Nginx配置文件语法
   ```bash
   nginx -t
   ```
3. **端口未开放**：确保服务器防火墙允许443端口
   ```bash
   # Ubuntu/Debian
   ufw allow 443/tcp
   
   # CentOS/RHEL
   firewall-cmd --permanent --add-port=443/tcp
   firewall-cmd --reload
   ```

## 安全最佳实践

1. 定期更新证书和服务器软件
2. 启用HTTP严格传输安全（HSTS）
3. 配置适当的CORS策略
4. 定期扫描SSL/TLS配置的安全漏洞

---

完成上述步骤后，您的网站将成功配置HTTPS，提供加密通信和更好的安全性。
