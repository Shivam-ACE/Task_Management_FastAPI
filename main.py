from fastapi import FastAPI, Request
from src.utils.db import Base, engine
from src.tasks.router import task_routes
from src.user.router import user_routes
from fastapi.responses import HTMLResponse ### for html page at /

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management Application", description="This is a sample FastAPI application.", version="1.0.0")

app.include_router(task_routes)
app.include_router(user_routes)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Task Management API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
            body { background: #0f172a; color: #e2e8f0; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .card { text-align: center; max-width: 560px; padding: 3rem 2rem; background: #1e293b; border-radius: 16px; border: 1px solid #334155; }
            h1 { font-size: 2rem; margin-bottom: 0.5rem; }
            h1 span { color: #38bdf8; }
            p { color: #94a3b8; margin-bottom: 2rem; }
            .links { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
            a { text-decoration: none; padding: 0.7rem 1.5rem; border-radius: 8px; font-weight: 600; transition: 0.2s; }
            .primary { background: #38bdf8; color: #0f172a; }
            .primary:hover { background: #7dd3fc; }
            .secondary { background: #334155; color: #e2e8f0; }
            .secondary:hover { background: #475569; }
            .status { margin-top: 2rem; font-size: 0.85rem; color: #64748b; }
            .dot { display: inline-block; width: 8px; height: 8px; background: #4ade80; border-radius: 50%; margin-right: 6px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Task <span>Management</span> API</h1>
            <p>A FastAPI backend for managing tasks and users — JWT auth, PostgreSQL, deployed on Render.</p>
            <div class="links">
                <a class="primary" href="/docs">API Docs</a>
                <a class="secondary" href="/health">Health Check</a>
                <a class="secondary" href="https://github.com/Shivam-ACE/Task_Management_FastAPI" target="_blank">GitHub</a>
            </div>
            <div class="status"><span class="dot"></span>all systems operational</div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
def health():
    return {"status": "OK"}
