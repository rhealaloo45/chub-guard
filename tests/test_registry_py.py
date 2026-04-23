# =========================
# 🔴 HUGGING FACE ACCELERATE (older style usage)
# =========================
from accelerate import Accelerator
import torch

accelerator = Accelerator(fp16=True)  # ❌ fp16 arg deprecated in newer versions

model = torch.nn.Linear(10, 2)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

model, optimizer = accelerator.prepare(model, optimizer)

for step in range(10):
    inputs = torch.randn(4, 10)
    outputs = model(inputs)
    loss = outputs.mean()

    accelerator.backward(loss)
    optimizer.step()
    optimizer.zero_grad()


# =========================
# 🔴 AIOHTTP (bad session handling)
# =========================
import aiohttp
import asyncio

async def fetch():
    session = aiohttp.ClientSession()  # ❌ not using async context manager
    resp = await session.get("https://example.com")
    data = await resp.text()
    print(data)
    await session.close()

asyncio.run(fetch())


# =========================
# 🔴 ALEMBIC (old migration style)
# =========================
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('age', sa.Integer))  # ❌ missing nullable/default

def downgrade():
    op.drop_column('users', 'age')


# =========================
# 🔴 ALBUMENTATIONS (older API pattern)
# =========================
import albumentations as A
import cv2

transform = A.Compose([
    A.RandomCrop(height=256, width=256),
    A.HorizontalFlip(p=0.5)
])

image = cv2.imread("image.jpg")
augmented = transform(image=image)  # ❌ missing additional targets handling
print(augmented["image"])


# =========================
# 🔴 APACHE AIRFLOW (old DAG style)
# =========================
from airflow import DAG
from airflow.operators.python_operator import PythonOperator  # ❌ deprecated import path
from datetime import datetime

def my_task():
    print("Running task")

dag = DAG(
    dag_id="old_dag",
    start_date=datetime(2020, 1, 1),
    schedule_interval="@daily",  # ❌ replaced with schedule
)

task = PythonOperator(
    task_id="task1",
    python_callable=my_task,
    dag=dag
)