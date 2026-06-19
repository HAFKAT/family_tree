import { useState } from 'react'

const steps = [
  {
    num: 1,
    icon: '📦',
    title: 'Push to GitHub',
    desc: 'Upload the entire flask_app folder to a GitHub repository. This is required for Render.',
    code: 'git init && git add . && git commit -m "Family tree app"'
  },
  {
    num: 2,
    icon: '🌐',
    title: 'Create Web Service on Render',
    desc: 'Go to Render.com → New + → Web Service. Connect your GitHub repo.',
    code: 'Build: pip install -r requirements.txt\nStart: gunicorn flask_app:app'
  },
  {
    num: 3,
    icon: '🗄️',
    title: 'Add Free PostgreSQL Database',
    desc: 'In Render, create a new PostgreSQL database (free tier). Name it family-tree-db.',
    code: 'New + → PostgreSQL → Free plan'
  },
  {
    num: 4,
    icon: '🔗',
    title: 'Connect Database',
    desc: 'Add DATABASE_URL from your Postgres database to the web service environment variables.',
    code: 'Environment → Add DATABASE_URL'
  },
  {
    num: 5,
    icon: '🚀',
    title: 'Deploy!',
    desc: 'Click Deploy. Render will automatically build and launch your app with PostgreSQL.',
    code: 'https://your-app.onrender.com'
  }
]

const features = [
  { icon: '🏠', title: 'Home Gallery', desc: 'Grid view of all members grouped by generation with live search' },
  { icon: '🌳', title: 'Visual Tree', desc: 'Interactive tree view showing spouse connections and family structure' },
  { icon: '👤', title: 'Member Profiles', desc: 'Full profile pages with bio, photo, and all relationships displayed' },
  { icon: '🔐', title: 'Secure Login', desc: 'Protected admin area with Flask-Login. Multiple admin accounts supported' },
  { icon: '🛠️', title: 'Full Admin Panel', desc: 'Dashboard, add/edit/delete members, manage users, all in one place' },
  { icon: '➕', title: 'Add Members', desc: 'Upload photos, set birth dates, link parents & spouses easily' },
  { icon: '✏️', title: 'Edit Anytime', desc: 'Update any family member\'s info, photo, and relationships' },
  { icon: '🗄️', title: 'PostgreSQL Database', desc: 'Production-grade Postgres on Render. Auto-falls back to SQLite locally.' },
  { icon: '📱', title: 'Responsive', desc: 'Works beautifully on mobile phones and tablets' },
]

const fileTree = [
  { name: 'flask_app.py', type: 'py', desc: 'Main Flask app — supports PostgreSQL + SQLite' },
  { name: 'models.py', type: 'py', desc: 'Database models (User + FamilyMember)' },
  { name: 'requirements.txt', type: 'txt', desc: 'flask, gunicorn, psycopg2, flask-login, sqlalchemy' },
  { name: 'Procfile', type: 'txt', desc: 'Tells Render to run gunicorn' },
  { name: 'render.yaml', type: 'yaml', desc: 'One-click Render config (web + Postgres DB)' },
  { name: 'runtime.txt', type: 'txt', desc: 'Python version for Render' },
  { name: 'templates/*.html', type: 'html', desc: 'All pages: public + full admin panel' },
  { name: 'README_DEPLOY.md', type: 'md', desc: 'Complete Render deployment guide' },
]

const typeColors: Record<string, string> = {
  py: 'bg-blue-100 text-blue-700',
  html: 'bg-orange-100 text-orange-700',
  txt: 'bg-gray-100 text-gray-600',
  md: 'bg-purple-100 text-purple-700',
}

