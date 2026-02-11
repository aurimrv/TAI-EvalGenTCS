# TAI-EvalGenTCS CLI

**Test AI Evaluator and Generator of Test Case Suites - Command Line Interface**

Ferramenta de linha de comando para avaliação e melhoria de suítes de teste baseada em 25 boas práticas de engenharia de software, desenvolvida como parte da pesquisa de doutorado na **Universidade Federal de São Carlos (UFSCar)**.

## 📋 Sobre o Projeto

Esta ferramenta implementa os resultados da tese de doutorado *"Towards a strategy and tool support for test generation based on good software testing practices: classification and prioritization"* de **Camilo Hernán Villota Ibarra**, oferecendo uma interface de linha de comando para:

- **Avaliar** a conformidade de casos de teste com 25 boas práticas fundamentais
- **Melhorar** automaticamente suítes de teste com base nas boas práticas
- **Gerar relatórios** detalhados em formato JSON

### Fundamentação Teórica

A ferramenta está fundamentada em uma **Revisão Sistemática da Literatura (SLR)** que:
- Identificou **131 práticas** de testes de software em 103 estudos primários
- Refinou e sintetizou essas práticas em **40 boas práticas essenciais**
- Validou empiricamente através de pesquisa com testers profissionais
- Implementa **25 boas práticas fundamentais** divididas em:
  - **Common Sense (CS)**: 14 práticas de senso comum validadas pela indústria
  - **Literature Supported (LS)**: 11 práticas respaldadas por pesquisas acadêmicas

## 🏗️ Arquitetura

O sistema utiliza uma **arquitetura multi-agente** com os seguintes componentes:

```
tai-evalgentcs-cli/
├── main.py                          # Ponto de entrada CLI
├── src/
│   ├── agents/                      # Agentes especializados
│   │   ├── test_analyzer_agent.py   # Análise de código de teste
│   │   └── test_improver_agent.py   # Geração de código melhorado
│   ├── config/                      # Configurações
│   │   └── settings.py              # Gerenciamento de configurações
│   ├── models/                      # Modelos de dados
│   │   └── practice_manager.py      # Gerenciamento de boas práticas
│   ├── services/                    # Serviços
│   │   ├── llm_client.py            # Cliente LLM com rate limiting
│   │   └── orchestrator.py          # Orquestração do workflow
│   └── utils/                       # Utilitários
│       └── logger.py                # Configuração de logging
├── data/
│   └── best_practices.json          # Definições das 25 boas práticas
├── requirements.txt                 # Dependências Python
└── .env.example                     # Template de configuração
```

### Componentes Principais

- **TestAnalyzerAgent**: Analisa código de teste e avalia conformidade com boas práticas
- **TestImproverAgent**: Gera versões melhoradas do código de teste
- **PracticeManager**: Gerencia as definições das 25 boas práticas
- **LLMClient**: Cliente para comunicação com OpenRouter API (rate limiting e retry)
- **TestEvaluationOrchestrator**: Coordena o fluxo de trabalho entre agentes

## 🚀 Instalação

### Requisitos

