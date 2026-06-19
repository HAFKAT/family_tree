# 🚀 Deploy Family Tree App to Render.com — Quick Guide

## 1. Push to GitHub
```bash
cd public/flask_app
git init
git add .
git commit -m "Initial commit - Family Tree"
git remote add origin https://github.com/YOUR_USERNAME/family-tree.git
git push -u origin main
```

## 2. Deploy on Render (2 clicks)

1. Go to https://render.com and log in
2. Click **New +** → **Web Service**
3. Connect your GitHub repo
4. Render will detect `render.yaml` automatically

## 3. Add Database

Render will ask to create a database. Or:
- Click **New +** → **PostgreSQL**
- Name: `family-tree-db`
- Plan: Free

## 4. That's it!

Your app will be live at:
`https://your-service-name.onrender.com`

---

## Default Login
- Username: `admin`
- Password: `family123`

Change the password after first login!

Full details in README_DEPLOY.md
