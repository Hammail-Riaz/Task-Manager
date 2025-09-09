from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.blueprints.tasks.models import Tasks
from datetime import datetime
from ...extensions import db

prof = Blueprint("profile", __name__, template_folder="templates")

@prof.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():    
    
    tasks = Tasks.query.filter_by(user_id = current_user.uid )    
    
    completed_list = tasks.filter_by(status="Completed").all()
    pending_list = tasks.filter_by(status="Pending").all()
    in_progress_list = tasks.filter_by(status="In Progress").all()
    cancelled_list = tasks.filter_by(status="Cancelled").all()
    
    total_tasks = tasks.count()
    completed_tasks = tasks.filter_by(status="Completed").count()
    in_progress_tasks = tasks.filter_by(status="In Progress").count()
    pending_tasks = tasks.filter_by(status="Pending").count()
    cancelled_tasks = tasks.filter_by(status="Cancelled").count()

    today = datetime.now().date()
    tasks_today_count = tasks.filter(
        db.func.date(Tasks.date_n_time) == today
    ).count()
    

    return render_template("dashboard.html",
                           user = current_user,
                           completed_list = completed_list,
                           pending_list = pending_list, in_progress_list = in_progress_list,
                           cancelled_list = cancelled_list,
                            total_tasks=total_tasks,
                            completed_tasks=completed_tasks,
                            in_progress_tasks=in_progress_tasks,
                            pending_tasks=pending_tasks,
                            cancelled_tasks=cancelled_tasks,
                            tasks_today_count=tasks_today_count,
                            
                           )