# rag-ollama-chroma-apple

For the article: <https://python.plainenglish.io/rag-local-dev-with-vs-code-dev-containers-ollama-and-rancher-desktop-ce418cb85149>

This article provides a way to set up a dev environment where we can do so on Apple Silicon by leveraging VS Code and its Dev Containers as an IDE with debugging, Ollama as an LLM runtime, and Rancher Desktop for the compute fabric for the Dev Containers.

The code is adapted from this awesome simple example: <https://mer.vin/2024/02/ollama-embedding/>

## Usage

### 1. Rancher Desktop Setup (1/7)

For my compute fabric, I have Rancher Desktop configured to use 6 GB mem and 2 CPUs, QEMU, and the dockerd (moby) container engine

### 2. VS Code integration with Rancher Desktop (2/7)

I assume you have the basic Python plugins (pylance) and only need to add the Dev Containers plugin in VS Code <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers>

To use Rancher Desktop's docker command with VS Code, search for docker in the settings and set the container path to `/Users/YOUR_USERNAME/.rd/bin/docker`.

### 3. Clone and open the rag-ollama-chroma repo (3/7)

Clone the repo and open it in VS Code with this command: 
`git clone https://github.com/jwsy/rag-ollama-chroma-apple.git`
The main.py file is based on the code shared by mer.vin <https://mer.vin/2024/02/ollama-embedding/> but I had to update it since it's a few months old…sheesh modern AI dev moves fast!

### 4. Start the VS Code dev container (4/7)

The `.devcontainer/devcontainer.json` config uses the Dockerfile in the same folder which is based on the default VS Code Poetry dev container.

### 5. Install Python Dependencies with Poetry & use the right interpreter (5/7)

Now that the container is up, install dependencies with poetry using `poetry install --no-root` which takes advantage of the `poetry.lock` file provided in the repo. I'm using the built-in VS Code terminal here and it took about 3  minutes to install the dependencies.

Change the Python interpreter to the right one in the container (`./venv/bin/python`) by clicking in the bottom right to bring up the dialog.

### 6. Use Ollama to retrieve models and serve an LLM API (6/7)

```
$ ollama pull nomic-embed-text:latest
pulling manifest
pulling 970aa74c0a90... 100% ▕████████████████████████████▏ 274 MB
...
verifying sha256 digest
writing manifest
removing any unused layers
success

$ ollama pull llama3:8b
pulling manifest
pulling 00e1317cbf74... 100% ▕████████████████████████████▏ 4.7 GB
...
verifying sha256 digest
writing manifest
removing any unused layers
success

$ ollama list
NAME                    ID           SIZE   MODIFIED
llama3:8b               a6990ed6be41 4.7 GB 4 seconds ago
nomic-embed-text:latest 0a109f422b47 274 MB 17 seconds ago
```

IMPORTANT: Start Ollama with `OLLAMA_HOST=0.0.0.0 ollama serve`, and note that we need to provide the OLLAMA_HOST arg so that the Dev Container can see this service. You'll see that `http://0.0.0.0:*` is bound as one of the OLLAMA_ORIGINS in the logs. This is important because the Dev Container thinks that the loopback 127.0.0.1 is its own container and not the local machine running Ollama.

### 7. Develop & Debug the app (7/7)

IMPORTANT: You will need to update line 16 with the local IP address of your machine. In the Mac Terminal app, the `ipconfig getifaddr en0` command will give you the right IP.
