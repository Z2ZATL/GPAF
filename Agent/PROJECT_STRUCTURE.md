# GPAF Project Structure

## 📁 Directory Organization

```
GPAF/
├── 🚀 Core Application Files
│   ├── agent.py              # Main agent implementation
│   ├── models.py             # AI model configurations  
│   ├── initialize.py         # System initialization
│   └── run.py               # Quick start script
│
├── 📜 Scripts & Runners
│   ├── scripts/
│   │   ├── run_ui.py        # Web UI runner
│   │   ├── run_cli.py       # CLI runner
│   │   ├── run_tunnel.py    # Tunnel runner
│   │   ├── preload.py       # Model preloader
│   │   ├── prepare.py       # Setup script
│   │   └── update_reqs.py   # Dependencies updater
│
├── ⚙️ Configuration
│   ├── config/
│   │   ├── requirements.txt # Python dependencies
│   │   ├── example.env      # Environment template
│   │   └── jsconfig.json    # JavaScript config
│
├── 🐳 Deployment
│   ├── deployment/
│   │   └── docker/
│   │       ├── docker-compose.yml  # Docker orchestration
│   │       ├── Dockerfile          # Container definition
│   │       ├── .dockerignore       # Docker ignore rules
│   │       ├── Makefile           # Docker commands
│   │       └── DOCKER_README.md   # Docker guide
│   │
│   └── docker.sh           # Docker convenience script
│
├── 🧠 Core Components  
│   ├── python/             # Python modules
│   ├── prompts/            # AI prompts
│   ├── memory/             # Agent memory
│   ├── knowledge/          # Knowledge base
│   └── instruments/        # Custom tools
│
├── 🌐 Web Interface
│   ├── webui/              # Web UI files
│   └── lib/                # Client libraries
│
├── 📊 Data & Logs
│   ├── logs/               # Application logs
│   ├── tmp/                # Temporary files
│   └── work_dir/           # Working directory
│
├── 📚 Documentation
│   ├── docs/               # Documentation files
│   ├── README.md           # Main readme
│   └── PROJECT_STRUCTURE.md # This file
│
└── 🔧 Development
    ├── .github/            # GitHub workflows
    ├── .vscode/            # VS Code settings
    ├── .gitignore          # Git ignore rules
    └── LICENSE             # License file
```

## 🚀 Quick Start

### Run GPAF
```bash
# Method 1: Direct run
python run.py

# Method 2: From scripts
python scripts/run_ui.py

# Method 3: CLI mode  
python scripts/run_cli.py
```

### Docker Deployment
```bash
# Using convenience script
./docker.sh up

# Using make
make -C deployment/docker run

# Using docker-compose directly
docker-compose -f deployment/docker/docker-compose.yml up -d
```

## 📝 Configuration

1. **Environment Setup**:
   ```bash
   cp config/example.env .env
   # Edit .env with your API keys
   ```

2. **Dependencies**:
   ```bash
   pip install -r config/requirements.txt
   ```

## 🔧 Development

- **Main code**: Core application files in root
- **Scripts**: All runners in `scripts/` directory  
- **Config**: All configuration in `config/` directory
- **Docker**: All deployment files in `deployment/docker/`

## 📁 Directory Purpose

| Directory | Purpose |
|-----------|---------|
| `scripts/` | Executable scripts and runners |
| `config/` | Configuration files |
| `deployment/docker/` | Docker deployment files |
| `python/` | Core Python modules |
| `webui/` | Web interface files |
| `docs/` | Documentation |
| `prompts/` | AI system prompts |
| `memory/` | Agent memory storage |
| `knowledge/` | Knowledge base |
| `logs/` | Application logs |

## 🎯 Benefits

- ✅ **Organized**: Related files grouped together
- ✅ **Scalable**: Easy to add new components
- ✅ **Maintainable**: Clear separation of concerns  
- ✅ **Docker-ready**: Deployment files isolated
- ✅ **Developer-friendly**: Quick access scripts available 