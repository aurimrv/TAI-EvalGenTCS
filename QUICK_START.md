# Guia de Início Rápido - TAI-EvalGenTCS CLI

Este guia fornece instruções rápidas para começar a usar a ferramenta.

## 📦 Instalação Rápida

```bash
# 1. Clone o repositório
git clone <repository-url>
cd tai-evalgentcs-cli

# 2. Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure o .env
cp .env.example .env
# Edite .env e adicione sua chave OpenRouter API
```

## 🔑 Obtendo Chave da API

1. Acesse [OpenRouter](https://openrouter.ai/)
2. Crie uma conta
3. Vá para [API Keys](https://openrouter.ai/keys)
4. Crie uma nova chave
5. Adicione crédito (mínimo $15 recomendado)
6. Copie a chave para o arquivo `.env`

## 🚀 Uso Básico

### Verificar Conformidade

```bash
python main.py --check-best-practice \
  --original-test-set examples/UserServiceTest.java \
  --output-dir ./reports
```

**Resultado:**
- `reports/UserServiceTest_bp_report.json` - Relatório completo

### Melhorar Testes

```bash
python main.py --improve-best-practice \
  --original-test-set examples/UserServiceTest.java \
  --output-dir ./improved
```

**Resultado:**
- `improved/UserServiceTest_improved.java` - Código melhorado
- `improved/UserServiceTest_bp_report.json` - Relatório completo
- `improved/UserServiceTest_improvement_summary.md` - Resumo

## 📊 Interpretando Resultados

### Status de Conformidade

- **✔️** - Prática atendida
- **❌** - Prática não atendida (veja sugestões)
- **⚪** - Prática não aplicável

### Scores

- **Method Compliance Score**: Conformidade por método (0-100%)
- **Overall Compliance Score**: Conformidade geral da classe (0-100%)
- **Practice Compliance Score**: Conformidade por prática (0-100% ou N/A)

## 🎯 Próximos Passos

1. Revise o relatório JSON gerado
2. Analise as práticas não atendidas (❌)
3. Compare o código original com o melhorado
4. Aplique as melhorias ao seu projeto
5. Execute novamente para verificar melhorias

## 💡 Dicas

- Use `--verbose` para ver logs detalhados
- Comece com `--check-best-practice` para entender o estado atual
- Use `--improve-best-practice` quando quiser sugestões concretas
- Revise manualmente o código melhorado antes de aplicar

## 🆘 Problemas Comuns

### Erro: "OPENROUTER_API_KEY not found"
- Verifique se o arquivo `.env` existe
- Confirme que a chave está corretamente configurada

### Erro: "Rate limit exceeded"
- Aguarde alguns minutos
- Verifique se tem crédito suficiente no OpenRouter
- Ajuste `RATE_LIMIT_REQUESTS_PER_MINUTE` no `.env`

### Erro: "Best practices file not found"
- Verifique se `data/best_practices.json` existe
- Execute a partir do diretório raiz do projeto

## 📚 Documentação Completa

Para informações detalhadas, consulte:
- `README.md` - Documentação completa
- `data/best_practices.json` - Definições das 25 práticas
- `data/report-schema.json` - Schema do relatório JSON
