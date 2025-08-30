# Docker Setup for GPAF (Agent Zero)

## 🚀 Quick Start

### วิธีที่ 1: ใช้ Docker Image ที่มีอยู่แล้ว

```bash
# Pull และ run ด้วยคำสั่งเดียว
docker pull frdel/agent-zero-run:latest
docker run -p 50001:80 frdel/agent-zero-run:latest

# หรือใช้ docker-compose
docker-compose up -d
```

เปิดเว็บเบราว์เซอร์ไปที่ http://localhost:50001

### วิธีที่ 2: Build จาก Source Code

```bash
# Build image
docker-compose build

# Run container
docker-compose up -d
```

## 📦 Docker Commands

### ใช้ Makefile (แนะนำ)

```bash
make help          # ดูคำสั่งทั้งหมด
make run           # รัน containers
make stop          # หยุด containers
make logs          # ดู logs
make shell         # เข้า shell ใน container
make clean         # ลบ containers และ images
```

### ใช้ Docker Compose โดยตรง

```bash
# รัน GPAF
docker-compose up -d

# รัน GPAF พร้อม Ollama (สำหรับ local LLM)
docker-compose --profile ollama up -d

# หยุด containers
docker-compose down

# ดู logs
docker-compose logs -f

# Restart
docker-compose restart
```

## 🛠️ Configuration

### Environment Variables

สร้างไฟล์ `.env` จาก `example.env`:

```bash
cp example.env .env
```

แก้ไขค่าต่าง ๆ ใน `.env`:

```env
# API Keys
API_KEY_OPENAI=your-openai-key
API_KEY_ANTHROPIC=your-anthropic-key
API_KEY_GOOGLE=your-google-key

# Authentication
AUTH_LOGIN=admin
AUTH_PASSWORD=your-password

# Timezone
TZ=Asia/Bangkok
```

### Volumes

Docker compose จะ mount directories เหล่านี้:

- `./work_dir:/root` - Working directory สำหรับ agent
- `./logs:/app/logs` - Log files
- `./memory:/app/memory` - Agent memory
- `./knowledge:/app/knowledge` - Knowledge base
- `./tmp:/app/tmp` - Temporary files

## 🔧 Troubleshooting

### Port ชนกัน

ถ้า port 50001 ถูกใช้แล้ว แก้ไขใน `docker-compose.yml`:

```yaml
ports:
  - "8080:80"  # เปลี่ยนเป็น port อื่น
```

### Permission Issues

ถ้ามีปัญหา permission บน Linux/Mac:

```bash
sudo chown -R $USER:$USER ./work_dir ./logs ./memory ./knowledge ./tmp
```

### Container ไม่ start

ดู logs เพื่อหาสาเหตุ:

```bash
docker-compose logs gpaf
```

## 🔄 Update

อัปเดต GPAF เป็นเวอร์ชันล่าสุด:

```bash
make update
# หรือ
docker pull frdel/agent-zero-run:latest
docker-compose up -d
```

## 🐳 Hacking Edition

สำหรับ cybersecurity tasks:

```bash
# ใช้ hacking image แทน
docker pull frdel/agent-zero-run:hacking
docker run -p 50001:80 frdel/agent-zero-run:hacking
```

## 📚 เพิ่มเติม

- [Agent Zero Documentation](https://github.com/frdel/agent-zero)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/) 