import webbrowser

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconRightWidget
from kivymd.uix.scrollview import MDScrollView
from pymongo import MongoClient
from bson.objectid import ObjectId
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
import random
from kivymd.uix.label import MDLabel

client = MongoClient("mongodb+srv://matics:matics@cluster0.mryusjj.mongodb.net/?retryWrites=true&w=majority")
db = client["Cluster0"]
users = db["users"]

exercicios = db["exercicos"]
simples = exercicios["simples"]
compostos = exercicios["compostos"]

user = {}

def peg_ex_simples(id_ex):  # retorna a questao a partir do id escolhido
    dic = {}
    exercicio = simples.find_one({"_id": ObjectId(id_ex)})
    dic["questao"] = exercicio["questao"]
    dic["j"] = exercicio["j"]
    dic["c"] = exercicio["c"]
    dic["i"] = exercicio["i"]
    dic["t"] = exercicio["t"]
    dic["resposta"] = exercicio["resposta"]
    if len(dic) < 1:
        cadastrar_simples("(Vunesp) Num balancete de uma empresa consta que certo capital foi aplicado a uma taxa de 30% ao ano durante 8 meses, rendendo juros simples no valor de R$ 192,00. O capital aplicado foi de:", "192", "?", "0.025", "8", "960")
        dic["questao"] = "(Vunesp) Num balancete de uma empresa consta que certo capital foi aplicado a uma taxa de 30% ao ano durante 8 meses, rendendo juros simples no valor de R$ 192,00. O capital aplicado foi de:"
        dic["j"] = "192"
        dic["c"] = "?"
        dic["i"] = "0.025"
        dic["t"] = "8"
        dic["resposta"] = "960"
    return dic

def peg_ex_composto(id_ex):  # retorna a questao a partir do id escolhido
    dic = {}
    exercicio = compostos.find_one({"_id": ObjectId(id_ex)})
    dic["questao"] = exercicio["questao"]
    dic["m"] = exercicio["m"]
    dic["c"] = exercicio["c"]
    dic["i"] = exercicio["i"]
    dic["t"] = exercicio["t"]
    dic["resposta"] = exercicio["resposta"]
    if len(dic) < 1:
        cadastrar_composto("Um investidor aplicou um capital a juros simples com taxa de 3% ao mês, durante sete meses, gerando R$ 1.785,00 de juros. O valor do capital investido é igual a:", "1785", "?", "0.03", "7", "8500")
        dic["questao"] = "Um investidor aplicou um capital a juros simples com taxa de 3% ao mês, durante sete meses, gerando R$ 1.785,00 de juros. O valor do capital investido é igual a:"
        dic["m"] = "1785"
        dic["c"] = "?"
        dic["i"] = "0.03"
        dic["t"] = "7"
        dic["resposta"] = "8500"
    return dic

def list_id_simples():
    list = []
    for i in simples.find():
        list.append(ObjectId(i["_id"]))
    if len(list) < 1:
        cadastrar_simples("(Vunesp) Num balancete de uma empresa consta que certo capital foi aplicado a uma taxa de 30% ao ano durante 8 meses, rendendo juros simples no valor de R$ 192,00. O capital aplicado foi de:", "192", "?", "0.025", "8", "960")
        for i in simples.find():
            list.append(ObjectId(i["_id"]))
    return list

def list_id_compostos():
    list = []
    for i in compostos.find():
        list.append(ObjectId(i["_id"]))
    if len(list) < 1:
        cadastrar_composto("Um investidor aplicou um capital a juros simples com taxa de 3% ao mês, durante sete meses, gerando R$ 1.785,00 de juros. O valor do capital investido é igual a:", "1785", "?", "0.03", "7", "8500")
        for i in compostos.find():
            list.append(ObjectId(i["_id"]))
    return list

def redundancia(email):  # Verifica se o email que foi passado ja esta cadastrado
    for i in users.find():
        if i["email"] == email:
            return False
    return True

def save_user(data):  # salva os dados do usuário na tela de login
    users.insert_one(data)

def logar(email, senha):  # Retorna se o usuário esta cadastrado ou não
    for i in users.find():
        if i["email"] == email:
            if i["senha"] == senha:
                return True
    return False

