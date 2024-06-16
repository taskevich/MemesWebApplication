import io

import pytest
import random
import requests


def test_get_memes():
    response = requests.get("http://localhost:8000/memes")
    assert response.status_code == 200
    assert response.json()["error"] == False


def test_add_meme():
    text = f"test {random.randint(1, 1000)}"
    files = {
        "image": ("1dOSgL-c-vI.jpg", open("1dOSgL-c-vI.jpg", "rb"), "image/jpeg"),
    }

    response = requests.post(
        f"http://localhost:8000/memes?text={text}",
        data={"text": text},
        files=files
    )

    assert response.status_code == 200
    assert response.json()["error"] == False


def test_update_meme():
    meme_id = random.randint(1, 1000)
    text = f"test {meme_id}"

    files = {
        "image": ("1dOSgL-c-vI.jpg", open("./1dOSgL-c-vI.jpg", "rb"), "image/jpeg"),
    }

    response = requests.put(
        f"http://localhost:8000/memes/{meme_id}?text={text}",
        files=files
    )

    assert response.status_code == 200
    assert response.json()["error"] == False


def test_delete_meme():
    meme_id = random.randint(2, 1000)
    response = requests.delete(f"http://localhost:8000/memes/{meme_id}")
    assert response.status_code == 200
    assert response.json()["error"] == True

    meme_id = 1
    response = requests.delete(f"http://localhost:8000/memes/{meme_id}")
    assert response.status_code == 200
    assert response.json()["error"] == False
