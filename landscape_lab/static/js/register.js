document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    
    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(registerForm);
        const data = {
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password'),
            confirmPassword: formData.get('confirmPassword')
        };

        // 客户端验证
        if (data.password !== data.confirmPassword) {
            alert('两次输入的密码不一致');
            return;
        }

        try {
            const response = await fetch('/api/users/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (response.ok) {
                // 注册成功，跳转到登录页面
                alert('注册成功，请登录');
                window.location.href = '/api/users/login';
            } else {
                // 显示错误信息
                alert(result.message || '注册失败，请检查输入信息');
            }
        } catch (error) {
            console.error('注册请求失败:', error);
            alert('网络错误，请稍后重试');
        }
    });

    // 输入框验证
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');

    [usernameInput, emailInput, passwordInput, confirmPasswordInput].forEach(input => {
        input.addEventListener('input', validateRegisterForm);
    });

    function validateRegisterForm() {
        const isUsernameValid = usernameInput.value.length >= 3;
        const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value);
        const isPasswordValid = passwordInput.value.length >= 8;
        const isConfirmPasswordValid = passwordInput.value === confirmPasswordInput.value;

        if (isUsernameValid && isEmailValid && isPasswordValid && isConfirmPasswordValid) {
            registerForm.querySelector('button').disabled = false;
        } else {
            registerForm.querySelector('button').disabled = true;
        }
    }
});
