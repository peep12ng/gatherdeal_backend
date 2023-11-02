def test_hotdeal_api(client):
    resp = client.post("/api/hotdeals/update")

    assert resp.status_code==200

    resp = client.get("/api/hotdeals/1")

    assert resp.status_code==200

    resp = client.get("/api/hotdeal/QZ_1418532")

    assert resp.status_code==200