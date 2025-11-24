# PowerShell测试脚本
Write-Host "开始测试API服务..." -ForegroundColor Cyan

# 定义要测试的URLs
$urls = @{
    "API测试端点" = "http://127.0.0.1:8000/api/test"
    "根路径" = "http://127.0.0.1:8000/"
}

# 禁用SSL验证和代理，以避免常见问题
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# 测试每个URL
$allSuccess = $true

foreach ($url in $urls.GetEnumerator()) {
    Write-Host "`n测试 $($url.Key): $($url.Value)" -ForegroundColor Yellow
    
    try {
        # 记录开始时间
        $startTime = Get-Date
        
        # 发送请求，添加-UseBasicParsing避免IE相关问题
        $response = Invoke-WebRequest -Uri $url.Value -Method Get -TimeoutSec 5 -UseBasicParsing
        
        # 计算响应时间
        $endTime = Get-Date
        $responseTime = ($endTime - $startTime).TotalMilliseconds
        
        # 显示成功信息
        Write-Host "✅ 成功！状态码: $($response.StatusCode)" -ForegroundColor Green
        Write-Host "响应时间: $([math]::Round($responseTime, 2)) ms" -ForegroundColor Green
        
        # 尝试解析JSON响应
        try {
            $jsonData = $response.Content | ConvertFrom-Json
            Write-Host "响应内容(JSON):" -ForegroundColor Green
            $jsonData | Format-List | ForEach-Object { Write-Host "  $_" -ForegroundColor Green }
        } catch {
            Write-Host "响应内容(非JSON): $($response.Content)" -ForegroundColor Green
        }
        
    } catch {
        Write-Host "❌ 失败！错误: $($_.Exception.Message)" -ForegroundColor Red
        $allSuccess = $false
    }
}

Write-Host "`n=========================================" -ForegroundColor Cyan
if ($allSuccess) {
    Write-Host "✅ 所有测试都成功了！" -ForegroundColor Green
    Write-Host "`n后端服务已成功启动并响应请求。" -ForegroundColor Green
    Write-Host "如果浏览器仍然显示'Failed to fetch'，请检查：" -ForegroundColor Yellow
    Write-Host "1. 前端代码中的API URL是否正确设置为http://localhost:5000/api" -ForegroundColor Yellow
    Write-Host "2. 浏览器控制台是否有其他错误信息" -ForegroundColor Yellow
    Write-Host "3. 尝试刷新浏览器或清除缓存" -ForegroundColor Yellow
} else {
    Write-Host "❌ 测试失败，请检查服务器状态。" -ForegroundColor Red
}
Write-Host "=========================================" -ForegroundColor Cyan
