from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os, uuid
from datetime import datetime

from models import db, User, FamilyMember

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'family-tree-super-secret-key-change-this-in-production-2025')

# ====================== DATABASE CONFIG ======================
# Render provides DATABASE_URL for PostgreSQL.
# Locally we fall back to SQLite.
basedir = os.path.abspath(os.path.dirname(__file__))

database_url = os.environ.get('DATABASE_URL')

if database_url:
    # Render Postgres — fix postgres:// to postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Local development
    os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'family_tree.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Uploads
UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)

# ====================== LOGIN ======================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access the admin area.'
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_default_admin():
    """Create default admin if none exists"""
    if User.query.count() == 0:
        admin = User(username='admin')
        admin.set_password('family123')  # CHANGE THIS ON PRODUCTION!
        db.session.add(admin)
        db.session.commit()
        print("✅ Default admin created → username: admin | password: family123")


def seed_sample_data():
    """Seed sample family data if database is empty"""
    if FamilyMember.query.count() > 0:
        return

    sample_members = [
        {"id": "g1", "name": "George Anderson", "birth_year": "1940", "death_year": "", "role": "Grandfather",
         "generation": 1, "parent_ids": [], "spouse_id": "g2",
         "bio": "The family patriarch, a retired carpenter who built the family home with his own hands.",
         "birth_place": "Boston, MA", "occupation": "Carpenter"},
        {"id": "g2", "name": "Margaret Anderson", "birth_year": "1943", "death_year": "", "role": "Grandmother",
         "generation": 1, "parent_ids": [], "spouse_id": "g1",
         "bio": "A devoted mother and grandmother who loves gardening and cooking.",
         "birth_place": "Cambridge, MA", "occupation": "Homemaker & Teacher"},
        {"id": "p1", "name": "Robert Anderson", "birth_year": "1965", "death_year": "", "role": "Father",
         "generation": 2, "parent_ids": ["g1", "g2"], "spouse_id": "p2",
         "bio": "Software engineer and avid hiker. Loves spending weekends outdoors with the family.",
         "birth_place": "Boston, MA", "occupation": "Software Engineer"},
        {"id": "p2", "name": "Susan Anderson", "birth_year": "1968", "death_year": "", "role": "Mother",
         "generation": 2, "parent_ids": [], "spouse_id": "p1",
         "bio": "A passionate nurse and community volunteer.",
         "birth_place": "New York, NY", "occupation": "Nurse"},
        {"id": "u1", "name": "James Anderson", "birth_year": "1970", "death_year": "", "role": "Uncle",
         "generation": 2, "parent_ids": ["g1", "g2"], "spouse_id": "u2",
         "bio": "An entrepreneur who runs a successful restaurant chain.",
         "birth_place": "Boston, MA", "occupation": "Entrepreneur"},
        {"id": "u2", "name": "Patricia Anderson", "birth_year": "1972", "death_year": "", "role": "Aunt",
         "generation": 2, "parent_ids": [], "spouse_id": "u1",
         "bio": "A talented interior designer with a passion for art.",
         "birth_place": "Chicago, IL", "occupation": "Interior Designer"},
        {"id": "c1", "name": "Emily Anderson", "birth_year": "1992", "death_year": "", "role": "Daughter",
         "generation": 3, "parent_ids": ["p1", "p2"], "spouse_id": "",
         "bio": "Medical student with a love for music.",
         "birth_place": "Seattle, WA", "occupation": "Medical Student"},
        {"id": "c2", "name": "Michael Anderson", "birth_year": "1995", "death_year": "", "role": "Son",
         "generation": 3, "parent_ids": ["p1", "p2"], "spouse_id": "",
         "bio": "Graphic designer and avid gamer.",
         "birth_place": "Seattle, WA", "occupation": "Graphic Designer"},
        {"id": "c3", "name": "Sophia Anderson", "birth_year": "1998", "death_year": "", "role": "Cousin",
         "generation": 3, "parent_ids": ["u1", "u2"], "spouse_id": "",
         "bio": "Architecture student who loves sketching cityscapes.",
         "birth_place": "Chicago, IL", "occupation": "Architecture Student"},
        {"id": "c4", "name": "Lucas Anderson", "birth_year": "2001", "death_year": "", "role": "Cousin",
         "generation": 3, "parent_ids": ["u1", "u2"], "spouse_id": "",
         "bio": "High school basketball star and aspiring sports journalist.",
         "birth_place": "Chicago, IL", "occupation": "Student"},
    ]

    for data in sample_members:
        member = FamilyMember(
            id=data['id'], name=data['name'], birth_year=data['birth_year'],
            death_year=data['death_year'], role=data['role'], generation=data['generation'],
            bio=data['bio'], birth_place=data['birth_place'], occupation=data['occupation'],
            spouse_id=data['spouse_id']
        )
        member.set_parent_ids(data['parent_ids'])
        db.session.add(member)

    db.session.commit()
    print("✅ Sample family data seeded.")


# ====================== APP STARTUP ======================
with app.app_context():
    db.create_all()
    create_default_admin()
    seed_sample_data()


# ====================== PUBLIC ROUTES ======================

@app.route('/')
def index():
    members = FamilyMember.query.order_by(FamilyMember.generation, FamilyMember.name).all()
    generations = {}
    for m in members:
        generations.setdefault(m.generation, []).append(m)
    gen_labels = {1: 'Grandparents', 2: 'Parents & Relatives', 3: 'Children & Cousins', 4: 'Grandchildren'}
    return render_template('index.html', members=members, generations=generations,
                           gen_labels=gen_labels, sorted_gens=sorted(generations.keys()))


