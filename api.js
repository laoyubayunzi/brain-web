// API基础URL
const API_BASE_URL = 'http://localhost:8000/api';

/**
 * 通用API请求函数
 * @param {string} endpoint - API端点
 * @param {Object} data - 请求数据
 * @param {string} method - HTTP方法
 * @returns {Promise} - 返回Promise对象
 */
async function apiRequest(endpoint, data = null, method = 'GET') {
    try {
        const url = `${API_BASE_URL}/${endpoint}`;
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        };

        if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `请求失败: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API请求错误:', error);
        throw error;
    }
}

/**
 * 提交申请表
 * @param {Object} applicationData - 申请表数据
 * @returns {Promise}
 */
async function submitApplication(applicationData) {
    return await apiRequest('apply', applicationData, 'POST');
}

/**
 * 提交联系表单
 * @param {Object} contactData - 联系表单数据
 * @returns {Promise}
 */
async function submitContact(contactData) {
    return await apiRequest('contact', contactData, 'POST');
}

/**
 * 订阅通讯
 * @param {Object} newsletterData - 通讯订阅数据
 * @returns {Promise}
 */
async function subscribeNewsletter(newsletterData) {
    return await apiRequest('newsletter', newsletterData, 'POST');
}

// 活动日历功能已移除

/**
 * 获取统计数据
 * @returns {Promise}
 */
async function getStats() {
    return await apiRequest('stats');
}

/**
 * 初始化表单提交事件监听
 */
function initFormSubmissions() {
    // 申请表单处理
    const applicationForm = document.querySelector('#join form');
    if (applicationForm) {
        applicationForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            try {
                // 收集表单数据
                const formData = new FormData(applicationForm);
                const data = {
                    name: formData.get('name'),
                    student_id: formData.get('student-id'),
                    email: formData.get('email'),
                    phone: formData.get('phone'),
                    major: formData.get('major'),
                    interests: Array.from(formData.getAll('interest')),
                    experience: formData.get('experience'),
                    reason: formData.get('reason')
                };
                
                // 显示加载状态
                const submitButton = applicationForm.querySelector('button[type="submit"]');
                const originalText = submitButton.textContent;
                submitButton.disabled = true;
                submitButton.textContent = '提交中...';
                
                // 提交数据
                const result = await submitApplication(data);
                
                // 显示成功消息
                alert(result.message);
                
                // 重置表单
                applicationForm.reset();
                
            } catch (error) {
                alert('提交失败: ' + error.message);
            } finally {
                // 恢复按钮状态
                const submitButton = applicationForm.querySelector('button[type="submit"]');
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = '提交申请';
                }
            }
        });
    }
    
    // 联系表单处理
    const contactForm = document.querySelector('#contact form');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            try {
                // 收集表单数据
                const formData = new FormData(contactForm);
                const data = {
                    'contact-name': formData.get('contact-name'),
                    'contact-email': formData.get('contact-email'),
                    'contact-subject': formData.get('contact-subject'),
                    'contact-message': formData.get('contact-message')
                };
                
                // 显示加载状态
                const submitButton = contactForm.querySelector('button[type="submit"]');
                submitButton.disabled = true;
                submitButton.textContent = '发送中...';
                
                // 提交数据
                const result = await submitContact(data);
                
                // 显示成功消息
                alert(result.message);
                
                // 重置表单
                contactForm.reset();
                
            } catch (error) {
                alert('发送失败: ' + error.message);
            } finally {
                // 恢复按钮状态
                const submitButton = contactForm.querySelector('button[type="submit"]');
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = '发送消息';
                }
            }
        });
    }
    
    // 订阅表单处理
    const newsletterForm = document.querySelector('footer form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            try {
                // 收集表单数据
                const formData = new FormData(newsletterForm);
                const data = {
                    email: formData.get('email')
                };
                
                // 显示加载状态
                const submitButton = newsletterForm.querySelector('button[type="submit"]');
                submitButton.disabled = true;
                submitButton.textContent = '订阅中...';
                
                // 提交数据
                const result = await subscribeNewsletter(data);
                
                // 显示成功消息
                alert(result.message);
                
                // 重置表单
                newsletterForm.reset();
                
            } catch (error) {
                alert('订阅失败: ' + error.message);
            } finally {
                // 恢复按钮状态
                const submitButton = newsletterForm.querySelector('button[type="submit"]');
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = '订阅';
                }
            }
        });
    }
}

// 活动日历功能已移除

/**
 * 从API加载统计数据并更新图表
 */
async function loadStatsAndUpdateCharts() {
    try {
        const result = await getStats();
        
        // 更新论文统计图表
        if (window.Chart && document.getElementById('papersChart')) {
            const papersCtx = document.getElementById('papersChart').getContext('2d');
            const papersChart = new Chart(papersCtx, {
                type: 'line',
                data: {
                    labels: result.paper_stats.map(item => item.year),
                    datasets: [{
                        label: '发表论文数量',
                        data: result.paper_stats.map(item => item.count),
                        borderColor: '#3B82F6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        // 更新研究领域分布图表
        if (window.Chart && document.getElementById('researchChart')) {
            const researchCtx = document.getElementById('researchChart').getContext('2d');
            const researchChart = new Chart(researchCtx, {
                type: 'doughnut',
                data: {
                    labels: result.research_areas.map(item => item.area),
                    datasets: [{
                        data: result.research_areas.map(item => item.percentage),
                        backgroundColor: ['#3B82F6', '#10B981', '#8B5CF6', '#EC4899', '#6B7280']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                boxWidth: 12,
                                padding: 10
                            }
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('加载统计数据失败:', error);
        // 如果API加载失败，使用之前的硬编码数据
    }
}

/**
 * 初始化所有API功能
 */
function initAPI() {
    // 初始化表单提交
    initFormSubmissions();
    
    // 页面加载完成后加载数据
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            loadStatsAndUpdateCharts();
        });
    } else {
        loadStatsAndUpdateCharts();
    }
}

// 导出默认对象
// 暴露API到全局作用域
window.API = {
    submitApplication,
    submitContact,
    subscribeNewsletter,
    getStats,
    initFormSubmissions,
    loadStatsAndUpdateCharts,
    initAPI
};

// 页面加载完成后初始化API
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAPI);
} else {
    initAPI();
}