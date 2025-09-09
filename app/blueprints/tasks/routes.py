from flask import Blueprint , render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from .forms import CreateTaskForm, EditTaskForm, DeleteTaskForm
from .models import Tasks
from ...extensions import db
from datetime import datetime
from .models import Tasks

tasks = Blueprint("tasks", __name__, template_folder="templates")

@tasks.route("/create", methods= ["GET", "POST"])
@login_required
def create():
    form = CreateTaskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        status = form.status.data
        
        existing = Tasks.query.filter_by(title=form.title.data).first()
        if existing:
            flash("A task with this title already exists. Please choose another.", "danger")
            return redirect(url_for("tasks.create"))

        
        task = Tasks(
            title = title,
            description = description,
            date_n_time = datetime.now().replace(microsecond = 0), 
            status = status,
            user_id = current_user.uid
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash("Your Note is created Successfully!", "success")
        return redirect(url_for('tasks.view'))
        
    return render_template("create.html", form=form)

@tasks.route("/edit/<int:tid>", methods=["GET", "POST"])
@login_required
def edit(tid):
    # Only allow the owner to edit
    task = Tasks.query.filter_by(tid=tid, user_id=current_user.uid).first_or_404()

    form = EditTaskForm(obj=task)  # pre-fill form

    if form.validate_on_submit():
        # Optional: check unique title per user
        existing = Tasks.query.filter_by(
            title=form.title.data, user_id=current_user.uid
        ).filter(Tasks.tid != tid).first()
        if existing:
            flash("You already have a task with this title. Choose another.", "danger")
            return redirect(url_for("tasks.edit", tid=tid))

        # Update task fields
        task.title = form.title.data
        task.description = form.description.data
        task.status = form.status.data
        db.session.commit()

        flash("Task updated successfully!", "success")
        return redirect(url_for("tasks.view"))

    return render_template("edit.html", task=task, form=form)


@tasks.route("/view")
@login_required
def view():
    form = DeleteTaskForm()
    
    status = request.args.get("status", "All")

    tasks = Tasks.query.filter_by(user_id = current_user.uid )
    if status == "All":
        tasks = tasks.order_by(Tasks.date_n_time.desc()).all()
    elif status == "Created Today":
        
        today = datetime.now().date()
        tasks = tasks.filter(
            db.func.date(Tasks.date_n_time) == today
        ).all()
    
    else:
        tasks = tasks.filter_by(status=status).order_by(Tasks.date_n_time.desc()).all()

    return render_template("view.html", tasks=tasks, selected_status=status, form=form )

@tasks.route("/delete/<int:tid>", methods=["POST"])
@login_required
def delete(tid):
    task = Tasks.query.filter_by(tid=tid, user_id=current_user.uid).first_or_404()
    
    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully!", "success")
    return redirect(url_for("tasks.view"))


