import base64
import hashlib
import hmac
import json
import secrets
import sqlite3
import subprocess
import threading

from flask import (
    Flask,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

FLAG_SQLI = f"flag{{sqli_auth_bypass_{secrets.token_hex(4)}}}"
FLAG_AUTH = f"flag{{reset_token_previsivel_{secrets.token_hex(4)}}}"
FLAG_AUTZ = f"flag{{mass_assignment_cargo_{secrets.token_hex(4)}}}"
FLAG_XSS = f"flag{{stored_xss_chamado_{secrets.token_hex(4)}}}"
FLAG_JWT = f"flag{{jwt_alg_none_{secrets.token_hex(4)}}}"
FLAG_FINAL = f"flag{{command_injection_final_{secrets.token_hex(4)}}}"

with open("/tmp/flag_final.txt", "w", encoding="utf-8") as _f:
    _f.write(FLAG_FINAL + "\n")

RESET_SALT = "nexa2026"

JWT_SECRET = secrets.token_hex(32)

COLAB_USUARIO = "ana.souza"
COLAB_SENHA = "Colab@123"

DB_LOCK = threading.Lock()
conn = sqlite3.connect(":memory:", check_same_thread=False)
conn.row_factory = sqlite3.Row


def preparar_banco():
    with DB_LOCK:
        conn.execute(
            """
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                email TEXT,
                usuario TEXT,
                senha TEXT,
                cargo TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE chamados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                protocolo TEXT,
                assunto TEXT,
                descricao TEXT,
                criado_em TEXT
            )
            """
        )

        admin_senha = secrets.token_hex(8)
        conn.execute(
            "INSERT INTO usuarios (nome, email, usuario, senha, cargo) VALUES (?, ?, ?, ?, ?)",
            ("TI Administrador", "ti.admin@nexacorp.com.br", "ti_admin", admin_senha, "admin"),
        )
        conn.execute(
            "INSERT INTO usuarios (nome, email, usuario, senha, cargo) VALUES (?, ?, ?, ?, ?)",
            ("Ana Souza", "ana.souza@nexacorp.com.br", COLAB_USUARIO, COLAB_SENHA, "colaborador"),
        )
        conn.execute(
            "INSERT INTO usuarios (nome, email, usuario, senha, cargo) VALUES (?, ?, ?, ?, ?)",
            ("Diego Lima", "diego.lima@nexacorp.com.br", "diego.lima", "Colab@456", "colaborador"),
        )
        conn.commit()


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def b64url_decode(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


def gerar_token(payload: dict) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = b64url_encode(json.dumps(header).encode())
    payload_b64 = b64url_encode(json.dumps(payload).encode())
    assinatura = hmac.new(
        JWT_SECRET.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256
    ).digest()
    return f"{header_b64}.{payload_b64}.{b64url_encode(assinatura)}"


def decodificar_token_inseguro(token: str):
    try:
        header_b64, payload_b64, assinatura_b64 = token.split(".")
        header = json.loads(b64url_decode(header_b64))
        payload = json.loads(b64url_decode(payload_b64))
    except Exception:
        return None

    alg = str(header.get("alg", "")).strip().lower()
    if alg == "none":
        return payload

    esperado = hmac.new(
        JWT_SECRET.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256
    ).digest()
    if not hmac.compare_digest(b64url_encode(esperado), assinatura_b64):
        return None
    return payload


def admin_autenticado() -> bool:
    if session.get("cargo") == "admin":
        return True
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        payload = decodificar_token_inseguro(auth[7:])
        if payload and payload.get("cargo") == "admin":
            return True
    return False


@app.route("/")
def index():
    return render_template("index.html", usuario=session.get("nome"), cargo=session.get("cargo"))


@app.route("/api/docs")
def api_docs():
    return jsonify(
        {
            "versao": "2.1.0",
            "endpoints": [
                {"rota": "/api/token", "metodo": "POST", "corpo": ["usuario", "senha"]},
                {"rota": "/api/perfil-jwt", "metodo": "GET", "auth": "Bearer"},
                {"rota": "/api/perfil", "metodo": "POST", "auth": "sessao"},
                {"rota": "/admin/diagnostico", "metodo": "GET/POST", "auth": "sessao admin ou Bearer admin"},
            ],
        }
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    flag = None
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        senha = request.form.get("senha", "")

        sql = (
            "SELECT id, nome, cargo, senha FROM usuarios WHERE usuario = '"
            + usuario
            + "' AND senha = '"
            + senha
            + "' LIMIT 1"
        )
        linha = None
        try:
            with DB_LOCK:
                linha = conn.execute(sql).fetchone()
        except sqlite3.Error as exc:
            erro = str(exc)

        if linha:
            session["user_id"] = linha["id"]
            session["nome"] = linha["nome"]
            session["cargo"] = linha["cargo"]

            if linha["cargo"] == "admin" and senha != linha["senha"]:
                flag = FLAG_SQLI

            destino = "painel_admin" if linha["cargo"] == "admin" else "index"
            if flag:
                return render_template("login.html", erro=None, flag=flag, destino=url_for(destino))
            return redirect(url_for(destino))

        if erro is None:
            erro = "Usuario ou senha invalidos."

    return render_template("login.html", erro=erro, flag=None, destino=None)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/painel-admin")
def painel_admin():
    if session.get("cargo") != "admin":
        return redirect(url_for("login"))
    return render_template("painel_admin.html", nome=session.get("nome"))


@app.route("/recuperar-senha", methods=["GET", "POST"])
def recuperar_senha():
    mensagem = None
    if request.method == "POST":
        mensagem = (
            "Se o email informado existir em nossa base, enviamos instrucoes "
            "de redefinicao para a caixa de entrada."
        )
    return render_template("recuperar_senha.html", mensagem=mensagem)


@app.route("/recuperar-senha/confirmar", methods=["GET", "POST"])
def recuperar_confirmar():
    resultado = None
    erro = None
    user_id = request.args.get("user_id", "") or request.form.get("user_id", "")
    token = request.args.get("token", "") or request.form.get("token", "")

    if request.method == "POST":
        nova_senha = request.form.get("nova_senha", "")

        if not user_id or not token or not nova_senha:
            erro = "Preencha todos os campos."
        else:
            try:
                uid = int(user_id)
            except ValueError:
                uid = None

            if uid is None:
                erro = "ID de usuario invalido."
            else:
                esperado = hashlib.md5(f"{uid}{RESET_SALT}".encode()).hexdigest()
                if hmac.compare_digest(esperado, token):
                    with DB_LOCK:
                        linha = conn.execute(
                            "SELECT cargo FROM usuarios WHERE id = ?", (uid,)
                        ).fetchone()
                        if linha:
                            conn.execute(
                                "UPDATE usuarios SET senha = ? WHERE id = ?", (nova_senha, uid)
                            )
                            conn.commit()
                            resultado = "Senha redefinida com sucesso. Voce ja pode fazer login."
                            if linha["cargo"] == "admin":
                                resultado += f" FLAG: {FLAG_AUTH}"
                        else:
                            erro = "Usuario nao encontrado."
                else:
                    erro = "Token invalido ou expirado."

    return render_template(
        "recuperar_confirmar.html",
        user_id=user_id,
        token=token,
        resultado=resultado,
        erro=erro,
    )


@app.route("/api/perfil", methods=["GET", "POST"])
def api_perfil():
    if "user_id" not in session:
        return jsonify({"erro": "autenticacao necessaria"}), 401

    uid = session["user_id"]

    if request.method == "GET":
        with DB_LOCK:
            linha = conn.execute(
                "SELECT nome, email, usuario, cargo FROM usuarios WHERE id = ?", (uid,)
            ).fetchone()
        return jsonify(dict(linha))

    dados = request.get_json(silent=True) or {}
    if not dados:
        return jsonify({"erro": "corpo JSON esperado"}), 400

    with DB_LOCK:
        antes = conn.execute("SELECT cargo FROM usuarios WHERE id = ?", (uid,)).fetchone()

        campos_validos = {"nome", "email", "usuario", "cargo"}
        atualizacoes = {k: v for k, v in dados.items() if k in campos_validos}
        if not atualizacoes:
            return jsonify({"erro": "nenhum campo valido enviado"}), 400

        set_clause = ", ".join(f"{campo} = ?" for campo in atualizacoes)
        valores = list(atualizacoes.values()) + [uid]
        conn.execute(f"UPDATE usuarios SET {set_clause} WHERE id = ?", valores)
        conn.commit()

        depois = conn.execute("SELECT cargo FROM usuarios WHERE id = ?", (uid,)).fetchone()

    resposta = {"ok": True, "cargo_atual": depois["cargo"]}
    if antes["cargo"] != "admin" and depois["cargo"] == "admin":
        session["cargo"] = "admin"
        resposta["flag"] = FLAG_AUTZ
    return jsonify(resposta)


@app.route("/chamados/novo", methods=["GET", "POST"])
def chamados_novo():
    protocolo = None
    if request.method == "POST":
        assunto = request.form.get("assunto", "")
        descricao = request.form.get("descricao", "")
        protocolo = secrets.token_hex(4)
        with DB_LOCK:
            conn.execute(
                "INSERT INTO chamados (protocolo, assunto, descricao, criado_em) "
                "VALUES (?, ?, ?, datetime('now'))",
                (protocolo, assunto, descricao),
            )
            conn.commit()
    return render_template("chamados_novo.html", protocolo=protocolo)


@app.route("/chamados/<protocolo>")
def chamados_detalhe(protocolo):
    with DB_LOCK:
        chamado = conn.execute(
            "SELECT * FROM chamados WHERE protocolo = ?", (protocolo,)
        ).fetchone()
    if chamado is None:
        return render_template("chamados_nao_encontrado.html", protocolo=protocolo), 404

    resposta = make_response(render_template("chamados_detalhe.html", chamado=chamado))
    resposta.set_cookie("flag_xss", FLAG_XSS, path="/chamados", httponly=False)
    return resposta


@app.route("/api/token", methods=["POST"])
def api_token():
    dados = request.get_json(silent=True) or request.form
    usuario = dados.get("usuario", "")
    senha = dados.get("senha", "")

    with DB_LOCK:
        linha = conn.execute(
            "SELECT cargo FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha)
        ).fetchone()

    if not linha:
        return jsonify({"erro": "credenciais invalidas"}), 401

    token = gerar_token({"sub": usuario, "cargo": linha["cargo"]})
    return jsonify({"token": token})


@app.route("/api/perfil-jwt")
def api_perfil_jwt():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"erro": "header Authorization: Bearer <token> obrigatorio"}), 401

    payload = decodificar_token_inseguro(auth[7:])
    if payload is None:
        return jsonify({"erro": "token invalido"}), 401

    resposta = {"sub": payload.get("sub"), "cargo": payload.get("cargo")}
    if payload.get("cargo") == "admin":
        resposta["flag"] = FLAG_JWT
    return jsonify(resposta)


@app.route("/admin/diagnostico", methods=["GET", "POST"])
def admin_diagnostico():
    if not admin_autenticado():
        return redirect(url_for("login"))

    saida = None
    host = ""
    if request.method == "POST":
        host = request.form.get("host", "")
        try:
            resultado = subprocess.run(
                f"ping -c 1 {host}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            saida = (resultado.stdout or "") + (resultado.stderr or "")
        except Exception as exc:
            saida = f"erro ao executar diagnostico: {exc}"

    return render_template("diagnostico.html", host=host, saida=saida)


if __name__ == "__main__":
    preparar_banco()
    app.run(host="0.0.0.0", port=80, threaded=False)
