document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(loginForm);
        const data = {
            username: formData.get('username'),
            password: formData.get('password')
        };

        try {
            const response = await fetch('/api/users/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (response.ok) {
                // 登录成功，跳转到用户主页
                window.location.href = '/api/users/profile';
            } else {
                // 显示错误信息
                alert(result.message || '登录失败，请检查用户名和密码');
            }
        } catch (error) {
            console.error('登录请求失败:', error);
            alert('网络错误，请稍后重试');
        }
    });

    // 输入框验证
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');

    usernameInput.addEventListener('input', validateInput);
    passwordInput.addEventListener('input', validateInput);

    function validateInput() {
        const isUsernameValid = usernameInput.value.length >= 3;
        const isPasswordValid = passwordInput.value.length >= 8;

        if (isUsernameValid && isPasswordValid) {
            loginForm.querySelector('button').disabled = false;
        } else {
            loginForm.querySelector('button').disabled = true;
        }
    }
});
