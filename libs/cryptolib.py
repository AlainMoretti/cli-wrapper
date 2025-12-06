# Copyright 2016 Netfishers
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import os
import struct

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    iv = get_random_bytes(16)
    
    # Lire le fichier en mode binaire
    with open(in_filename, 'rb') as f:
        plaintext = f.read()
    
    # Padding PKCS7
    pad_len = 16 - (len(plaintext) % 16)
    plaintext += bytes([pad_len] * pad_len)
    
    # Créer le cipher avec IV en bytes (corrige l'erreur)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = encryptor.encrypt(plaintext)
    
    # Écrire IV + ciphertext dans le fichier .enc
    with open(in_filename + '.enc', 'wb') as f:
        f.write(iv + ciphertext)



def decrypt_file(key, enc_filename, out_filename):
    """Decrypt file avec détection automatique legacy/nouveau format"""
    with open(enc_filename, 'rb') as f:
        data = f.read()
    
    # Vérifier taille minimale
    if len(data) < 16:
        raise ValueError("Fichier trop court pour être valide")
    
    # Essayer d'abord le NOUVEAU format (IV 16 bytes + data multiple de 16)
    iv = data[:16]
    ciphertext = data[16:]
    
    if len(ciphertext) % 16 == 0:
        try:
            decryptor = AES.new(key, AES.MODE_CBC, iv)
            padded_plaintext = decryptor.decrypt(ciphertext)
            plaintext = unpad(padded_plaintext, AES.block_size)
            with open(out_filename, 'wb') as f:
                f.write(plaintext)
            print(f"Déchiffré NOUVEAU format: {len(plaintext)} bytes")
            return
        except ValueError:
            pass  # Pas le nouveau format, essayer legacy
    
    # LEGACY format (fichier tronqué ou sans padding correct)
    print("Détection legacy format (fichier ancien)...")
    iv = data[:16]
    ciphertext = data[16:]
    
    # Padding manuel pour legacy (remplir jusqu'au prochain multiple de 16)
    pad_len = 16 - (len(ciphertext) % 16)
    if pad_len != 16:  # Pas déjà multiple de 16
        ciphertext += b'\x00' * pad_len
    
    decryptor = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = decryptor.decrypt(ciphertext)
    
    # Nettoyer les zéros de padding legacy
    plaintext = padded_plaintext.rstrip(b'\x00')
    
    with open(out_filename, 'wb') as f:
        f.write(plaintext)
    print(f"Déchiffré LEGACY format: {len(plaintext)} bytes (padding nettoyé)")


# def decrypt_file_to_array(key, in_filename, chunksize=24*1024):
#     with open(in_filename, 'rb') as infile:
#         origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
#         iv = infile.read(16)
#         decryptor = AES.new(key, AES.MODE_CBC, iv)
#         out = ''
#         while True:
#             chunk = infile.read(chunksize)
#             if len(chunk) == 0:
#                 break
#             out += (decryptor.decrypt(chunk))
#     array_out = out.split('\n')
#     #remove leading and trailing unexpected characters
#     array_out = [i.strip() for i in array_out]
#     #array_out.pop()
#     return array_out

def decrypt_file_to_array(key, in_filename, chunksize=24*1024):
    """Déchiffre un fichier .enc et retourne un array de lignes (compatible legacy ET nouveau format)"""
    
    with open(in_filename, 'rb') as infile:
        data = infile.read()
    
    if len(data) < 16:
        raise ValueError("Fichier trop court pour être valide")
    
    # === FORMAT NOUVEAU (IV 16 bytes + ciphertext) ===
    iv = data[:16]
    ciphertext = data[16:]
    
    if len(ciphertext) % 16 == 0:
        try:
            decryptor = AES.new(key, AES.MODE_CBC, iv)
            padded_plaintext = decryptor.decrypt(ciphertext)
            plaintext = unpad(padded_plaintext, AES.block_size).decode('utf-8')
            
            # Split en lignes et nettoyage
            array_out = plaintext.split('\n')
            array_out = [i.strip() for i in array_out if i.strip()]  # Supprime lignes vides
            return array_out
            
        except (ValueError, UnicodeDecodeError):
            pass  # Pas le nouveau format
    
    # === FORMAT LEGACY (taille + IV + chunks) ===
    try:
        infile.seek(0)
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        
        out = b''
        while True:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break
            out += decryptor.decrypt(chunk)
        
        # Truncate to original size and decode
        plaintext = out[:origsize].decode('utf-8')
        array_out = plaintext.split('\n')
        array_out = [i.strip() for i in array_out if i.strip()]
        return array_out
        
    except (struct.error, UnicodeDecodeError):
        raise ValueError("Format de fichier non reconnu ou mot de passe incorrect")

