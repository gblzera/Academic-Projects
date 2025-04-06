import tkinter as tk
from tkinter import messagebox
import time
import threading
import pygame
import os
import csv
from datetime import datetime

# Caminhos
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_MUSICA = os.path.join(DIRETORIO_ATUAL, "assets", "musica.mp3")
ARQUIVO_HISTORICO = os.path.join(DIRETORIO_ATUAL, "historico_estudos.csv")

pygame.mixer.init()

# Globais
tempo_restante = 0
cronometro_ativo = False
pausado = False
inicio_sessao = None
topico_estudo = ""

def tocar_musica():
    try:
        pygame.mixer.music.stop()  # Impede sobreposição
        pygame.mixer.music.load(CAMINHO_MUSICA)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Erro ao tocar música: {e}")

def salvar_no_historico(topico, duracao_segundos):
    duracao_min = round(duracao_segundos / 60, 2)
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    novo_registro = [agora, topico, f"{duracao_min} minutos"]

    escrever_cabecalho = not os.path.exists(ARQUIVO_HISTORICO)

    with open(ARQUIVO_HISTORICO, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if escrever_cabecalho:
            writer.writerow(["Data/Hora", "Tópico", "Duração"])
        writer.writerow(novo_registro)

def abrir_historico():
    if not os.path.exists(ARQUIVO_HISTORICO):
        messagebox.showinfo("Histórico vazio", "Nenhum estudo registrado ainda.")
        return

    janela_hist = tk.Toplevel(janela)
    janela_hist.title("Histórico de Estudos")
    janela_hist.configure(bg="black")
    janela_hist.geometry("550x300")

    # Centralizar a janela na tela
    janela_hist.update_idletasks()
    largura = janela_hist.winfo_width()
    altura = janela_hist.winfo_height()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela_hist.geometry(f"{largura}x{altura}+{x}+{y}")

    tk.Label(janela_hist, text="Histórico de Estudos", font=("Helvetica", 16, "bold"), bg="black", fg="white").pack(pady=10)

    frame_tabela = tk.Frame(janela_hist, bg="black")
    frame_tabela.pack(fill=tk.BOTH, expand=True)

    # Cabeçalho
    cabecalhos = ["Data/Hora", "Tópico", "Duração"]
    for i, cabecalho in enumerate(cabecalhos):
        tk.Label(frame_tabela, text=cabecalho, font=("Helvetica", 12, "bold"), bg="gray20", fg="white", borderwidth=1, relief="solid", padx=10, pady=5).grid(row=0, column=i, sticky="nsew")

    # Carrega dados
    with open(ARQUIVO_HISTORICO, newline='', encoding="utf-8") as f:
        leitor = csv.reader(f)
        next(leitor)  # pula cabeçalho
        for linha_idx, linha in enumerate(leitor, start=1):
            for col_idx, valor in enumerate(linha):
                tk.Label(frame_tabela, text=valor, font=("Helvetica", 10), bg="black", fg="white", borderwidth=1, relief="solid", padx=8, pady=4).grid(row=linha_idx, column=col_idx, sticky="nsew")

    for i in range(3):
        frame_tabela.grid_columnconfigure(i, weight=1)

def atualizar_tempo():
    global tempo_restante, cronometro_ativo, pausado, inicio_sessao
    while tempo_restante > 0 and cronometro_ativo:
        if not pausado:
            tempo_restante -= 1
            minutos, segundos = divmod(tempo_restante, 60)
            label_tempo.config(text=f"{minutos:02}:{segundos:02}")
        time.sleep(1)
    if tempo_restante == 0 and cronometro_ativo:
        cronometro_ativo = False
        tocar_musica()
        messagebox.showinfo("Tempo finalizado", "Boa! Sessão de estudo encerrada.")
        duracao_total = int(time.time() - inicio_sessao)
        salvar_no_historico(topico_estudo, duracao_total)

def iniciar_cronometro():
    global tempo_restante, cronometro_ativo, pausado, inicio_sessao, topico_estudo
    if cronometro_ativo:
        return
    try:
        tempo_em_minutos = int(entry_tempo.get())
        topico = entry_topico.get()
        if not topico or topico.strip() == "" or topico == "O que vai estudar?":
            messagebox.showwarning("Campo vazio", "Por favor, digite o que vai estudar.")
            return

        topico_estudo = topico
        tempo_restante = tempo_em_minutos * 60
        inicio_sessao = time.time()
        cronometro_ativo = True
        pausado = False
        thread = threading.Thread(target=atualizar_tempo)
        thread.daemon = True
        thread.start()
    except ValueError:
        messagebox.showerror("Erro", "Insira um número válido de minutos.")

def pausar_cronometro():
    global pausado
    pausado = not pausado
    botao_pausar.config(text="Retomar" if pausado else "Pausar")

def limpar_placeholder(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg="white")

def colocar_placeholder(event, entry, placeholder):
    if not entry.get():
        entry.insert(0, placeholder)
        entry.config(fg="gray")

# Janela principal
janela = tk.Tk()
janela.title("Cronômetro Flip Clock com Histórico")
janela.configure(bg="black")
janela.geometry("500x380")

# Label digital com fonte personalizada
try:
    label_tempo = tk.Label(janela, text="00:00", font=("DS-Digital", 72, "bold"), fg="white", bg="black")
except tk.TclError:
    label_tempo = tk.Label(janela, text="00:00", font=("Courier", 72, "bold"), fg="white", bg="black")
label_tempo.pack(pady=20)

# Entry: o que estudar
entry_topico = tk.Entry(janela, font=("Helvetica", 14), justify='center', fg="gray", bg="#111")
entry_topico.insert(0, "O que vai estudar?")
entry_topico.bind("<FocusIn>", lambda e: limpar_placeholder(e, entry_topico, "O que vai estudar?"))
entry_topico.bind("<FocusOut>", lambda e: colocar_placeholder(e, entry_topico, "O que vai estudar?"))
entry_topico.pack(pady=5)

# Entry: tempo
entry_tempo = tk.Entry(janela, font=("Helvetica", 14), justify='center', fg="gray", bg="#111")
entry_tempo.insert(0, "Minutos")
entry_tempo.bind("<FocusIn>", lambda e: limpar_placeholder(e, entry_tempo, "Minutos"))
entry_tempo.bind("<FocusOut>", lambda e: colocar_placeholder(e, entry_tempo, "Minutos"))
entry_tempo.pack(pady=5)

# Botões
frame_botoes = tk.Frame(janela, bg="black")
frame_botoes.pack(pady=20)

botao_iniciar = tk.Button(frame_botoes, text="Iniciar", font=("Helvetica", 12, "bold"), bg="#2ecc71", fg="white", command=iniciar_cronometro)
botao_iniciar.pack(side=tk.LEFT, padx=10)

botao_pausar = tk.Button(frame_botoes, text="Pausar", font=("Helvetica", 12, "bold"), bg="#f39c12", fg="black", command=pausar_cronometro)
botao_pausar.pack(side=tk.LEFT, padx=10)

botao_historico = tk.Button(janela, text="Ver Histórico de Estudos", font=("Helvetica", 12, "bold"), bg="#3498db", fg="white", command=abrir_historico)
botao_historico.pack(pady=10)

# Start
janela.mainloop()
