import numpy as np


alfabeto = 'abcdefghijklmnopqrstuvwxyz '
modulo = len(alfabeto)

#função para validar se a matriz usada como chave, é inversível no mod a ser usado
#Critérios necessários: Determinante não nulo e MDC entre o determinante e modulo deve ser 1
def chave_valida(matriz, modulo):
    #calcula e verifica se o determinante é não-nulo
    determinante = int(np.round(np.linalg.det(matriz)))
    if determinante == 0:
        return False, f'Determinente nulo, matriz não válida'
    mdc , x, y = euclidianoExtendido(determinante, modulo)
    if mdc != 1:
        return False, f'Determinante não é coprimo do módulo'
    
    return True, f'Matriz chave válida'

#mapenado cada letra do alfabeto a um número equivalente, entre 0 e 25
letras_indice = dict(zip(alfabeto, range(len(alfabeto))))
indice_letras = dict(zip(range(len(alfabeto)), alfabeto))

#pré-processamento da mensagem, retirando espaçoes e letras maiúsculas, e salvando onde estavam e traduzindo
#as letras para número, além de dividir a string no tamanho da chave 
def process_string(mensagem, chave):
    mensagem.lower()
    mensagem_num = []
    for caracter in mensagem:
        mensagem_num.append(letras_indice[caracter])
    #dando split na mensagem em números, para a que a multiplicação pela matriz chave possa ser feita 
    split = [mensagem_num[i:i+int(chave.shape[0])] for i in range (0, len(mensagem_num), int(chave.shape[0]))]
    return  split

#função que gera, a partir do texto 'traduzido' e dividido, a cifra
def encriptando (chave, split):
    cifra = ''
    for bloco in split:
        bloco = np.transpose(np.asarray(bloco))[:,np.newaxis] #corrigindo o formato do bloco transposto com [:,np.newaxis]
        #verificando se todos os 'blocos' estão preenchidos, se não adiciona um 'b' para completar
        while bloco.shape[0] != chave.shape[0]:
            bloco = np.append(bloco, letras_indice['b'])

        # Após o preenchimento, converta novamente o bloco para o formato correto
        bloco = np.reshape(bloco, (chave.shape[0], 1))

        numeros = np.dot(chave, bloco) % modulo

        n = numeros.shape[0]

        #mapeando so números já encriptados, de volta para texto
        for idc in range(n):
            numero = int(numeros[idc, 0])
            cifra += indice_letras[numero]

    return cifra

#----------------------FUNCIONANDO ATÉ AQUI-----------------------------------------------

#implementação do euclidiano extendido, a fim de determinar o mdc, e calcular a inversa
def euclidianoExtendido (a,b):
    resto = a%b if b>0 else a % -b
    quociente = a//b
    if resto ==0:
        return(b, 0 , 1)
    else:
        mdc,x,y = euclidianoExtendido(b, resto)
        return (mdc, y, x-quociente*y)
#calcucla o inverso modular de 'a' no mod especificado, utilizado para o cálculo da chave de descriptografia
def mod_inversa(a, mod):
    ecd, x, y = euclidianoExtendido(a, mod)
    if ecd != 1:
        raise ValueError(f"O número {a} não tem inverso no módulo {mod}")
    return x%mod


#função que gera a inversa da chave
def chave_inversa(chave):
    # Determinante da matriz
    determinante = int(np.round(np.linalg.det(chave)))  # Garantir que é inteiro
    det_inversa_modular = mod_inversa(determinante, modulo)  # Inverso modular do determinante
    
    # Matriz adjunta
    adjunta = np.round(determinante * np.linalg.inv(chave)).astype(int) % modulo
    
    # Inversa no módulo
    inversa_chave = (det_inversa_modular * adjunta) % modulo
    
    return inversa_chave



#função que descriptografa, a partir da cifra e da inversa da chave
def descriptando(cifra, inversa_chave, tamanho_original):
    # Passando a cifra de texto para números
    mensagem = ''
    cifra_num = [letras_indice[caracter] for caracter in cifra]
    
    # Dividindo a cifra em blocos
    split = [cifra_num[i:i+inversa_chave.shape[0]] for i in range(0, len(cifra_num), inversa_chave.shape[0])]
    
    # Descriptografando cada bloco
    for bloco in split:
        bloco = np.transpose(np.asarray(bloco))[:, np.newaxis]
        numeros = np.dot(inversa_chave, bloco) % modulo
        
        for numero in numeros.flatten():
            mensagem += indice_letras[int(numero)]
    
    # Remover caracteres extras adicionados no preenchimento
    return mensagem[:tamanho_original]


#função que restaura os espaços e letras maiúsculas

def main():
    chave = np.array([[3, 10, 20], [20, 19, 17], [23,78,17]])  # Matriz 3x3 que funciona com mod 27
    if (chave_valida(chave, modulo)):

        mensagem = 'ola mundo'

        # Processamento da mensagem
        tamanho_original = len(mensagem)
        split = process_string(mensagem, chave)

        # Encriptação
        mensagem_cifrada = encriptando(chave, split)
        print(f"Mensagem cifrada: {mensagem_cifrada}")

        # Cálculo da chave inversa
        chave_inv = chave_inversa(chave)

        # Descriptografia
        mensagem_descifrada = descriptando(mensagem_cifrada, chave_inv, tamanho_original)
        print(f"Mensagem descifrada: {mensagem_descifrada}")

main()