@app.route('/member/<member_id>')
def member_detail(member_id):
    member = FamilyMember.query.get_or_404(member_id)
    all_members = FamilyMember.query.all()
    member_dict = member.to_dict()

    parents = [m for m in all_members if m.id in member.get_parent_ids()]
    spouse = FamilyMember.query.get(member.spouse_id) if member.spouse_id else None
    children = [m for m in all_members if member_id in m.get_parent_ids()]
    siblings = []
    parent_ids = member.get_parent_ids()
    if parent_ids:
        for m in all_members:
            if m.id != member_id and any(pid in m.get_parent_ids() for pid in parent_ids):
                siblings.append(m)

    return render_template('member.html', member=member, member_dict=member_dict,
                           parents=parents, spouse=spouse, children=children,
                           siblings=siblings, all_members=all_members)


@app.route('/tree')
def tree():
    members = FamilyMember.query.all()
    return render_template('tree.html', members=members)


# ====================== AUTH ======================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


# ====================== ADMIN SECTION ======================

@app.route('/admin')
@login_required
def admin_dashboard():
    total_members = FamilyMember.query.count()
    total_users = User.query.count()
    gen_count = FamilyMember.query.with_entities(FamilyMember.generation).distinct().count()
    recent_members = FamilyMember.query.order_by(FamilyMember.updated_at.desc()).limit(6).all()

    return render_template('admin_dashboard.html',
                           total_members=total_members,
                           total_users=total_users,
                           gen_count=gen_count,
                           recent_members=recent_members)


@app.route('/admin/members')
@login_required
def admin_members():
    members = FamilyMember.query.order_by(FamilyMember.generation, FamilyMember.name).all()
    return render_template('admin_members.html', members=members)


@app.route('/admin/add', methods=['GET', 'POST'])
@login_required
def admin_add_member():
    all_members = FamilyMember.query.order_by(FamilyMember.name).all()

    if request.method == 'POST':
        photo_filename = ''
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                photo_filename = f"{uuid.uuid4().hex}.{ext}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        parent_ids = request.form.getlist('parent_ids')

        new_member = FamilyMember(
            id=str(uuid.uuid4().hex[:8]),
            name=request.form.get('name', '').strip(),
            birth_year=request.form.get('birth_year', '').strip(),
            death_year=request.form.get('death_year', '').strip(),
            role=request.form.get('role', '').strip(),
            generation=int(request.form.get('generation', 1)),
            bio=request.form.get('bio', '').strip(),
            photo=photo_filename,
            birth_place=request.form.get('birth_place', '').strip(),
            occupation=request.form.get('occupation', '').strip(),
            spouse_id=request.form.get('spouse_id', '').strip()
        )
        new_member.set_parent_ids(parent_ids)

        db.session.add(new_member)
        db.session.commit()

        flash(f'{new_member.name} has been added to the family tree!', 'success')
        return redirect(url_for('member_detail', member_id=new_member.id))

    return render_template('admin_add_member.html', members=all_members)


@app.route('/admin/edit/<member_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_member(member_id):
    member = FamilyMember.query.get_or_404(member_id)
    all_members = FamilyMember.query.order_by(FamilyMember.name).all()

    if request.method == 'POST':
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and allowed_file(file.filename):
                if member.photo:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], member.photo)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                ext = file.filename.rsplit('.', 1)[1].lower()
                photo_filename = f"{uuid.uuid4().hex}.{ext}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
                member.photo = photo_filename

        parent_ids = request.form.getlist('parent_ids')

        member.name = request.form.get('name', '').strip()
        member.birth_year = request.form.get('birth_year', '').strip()
        member.death_year = request.form.get('death_year', '').strip()
        member.role = request.form.get('role', '').strip()
        member.generation = int(request.form.get('generation', 1))
        member.bio = request.form.get('bio', '').strip()
        member.birth_place = request.form.get('birth_place', '').strip()
        member.occupation = request.form.get('occupation', '').strip()
        member.spouse_id = request.form.get('spouse_id', '').strip()
        member.set_parent_ids(parent_ids)

        db.session.commit()

        flash(f'{member.name}\'s information has been updated!', 'success')
        return redirect(url_for('member_detail', member_id=member.id))

    return render_template('admin_edit_member.html', member=member, members=all_members)


@app.route('/admin/delete/<member_id>', methods=['POST'])
@login_required
def admin_delete_member(member_id):
    member = FamilyMember.query.get_or_404(member_id)

    if member.photo:
        old_path = os.path.join(app.config['UPLOAD_FOLDER'], member.photo)
        if os.path.exists(old_path):
            os.remove(old_path)

    for m in FamilyMember.query.all():
        if member_id in m.get_parent_ids():
            new_parents = [p for p in m.get_parent_ids() if p != member_id]
            m.set_parent_ids(new_parents)
        if m.spouse_id == member_id:
            m.spouse_id = ''

    db.session.delete(member)
    db.session.commit()

    flash(f'{member.name} has been removed from the family tree.', 'success')
    return redirect(url_for('admin_members'))


# ====================== ADMIN: USER MANAGEMENT ======================

@app.route('/admin/users')
@login_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)


@app.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
def admin_add_user():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('admin_add_user'))

        if User.query.filter_by(username=username).first():
            flash('A user with that username already exists.', 'error')
            return redirect(url_for('admin_add_user'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash(f'User "{username}" has been created successfully.', 'success')
        return redirect(url_for('admin_users'))

    return render_template('admin_add_user.html')


@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if current_user.id == user_id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin_users'))

    user = User.query.get_or_404(user_id)
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'User "{username}" has been deleted.', 'success')
    return redirect(url_for('admin_users'))


if __name__ == '__main__':
    app.run(debug=True)
