"""Define (ou troca) a senha do swipe.ezeos.com.br.

Uso, no terminal: python ezeOS/swipe/definir-senha.py
A senha é digitada escondida e nunca é gravada: só o código (hash APR1, o
formato do Apache) vai pro ezeOS/swipe/.htpasswd, que fica fora do git.
Depois é só subir o .htpasswd pro servidor (a skill /swipe faz isso).
"""
import getpass
import hashlib
import secrets
from pathlib import Path

AQUI = Path(__file__).resolve().parent
USUARIO = "eze"
ITOA64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def apr1(senha: str, sal: str) -> str:
    """Hash $apr1$ (MD5 do Apache), igual ao do htpasswd -m."""
    s, p, magic = sal.encode(), senha.encode(), b"$apr1$"
    final = hashlib.md5(p + s + p).digest()
    ctx = p + magic + s
    for i in range(len(p), 0, -16):
        ctx += final[: min(16, i)]
    i = len(p)
    while i:
        ctx += b"\x00" if i & 1 else p[:1]
        i >>= 1
    final = hashlib.md5(ctx).digest()
    for i in range(1000):
        c = (p if i & 1 else final)
        if i % 3:
            c += s
        if i % 7:
            c += p
        c += final if i & 1 else p
        final = hashlib.md5(c).digest()

    def to64(v, n):
        out = ""
        for _ in range(n):
            out += ITOA64[v & 0x3F]
            v >>= 6
        return out

    f = final
    texto = (
        to64((f[0] << 16) | (f[6] << 8) | f[12], 4)
        + to64((f[1] << 16) | (f[7] << 8) | f[13], 4)
        + to64((f[2] << 16) | (f[8] << 8) | f[14], 4)
        + to64((f[3] << 16) | (f[9] << 8) | f[15], 4)
        + to64((f[4] << 16) | (f[10] << 8) | f[5], 4)
        + to64(f[11], 2)
    )
    return f"$apr1${sal}${texto}"


def main():
    senha = getpass.getpass(f"Senha nova do swipe (usuário {USUARIO}): ")
    if len(senha) < 8:
        raise SystemExit("Use pelo menos 8 caracteres.")
    if getpass.getpass("Repete a senha: ") != senha:
        raise SystemExit("As senhas não batem. Nada foi gravado.")
    sal = "".join(secrets.choice(ITOA64) for _ in range(8))
    (AQUI / ".htpasswd").write_text(f"{USUARIO}:{apr1(senha, sal)}\n", encoding="utf-8")
    print(f"Pronto. Usuário {USUARIO}, senha gravada em código no ezeOS/swipe/.htpasswd.")
    print("Agora me avisa que eu subo pro servidor.")


if __name__ == "__main__":
    main()
