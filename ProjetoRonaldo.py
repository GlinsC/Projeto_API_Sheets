import customtkinter as ctk
import gspread
from tkinter import ttk
from oauth2client.service_account import ServiceAccountCredentials

# Tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Google Sheets
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
client = gspread.authorize(creds)

sheet = client.open_by_key("12xBpf804UtSdqLtjx1rRmE0WVcoQxrMrooAWoxqfFG8").sheet1

# Histórico em memória (zera ao fechar)
historico = []

# Função salvar
def salvar():
    nome = entry_nome.get()
    pagamento = combo_pagamento.get()

    try:
        valor = float(entry_valor.get().replace(",", "."))
    except ValueError:
        status_label.configure(text="Digite o valor corretamente!", text_color="red")
        return

    if nome and pagamento:
        # Salva no Google Sheets
        sheet.append_row([nome, valor, pagamento], value_input_option="USER_ENTERED")

        # Salva no histórico local
        historico.append((nome, valor, pagamento))

        # Atualiza tabela
        atualizar_tabela()

        status_label.configure(text="✅ Salvo com sucesso!", text_color="green")

        entry_nome.delete(0, 'end')
        entry_valor.delete(0, 'end')
        combo_pagamento.set("")
    else:
        status_label.configure(text="⚠️ Preencha todos os campos!", text_color="red")

# Atualiza tabela
def atualizar_tabela():
    for item in tabela.get_children():
        tabela.delete(item)

    for venda in historico:
        tabela.insert("", "end", values=venda)

# Interface
app = ctk.CTk()
app.title("Registro de Vendas")
app.geometry("800x500")

# Título
titulo = ctk.CTkLabel(app, text="Registro de Vendas Teste", font=("Arial", 20))
titulo.pack(pady=15)

# Inputs
entry_nome = ctk.CTkEntry(app, placeholder_text="Nome do vendedor")
entry_nome.pack(pady=10)

entry_valor = ctk.CTkEntry(app, placeholder_text="Valor da compra")
entry_valor.pack(pady=10)

combo_pagamento = ctk.CTkComboBox(app, values=["Pix", "Cartão Credito", "Cartão Débito", "Dinheiro"])
combo_pagamento.pack(pady=10)

btn_salvar = ctk.CTkButton(app, text="Salvar", command=salvar)
btn_salvar.pack(pady=15)

status_label = ctk.CTkLabel(app, text="")
status_label.pack(pady=10)

# Frame da tabela
frame_tabela = ctk.CTkFrame(app)
frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

# 🔥 Estilo do Treeview (dark)
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#2b2b2b",
                foreground="white",
                rowheight=25,
                fieldbackground="#2b2b2b",
                font=("Arial", 14),
                bordercolor="#343638",
                borderwidth=0)

style.map("Treeview",
          background=[("selected", "#1f6aa5")])

style.configure("Treeview.Heading",
                background="#1f1f1f",
                foreground="white",
                font=("Arial", 14),
                relief="flat")

# Tabela
tabela = ttk.Treeview(frame_tabela, columns=("Nome Vendedor", "Valor", "Pagamento"), show="headings")

tabela.heading("Nome Vendedor", text="Nome Vendedor")
tabela.heading("Valor", text="Valor")
tabela.heading("Pagamento", text="Pagamento")

tabela.column("Nome Vendedor", anchor="center")
tabela.column("Valor", anchor="center")
tabela.column("Pagamento", anchor="center")

tabela.pack(fill="both", expand=True)

app.mainloop()