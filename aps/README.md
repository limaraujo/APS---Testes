# APS - Testes

Documentação focada exclusivamente na execução e manutenção dos testes automatizados.

## Estrutura esperada

```text
. (venv)
└── aps
	├── pytest.ini
	├── requirements.txt
	├── src
	└── tests
```

## Arquivos de teste

- [tests/test_main.py](tests/test_main.py): suíte principal com cenários de aprovação, revisão manual, rejeição, validações e casos de fronteira.
- [pytest.ini](pytest.ini): configuração do pytest com pythonpath = .

## Pré-requisitos

- Python 3.10+
- pip

## Preparação do ambiente

Entre na pasta [aps](.) e instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução dos testes

### Linux/macOS


```bash
python3 -m pytest -q
```

### Windows (PowerShell)

```powershell
python -m pytest -q
```


## Cobertura de testes

### Linux/macOS

Cobertura no terminal:

```bash
cd aps
python3 -m pytest --cov=src --cov-report=term-missing
```

Relatório HTML:

```bash
cd aps
python3 -m pytest --cov=src --cov-report=html
```

### Windows (PowerShell)

Cobertura no terminal:

```powershell
cd aps
python -m pytest --cov=src --cov-report=term-missing
```

Relatório HTML:

```powershell
cd
python -m pytest --cov=src --cov-report=html
```

Depois da execução, abra htmlcov/index.html.

## Geração do CFG (Control Flow Graph)

### Linux/macOS

```bash
cd aps
python3 cfg.py
```

### Windows (PowerShell)

```powershell
cd aps
python cfg.py
```

**Observação:** Requer Graphviz instalado no sistema. Se receber erro sobre `dot` não encontrado, instale em:
- **Windows:** https://graphviz.org/download/ ou `choco install graphviz`
- **macOS:** `brew install graphviz`
- **Linux:** `apt install graphviz`

## Escopo atualmente coberto

A suíte em [tests/test_main.py](tests/test_main.py) cobre:

- fluxo aprovado
- fluxo de revisão manual por idade, GPA e frequência
- fluxo de rejeição por idade, GPA, frequência, disciplinas obrigatórias e histórico disciplinar
- validação de entradas inválidas com ValueError
- limites importantes das regras (16, 18, 6.0, 7.0, 75.0 e 80.0)
- prioridade de rejeição sobre revisão manual
