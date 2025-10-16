import ply.lex as lex
import json
import os
from datetime import datetime

# ---------- TOKENS ----------
tokens = (
    'LISTAR', 'MOEDA', 'SELECIONAR', 'SALDO', 'STATUS',
    'ADICIONAR', 'REMOVER', 'RESET', 'ALTERAR_PRECO', 'ADMIN', 'CLIENT', 'SAIR', 'HELP',
    'CODIGO', 'VALOR', 'NOME', 'NUMERO',
)

def t_LISTAR(t):
    r'LISTAR'
    return t

def t_MOEDA(t):
    r'MOEDA'
    return t

def t_SELECIONAR(t):
    r'SELECIONAR'
    return t

def t_SALDO(t):
    r'SALDO'
    return t

def t_STATUS(t):
    r'STATUS'
    return t

def t_ADICIONAR(t):
    r'ADICIONAR'
    return t

def t_REMOVER(t):
    r'REMOVER'
    return t

def t_RESET(t):
    r'RESET'
    return t

def t_ALTERAR_PRECO(t):
    r'ALTERAR_PRECO'
    return t

def t_ADMIN(t):
    r'ADMIN'
    return t

def t_CLIENT(t):
    r'CLIENT'
    return t

def t_SAIR(t):
    r'SAIR'
    return t

def t_HELP(t):
    r'HELP'
    return t

def t_CODIGO(t):
    r'[A-Z]\d{2}'
    return t

def t_VALOR(t):
    r'\d+[eEcC]'
    t.value = t.value.lower()
    return t

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    return t

def t_NOME(t):
    r'[A-Za-zÀ-ÿ_][A-Za-zÀ-ÿ0-9_]*'
    return t

