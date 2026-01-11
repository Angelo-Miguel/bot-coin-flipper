> [!WARNING]
> Este repositório está em desenvolvimento ativo (Work in Progress). Mudanças frequentes podem ocorrer.

# Bot Coin Flipper

Bot simples de Discord para escolher aleatoriamente entre opções separadas por vírgula + espaço.

## Funcionalidades

-  /flip — Recebe uma lista separada por `,` (vírgula + espaço) e retorna uma opção aleatória.
-  Logs gravados em [flipper_bot.log](utils/flipper_bot.log) (logger rotativo).

## Requisitos

-  Python 3.8+
-  Dependências (veja [requirements.txt](requirements.txt)`):
   -  discord.py
   -  dotenv

## Instalação

1. Clone o repositório:

   ```sh
   git clone https://github.com/Angelo-Miguel/bot-coin-flipper.git
   cd bot-coin-flipper
   ```

2. Crie e ative um ambiente virtual (recomendado):

   ```
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   ```

3. Instale as dependências:

   ```sh
   pip install -r requirements.txt

   ```

4. Crie um arquivo `.env` na raiz com o token do bot:

   ```sh
   DISCORD_TOKEN=seu_token_aqui
   ```

   > ⚠️ Nunca compartilhe seu token publicamente.

5. Como rodar

   ```sh
   python bot.py
   ```

   O bot sincroniza os comandos de aplicação (slash commands) ao conectar-se.

6. Uso do comando `/flip`:

   -  Comando: `/flip query:"opção1, opção2, opção3"`
   -  Exemplo:

      -  Entrada: `/flip query:"cara, coroa"`
      -  Saída: ´cara´(ou `coroa`, aleatoriamente)

      > 💡 Observação: o separador atual é `, ` (vírgula + espaço). Evite usar apenas vírgula sem espaço.

## Estrutura do projeto

```
.
├── commands/
│   └── flipper_commands.py     # Comando /flip
├── core/
│   └── bot_client.py           # Classe FlipperBot e setup de cogs
├── utils/
│   └── logger.py               # Log do Sistema
├── config.py                   # Configuração do Sistema
├── .env                        # Variáveis de ambiente (configurações sensíveis)
├── bot.py                      # Ponto de entrada da aplicação
├── .gitignore                  # Arquivos e pastas ignorados pelo Git
├── LICENSE                     # Licença do projeto
├── readme.md                   # Documentação do projeto
└── requirements.txt            # Lista de dependências do Python
```

## Colaboradores

<table>
  <tr>
      <td align="center">
      <a href="https://github.com/Angelo-Miguel" title="GitHub de Angelo Miguel Santa Rosa">
        <img src="https://avatars.githubusercontent.com/u/127904294?v=4" width="100px;" alt="Foto do Angelo Miguel Santa Rosa no GitHub"/><br>
        <sub>
          <b>Angelo Miguel</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

## Licença

Este projeto é apenas para fins acadêmicos.

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE) para mais detalhes.
