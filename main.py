from flet import *
import sqlite3

# CONECTANDO AO BANCO DE DADOS
conexao = sqlite3.connect("dados.db", check_same_thread=False)
cursor = conexao.cursor()

# CRIANDO A TABELA DE CADASTRO NO BANCO DE DADOS
def tabela_cliente():
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)
    '''
    )

class App(UserControl):
    def __init__(self):
        super().__init__()

        self.todos_cadastros = Column(
            auto_scroll=True
        )

        self.adicionar_nome = TextField(
            label="Nome",
            width=800,
            border_radius=border_radius.all(6),
            border_color="black",
            filled=True,
            text_size=22,
            hint_text="Digite o nome cliente",
            content_padding=20,
        )

        self.editar_cadastro = TextField(
            label="Editar",
            width=800,
            border_radius=border_radius.all(6),
            border_color="black",
            filled=True,
            text_size=22,
            hint_text="Digite sua alteração",
            content_padding=20,
        )

    ### FUNÇÕES ###

    # FUNÇÃO DELETAR CADASTRO
    def deletar(self, x, y):
        cursor.execute("DELETE FROM clientes WHERE id = ?", [x])
        y.open = False
        # CHAMAR A FUNÇÃO PARA RENDERIZAR OS CADASTROS
        self.todos_cadastros.controls.clear()
        self.renderizar_todos()
        self.page.update()

    # FUNÇÃO EDITAR/ATUALIZAR CADASTRO
    def atualizar(self, x, y, z):
        cursor.execute("UPDATE clientes SET nome = ? WHERE id = ?", (y, x))
        conexao.commit()
        z.open = False
        # CHAMAR A FUNÇÃO PARA RENDERIZAR OS CADASTROS
        self.todos_cadastros.controls.clear()
        self.renderizar_todos()
        self.page.update()

    # FUNÇÃO ABRIR MENU PARA EDITAR CADASTRO
    def abrir_acoes(self, e):
        id_user = e.control.leading.value
        self.editar_cadastro.value = e.control.title.value
        self.page.update()

        alerta_dialogo = AlertDialog(
            title=Text(f"Editar ID {id_user}"),
            content=self.editar_cadastro,

            # BOTÕES DE AÇÃO
            actions=[
                ElevatedButton(
                    "Deletar",
                    color="white",
                    bgcolor="red",
                    on_click=lambda e:self.deletar(id_user,
                                                   alerta_dialogo
                                                   )
                ),
                ElevatedButton(
                    "Atualizar",
                    color="white",
                    bgcolor="green",
                    on_click=lambda e:self.atualizar(id_user,
                                                     self.editar_cadastro.value,
                                                     alerta_dialogo
                                                     )
                )
            ],
            actions_alignment="spaceBetween"
        )

        self.page.dialog = alerta_dialogo
        alerta_dialogo.open = True
        self.page.update()

    # READ - LENDO/EXIBINDO OS DADOS DO BANCO DE DADOS
    def renderizar_todos(self):
        cursor.execute("SELECT * FROM clientes")
        conexao.commit()
        meus_cadastros = cursor.fetchall()

        for cadastro in meus_cadastros:
            self.todos_cadastros.controls.append(
                ListTile(
                    leading=Text(cadastro[0], size=16, color="white"),
                    title=Text(cadastro[1], size=20, color="white"),
                    #subtitle=Text(cadastro[0], size=16, color="white"),
                    on_click=self.abrir_acoes
                )
            )
        self.update()

    def ciclo(self):
        self.renderizar_todos()

    # CREATE - CRIANDO DADOS DENTRO DO BANCO DE DADOS
    def adicionar_novo_cadastro(self, e):
        tabela_cliente()
        cursor.execute("INSERT INTO clientes (nome) VALUES (?)",
                       [self.adicionar_nome.value])
        conexao.commit()

        # CHAMAR A FUNÇÃO PARA RENDERIZAR OS CADASTROS
        self.todos_cadastros.controls.clear()
        self.renderizar_todos()
        self.page.update()

    # CONSTRUINDO A APLICAÇÃO
    def build(self):
        return Column([
            # TÍTULO, CABEÇALHO
            Text(
                "CADASTRO DE CLIENTES - com SQLite",
                size=22,
                weight="bold",
                color="white",
            ),
            # CAMPO DE CADASTRO - NOME
            self.adicionar_nome,
            # BOTÃO DE ADIIONAR NOVO CADASTRO
            ElevatedButton(
                width=180,
                height=40,
                bgcolor="blue700",
                on_click=self.adicionar_novo_cadastro,
                style=ButtonStyle(
                    shape=RoundedRectangleBorder(radius=6)
                ),
                content=Container(
                    content=Row(
                        [
                            Icon(name=icons.SAVE_ALT_OUTLINED, color="white"),
                            Text("Adicionar", size=20, color="white"),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    )
                )
            ),
            # LISTA DE CADASTROS
            self.todos_cadastros
        ])


def main(page: Page):
    page.bgcolor = colors.DEEP_ORANGE_900
    page.scroll = True
        

    minha_aplicacao = App()
       

    page.add(
        minha_aplicacao,
    )


app(target=main, assets_dir="assets")
