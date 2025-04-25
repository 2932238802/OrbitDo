// ————————————————————————————————————————————————————————————————
// 参数

// 提交按钮
const submit_btn = document.getElementById('submit-btn');

// 计时
let timeleft = 60;
let time = document.getElementById('timer');
let time_flow;

// 分数
let score = document.getElementById('score');

// 输入框
let input = document.getElementById('user-input');

// 历史区
let history = document.getElementById('history');

// 重新开始按钮
let restart_btn = document.getElementById('restart-btn');

// 上交的框
let game_form = document.getElementById('game-form');

// ————————————————————————————————————————————————————————————————
// 组件函数
const UpdateTime = () => {
    if (timeleft > 0) {
        timeleft--;
        time.textContent = timeleft;
    } else {
        alert('时间到了铁子！');
        clearInterval(time_flow);
        if (restart_btn) {
            restart_btn.style.display = 'block';
        }
        submit_btn.disabled = true;
        input.disabled = true;
    }
};

function Restart() {
    document.getElementById('user-input').disabled = false;
    document.getElementById('submit-btn').disabled = false;
    document.getElementById('restart-btn').style.display = 'none';
    document.getElementById('score').textContent = '0';
    document.getElementById('timer').textContent = '60';
    document.getElementById('current-idiom').textContent = '龙飞凤舞';
    document.getElementById('history').innerHTML = `
        <div class="history-item">
            <span>【系统】游戏开始！</span>
            <span>现在</span>
        </div>
    `;
    document.getElementById('user-input').value = '';
    timeleft = 60;
    time_flow = setInterval(UpdateTime, 1000);
}

const PostData = async (data) => {
    try {
        const response = await fetch('/returnanswer/', {
            method: 'POST',
            // 这样同源 会好点
            mode: 'same-origin',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
            },
            redirect: 'follow',
            referrerPolicy: 'no-referrer',
            body: JSON.stringify(data),
        });

        // 不行就抛出错误
        if (!response.ok) {
            throw new Error(`Http ${response.status} 错误!`);
        }
        return await response.json();
    } catch (error) {
        // 去接受上面的错误
        console.error('错误:', error);
    }
};

time_flow = setInterval(UpdateTime, 1000);

// ————————————————————————————————————————————————————————————————
// 业务函数
const Submit = (event) => {
    event.preventDefault();

    let current_idiom = document.getElementById('current-idiom').textContent;
    input.disabled = true;
    submit_btn.disabled = true;

    // 获得成语数据
    const idiom = input.value.trim();

    if (idiom === '') {
        alert('请输入一个成语!!!');
        input.disabled = false;
        submit_btn.disabled = false;
        return;
    }

    const data = { idiom: idiom };

    // 输出参数
    PostData(data)
        .then((response) => {
            if (response.valid) {
                document.getElementById('current-idiom').textContent = idiom;

                // 更新分数
                let currentScore = parseInt(score.textContent, 10); // 使用 score
                currentScore++;
                score.textContent = currentScore;

                // 清空输入框
                input.value = '';

                // 历史记录处理一下
                // 格式化一下时间
                const current_time = new Date().toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                });

                const newspan = document.createElement('div');
                newspan.className = 'history-item';
                newspan.innerHTML = `<span>${current_idiom}->${idiom}</span><span>${current_time}</span>`;
                history.appendChild(newspan);
                history.scrollTop = history.scrollHeight;
            } else {
                alert(`${response.message}`);
                input.value = '';
            }
            // 重新启用 输入和按钮
            input.disabled = false;
            submit_btn.disabled = false;
        })
        .catch((error) => {
            console.error('游戏出错', error);
            alert('提交失败，请稍后重试');

            // 重新启用
            input.disabled = false;
            submit_btn.disabled = false;
        });
};

// ————————————————————————————————————————————————————————————————
// 响应式
document.addEventListener('DOMContentLoaded', () => {
    if (submit_btn) {
        submit_btn.addEventListener('click', Submit);
    } else {
        console.error('找不到提交成语的按钮元素');
    }

    if (restart_btn) {
        restart_btn.addEventListener('click', Restart);
    } else {
        console.error('找不到重开的按钮元素');
    }
});
