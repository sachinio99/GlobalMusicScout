from fastapi.testclient import TestClient
from fastapi import FastAPI

from .main import app  

#access_token = "BQDRx1ohl64TA5XFKXndHKeGOn0_o4pliK11Jdv3LlLGlcnlBJkWc_pWGi89BpFq2YS4Y6khqOlt_ej8L5R8MNnUAPEkJRe1GKWGIIo8Jb5KKVY0_d9sOiBfPpoHnTErWUwPpLPY3ynQy1_-YiY_RUWzjkfGTUztEhYHdTsaQbfcGH34vBge_PtGE4cjnl-3wtdmehFfTt_v2dHsjSXITjHaewvxxD0UuL_gWgO-ktaVCKI"
client = TestClient(app)

def  test_search_song():
    response = client.get("http://localhost:8000/searchSong/{query}",params={"query": 'Cant Tell Me Nothing',type: "track"})
    assert response.status_code == 200
    assert "results" in response.json()