def Peg_Pontos(email):  # Retorna os pontos do ususarios que esta logado
    User = users.find_one({"email": email})
    return User["pontos"]

def peg_user(email):  # Retorna o json do usuário
    User = users.find_one({"email": email})
    return User

def aumentar_pontos(quantidade, email):  # Aumenta a quantidade pontos nos dados do  usuário
    User = users.find_one({"email": email})
    pontos_novos = int(User["pontos"]) + int(quantidade)
    users.update_one(User, {"$set": {"pontos": pontos_novos}})

def diminuir_pontos(quantidade, email):  # Diminui a quantidade pontos nos dados do  usuário
    User = users.find_one({"email": email})
    pontos_novos = int(User["pontos"]) - int(quantidade)
    users.update_one(User, {"$set": {"pontos": pontos_novos}})

def cadastrar_simples(j, c, i, t, questao, resposta):
    Questao = {
    "questao": questao,
    "j": j.replace(",", "."),
    "c": c.replace(",", "."),
    "i": i.replace(",", "."),
    "t": t.replace(",", "."),
    "resposta": resposta.replace(",", ".")
}
    simples.insert_one(Questao)

def cadastrar_composto(m, c, i, t, questao, resposta):
    Questao = {
        "questao": questao,
        "m": m.replace(",", "."),
        "c": c.replace(",", "."),
        "i": i.replace(",", "."),
        "t": t.replace(",", "."),
        "resposta": resposta.replace(",", ".")
    }
    compostos.insert_one(Questao)

def delete_simples(id):
    questao = simples.find_one({"_id": ObjectId(id)})
    simples.delete_one(questao)

def delete_compostos(id):
    questao = compostos.find_one({"_id": ObjectId(id)})
    compostos.delete_one(questao)

class Login_Screen(Screen):
    def login(self):
        user.clear()
        self.email = self.ids.email.text
        self.senha = self.ids.senha.text
        if self.email != "" and self.senha != "":
            if logar(self.email, self.senha):
                user['email'] = self.email
                MDApp.get_running_app().root.current = "home"
                try:
                    self.ids.Login.remove_widget(self.menssagem)
                except:
                    pass
            else:
                try:
                    self.ids.Login.remove_widget(self.menssagem)
                except:
                    pass
                self.Aviso("Email ou senha inválido", "red")
        else:
            try:
                self.ids.Login.remove_widget(self.menssagem)
            except:
                pass
            self.Aviso("Por favor, preencha todos os campos", "red")

    def Aviso(self, Menssagem, color):
        self.menssagem = MDLabel(text=str(Menssagem),
                            font_style='Subtitle2',
                            halign='center',
                            pos_hint={'center_y': .3},
                            theme_text_color="Custom",
                            text_color=color)
        self.ids.Login.add_widget(self.menssagem)

class Register_Screen(Screen):
    def registrar(self):
        user.clear()
        self.nome = self.ids.nome.text
        self.email = self.ids.email.text
        self.senha = self.ids.senha.text
        self.confsenha = self.ids.conf_senha.text
        if self.nome != "" and self.email != "" and self.senha != "":
            if self.senha == self.confsenha:
                if redundancia(self.email):
                    save_user({"nome": self.nome, "email": self.email, "senha": self.senha, "pontos": 30})
                    user['email'] = self.email
                    MDApp.get_running_app().root.current = "home"
                    try:
                        self.ids.Registrar.remove_widget(self.menssagem)
                    except:
                        pass
                else:
                    try:
                        self.ids.Registrar.remove_widget(self.menssagem)
                    except:
                        pass
                    self.Aviso("Esse email ja existe!", "red")
            else:
                try:
                    self.ids.Registrar.remove_widget(self.menssagem)
                except:
                    pass
                self.Aviso("As senhas não estão iguais!", "red")
        else:
            try:
                self.ids.Registrar.remove_widget(self.menssagem)
            except:
                pass
            self.Aviso("Por favor, preencha todos os campos", "red")

    def Aviso(self, Menssagem, color):
        self.menssagem = MDLabel(text=str(Menssagem),
                            font_style='Subtitle2',
                            halign='center',
                            pos_hint={'center_y': .3},
                            theme_text_color="Custom",
                            text_color=color)
        self.ids.Registrar.add_widget(self.menssagem)

