#!/bin/bash

# SAU脑机与人工智能俱乐部网站 - 服务器环境设置脚本
# 此脚本用于在Ubuntu/Debian服务器上设置完整的部署环境

echo "===================================="
echo "SAU脑机与人工智能俱乐部网站部署环境设置"
echo "===================================="

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then
  echo "请以root权限运行此脚本：sudo $0"
  exit 1
fi

# 更新系统包
echo "更新系统包..."
apt update
apt upgrade -y

# 安装基本工具
echo "安装基本工具..."
apt install -y build-essential git curl wget unzip

# 安装Python和相关工具
echo "安装Python和相关工具..."
apt install -y python3 python3-pip python3-venv python3-dev

# 升级pip
echo "升级pip..."
pip3 install --upgrade pip

# 安装Nginx
echo "安装Nginx..."
apt install -y nginx

# 启动并启用Nginx
systemctl start nginx
systemctl enable nginx

# 安装MySQL（可选）
read -p "是否安装MySQL数据库？(y/n) [n]: " install_mysql
if [[ $install_mysql == "y" || $install_mysql == "Y" ]]; then
  echo "安装MySQL..."
  apt install -y mysql-server mysql-client
  
  # 启动并启用MySQL
  systemctl start mysql
  systemctl enable mysql
  
  echo "MySQL已安装。请在部署应用后手动创建数据库和用户。"
  echo "示例命令："
  echo "mysql -u root -p"
  echo "CREATE DATABASE brainweb;"
  echo "CREATE USER 'brainweb_user'@'localhost' IDENTIFIED BY 'your_password';"
  echo "GRANT ALL PRIVILEGES ON brainweb.* TO 'brainweb_user'@'localhost';"
  echo "FLUSH PRIVILEGES;"
fi

# 创建项目目录
echo "创建项目目录结构..."
mkdir -p /var/www/brain-web/frontend
mkdir -p /var/www/brain-web/backend/instance

# 设置目录权限
echo "设置目录权限..."
chown -R www-data:www-data /var/www/brain-web
chmod -R 755 /var/www/brain-web

# 配置防火墙
echo "配置防火墙..."
apt install -y ufw
ufw allow 'Nginx Full'
ufw allow OpenSSH
ufw --force enable

# 安装Node.js（用于前端构建，如果需要）
read -p "是否安装Node.js用于前端构建？(y/n) [n]: " install_node
if [[ $install_node == "y" || $install_node == "Y" ]]; then
  echo "安装Node.js..."
  curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
  apt install -y nodejs
  npm install -g npm
fi

# 显示安装摘要
echo "===================================="
echo "环境设置完成！"
echo "===================================="
echo "已安装的组件："
echo "- Python $(python3 --version)"
echo "- pip $(pip3 --version | head -n 1)"
echo "- Nginx $(nginx -v 2>&1)"
if [[ $install_mysql == "y" || $install_mysql == "Y" ]]; then
  echo "- MySQL $(mysql --version)"
fi
if [[ $install_node == "y" || $install_node == "Y" ]]; then
  echo "- Node.js $(node --version)"
  echo "- npm $(npm --version)"
fi
echo ""
echo "项目目录：/var/www/brain-web"
echo "前端目录：/var/www/brain-web/frontend"
echo "后端目录：/var/www/brain-web/backend"
echo ""
echo "下一步操作："
echo "1. 将前端文件复制到 /var/www/brain-web/frontend"
echo "2. 将后端文件复制到 /var/www/brain-web/backend"
echo "3. 按照DEPLOYMENT_GUIDE.md配置服务"
echo ""
echo "端口开放状态："
echo "- 80 (HTTP) - 已开放"
echo "- 443 (HTTPS) - 已开放"
echo "- 22 (SSH) - 已开放"
echo "===================================="
