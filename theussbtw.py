import os
import sys
import argparse
import getpass
from pathlib import Path
from cryptography.fernet import Fernet #testando o fernet


class Encryptor:
    def __init__(self, key_file):
        self.key_file = key_file
        self.cipher = None
    
    def key_exists(self):
        return os.path.exists(self.key_file)
    
    def load_key(self):
        if not self.key_exists():
            print(f"Erro: chave nao encontrada em '{self.key_file}'")
            print("Gere uma chave primeiro: python encryptor.py -g")
            return False
        
        try:
            with open(self.key_file, "rb") as f:
                key = f.read()
            self.cipher = Fernet(key)
            return True
        except Exception as e:
            print(f"Erro ao carregar chave: {e}")
            return False
    
    def generate_key(self):
        if self.key_exists():
            print(f"Erro: chave ja existe em '{self.key_file}'")
            return False
        
        try:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            print(f"Chave gerada com sucesso: {self.key_file}")
            return True
        except Exception as e:
            print(f"Erro ao gerar chave: {e}")
            return False
    
    def verify_key(self):
        while True:
            key_input = getpass.getpass("Digite a chave: ")
            
            try:
                with open(self.key_file, "rb") as f:
                    stored_key = f.read()
                
                if key_input.encode() == stored_key:
                    return True
                
                print("Erro: chave incorreta. Tente novamente.")
            except Exception:
                print("Erro: chave incorreta. Tente novamente.")
    
    def encrypt_file(self, input_path, output_path=None):
        if not os.path.exists(input_path):
            print(f"Erro: arquivo '{input_path}' nao encontrado")
            return False
        
        if not self.cipher:
            print("Erro: chave nao carregada")
            return False
        
        output = output_path or f"{input_path}.enc"
        
        try:
            with open(input_path, "rb") as f:
                data = f.read()
            
            encrypted = self.cipher.encrypt(data)
            
            with open(output, "wb") as f:
                f.write(encrypted)
            
            print(f"Encriptado: {output} ({len(data)} -> {len(encrypted)} bytes)")
            
            os.remove(input_path)
            print(f"Original deletado: {input_path}")
            
            return True
        except Exception as e:
            print(f"Erro ao encriptar: {e}")
            return False
    
    def decrypt_file(self, input_path, output_path=None):
        if not os.path.exists(input_path):
            print(f"Erro: arquivo '{input_path}' nao encontrado")
            return False
        
        if not self.cipher:
            print("Erro: chave nao carregada")
            return False
        
        output = output_path or input_path.rstrip('.enc')
        
        try:
            with open(input_path, "rb") as f:
                encrypted = f.read()
            
            data = self.cipher.decrypt(encrypted)
            
            with open(output, "wb") as f:
                f.write(data)
            
            print(f"Decriptado: {output} ({len(encrypted)} -> {len(data)} bytes)")
            
            os.remove(input_path)
            print(f"Arquivo encriptado deletado: {input_path}")
            
            return True
        except Exception as e:
            print(f"Erro ao decriptar: {e}")
            return False
    
    def process_directory(self, directory, decrypt=False, recursive=True):
        if not os.path.isdir(directory):
            print(f"Erro: '{directory}' nao eh um diretorio valido")
            return
        
        success = 0
        pattern = "**/*.enc" if decrypt else "**/*" if recursive else "*"
        
        for file_path in Path(directory).glob(pattern):
            if not file_path.is_file():
                continue
            
            if file_path.name.endswith(".enc") and not decrypt:
                continue
            
            if file_path.name == self.key_file:
                continue
            
            print(f"Processando: {file_path}")
            
            if decrypt:
                success += self.decrypt_file(str(file_path))
            else:
                success += self.encrypt_file(str(file_path))
        
        print(f"Resumo: {success} sucesso(s)")


def main():
    parser = argparse.ArgumentParser(
        description="Encriptador & Decriptador de arquivos | @Theussbtw"
    )
    
    parser.add_argument("-e", "--encrypt", type=str, help="Arquivo ou diretorio para encriptar")
    parser.add_argument("-d", "--decrypt", type=str, help="Arquivo ou diretorio para decriptar")
    parser.add_argument("-o", "--output", type=str, help="Arquivo de saida")
    parser.add_argument("-k", "--key", type=str, default="encryption.key", help="Arquivo de chave")
    parser.add_argument("-r", "--recursive", action="store_true", help="Processamento recursivo")
    parser.add_argument("-g", "--generate-key", action="store_true", help="Gerar chave")
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    encryptor = Encryptor(args.key)
    
    if args.generate_key:
        encryptor.generate_key()
        return
    
    if args.encrypt:
        if not encryptor.key_exists():
            print(f"Erro: chave nao encontrada em '{args.key}'")
            print("Gere uma chave primeiro: python encryptor.py -g")
            return
        
        if not encryptor.load_key():
            return
        
        if not encryptor.verify_key():
            print("Acesso negado")
            return
        
        path = args.encrypt
        if os.path.isdir(path):
            encryptor.process_directory(path, decrypt=False, recursive=args.recursive)
        else:
            encryptor.encrypt_file(path, args.output)
    
    elif args.decrypt:
        if not encryptor.key_exists():
            print(f"Erro: chave nao encontrada em '{args.key}'")
            print("Gere uma chave primeiro: python encryptor.py -g")
            return
        
        if not encryptor.load_key():
            return
        
        if not encryptor.verify_key():
            print("Acesso negado")
            return
        
        path = args.decrypt
        if os.path.isdir(path):
            encryptor.process_directory(path, decrypt=True, recursive=args.recursive)
        else:
            encryptor.decrypt_file(path, args.output)


if __name__ == "__main__":
    main()
