def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    assert (
        "Let's play! Visit route /card for a random classic card."
        in res.json()["message"]
    )
