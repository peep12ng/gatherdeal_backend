def test_hotdeal_api(client):
    resp = client.post("/api/hotdeals/update")

    assert resp.status_code==200

    resp = client.get("/api/hotdeals/?page=1&per_page=10")

    assert resp.status_code==200

    resp = client.get("/api/hotdeal/QZ_1418532")

    assert resp.status_code==200