- Python 3.11 ou superior
- Conta no [OpenRouter](https://openrouter.ai/)
- Crédito mínimo de $15 no OpenRouter (para rate limits adequados)

### Passos de Instalação

1. **Clone o repositório:**
```bash
git clone <repository-url>
cd tai-evalgentcs-cli
```

2. **Crie um ambiente virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite .env e adicione sua chave de API do OpenRouter
```

## ⚙️ Configuração

Edite o arquivo `.env` com suas configurações:

```env
# OpenRouter API Key (obrigatório)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Modelo LLM (recomendado: openai/gpt-4.1-mini)
LLM_MODEL=openai/gpt-4.1-mini

# Temperatura (0.0-1.0, recomendado: 0.1 para análise de código)
LLM_TEMPERATURE=0.1

# Rate Limiting (para crédito > $15)
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_TOKENS_PER_MINUTE=100000
```

## 📖 Uso

### Modo 1: Verificar Conformidade com Boas Práticas

Gera um relatório JSON detalhado sobre a conformidade do código de teste:

```bash
python main.py --check-best-practice \
  --original-test-set tests/UserServiceTest.java \
  --output-dir ./reports
```

**Saída:**
- `UserServiceTest_bp_report.json`: Relatório completo em JSON

### Modo 2: Melhorar Suíte de Testes

Gera uma versão melhorada do código de teste baseada nas boas práticas:

```bash
python main.py --improve-best-practice \
  --original-test-set tests/UserServiceTest.java \
  --output-dir ./improved
```

**Saída:**
- `UserServiceTest_improved.java`: Código de teste melhorado
- `UserServiceTest_bp_report.json`: Relatório completo em JSON
- `UserServiceTest_improvement_summary.md`: Resumo das melhorias

### Opções Adicionais

```bash
# Usar modelo LLM específico
python main.py --check-best-practice \
  --original-test-set tests/UserServiceTest.java \
  --output-dir ./reports \
  --llm-model openai/gpt-4-turbo

# Ativar logging verbose
python main.py --check-best-practice \
  --original-test-set tests/UserServiceTest.java \
  --output-dir ./reports \
  --verbose

# Usar arquivo de configuração customizado
python main.py --check-best-practice \
  --original-test-set tests/UserServiceTest.java \
  --output-dir ./reports \
  --config custom.env
```

## 📊 Formato do Relatório

O relatório JSON segue o schema definido em `report-schema.json` e inclui:

### Estrutura do Relatório

```json
{
  "test_class_name": "UserServiceTest",
  "test_methods": [
    {
      "test_method_name": "testCreateUser",
      "practices_evaluation": [
        {
          "practice_code": "CS-01",
          "practice_title": "Especificação Atômica de Casos de Teste",
          "status": "✔️",
          "justification": "O teste foca em um único comportamento...",
          "original_code": null,
          "improved_code": null
        }
      ],
      "method_compliance_score": "92%",
      "suggested_code": "..."
    }
  ],
  "practices_report": [
    {
      "practice_code": "CS-01",
      "practice_title": "Especificação Atômica de Casos de Teste",
      "description": "...",
      "compliant_methods": 5,
      "non_compliant_methods": 1,
      "not_applicable_methods": 0,
      "total_methods": 6,
      "compliance_score": "83%"
    }
  ],
  "overall_compliance_score": "87%"
}
```

### Status de Conformidade

- **✔️ (Atende)**: A prática é seguida corretamente
- **❌ (Não Atende)**: A prática não é seguida (com sugestão de melhoria)
- **⚪ (Não Aplicável)**: A prática não se aplica ao contexto do teste

## 🎯 As 25 Boas Práticas

### Common Sense Practices (CS-01 a CS-14)

1. **CS-01**: Especificação Atômica de Casos de Teste
2. **CS-02**: Independência Completa de Casos de Teste
3. **CS-03**: Cobertura de Fluxos Normais e Excepcionais
4. **CS-04**: Análise de Valores Limite
5. **CS-05**: Modularidade Completa de Casos de Teste
6. **CS-06**: Análise Detalhada de Tamanho e Complexidade
7. **CS-07**: Design Complexo para Detecção de Falhas
8. **CS-08**: Manutenção Completa do Código de Teste
9. **CS-09**: Rastreabilidade Completa de Casos de Teste
10. **CS-10**: Uso Rigoroso de Testes de Performance e Segurança
11. **CS-11**: Revisão Regular de Casos de Teste
12. **CS-12**: Compreensão Clara de Casos de Teste
13. **CS-13**: Cobertura Estruturada do Processo de Teste
14. **CS-14**: Garantia Completa da Qualidade do Código de Teste

### Literature Supported Practices (LS-01 a LS-11)

1. **LS-01**: Utilização Adequada de Cobertura de Código
2. **LS-02**: Utilização Necessária de Testes Ausentes
3. **LS-03**: Utilização Eficiente de Cobertura de Código
4. **LS-04**: Pegada Pequena de Geração de Código de Teste
5. **LS-05**: Priorização Completa do Design de Casos de Teste
6. **LS-06**: Adição Responsável de Manutenção de Código de Teste
7. **LS-07**: Utilização Adequada de Asserções de Teste
8. **LS-08**: Adição Responsável de Comentários de Depuração
9. **LS-09**: Design Determinístico de Resultados de Teste
10. **LS-10**: Evitar Completamente Efeitos Colaterais de Teste
11. **LS-11**: Utilização Adequada de Rótulos e Categorias

Detalhes completos em `data/best_practices.json`.

## 🔧 Desenvolvimento

### Executar Testes

```bash
pytest tests/ -v --cov=src
```

### Estrutura de Código Limpo

O projeto segue princípios de **Clean Architecture**:

- **Separação de responsabilidades**: Cada módulo tem uma responsabilidade clara
- **Inversão de dependências**: Componentes dependem de abstrações
- **Testabilidade**: Código facilmente testável com mocks
- **Configuração externa**: Todas as configurações via `.env`

## 📚 Referências

- **Tese de Doutorado**: "Towards a strategy and tool support for test generation based on good software testing practices: classification and prioritization"
- **Autor**: Camilo Hernán Villota Ibarra
- **Orientador**: Prof. Dr. Auri Marcelo Rizzo Vincenzi
- **Co-orientador**: Prof. Dr. José Carlos Maldonado
- **Instituição**: Universidade Federal de São Carlos (UFSCar)

## 📄 Licença

Este projeto é parte de uma pesquisa acadêmica na UFSCar.

## 👥 Autores

- **Camilo Hernán Villota Ibarra** - Autor Principal e Pesquisador
- **Auri Marcelo Rizzo Vincenzi** - Orientador
- **José Carlos Maldonado** - Co-orientador

## 🤝 Contribuições

Para questões, sugestões ou contribuições, entre em contato com os autores.
