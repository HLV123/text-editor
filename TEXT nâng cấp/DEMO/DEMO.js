class TodoApp {
    constructor() {
        this.todos = [];
        this.nextId = 1;
    }

    addTodo(text) {
        const todo = {
            id: this.nextId++,
            text: text,
            completed: false,
            createdAt: new Date()
        };
        this.todos.push(todo);
        return todo;
    }

    completeTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = true;
            return true;
        }
        return false;
    }

    deleteTodo(id) {
        const index = this.todos.findIndex(t => t.id === id);
        if (index !== -1) {
            this.todos.splice(index, 1);
            return true;
        }
        return false;
    }

    getTodos(filter = 'all') {
        switch (filter) {
            case 'active':
                return this.todos.filter(t => !t.completed);
            case 'completed':
                return this.todos.filter(t => t.completed);
            default:
                return [...this.todos];
        }
    }
}

// Sử dụng ứng dụng
const app = new TodoApp();
app.addTodo("Học JavaScript");
app.addTodo("Làm bài tập");
app.completeTodo(1);
console.log(app.getTodos());