class Home_Screen(Screen):
    def pontos(self):
        try:
            self.email = user["email"]
        except:
            pass
        self.ponts = MDLabel(text=str(Peg_Pontos(self.email)),
                                font_style='H4',
                                pos_hint={'center_y': 2.55, 'center_x': 1.02},
                                theme_text_color="Custom",
                                text_color="#EE8F00",
                                font_size=50)
        self.ids.Pontos.add_widget(self.ponts)

    def mudar_icon(self):
        self.remove()
        self.ids.icon_olho.icon = "eye"

    def remove(self):
        try:
            self.ids.Pontos.remove_widget(self.ponts)
        except:
            pass

    def voltar_home(self):
        self.ids.tela_zerado.pos_hint = {'center_y': 10}

    def exercicio_simples(self):
        pontos = Peg_Pontos(user["email"])
        if pontos > 0:
            MDApp.get_running_app().root.current = "exercicio_simples"
        else:
            self.ids.tela_zerado.pos_hint = {'center_y': .5}

    def exercicio_composto(self):
        pontos = Peg_Pontos(user["email"])
        if pontos > 0:
            MDApp.get_running_app().root.current = "exercicio_composto"
        else:
            self.ids.tela_zerado.pos_hint = {'center_y': .5}

    def sair_lista(self):
        try:
            self.ids.lista.pos_hint = {"center_y": 10}
            self.ids.lista_users.remove_widget(self.scrow)
        except:
            pass

    def lista_simples(self):
        try:
            self.ids.lista_users.remove_widget(self.scrow)
        except:
            pass
        self.ids.lista.pos_hint = {"center_y": .5}

        self.lista_itens = []
        self.scrow = MDScrollView()
        self.list = MDList()

        for i in simples.find():
            self.items = OneLineAvatarIconListItem(IconRightWidget(id=str(ObjectId(i['_id'])), icon="trash-can-outline", on_release=lambda x: self.excluir_questao_simples(x.id)), id=str(ObjectId(i['_id'])), text=i['questao'], on_release=lambda x: self.dentro_questao_simples(x.id))
            self.lista_itens.append(self.items)
            self.list.add_widget(self.items)
        self.scrow.add_widget(self.list)
        self.ids.lista_users.add_widget(self.scrow)

    def deleta_e_atualiza_simples(self, id):
        delete_simples(id)
        self.lista_simples()
        self.dialog.dismiss(force=True)
        self.ids.exercicio_simp.pos_hint = {"center_y": 10}

    def deleta_e_atualiza_compostos(self, id):
        delete_compostos(id)
        self.lista_compostos()
        self.dialog.dismiss(force=True)
        self.ids.exercicio_comp.pos_hint = {"center_y": 10}

    def excluir_questao_simples(self, id):
        self.dialog = MDDialog(
            text="Tem certeza que deseja excluir esse usúario?",
            buttons=[
                MDFlatButton(
                    text="Não",
                    theme_text_color="Custom",
                    text_color="blue",
                    on_release=lambda x: self.dialog.dismiss(force=True)
                ),
                MDFlatButton(
                    text="Sim",
                    theme_text_color="Custom",
                    text_color="blue",
                    on_release=lambda x: self.deleta_e_atualiza_simples(id)
                )])
        self.dialog.open()

    def excluir_questao_compostos(self, id):
        self.dialog = MDDialog(
            text="Tem certeza que deseja excluir esse usúario?",
            buttons=[
                MDFlatButton(
                    text="Não",
                    theme_text_color="Custom",
                    text_color="blue",
                    on_release=lambda x: self.dialog.dismiss(force=True)
                ),
                MDFlatButton(
                    text="Sim",
                    theme_text_color="Custom",
                    text_color="blue",
                    on_release=lambda x: self.deleta_e_atualiza_compostos(id)
                )])
        self.dialog.open()

    def dentro_questao_simples(self, id):
        self.ids.exercicio_simp.pos_hint = {"center_y": .5}
        self.questao = simples.find_one({"_id": ObjectId(id)})
        self.ids.dentro_questao_simp.text = self.questao["questao"]
        self.ids.respostass.text = f'J = {self.questao["j"]}     C = {self.questao["c"]}     I = {self.questao["i"]}     T = {self.questao["t"]}\n\n Resposta = {self.questao["resposta"]}'

    def dentro_questao_compostos(self, id):
        self.ids.exercicio_comp.pos_hint = {"center_y": .5}
        self.questao = compostos.find_one({"_id": ObjectId(id)})
        self.ids.dentro_questao_comp.text = self.questao["questao"]
        self.ids.respostasc.text = f'M = {self.questao["m"]}     C = {self.questao["c"]}     I = {self.questao["i"]}     T = {self.questao["t"]}\n\n Resposta = {self.questao["resposta"]}'

    def sair_dentro_questao_simples(self):
        self.ids.exercicio_simp.pos_hint = {"center_y": 10}

    def sair_dentro_questao_compostos(self):
        self.ids.exercicio_comp.pos_hint = {"center_y": 10}

    def lista_compostos(self):
        try:
            self.ids.lista_users.remove_widget(self.scrow)
        except:
            pass
        self.ids.lista.pos_hint = {"center_y": .5}

        self.lista_itens = []
        self.scrow = MDScrollView()
        self.list = MDList()

        for i in compostos.find():
            self.items = OneLineAvatarIconListItem(IconRightWidget(id=str(ObjectId(i['_id'])), icon="trash-can-outline", on_release=lambda x: self.excluir_questao_compostos(x.id)), id=str(ObjectId(i['_id'])), text=i['questao'], on_release=lambda x: self.dentro_questao_compostos(x.id))
            self.lista_itens.append(self.items)
            self.list.add_widget(self.items)
        self.scrow.add_widget(self.list)
        self.ids.lista_users.add_widget(self.scrow)

