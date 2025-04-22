// ————————————————————————————————————————————————————————————
// 增加任务的按钮
const add_task_btn = document.getElementById('add-task-btn');

// 输入框
const task_input = document.getElementById('task-input');

// 任务栏 (ul 元素)
const task_list = document.getElementById('task-list');

// 显示没有代办事务的事务框 (p 元素)
const empty_message = document.getElementById('empty-message');

// 提示信息 (用于空输入提示)
const message = document.getElementById('input-message');

// 清理已经删除的任务
const clear_task = document.getElementById('clear-task');

// ————————————————————————————————————————————————————————————
// 组件函数
/**
 * 增加任务后 清空输入行
 */
const ClearContent = () => {
    // 清空内容
    task_input.value = '';
};

/**
 * 检查输入框是否为空
 * @returns {boolean} 如果为空或只有空格则返回 true，否则返回 false
 */
const IsEmpty = () => {
    return task_input.value.trim() === '';
};

/**
 * 显示临时的空输入提示消息
 */
const showTemporaryMessage = () => {
    if (message) {
        message.style.display = 'block';
        setTimeout(() => {
            message.style.display = 'none';
        }, 2000);
    }
};

const UpdateEmptyMessageVisibility = () => {
    if (!task_list || !empty_message) return; // 确保元素存在

    const all_tasks = task_list.querySelectorAll('li');
    const completed_tasks = task_list.querySelectorAll('li.completed');

    // 如果没有任务，或者有任务但所有任务都已完成
    if (
        all_tasks.length === 0 ||
        (all_tasks.length > 0 && all_tasks.length === completed_tasks.length)
    ) {
        empty_message.style.display = 'block';
    } else {
        empty_message.style.display = 'none';
    }
};

// ————————————————————————————————————————————————————————————
// 业务函数

/**
 * 增加任务
 * @param {Event} event - 触发展示的事件对象 (用于 preventDefault)
 */
const AddTask = (event) => {
    // 防止表单提交等默认行为
    if (event) {
        event.preventDefault();
    }

    // 增加任务 如果为空提示不能为空
    if (IsEmpty()) {
        showTemporaryMessage();
    }
    // 如果不是空 增加到任务区
    else {
        const taskText = task_input.value.trim();
        const new_task_li = document.createElement('li');
        // new_task_li.draggable = true; // REMOVED: 不再需要拖动

        const new_task_span = document.createElement('span');
        new_task_span.textContent = taskText;

        const new_task_btn = document.createElement('button');
        new_task_btn.classList.add('delete-btn');
        new_task_btn.textContent = '删除'; // 按钮文本

        new_task_li.appendChild(new_task_span);
        new_task_li.appendChild(new_task_btn);

        task_list.appendChild(new_task_li); // 添加到列表末尾

        // 更新空消息状态
        UpdateEmptyMessageVisibility();
    }
    // 然后清理输入框
    ClearContent();

    // 让输入框重新获得焦点
    task_input.focus();
};

/**
 * "删除"任务 (切换完成状态并移动)
 * 增加删除的样式，并将完成的任务移到底部，未完成的移到顶部
 * @param {Event} event - 点击事件对象
 */
const DeleteTask = (event) => {
    const button_clicked = event.target;
    const task_item = button_clicked.closest('li');
    if (task_item && task_list) {
        task_item.classList.toggle('completed');

        if (task_item.classList.contains('completed')) {
            button_clicked.textContent = '恢复';
            task_list.appendChild(task_item); // 完成的移到底部
        } else {
            button_clicked.textContent = '删除';
            task_list.prepend(task_item); // 未完成的移到顶部
        }

        // 更新空消息状态
        UpdateEmptyMessageVisibility();
    }
};

/**
 *
 */
const ClearTask = () => {};

// ————————————————————————————————————————————————————————————
// 主要倾听业务代码
document.addEventListener('DOMContentLoaded', () => {
    if (add_task_btn) {
        add_task_btn.addEventListener('click', AddTask);
    } else {
        console.error("错误：未找到 ID 为 'add-task-btn' 的元素。");
    }

    if (task_input) {
        task_input.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                AddTask(event); // 传递事件对象
            }
        });
    } else {
        console.error("错误：未找到 ID 为 'task-input' 的元素。");
    }

    if (task_list) {
        task_list.addEventListener('click', (event) => {
            if (event.target.classList.contains('delete-btn')) {
                DeleteTask(event);
            }
        });
    } else {
        console.error("错误：未找到 ID 为 'task-list' 的元素。");
    }
    UpdateEmptyMessageVisibility();
});