export default function App() {
  const [copiedStep, setCopiedStep] = useState<number | null>(null)

  const copyCode = (text: string, idx: number) => {
    navigator.clipboard.writeText(text)
    setCopiedStep(idx)
    setTimeout(() => setCopiedStep(null), 2000)
  }

  return (
    <div className="min-h-screen bg-stone-50 font-sans">
      {/* NAVBAR */}
      <nav className="bg-gradient-to-r from-green-900 to-green-700 sticky top-0 z-50 shadow-lg">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🌳</span>
            <div>
              <div className="text-white font-bold text-lg leading-tight font-serif">Family Tree App</div>
              <div className="text-green-300 text-xs tracking-widest uppercase">Flask + Render</div>
            </div>
          </div>
          <a
            href="/flask_app/README_DEPLOY.md"
            target="_blank"
            className="bg-amber-400 hover:bg-amber-300 text-green-900 font-bold px-4 py-2 rounded-lg text-sm transition-all flex items-center gap-2"
          >
            📄 Full Guide
          </a>
        </div>
      </nav>

      {/* HERO */}
      <div className="bg-gradient-to-br from-green-900 via-green-800 to-green-600 text-white py-20 px-6 relative overflow-hidden">
        <div className="absolute inset-0 opacity-5 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGcgZmlsbD0id2hpdGUiPjxwYXRoIGQ9Ik0zNiAzNHYtNGgtMnY0aC00djJoNHY0aDJ2LTRoNHYtMmgtNHoiLz48L2c+PC9zdmc+')]"></div>
        <div className="max-w-4xl mx-auto text-center relative">
          <div className="text-7xl mb-6">🌳</div>
          <h1 className="text-5xl font-bold font-serif mb-4">Family Tree Web App</h1>
          <p className="text-green-200 text-xl mb-8 max-w-2xl mx-auto leading-relaxed">
            A complete Flask web application to document and display your family history —
            with photos, biographies, and visual tree connections. Ready to deploy on Render.com with PostgreSQL!
          </p>
          <div className="flex flex-wrap gap-4 justify-center mb-10">
            <div className="bg-white/10 backdrop-blur border border-white/20 rounded-xl px-5 py-3 text-center">
              <div className="text-2xl font-bold text-amber-300">8</div>
              <div className="text-xs text-green-200 uppercase tracking-wide">Files Ready</div>
            </div>
            <div className="bg-white/10 backdrop-blur border border-white/20 rounded-xl px-5 py-3 text-center">
              <div className="text-2xl font-bold text-amber-300">5</div>
              <div className="text-xs text-green-200 uppercase tracking-wide">Deploy Steps</div>
            </div>
            <div className="bg-white/10 backdrop-blur border border-white/20 rounded-xl px-5 py-3 text-center">
              <div className="text-2xl font-bold text-amber-300">Free</div>
              <div className="text-xs text-green-200 uppercase tracking-wide">Render + Postgres</div>
            </div>
            <div className="bg-white/10 backdrop-blur border border-white/20 rounded-xl px-5 py-3 text-center">
              <div className="text-2xl font-bold text-amber-300">10</div>
              <div className="text-xs text-green-200 uppercase tracking-wide">Sample Members</div>
            </div>
          </div>
          <div className="bg-amber-400/20 border border-amber-400/40 rounded-xl p-4 text-sm text-amber-200 inline-block">
            📁 All Flask app files are in: <code className="bg-black/30 px-2 py-1 rounded font-mono">public/flask_app/</code>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-16">

        {/* FEATURES */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold font-serif text-green-900 mb-2 text-center">✨ App Features</h2>
          <p className="text-center text-stone-500 mb-10">Everything included out of the box</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {features.map(f => (
              <div key={f.title} className="bg-white rounded-2xl border border-stone-200 shadow-sm p-5 hover:shadow-md hover:-translate-y-1 transition-all">
                <div className="text-3xl mb-3">{f.icon}</div>
                <div className="font-bold text-green-900 mb-1 text-sm">{f.title}</div>
                <div className="text-stone-500 text-xs leading-relaxed">{f.desc}</div>
              </div>
            ))}
          </div>
        </section>

        {/* FILE STRUCTURE */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold font-serif text-green-900 mb-2 text-center">📁 Generated Files</h2>
          <p className="text-center text-stone-500 mb-10">All files are ready to deploy on Render.com</p>
          <div className="bg-white rounded-2xl border border-stone-200 shadow-sm overflow-hidden">
            <div className="bg-green-900 text-green-200 text-sm font-mono px-6 py-3 flex items-center gap-2">
              <span className="text-green-400">📂</span> public/flask_app/
            </div>
            <div className="divide-y divide-stone-100">
              {fileTree.map(f => (
                <div key={f.name} className="flex items-center gap-4 px-6 py-3.5 hover:bg-stone-50 transition-colors">
                  <span className={`text-xs font-mono font-bold px-2 py-0.5 rounded ${typeColors[f.type]}`}>.{f.type}</span>
                  <code className="text-green-800 font-mono text-sm font-semibold flex-1">{f.name}</code>
                  <span className="text-stone-400 text-sm hidden md:block">{f.desc}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* DEPLOY STEPS */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold font-serif text-green-900 mb-2 text-center">🚀 Deployment Steps</h2>
          <p className="text-center text-stone-500 mb-10">Follow these steps to go live on Render.com</p>
          <div className="space-y-4">
            {steps.map((step, idx) => (
              <div key={step.num} className="bg-white rounded-2xl border border-stone-200 shadow-sm overflow-hidden">
                <div className="flex items-start gap-4 p-5">
                  <div className="bg-green-900 text-white font-bold text-lg rounded-xl w-11 h-11 flex items-center justify-center flex-shrink-0 font-serif">
                    {step.num}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xl">{step.icon}</span>
                      <span className="font-bold text-green-900">{step.title}</span>
                    </div>
                    <p className="text-stone-500 text-sm mb-3">{step.desc}</p>
                    <div className="relative">
                      <pre className="bg-stone-900 text-green-300 text-xs font-mono rounded-lg p-4 overflow-x-auto whitespace-pre-wrap">{step.code}</pre>
                      <button
                        onClick={() => copyCode(step.code, idx)}
                        className="absolute top-2 right-2 bg-white/10 hover:bg-white/20 text-white text-xs px-2 py-1 rounded transition-all"
                      >
                        {copiedStep === idx ? '✅ Copied!' : '📋 Copy'}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* WSGI FULL CODE */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold font-serif text-green-900 mb-2 text-center">⚙️ WSGI Configuration</h2>
          <p className="text-center text-stone-500 mb-8">No WSGI file needed — Render uses gunicorn automatically via Procfile</p>
          <div className="bg-white rounded-2xl border border-stone-200 shadow-sm overflow-hidden">
            <div className="bg-stone-800 text-stone-300 text-xs px-6 py-3 flex items-center justify-between">
              <span>No manual WSGI — handled by Render + Gunicorn</span>
              <button
                onClick={() => copyCode(`import sys\nimport os\n\n# Add your project directory to the path\nproject_home = '/home/YOUR_USERNAME/family_tree'\nif project_home not in sys.path:\n    sys.path = [project_home] + sys.path\n\n# Import the Flask app as 'application' (required by WSGI)\nfrom flask_app import app as application`, 99)}
                className="bg-white/10 hover:bg-white/20 text-white text-xs px-3 py-1 rounded transition-all"
              >
                {copiedStep === 99 ? '✅ Copied!' : '📋 Copy All'}
              </button>
            </div>
            <pre className="bg-stone-900 text-green-300 text-sm font-mono p-6 overflow-x-auto">{`import sys
import os

# Add your project directory to the path
project_home = '/home/YOUR_USERNAME/family_tree'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Import the Flask app as 'application' (required by WSGI)
from flask_app import app as application`}</pre>
          </div>
        </section>

        {/* CUSTOMIZATION */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold font-serif text-green-900 mb-8 text-center">🎨 Customization</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white rounded-2xl border border-stone-200 shadow-sm p-6">
              <div className="text-3xl mb-3">👨‍👩‍👧‍👦</div>
              <h3 className="font-bold text-green-900 mb-2">Change Family Name</h3>
              <p className="text-stone-500 text-sm">Search & replace <code className="bg-stone-100 px-1 rounded">Anderson</code> with your family name in <code className="bg-stone-100 px-1 rounded">base.html</code> and <code className="bg-stone-100 px-1 rounded">flask_app.py</code></p>
            </div>
            <div className="bg-white rounded-2xl border border-stone-200 shadow-sm p-6">
              <div className="text-3xl mb-3">📸</div>
              <h3 className="font-bold text-green-900 mb-2">Add Real Photos</h3>
              <p className="text-stone-500 text-sm">Use the Add/Edit member forms to upload actual family photos (JPG, PNG, GIF). They'll be stored in <code className="bg-stone-100 px-1 rounded">static/uploads/</code></p>
            </div>
            <div className="bg-white rounded-2xl border border-stone-200 shadow-sm p-6">
              <div className="text-3xl mb-3">✏️</div>
              <h3 className="font-bold text-green-900 mb-2">Edit Sample Data</h3>
              <p className="text-stone-500 text-sm">The app comes with 10 sample members. Edit or delete them via the web interface, or directly edit <code className="bg-stone-100 px-1 rounded">data/family.json</code></p>
            </div>
          </div>
        </section>

        {/* PAGES PREVIEW */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold font-serif text-green-900 mb-8 text-center">📄 Pages in the App</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {[
              { url: '/', label: 'Home Page', desc: 'Shows all family members in a responsive grid, grouped by generation, with live search.' },
              { url: '/tree', label: 'Tree View', desc: 'Visual family tree with generation layers, spouse connectors, and clickable member cards.' },
              { url: '/member/<id>', label: 'Member Profile', desc: 'Full profile: photo, bio, birthplace, occupation, parents, spouse, children & siblings.' },
              { url: '/add', label: 'Add Member', desc: 'Form to add a new person with photo upload, generation, parent and spouse selection.' },
              { url: '/edit/<id>', label: 'Edit Member', desc: 'Same as add, pre-filled with existing data. Change photo without deleting the old one.' },
            ].map(p => (
              <div key={p.url} className="bg-white rounded-2xl border border-stone-200 shadow-sm p-5 flex gap-4">
                <code className="bg-green-50 text-green-700 text-xs font-mono font-bold px-3 py-2 rounded-lg self-start whitespace-nowrap">{p.url}</code>
                <div>
                  <div className="font-bold text-green-900 mb-1">{p.label}</div>
                  <div className="text-stone-500 text-sm">{p.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* CTA */}
        <section>
          <div className="bg-gradient-to-r from-green-900 to-green-700 rounded-2xl p-10 text-center text-white">
            <div className="text-5xl mb-4">🌳</div>
            <h2 className="text-3xl font-bold font-serif mb-3">Ready to Go Live!</h2>
            <p className="text-green-200 mb-8 max-w-lg mx-auto">
              All files are in <code className="bg-black/30 px-2 py-1 rounded">public/flask_app/</code>.
              Follow the 5-step guide to get your family tree live on Render in minutes.
            </p>
            <div className="flex flex-wrap gap-4 justify-center">
              <a
                href="https://render.com"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-amber-400 hover:bg-amber-300 text-green-900 font-bold px-6 py-3 rounded-xl transition-all"
              >
                🚀 Go to Render.com
              </a>
              <a
                href="/flask_app/README_DEPLOY.md"
                target="_blank"
                className="border border-white/40 hover:bg-white/10 text-white font-bold px-6 py-3 rounded-xl transition-all"
              >
                📄 Full Deploy Guide
              </a>
            </div>
          </div>
        </section>

      </div>

      <footer className="bg-green-950 text-green-400 text-center py-6 text-sm">
        🌳 <strong>Family Tree App</strong> — Built with Flask & Python • Deploy on Render.com
      </footer>
    </div>
  )
}