class Estudar_Simples_Screen(Screen):
    pass

class Formula_Simples_Screen(Screen):
    def video(self):
        pontos = Peg_Pontos(user["email"])
        if int(pontos) == 0:
            aumentar_pontos(10, user["email"])
        site = 'https://www.youtube.com/watch?v=BWCiDbmaCxM&t=115s'
        webbrowser.open_new(site)

class Estudar_Compostos_Screen(Screen):
    pass

class Formula_Compostos_Screen(Screen):
    def video(self):
        site = 'https://www.youtube.com/watch?v=FUsi1-hwK60'
        webbrowser.open_new(site)

class Exercicio_Simples_Screen(Screen):
    def ger_exercicio(self):
        ids = list_id_simples()
        id_escolhido = random.choice(ids)
        self.ex_escolhido = peg_ex_simples(id_escolhido)
        return self.ex_escolhido

    def questao(self):
        exerc = self.ger_exercicio()
        self.ids.tela_questao.pos_hint = {'center_y': .5}
        self.ids.lbquestao.text = exerc["questao"]

    def voltar_cards(self):
        self.ids.tela_questao.pos_hint = {'center_y': 10}

    def responder(self):
        self.ids.responder_questao.pos_hint = {'center_y': .5}

    def voltar_questao(self):
        self.ids.tela_questao.pos_hint = {'center_y': .5}
        self.ids.responder_questao.pos_hint = {'center_y': 10}
        self.ids.valuej.text = ""
        self.ids.valuec.text = ""
        self.ids.valuei.text = ""
        self.ids.valuet.text = ""
        self.ids.valueresposta.text = ""

    def voltar_home(self):
        self.ids.responder_questao.pos_hint = {'center_y': 10}
        self.ids.tela_questao.pos_hint = {'center_y': 10}
        self.ids.tela_resposta.pos_hint = {'center_y': 10}
        self.ids.valuej.text = ""
        self.ids.valuec.text = ""
        self.ids.valuei.text = ""
        self.ids.valuet.text = ""
        self.ids.valueresposta.text = ""

    def resposta_certa(self, resposta):
        self.ids.cj.text = f'J = {resposta["j"]}'
        self.ids.cc.text = f'C = {resposta["c"]}'
        self.ids.ci.text = f'I = {resposta["i"]}'
        self.ids.ct.text = f'T = {resposta["t"]}'
        self.ids.cresposta.text = f'Resposta = {resposta["resposta"]}'
        self.ids.cj.color = 'green'
        self.ids.cc.color = 'green'
        self.ids.ci.color = 'green'
        self.ids.ct.color = 'green'
        self.ids.cresposta.color = 'green'

    def conferir_questao(self):
        j = self.ids.valuej.text.replace(",", ".")
        c = self.ids.valuec.text.replace(",", ".")
        i = self.ids.valuei.text.replace(",", ".")
        t = self.ids.valuet.text.replace(",", ".")
        resposta = self.ids.valueresposta.text.replace(",", ".")
        if j == self.ex_escolhido["j"] and c == self.ex_escolhido["c"] and i == self.ex_escolhido["i"] and t == \
                self.ex_escolhido["t"]:
            if resposta == self.ex_escolhido["resposta"]:
                aumentar_pontos(10, user["email"])
                self.resposta_certa(self.ex_escolhido)
                self.ids.parabens.text = f'Parabéns'
                self.ids.pontos.text = f'+10 Pontos'
                self.ids.sj.text = f'J = {j}'
                self.ids.sc.text = f'C = {c}'
                self.ids.si.text = f'I = {i}'
                self.ids.st.text = f'T = {t}'
                self.ids.sresposta.text = f'Resposta = {resposta}'
                self.ids.pontos.color = f'green'
                self.ids.sj.color = 'green'
                self.ids.sc.color = 'green'
                self.ids.si.color = 'green'
                self.ids.st.color = 'green'
                self.ids.sresposta.color = 'green'
            else:
                self.resposta_certa(self.ex_escolhido)
                self.ids.parabens.text = ''
                self.ids.pontos.text = '+5 Pontos'
                self.ids.sj.text = f'J = {j}'
                self.ids.sc.text = f'C = {c}'
                self.ids.si.text = f'I = {i}'
                self.ids.st.text = f'T = {t}'
                self.ids.sresposta.text = f'Resposta = {resposta}'
                self.ids.pontos.color = 'green'
                self.ids.sj.color = 'green'
                self.ids.sc.color = 'green'
                self.ids.si.color = 'green'
                self.ids.st.color = 'green'
                self.ids.sresposta.color = 'red'
                aumentar_pontos(5, user["email"])
        else:
            if resposta == self.ex_escolhido["resposta"]:
                self.resposta_certa(self.ex_escolhido)
                self.ids.parabens.text = ''
                self.ids.pontos.text = '+5 Pontos'
                self.ids.sj.text = f'J = {j}'
                self.ids.sc.text = f'C = {c}'
                self.ids.si.text = f'I = {i}'
                self.ids.st.text = f'T = {t}'
                self.ids.sresposta.text = f'Resposta = {resposta}'
                self.ids.pontos.color = 'green'
                if self.ex_escolhido["j"] == j:
                    self.ids.sj.color = 'green'
                else:
                    self.ids.sj.color = 'red'
                if self.ex_escolhido["c"] == c:
                    self.ids.sc.color = 'green'
                else:
                    self.ids.sc.color = 'red'
                if self.ex_escolhido["i"] == i:
                    self.ids.si.color = 'green'
                else:
                    self.ids.si.color = 'red'
                if self.ex_escolhido["t"] == t:
                    self.ids.st.color = 'green'
                else:
                    self.ids.st.color = 'red'
                self.ids.sresposta.color = 'green'
                aumentar_pontos(5, user["email"])
            else:
                self.resposta_certa(self.ex_escolhido)
                self.ids.parabens.text = ''
                self.ids.pontos.text = '-10 Pontos'
                self.ids.sj.text = f'J = {j}'
                self.ids.sc.text = f'C = {c}'
                self.ids.si.text = f'I = {i}'
                self.ids.st.text = f'T = {t}'
                self.ids.sresposta.text = f'Resposta = {resposta}'
                self.ids.pontos.color = 'red'
                if self.ex_escolhido["j"] == j:
                    self.ids.sj.color = 'green'
                else:
                    self.ids.sj.color = 'red'
                if self.ex_escolhido["c"] == c:
                    self.ids.sc.color = 'green'
                else:
                    self.ids.sc.color = 'red'
                if self.ex_escolhido["i"] == i:
                    self.ids.si.color = 'green'
                else:
                    self.ids.si.color = 'red'
                if self.ex_escolhido["t"] == t:
                    self.ids.st.color = 'green'
                else:
                    self.ids.st.color = 'red'
                self.ids.sresposta.color = 'red'
                diminuir_pontos(10, user["email"])
        self.voltar_home()
        self.ids.tela_resposta.pos_hint = {'center_y': .5}


