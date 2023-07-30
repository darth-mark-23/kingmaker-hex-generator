# kingmaker-hex-generator

For a personal game, this generates attributes for a hex and uses ChatGPT to provide ideas and flavour.

## Quick Start

1. Make a virtual environment

```python -m venv venv```

   - Powershell:

```.\venv\Scripts\Activate.ps1```

   - Linux / Bash:

```source ./venv/Scripts/activate```
        
2. Install dependencies

```python -m pip install openai```
```python -m pip install pyyaml```

3. Get an API key from OpenAI and put it into an environment variable called `OPENAI_API_KEY` (you'll need to restart your console to make it take effect)
   
4. Generate the default hex data:

```python generate.py```

5. Generate custom data:

```python generate.py my_custom.yaml```
