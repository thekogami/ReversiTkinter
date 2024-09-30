import tkinter as tk
import random

# Variáveis globais
boardLength = 8
boardArray = [[0 for _ in range(boardLength)] for _ in range(boardLength)]
currentPlayer = 1  # 1 para jogador 1 (preto), -1 para jogador 2 (algoritmo branco)

# Função para inicializar o tabuleiro
def initialize_board():
    boardArray[3][3] = boardArray[4][4] = -1
    boardArray[3][4] = boardArray[4][3] = 1

# Função para atualizar o tabuleiro gráfico e o contador de peças
def update_board():
    black_count = 0
    white_count = 0
    for i in range(boardLength):
        for j in range(boardLength):
            if boardArray[i][j] == 1:
                buttons[i][j].config(bg='black')
                black_count += 1
            elif boardArray[i][j] == -1:
                buttons[i][j].config(bg='white')
                white_count += 1
            else:
                buttons[i][j].config(bg='green')
    
    # Atualiza os contadores de peças
    black_count_label.config(text=f'Peças Pretas: {black_count}')
    white_count_label.config(text=f'Peças Brancas: {white_count}')
    
    # Verifica se o jogo terminou
    if not get_valid_moves(1) and not get_valid_moves(-1):
        end_game(black_count, white_count)

# Função para verificar movimentos válidos
def is_valid_move(x, y, player):
    if boardArray[x][y] != 0:
        return False
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < boardLength and 0 <= ny < boardLength and boardArray[nx][ny] == -player:
            while 0 <= nx < boardLength and 0 <= ny < boardLength:
                if boardArray[nx][ny] == 0:
                    break
                if boardArray[nx][ny] == player:
                    return True
                nx += dx
                ny += dy
    return False

# Função para fazer um movimento
def make_move(x, y, player):
    boardArray[x][y] = player
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < boardLength and 0 <= ny < boardLength and boardArray[nx][ny] == -player:
            flip_positions = []
            while 0 <= nx < boardLength and 0 <= ny < boardLength:
                if boardArray[nx][ny] == 0:
                    break
                if boardArray[nx][ny] == player:
                    for px, py in flip_positions:
                        boardArray[px][py] = player
                    break
                flip_positions.append((nx, ny))
                nx += dx
                ny += dy

# Função para obter os movimentos válidos
def get_valid_moves(player):
    valid_moves = []
    for i in range(boardLength):
        for j in range(boardLength):
            if is_valid_move(i, j, player):
                valid_moves.append((i, j))
    return valid_moves

# Função para manipular o turno do jogador humano
def on_click(x, y):
    global currentPlayer
    if currentPlayer == 1:  # Movimento do jogador humano
        if is_valid_move(x, y, currentPlayer):
            make_move(x, y, currentPlayer)
            update_board()
            currentPlayer = -1  # Troca para o jogador 2 (algoritmo)
            root.after(1000, ai_move)  # Chama a jogada do algoritmo após 1 segundo

# Função para a jogada do algoritmo
def ai_move():
    global currentPlayer
    valid_moves = get_valid_moves(currentPlayer)
    if valid_moves:
        # Algoritmo simples que escolhe um movimento aleatório válido
        x, y = random.choice(valid_moves)
        make_move(x, y, currentPlayer)
        update_board()
        currentPlayer = 1  # Troca para o jogador humano

# Função para encerrar o jogo e mostrar o vencedor
def end_game(black_count, white_count):
    if black_count > white_count:
        winner = "Jogador 1 (Preto) venceu!"
    elif white_count > black_count:
        winner = "Jogador 2 (Branco) venceu!"
    else:
        winner = "Empate!"

    # Mostrar uma mensagem de vitória
    win_popup = tk.Toplevel(root)
    win_popup.title("Fim de Jogo!")
    win_label = tk.Label(win_popup, text=winner, font=("Arial", 18), padx=20, pady=20)
    win_label.pack()

    # Botão para fechar o jogo
    close_button = tk.Button(win_popup, text="Fechar", command=root.quit, font=("Arial", 12), padx=20, pady=10)
    close_button.pack()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Reversi/Othello")

# Obter a largura e altura da tela
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcula o tamanho de cada botão com base na tela e no tamanho do tabuleiro
button_width = screen_width // boardLength
button_height = screen_height // boardLength

# Criar botões e configurar o tabuleiro
buttons = [[None for _ in range(boardLength)] for _ in range(boardLength)]
for i in range(boardLength):
    for j in range(boardLength):
        button = tk.Button(root, width=button_width // 10, height=button_height // 20, bg='green', command=lambda i=i, j=j: on_click(i, j))
        button.grid(row=i, column=j, sticky='nsew')
        buttons[i][j] = button

# Adicionar rótulos para contagem de peças
black_count_label = tk.Label(root, text="Peças Pretas: 2", font=("Arial", 12))
black_count_label.grid(row=boardLength, column=0, columnspan=4, sticky='nsew')

white_count_label = tk.Label(root, text="Peças Brancas: 2", font=("Arial", 12))
white_count_label.grid(row=boardLength, column=4, columnspan=4, sticky='nsew')

# Ajustar o redimensionamento automático
for i in range(boardLength):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

initialize_board()
update_board()

# Iniciar o loop principal da interface gráfica
root.mainloop()
