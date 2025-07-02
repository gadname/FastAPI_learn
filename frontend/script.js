document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('new-task-input');
    const addTaskButton = document.getElementById('add-task-button');
    const todoColumn = document.getElementById('todo-column').querySelector('.tasks-container');
    const columns = document.querySelectorAll('.column .tasks-container');

    let draggedTask = null;
    let taskIdCounter = 0; // Simple counter for unique task IDs

    // Sample tasks (optional)
    const initialTasks = [
        { id: `task-${taskIdCounter++}`, text: 'Design homepage', column: 'todo' },
        { id: `task-${taskIdCounter++}`, text: 'Develop API endpoints', column: 'inprogress' },
        { id: `task-${taskIdCounter++}`, text: 'Test feature X', column: 'done' }
    ];

    function createTaskElement(task) {
        const taskElement = document.createElement('div');
        taskElement.classList.add('task-card');
        taskElement.setAttribute('draggable', 'true');
        taskElement.setAttribute('id', task.id);
        taskElement.textContent = task.text;

        taskElement.addEventListener('dragstart', (event) => {
            draggedTask = event.target;
            event.dataTransfer.setData('text/plain', event.target.id);
            setTimeout(() => {
                event.target.style.display = 'none'; // Hide original while dragging
            }, 0);
        });

        taskElement.addEventListener('dragend', (event) => {
            setTimeout(() => {
                if (draggedTask) { // Check if it was dropped in a valid target
                    draggedTask.style.display = 'block'; // Make it visible again
                }
                draggedTask = null;
            }, 0);
        });
        return taskElement;
    }

    function renderTasks() {
        initialTasks.forEach(task => {
            const taskElement = createTaskElement(task);
            if (task.column === 'todo') {
                todoColumn.appendChild(taskElement);
            } else if (task.column === 'inprogress') {
                document.getElementById('inprogress-column').querySelector('.tasks-container').appendChild(taskElement);
            } else if (task.column === 'done') {
                document.getElementById('done-column').querySelector('.tasks-container').appendChild(taskElement);
            }
        });
    }

    function addNewTask() {
        const taskText = taskInput.value.trim();
        if (taskText === '') {
            alert('Please enter a task description.');
            return;
        }

        const newTask = {
            id: `task-${taskIdCounter++}`,
            text: taskText,
            // New tasks always start in 'todo'
        };

        const taskElement = createTaskElement(newTask);
        todoColumn.appendChild(taskElement);
        taskInput.value = ''; // Clear input field
    }

    addTaskButton.addEventListener('click', addNewTask);
    taskInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            addNewTask();
        }
    });

    columns.forEach(column => {
        column.addEventListener('dragover', (event) => {
            event.preventDefault(); // Allow dropping
        });

        column.addEventListener('drop', (event) => {
            event.preventDefault();
            if (draggedTask && event.target.classList.contains('tasks-container')) {
                event.target.appendChild(draggedTask);
                // draggedTask will be made visible again in its 'dragend' event
            } else if (draggedTask && event.target.classList.contains('column')) {
                // If dropped on column itself, append to its tasks-container
                event.target.querySelector('.tasks-container').appendChild(draggedTask);
            } else if (draggedTask && event.target.classList.contains('task-card')) {
                // If dropped on another task card, append to the parent tasks-container
                event.target.parentElement.appendChild(draggedTask);
            }
            // The draggedTask's display is handled in dragend
        });
    });

    // Initial rendering of tasks
    renderTasks();
});
