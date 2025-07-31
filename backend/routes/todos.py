from flask import Blueprint, request, jsonify
from models.models import Todo, db
from utils.auth import jwt_required_with_user
from utils.email_service import send_todo_notification
from datetime import datetime

todos_bp = Blueprint('todos', __name__, url_prefix='/api/todos')

@todos_bp.route('', methods=['GET'])
@jwt_required_with_user
def get_todos(current_user):
    """Get all todos for current user"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        completed = request.args.get('completed')
        priority = request.args.get('priority')
        search = request.args.get('search', '').strip()
        
        # Build query
        query = Todo.query.filter_by(user_id=current_user.id)
        
        # Apply filters
        if completed is not None:
            completed_bool = completed.lower() in ['true', '1', 'yes']
            query = query.filter_by(completed=completed_bool)
        
        if priority and priority in ['low', 'medium', 'high']:
            query = query.filter_by(priority=priority)
        
        if search:
            query = query.filter(
                Todo.title.ilike(f'%{search}%') | 
                Todo.description.ilike(f'%{search}%')
            )
        
        # Order by created_at desc
        query = query.order_by(Todo.created_at.desc())
        
        # Paginate
        todos_pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        todos = [todo.to_dict() for todo in todos_pagination.items]
        
        return jsonify({
            'todos': todos,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': todos_pagination.total,
                'pages': todos_pagination.pages,
                'has_next': todos_pagination.has_next,
                'has_prev': todos_pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        print(f"Error getting todos: {e}")
        return jsonify({'error': 'Failed to get todos'}), 500

@todos_bp.route('', methods=['POST'])
@jwt_required_with_user
def create_todo(current_user):
    """Create a new todo"""
    try:
        data = request.get_json()
        
        title = data.get('title', '').strip()
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        description = data.get('description', '').strip() or None
        priority = data.get('priority', 'medium')
        due_date_str = data.get('due_date')
        
        # Validate priority
        if priority not in ['low', 'medium', 'high']:
            priority = 'medium'
        
        # Parse due date
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Invalid due_date format. Use ISO format.'}), 400
        
        # Create todo
        todo = Todo(
            title=title,
            user_id=current_user.id,
            description=description,
            priority=priority,
            due_date=due_date
        )
        
        db.session.add(todo)
        db.session.commit()
        
        # Send email notification
        send_todo_notification(
            current_user.email,
            current_user.first_name,
            todo.title,
            todo.description
        )
        
        return jsonify({
            'message': 'Todo created successfully',
            'todo': todo.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating todo: {e}")
        return jsonify({'error': 'Failed to create todo'}), 500

@todos_bp.route('/<int:todo_id>', methods=['GET'])
@jwt_required_with_user
def get_todo(current_user, todo_id):
    """Get a specific todo"""
    try:
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
        
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404
        
        return jsonify({'todo': todo.to_dict()}), 200
        
    except Exception as e:
        print(f"Error getting todo: {e}")
        return jsonify({'error': 'Failed to get todo'}), 500

@todos_bp.route('/<int:todo_id>', methods=['PUT'])
@jwt_required_with_user
def update_todo(current_user, todo_id):
    """Update a todo"""
    try:
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
        
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'title' in data:
            title = data['title'].strip()
            if not title:
                return jsonify({'error': 'Title cannot be empty'}), 400
            todo.title = title
        
        if 'description' in data:
            todo.description = data['description'].strip() or None
        
        if 'priority' in data:
            priority = data['priority']
            if priority in ['low', 'medium', 'high']:
                todo.priority = priority
        
        if 'due_date' in data:
            due_date_str = data['due_date']
            if due_date_str:
                try:
                    todo.due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                except ValueError:
                    return jsonify({'error': 'Invalid due_date format'}), 400
            else:
                todo.due_date = None
        
        if 'completed' in data:
            completed = data['completed']
            if completed and not todo.completed:
                todo.mark_completed()
            elif not completed and todo.completed:
                todo.mark_incomplete()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Todo updated successfully',
            'todo': todo.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating todo: {e}")
        return jsonify({'error': 'Failed to update todo'}), 500

@todos_bp.route('/<int:todo_id>', methods=['DELETE'])
@jwt_required_with_user
def delete_todo(current_user, todo_id):
    """Delete a todo"""
    try:
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
        
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404
        
        db.session.delete(todo)
        db.session.commit()
        
        return jsonify({'message': 'Todo deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting todo: {e}")
        return jsonify({'error': 'Failed to delete todo'}), 500

@todos_bp.route('/stats', methods=['GET'])
@jwt_required_with_user
def get_todo_stats(current_user):
    """Get todo statistics for current user"""
    try:
        total_todos = Todo.query.filter_by(user_id=current_user.id).count()
        completed_todos = Todo.query.filter_by(user_id=current_user.id, completed=True).count()
        pending_todos = total_todos - completed_todos
        
        # Get todos by priority
        high_priority = Todo.query.filter_by(user_id=current_user.id, priority='high', completed=False).count()
        medium_priority = Todo.query.filter_by(user_id=current_user.id, priority='medium', completed=False).count()
        low_priority = Todo.query.filter_by(user_id=current_user.id, priority='low', completed=False).count()
        
        # Get overdue todos
        now = datetime.utcnow()
        overdue_todos = Todo.query.filter(
            Todo.user_id == current_user.id,
            Todo.completed == False,
            Todo.due_date < now
        ).count()
        
        return jsonify({
            'stats': {
                'total_todos': total_todos,
                'completed_todos': completed_todos,
                'pending_todos': pending_todos,
                'completion_rate': round((completed_todos / total_todos * 100) if total_todos > 0 else 0, 2),
                'priority_breakdown': {
                    'high': high_priority,
                    'medium': medium_priority,
                    'low': low_priority
                },
                'overdue_todos': overdue_todos
            }
        }), 200
        
    except Exception as e:
        print(f"Error getting todo stats: {e}")
        return jsonify({'error': 'Failed to get statistics'}), 500
