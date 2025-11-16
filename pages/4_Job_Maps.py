# ==========================================================
# FULLSCREEN FINAL — BOTÕES ABAIXO DA TABELA E FUNCIONAIS
# ==========================================================

if "fs" not in st.session_state:
    st.session_state.fs = False

# Render tabela SEM botões ainda
st.markdown(content, unsafe_allow_html=True)

# Agora sim renderizamos o botão ABAIXO DA TABELA
button_area = st.container()

# ----------------------------------------------------------
# BOTÃO TELA CHEIA
# ----------------------------------------------------------
if not st.session_state.fs:

    with button_area:
        st.markdown("""
        <div class='button-wrapper'>
            <button class='full-btn' id='enter-btn'>Tela Cheia</button>
        </div>
        <script>
            document.getElementById("enter-btn").onclick = function() {
                fetch("/_toggle_fs?mode=enter").then(() => window.parent.location.reload());
            }
        </script>
        """, unsafe_allow_html=True)

else:

    # FULLSCREEN WRAPPER
    st.markdown("<div class='fullscreen-container'>", unsafe_allow_html=True)
    st.markdown(content, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    with button_area:
        st.markdown("""
        <div class='button-wrapper'>
            <button class='full-btn' id='exit-btn'>Sair</button>
        </div>
        <script>
            document.getElementById("exit-btn").onclick = function() {
                fetch("/_toggle_fs?mode=exit").then(() => window.parent.location.reload());
            }
        </script>
        """, unsafe_allow_html=True)

# ----------------------------------------------------------
# ENDPOINT SECRETO STREAMLIT
# ----------------------------------------------------------
from streamlit.web.server.websocket_headers import _set_websocket_response_headers
from streamlit.web.server import Server

def toggle_fs_handler(request):
    mode = request.query_params.get("mode", "")

    if mode == "enter":
        st.session_state.fs = True
    if mode == "exit":
        st.session_state.fs = False

    return {"status": "ok"}

# Registrar endpoint se ainda não existe
srv = Server.get_current()
if "_toggle_fs" not in srv._endpoint_registry:
    srv.add_endpoint("/_toggle_fs", toggle_fs_handler)
