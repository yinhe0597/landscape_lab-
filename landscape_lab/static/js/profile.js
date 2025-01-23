document.addEventListener('DOMContentLoaded', function() {
    // 加载用户项目数据
    loadUserProjects();

    // 绑定修改密码表单提交事件
    const changePasswordForm = document.getElementById('changePasswordForm');
    if (changePasswordForm) {
        changePasswordForm.addEventListener('submit', handleChangePassword);
    }

    // 绑定退出登录按钮点击事件
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', handleLogout);
    }
});

async function loadUserProjects() {
    try {
        const response = await fetch('/api/users/projects');
        const projects = await response.json();
        
        if (response.ok) {
            renderProjects(projects);
        } else {
            console.error('获取项目数据失败:', projects.message);
        }
    } catch (error) {
        console.error('网络请求失败:', error);
    }
}

function renderProjects(projects) {
    const projectList = document.querySelector('.project-list');
    if (!projectList) return;

    projectList.innerHTML = projects.map(project => `
        <div class="project-item">
            <h4>${project.name}</h4>
            <p>创建时间：${new Date(project.created_at).toLocaleDateString()}</p>
            <a href="/projects/${project.id}" class="btn-view">查看详情</a>
        </div>
    `).join('');
}

async function handleChangePassword(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        oldPassword: formData.get('oldPassword'),
        newPassword: formData.get('newPassword'),
        confirmPassword: formData.get('confirmPassword')
    };

    // 客户端验证
    if (data.newPassword !== data.confirmPassword) {
        alert('新密码和确认密码不一致');
        return;
    }

    try {
        const response = await fetch('/api/users/change-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        if (response.ok) {
            alert('密码修改成功');
            window.location.reload();
        } else {
            alert(result.message || '密码修改失败');
        }
    } catch (error) {
        console.error('密码修改请求失败:', error);
        alert('网络错误，请稍后重试');
    }
}

async function handleLogout() {
    try {
        const response = await fetch('/api/users/logout', {
            method: 'POST'
        });

        if (response.ok) {
            window.location.href = '/api/users/login';
        } else {
            const result = await response.json();
            alert(result.message || '退出登录失败');
        }
    } catch (error) {
        console.error('退出登录请求失败:', error);
        alert('网络错误，请稍后重试');
    }
}