class Exercicio_Composto_Screen(Screen):
    def ger_exercicio(self):
        ids = list_id_compostos()
        id_escolhido = random.choice(ids)
        self.ex_escolhido = peg_ex_composto(id_escolhido)
        return self.ex_escolhido

    def questao(self):
        exerc = self.ger_exercicio()
        self.ids.tela_questao.pos_hint = {'center_y': .5}
        self.ids.lbquestao.text = exerc["questao"]

    def voltar_cards(self):
        self.ids.tela_questao.pos_hint = {'center_y': 10}

    def responder(self):
        self.ids.responder_questao.pos_hint = {'center_y': .5}

    def voltar_questao(self):
        self.ids.tela_questao.pos_hint = {'center_y': .5}
        self.ids.responder_questao.pos_hint = {'center_y': 10}
        self.ids.valuem.text = ""
        self.ids.valuec.text = ""
        self.ids.valuei.text = ""
        self.ids.valuet.text = ""
        self.ids.valueresposta.text = ""

    def voltar_home(self):
        self.ids.responder_questao.pos_hint = {'center_y': 10}
        self.ids.tela_questao.pos_hint = {'center_y': 10}
        self.ids.tela_resposta.pos_hint = {'center_y': 10}
        self.ids.valuem.text = ""
        self.ids.valuec.text = ""
        self.ids.valuei.text = ""
        self.ids.valuet.text = ""
        self.ids.valueresposta.text = ""

    def resposta_certa(self, resposta):
        self.ids.cm.text = f'M = {resposta["m"]}'
        self.ids.cc.text = f'C = {resposta["c"]}'
        self.ids.ci.text = f'I = {resposta["i"]}'
        self.ids.ct.text = f'T = {resposta["t"]}'
        self.ids.cresposta.text = f'Resposta = {resposta["resposta"]}'
        self.ids.cm.color = 'green'
        self.ids.cc.color = 'green'
        self.ids.ci.color = 'green'
        self.ids.ct.color = 'green'
        self.ids.cresposta.color = 'green'

    def conferir_questao(self):
        m = self.ids.valuem.text.replace(",", ".")
        c = self.ids.valuec.text.replace(",", ".")
        i = self.ids.valuei.text.replace(",", ".")
        t = self.ids.valuet.text.replace(",", ".")
        resposta = self.ids.valueresposta.text.replace(",", ".")
        if m == self.ex_escolhido["m"] and c == self.ex_escolhido["c"] and i == self.ex_escolhido["i"] and t == \
                self.ex_escolhido["t"]:
            if resposta == self.ex_escolhido["resposta"]:
                aumentar_pontos(10, user["email"])
                self.resposta_certa(self.ex_escolhido)
                self.ids.parabens.text = f'Parabéns'
                self.ids.pontos.text = f'+10 Pontos'
                self.ids.sm.text = f'M = {m}'
                self.ids.sc.text = f'C = {c}'
                self.ids.si.text = f'I = {i}'
                self.ids.st.text = f'T = {t}'
                self.ids.sresposta.text = f'Resposta = {resposta}'
                self.ids.pontos.color = f'green'
                self.ids.sm.color = 'green'
                self.ids.sc.color = 'green'
                self.ids.si.color = 'green'
                self.ids.st.color = 'green'
                self.ids.sresposta.color = 'green'
            else:
                self.resposta_certa(self.ex_escolhido)
                self.ids.parabens.text = ''
                self.ids.pontos.text = '+5 Pontos'
                self.ids.sm.text = f'M = {m}'
                self.ids.sc.text = f'C = {c}'
                self.ids.si.text = f'I = {i}'
                self.ids.st.text = f'T = {t}'
                self.ids.sresposta.text = f'Resposta = {resposta}'
                self.ids.pontos.color = 'green'
                self.ids.sm.color = 'green'
                self.ids.sc.color = 'green'
                self.ids.si.color = 'green'
                self.ids.st.color = 'green'
                self.ids.sresposta.color = 'red'
                aumentar_pontos(5, user["email"])
        else:
            if resposta == self.ex_escolhido["resposta"]:
                self.resposta_certa(self.ex_escolhido)
                self.ids.parabens.text = ''
                self.ids.pontos.text = '+5 Pontos'
                self.ids.sm.text = f'M = {m}'
                self.ids.sc.text = f'C = {c}'
                self.ids.si.text = f'I = {i}'
                self.ids.st.text = f'T = {t}'
                self.ids.sresposta.text = f'Resposta = {resposta}'
                self.ids.pontos.color = 'green'
                if self.ex_escolhido["m"] == m:
                    self.ids.sm.color = 'green'
                else:
                    self.ids.sm.color = 'red'
                if self.ex_escolhido["c"] == c:
                    self.ids.sc.color = 'green'
                else:
                    self.ids.sc.color = 'red'
                if self.ex_escolhido["i"] == i:
                    self.ids.si.color = 'green'
                else:
                    self.ids.si.color = 'red'
                if self.ex_escolhido["t"] == t:
                    self.ids.st.color = 'green'
                else:
                    self.ids.st.color = 'red'
                self.ids.sresposta.color = 'green'
                aumentar_pontos(5, user["email"])
            else:
                self.resposta_certa(self.ex_escolhido)
                self.ids.parabens.text = ''
                self.ids.pontos.text = '-10 Pontos'
                self.ids.sm.text = f'M = {m}'
                self.ids.sc.text = f'C = {c}'
                self.ids.si.text = f'I = {i}'
                self.ids.st.text = f'T = {t}'
                self.ids.sresposta.text = f'Resposta = {resposta}'
                self.ids.pontos.color = 'red'
                if self.ex_escolhido["m"] == m:
                    self.ids.sj.color = 'green'
                else:
                    self.ids.sm.color = 'red'
                if self.ex_escolhido["c"] == c:
                    self.ids.sc.color = 'green'
                else:
                    self.ids.sc.color = 'red'
                if self.ex_escolhido["i"] == i:
                    self.ids.si.color = 'green'
                else:
                    self.ids.si.color = 'red'
                if self.ex_escolhido["t"] == t:
                    self.ids.st.color = 'green'
                else:
                    self.ids.st.color = 'red'
                self.ids.sresposta.color = 'red'
                diminuir_pontos(10, user["email"])
        self.voltar_home()
        self.ids.tela_resposta.pos_hint = {'center_y': .5}

