# Start from Python 3.14 - the same version as your laptop
FROM python:3.14-slim

# Hugging Face Spaces run the app as a normal user (id 1000), not as admin
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1
WORKDIR /home/user/app

# Install packages first.
# PyTorch comes from its CPU-only download page, so the GPU parts are skipped.
COPY --chown=user requirements-app.txt .
RUN pip install --no-cache-dir torch==2.14.1 --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements-dev.txt

# Then copy your code
COPY --chown=user . .

# Hugging Face shows the app on port 7860
EXPOSE 7860
CMD ["sh", "start.sh"]