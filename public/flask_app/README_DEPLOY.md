# 🌳 Anderson Family Tree — Deploy on Render.com

This is a complete **Flask + PostgreSQL** family tree web application with:
- ✅ Full SQLite → PostgreSQL support
- ✅ Secure login with Flask-Login
- ✅ Admin dashboard + user management
- ✅ Photo uploads
- ✅ Parent & spouse relationship linking
- ✅ Beautiful public family tree

---

## 🚀 Deploy to Render (Recommended - Free Tier)

Render makes it extremely easy to deploy this app with a managed PostgreSQL database.

### Option 1: One-Click Deploy (Fastest)

1. Push this folder to a **GitHub repository** (or GitLab)
2. Go to [https://render.com](https://render.com) and sign up
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repo and select the `family_tree` folder (or root)
5. Render will automatically detect `render.yaml`
6. Click **"Create Web Service"**

Render will:
- Create a free PostgreSQL database
- Deploy your app
- Set all environment variables automatically

### Option 2: Manual Deploy (Step-by-step)

#### Step 1: Create a Git Repository
```bash
cd family_tree
git init
git add .
git commit -m "Initial family tree app"
git remote add origin https://github.com/YOUR_USERNAME/family-tree.git
git push -u origin main
```

#### Step 2: Create the Web Service on Render
1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repo
4. Fill in:
   - **Name**: `family-tree-app` (or anything)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn flask_app:app`

#### Step 3: Add a PostgreSQL Database
1. In the same dashboard, click **New +** → **PostgreSQL**
2. Name it `family-tree-db`
3. Choose **Free** plan
4. Create the database

#### Step 4: Link the Database
1. Go back to your Web Service
2. Go to **Environment** tab
3. Click **"Add Environment Variable"**
4. Add:
   - Key: `DATABASE_URL`
   - Value: Copy the **Internal Database URL** from your Postgres database (or use the "Connect" button)
5. Also add:
   - Key: `SECRET_KEY`
   - Value: Any long random string (Render can auto-generate one)

#### Step 5: Deploy
Click **"Manual Deploy"** → **"Deploy latest commit"**

Your app will be live at:
`https://family-tree-app.onrender.com`

---

## 🔐 Default Admin Login

After deployment:
- **URL**: `https://your-app.onrender.com/login`
- **Username**: `admin`
- **Password**: `family123`

**IMPORTANT**: Log in immediately and change the password!

---

## 🛠️ How to Change the Default Password

1. Log in at `/login`
2. Go to **Admin → Manage Users**
3. Create a new admin user with a strong password
4. Delete the default `admin` account

---

## 📁 Key Files for Render

| File            | Purpose                              |
|-----------------|--------------------------------------|
| `render.yaml`   | One-click configuration (web + db)   |
| `Procfile`      | Tells Render to use Gunicorn         |
| `requirements.txt` | All Python packages               |
| `flask_app.py`  | Main app (auto-detects DATABASE_URL) |

---

## 🔧 Environment Variables (Important)

| Variable       | Required | Description                              |
|----------------|----------|------------------------------------------|
| `SECRET_KEY`   | Yes      | Long random string for sessions          |
| `DATABASE_URL` | Yes      | PostgreSQL connection string (Render)    |

Render automatically sets `DATABASE_URL` when you link a database.

---

## 📸 Photo Uploads on Render

Render's free tier has **ephemeral disk** — uploaded files will be lost on every deploy.

### Solutions:

**Option A (Recommended)**: Use a free external image host
- Upload photos to [Imgur](https://imgur.com), [Cloudinary](https://cloudinary.com), or similar
- Paste the public image URL into a new "Photo URL" field (you can easily add this later)

**Option B**: Upgrade to Render paid plan ($7/mo) for persistent disk

**Option C**: Switch to a service that supports persistent storage (Railway, Fly.io, etc.)

> Note: For family photos, Option A is often better for privacy and reliability anyway.

---

## 🌍 Custom Domain

After deploying:
1. Go to your service on Render
2. Go to **Settings** → **Custom Domains**
3. Add your domain (e.g. `family.anderson.com`)
4. Follow the DNS instructions

---

## 🔄 Updating the App

Just push new commits to your GitHub repo. Render will automatically redeploy.

You can also trigger manual deploys from the dashboard.

---

## 🛡️ Security Recommendations

1. Change the default admin password **immediately**
2. Set a strong `SECRET_KEY`
3. Never commit `family_tree.db` if you test locally
4. Consider enabling Render's free SSL (it's automatic)

---

## 📞 Useful Render URLs

- Dashboard: https://dashboard.render.com
- Docs: https://render.com/docs

---

## ✅ You're Live!

After deployment you will have:
- Beautiful public family tree at the root URL
- Secure admin area at `/login`
- Real PostgreSQL database
- Full CRUD for family members

Enjoy building your family legacy! 🌳