class Cadastrar_Simples_Screen(Screen):
    def cadastrar(self):
        j = self.ids.valuej.text
        c = self.ids.valuec.text
        i = self.ids.valuei.text
        t = self.ids.valuet.text
        questao = self.ids.valuequestao.text
        resposta = self.ids.valueresposta.text
        cadastrar_simples(j, c, i, t, questao, resposta)
        self.ids.valuej.text = ""
        self.ids.valuec.text = ""
        self.ids.valuei.text = ""
        self.ids.valuet.text = ""
        self.ids.valuequestao.text = ""
        self.ids.valueresposta.text = ""

class Cadastrar_Composto_Screen(Screen):
    def cadastrar(self):
        m = self.ids.valuem.text
        c = self.ids.valuec.text
        i = self.ids.valuei.text
        t = self.ids.valuet.text
        questao = self.ids.valuequestao.text
        resposta = self.ids.valueresposta.text
        cadastrar_composto(m, c, i, t, questao, resposta)
        self.ids.valuem.text = ""
        self.ids.valuec.text = ""
        self.ids.valuei.text = ""
        self.ids.valuet.text = ""
        self.ids.valuequestao.text = ""
        self.ids.valueresposta.text = ""

class Screen_Manager(ScreenManager):
    pass

class Aplicativo_(MDApp):
    def build(self):
        Window.size = (1024, 720)
        self.title = 'Matics'
        self.theme_cls.primary_palette = 'Blue'
        return Builder.load_file("main.kv")

if __name__ == "__main__":
    Aplicativo_().run()