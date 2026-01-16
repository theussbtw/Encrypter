Um Encriptador & Descriptografador de arquivos, feito por mim em Python apenas para estudos. Em breve será reescrito em Rust.

# Requisitos & Dependencias
- Python
- pip install cryptography

# ARGUMENTOS

-e, --encrypt     Arquivo ou diretorio para encriptar
-d, --decrypt     Arquivo ou diretorio para decriptar
-o, --output      Arquivo de saida (opcional)
-k, --key         Arquivo de chave (padrao: encryption.key)
-r, --recursive   Processamento recursivo em diretorios
-g, --generate-key Gerar nova chave

# EXEMPLOS

Linux/Mac
python3 theussbtw.py -g
python3 theussbtw.py -e documento.pdf
python3 theussbtw.py -d documento.pdf.enc
python3 theussbtw.py -e /home/usuario/backup -r

# Windows
python theussbtw.py -g
python theussbtw.py -e documento.pdf
python theussbtw.py -d documento.pdf.enc
python theussbtw.py -e C:\Users\usuario\Documents -r

# FLUXO DE FUNCIONAMENTO

Encriptacao
1. Verifica se a chave existe
2. Solicita a chave (senha)
3. Valida a chave
4. Encripta o arquivo usando Fernet (AES-128)
5. Salva com extensao .enc
6. Deleta o arquivo original

Decriptacao
1. Verifica se a chave existe
2. Solicita a chave (senha)
3. Valida a chave
4. Decripta o arquivo usando Fernet
5. Salva com nome original (sem .enc)
6. Deleta o arquivo .enc

# SEGURANCA

- Usa criptografia simetrica Fernet (AES-128 em modo CBC)
- Autenticacao HMAC integrada
- Chave deve ser guardada com seguranca
- NUNCA compartilhe o arquivo encryption.key
- A chave e pedida a cada operaçao (encriptacao/decriptacao)

# TIPOS DE ARQUIVO SUPORTADOS

Funciona com qualquer tipo de arquivo:
- Texto: .txt, .md, .json, .xml
- Compactados: .zip, .rar, .7z, .tar.gz
- Documentos: .pdf, .docx, .xlsx
- Midia: .jpg, .png, .mp4, .mp3
- Executaveis: .exe, .sh, .app


Contribuicoes sao bem-vindas!!