t_ignore = " \t,."

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"maq: Caractere inválido: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# ---------- CLASSE DA VENDING MACHINE ----------
class VendingMachine:
    def __init__(self, stock_file="stock.json", admin_code="1234"):
        self.stock_file = stock_file
        self.saldo = 0.0
        self.stock = self.carregar_stock()
        self.moedas_validas = {"1e":1.0, "50c":0.5, "20c":0.2, "10c":0.1, "5c":0.05, "2c":0.02, "1c":0.01}
        self.admin_code = admin_code
        self.admin = False

    def carregar_stock(self):
        if os.path.exists(self.stock_file):
            try:
                with open(self.stock_file, "r", encoding="utf-8") as f:
                    stock = json.load(f)
                stock.sort(key=lambda x: x["cod"])
                hoje = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"maq: {hoje}, Stock carregado, Estado atualizado.")
                return stock
            except Exception as e:
                print(f"maq: Erro a carregar stock: {e}")
                return []
        else:
            print("maq: Ficheiro de stock não encontrado.")
            return []

    def gravar_stock(self):
        try:
            self.stock.sort(key=lambda x: x["cod"])
            with open(self.stock_file, "w", encoding="utf-8") as f:
                json.dump(self.stock, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"maq: Erro ao gravar stock: {e}")

    def formatar_saldo(self, valor):
        euros = int(valor)
        centimos = round((valor - euros) * 100)
        if euros > 0 and centimos > 0:
            return f"{euros}e{centimos}c"
        elif euros > 0:
            return f"{euros}e"
        else:
            return f"{centimos}c"

    def listar(self):
        print("maq:")
        print("cod | nome                 | quant | preço")
        print("--------------------------------------------")
        for produto in self.stock:
            if self.admin or produto["quant"] > 0:
                print(f"{produto['cod']} | {produto['nome']:20} | {produto['quant']:5} | {produto['preco']:5.2f}€")
        print("--------------------------------------------")

    def processar_moedas(self, texto_moedas):
        """Processa diretamente o texto das moedas para ser mais flexível"""
        import re
        
        # Encontrar todas as moedas no texto usando regex
        moedas_encontradas = re.findall(r'(\d+[eEcC])', texto_moedas)
        
        if not moedas_encontradas:
            print("maq: Por favor especifique moedas (ex: MOEDA 1e 50c 20c 5c)")
            return
            
        total_inserido = 0
        for moeda in moedas_encontradas:
            moeda = moeda.lower()
            if moeda in self.moedas_validas:
                valor = self.moedas_validas[moeda]
                self.saldo += valor
                total_inserido += valor
                print(f"maq: Inseriu {moeda} ({valor:.2f}€)")
            else:
                print(f"maq: Moeda inválida: {moeda}")
        
        print(f"maq: Total inserido: {total_inserido:.2f}€")
        print(f"maq: Saldo atual = {self.formatar_saldo(self.saldo)}")

    def selecionar_produto(self, codigo):
        for produto in self.stock:
            if produto["cod"] == codigo:
                if produto["quant"] <= 0:
                    print(f"maq: Produto '{produto['nome']}' esgotado.")
                    return
                
                if self.saldo >= produto["preco"]:
                    produto["quant"] -= 1
                    self.saldo -= produto["preco"]
                    self.gravar_stock()
                    print(f"maq: Pode retirar o produto dispensado \"{produto['nome']}\"")
                    print(f"maq: Saldo restante = {self.formatar_saldo(self.saldo)}")
                else:
                    falta = produto["preco"] - self.saldo
                    print(f"maq: Saldo insuficiente para satisfazer o seu pedido")
                    print(f"maq: Saldo = {self.formatar_saldo(self.saldo)}; Pedido = {self.formatar_saldo(produto['preco'])}; Falta = {self.formatar_saldo(falta)}")
                return
                
        print("maq: Código inválido.")

    def devolver_troco(self):
        if self.saldo <= 0:
            print("maq: Sem troco.")
            return
            
        saldo_restante = self.saldo
        troco = []
        
        # Ordenar moedas por valor descendente
        moedas_ordenadas = sorted(self.moedas_validas.items(), key=lambda x: x[1], reverse=True)
        
        for moeda_str, valor in moedas_ordenadas:
            count = int(saldo_restante // valor)
            if count > 0:
                troco.append(f"{count}x {moeda_str}")
                saldo_restante = round(saldo_restante - count * valor, 2)
        
        if troco:
            print(f"maq: Pode retirar o troco: {', '.join(troco)}.")
        else:
            print("maq: Sem troco.")
        
        self.saldo = 0

    def mostrar_saldo(self):
        print(f"maq: Saldo = {self.formatar_saldo(self.saldo)}")

    def mostrar_status(self):
        if not self.admin:
            print("maq: Comando restrito a administrador.")
            return
            
        produtos_baixos = [p for p in self.stock if p["quant"] <= 2]
        if produtos_baixos:
            print("maq: Produtos com stock baixo:")
            for produto in produtos_baixos:
                print(f"maq: - {produto['cod']}: {produto['nome']} ({produto['quant']} unidades)")
        else:
            print("maq: Todos os produtos têm stock suficiente.")

    def ativar_admin(self):
        codigo = input("maq: Insira código de administrador: ")
        if codigo == self.admin_code:
            self.admin = True
            print("maq: Modo administrador ativado.")
        else:
            print("maq: Código incorreto.")

    def desativar_admin(self):
        if not self.admin:
            print("maq: Já se encontra no modo cliente.")
            return
        self.admin = False
        print("maq: Modo cliente ativado. Permissões de administrador revogadas.")


    def adicionar_produto(self, tokens):
        if not self.admin:
            print("maq: Comando restrito a administrador.")
            return
            
        # Juntar todos os tokens para processar o nome do produto
        args = [t.value for t in tokens]
        if len(args) < 4:
            print("maq: Uso: ADICIONAR <codigo> <nome> <quantidade> <preco>")
            return
            
        codigo = args[0]
        # O nome do produto pode ter múltiplas palavras
        nome_parts = args[1:-2]
        nome = ' '.join(nome_parts)
        quantidade = int(args[-2])
        preco = float(args[-1])
        
        # Verificar se produto já existe
        for produto in self.stock:
            if produto["cod"] == codigo:
                produto["quant"] += quantidade
                produto["preco"] = preco
                print(f"maq: Produto '{nome}' atualizado. Quantidade: {produto['quant']}")
                self.gravar_stock()
                return
                
        # Adicionar novo produto
        novo_produto = {
            "cod": codigo,
            "nome": nome,
            "quant": quantidade,
            "preco": preco
        }
        self.stock.append(novo_produto)
        print(f"maq: Produto '{nome}' adicionado com sucesso.")
        self.gravar_stock()

    def remover_produto(self, codigo):
        """Remove um produto do stock (apenas admin)"""
        if not self.admin:
            print("maq: Comando restrito a administrador.")
            return

        # Procurar o produto pelo código
        for i, produto in enumerate(self.stock):
            if produto["cod"] == codigo:
                removido = self.stock.pop(i)
                self.gravar_stock()
                print(f"maq: Produto '{removido['nome']}' ({removido['cod']}) removido com sucesso.")
                return

        # Se não encontrou o código
        print(f"maq: Código de produto '{codigo}' não encontrado.")

    def reset_stock(self):
        if not self.admin:
            print("maq: Comando restrito a administrador.")
            return
            
        self.stock = []
        self.gravar_stock()
        print("maq: Stock reiniciado.")

    def alterar_preco(self, tokens):
        if not self.admin:
            print("maq: Comando restrito a administrador.")
            return
            
        if len(tokens) < 2:
            print("maq: Uso: ALTERAR_PRECO <codigo> <novo_preco>")
            return
            
        codigo = tokens[0].value
        novo_preco = float(tokens[1].value)
        
        for produto in self.stock:
            if produto["cod"] == codigo:
                produto["preco"] = novo_preco
                self.gravar_stock()
                print(f"maq: Preço de '{produto['nome']}' alterado para {novo_preco:.2f}€")
                return
                
        print("maq: Código de produto não encontrado.")

    def mostrar_ajuda(self):
        print("""
maq: Comandos disponíveis:
 LISTAR                  - Lista todos os produtos disponíveis
 MOEDA <valores>         - Insere moedas (ex: MOEDA 1e 50c 20c 5c)
 SELECIONAR <codigo>     - Seleciona um produto pelo código
 SALDO                   - Mostra o saldo atual
 SAIR                    - Devolve o troco e termina
 ADMIN                   - Ativa modo administrador (pede código)
 CLIENT                  - Sai do modo administrador e volta ao modo cliente (admin)
 STATUS                  - Mostra produtos com stock baixo (admin)
 ADICIONAR <c> <n> <q> <p> - Adiciona produto (admin)
 REMOVER <c>             - Remove produto pelo código (admin)
 RESET                   - Reinicia stock (admin)
 ALTERAR_PRECO <c> <p>   - Altera preço (admin)
 HELP                    - Mostra esta ajuda

Moedas aceites: 1e, 50c, 20c, 10c, 5c, 2c, 1c
Exemplos:
  MOEDA 1e 50c 20c
    ou
  MOEDA 1e,50c,20c,5c
  SELECIONAR A23
  ADICIONAR D03 Sandes Mista 10 2.50
""")

    def processar_comando(self, comando):
        """Processa um comando completo"""
        try:
            lexer.input(comando)
            tokens = list(lexer)
            if not tokens:
                print("maq: Comando não reconhecido.")
                return
            comando_principal = tokens[0]
            if comando_principal.type == 'LISTAR':
                self.listar()
            elif comando_principal.type == 'MOEDA':
                # Extrair a parte das moedas do comando completo
                partes = comando.split(' ', 1)
                if len(partes) > 1:
                    texto_moedas = partes[1]
                    self.processar_moedas(texto_moedas)
                else:
                    print("maq: Por favor especifique moedas (ex: MOEDA 1e 50c 20c 5c)")
            elif comando_principal.type == 'SELECIONAR':
                if len(tokens) > 1 and tokens[1].type == 'CODIGO':
                    self.selecionar_produto(tokens[1].value)
                else:
                    print("maq: Uso: SELECIONAR <codigo> (ex: SELECIONAR A23)")
            elif comando_principal.type == 'SALDO':
                self.mostrar_saldo()
            elif comando_principal.type == 'STATUS':
                self.mostrar_status()
            elif comando_principal.type == 'ADMIN':
                self.ativar_admin()
            elif comando_principal.type == 'CLIENT':
                self.desativar_admin()
            elif comando_principal.type == 'ADICIONAR':
                self.adicionar_produto(tokens[1:])
            elif comando_principal.type == 'REMOVER':
                if len(tokens) > 1 and tokens[1].type == 'CODIGO':
                    self.remover_produto(tokens[1].value)
                else:
                    print("maq: Uso: REMOVER <codigo> (ex: REMOVER A23)")
            elif comando_principal.type == 'RESET':
                self.reset_stock()
            elif comando_principal.type == 'ALTERAR_PRECO':
                self.alterar_preco(tokens[1:])
            elif comando_principal.type == 'HELP':
                self.mostrar_ajuda()                
            elif comando_principal.type == 'SAIR':
                self.devolver_troco()
                self.gravar_stock()
                return True               
            else:
                print("maq: Comando não reconhecido. Digite HELP para ajuda.")         
        except Exception as e:
            print(f"maq: Erro ao processar comando: {e}")  
        return False

    def run(self):
        print("maq: Bom dia! Estou disponível para atender o seu pedido.")
        print("maq: Digite HELP para ver os comandos disponíveis.")
        
        while True:
            try:
                comando = input(">> ").strip()
                if not comando:
                    continue
                # Converter para maiúsculas para comandos
                comando_upper = comando.upper()
                if self.processar_comando(comando_upper):
                    print("maq: Até à próxima!")
                    break       
            except KeyboardInterrupt:
                print("\nmaq: A desligar...")
                self.devolver_troco()
                break
            except EOFError:
                print("\nmaq: A desligar...")
                self.devolver_troco()
                break

if __name__ == "__main__":
    maquina = VendingMachine()
    maquina.run()