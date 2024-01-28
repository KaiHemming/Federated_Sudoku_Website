from flask import Blueprint, request, jsonify
import requests
from routes.generate_code import encrypt_data, decrypt_data

oauth_bp = Blueprint('oauth_bp', __name__)


@oauth_bp.route('/oauth/redirect/', methods=['POST'])
def oauth_redirect():
    # default when http request is successful
    response_object = {'status': 'success'}
    post_data = request.get_json()

    client_id = post_data.get('client_id')
    code = post_data.get('code')

    clientIdToWebsiteMap = {
            "cs3099-g1": "https://cs3099user01.host.cs.st-andrews.ac.uk/rest",
            "aces_g2": "https://cs3099user02.host.cs.st-andrews.ac.uk",
            "cs3099group03": "https://cs3099user03.host.cs.st-andrews.ac.uk",
            "cs3099-g4": "https://cs3099user04.host.cs.st-andrews.ac.uk",
            "g6": "https://cs3099user06.host.cs.st-andrews.ac.uk",
            "aces-g7": "https://cs3099user07.host.cs.st-andrews.ac.uk/api",
            "aces-eight": "https://cs3099user08.host.cs.st-andrews.ac.uk",
            "aces-g9": "https://cs3099user09.host.cs.st-andrews.ac.uk",
        }

    client_url = clientIdToWebsiteMap[client_id]

    response = requests.post(client_url + "/oauth/token", json={
                          "client_id": "aces5",
                          "client_secret": "TOk03wZOjy2ZNvSkGKzX6YUcvK5udxILmKF03K5ImehmGB8Jqibwp5awcHuaDx0mtoCY83e3KcWifeDddsEyugcHM1o9j0blDVxMOeOwVNymlEeHWtgfcgT1XS91iLg6PKqCuuAAZvS3k2mjl0npOIE3hQNJp5I7HSBrgC12y298RHmGW3infRDlMqLIzBMFi3jrJN6A8oqeBEgdnwepovYpTqkk7k5e6iJA2n181zUFnQeLpwvKm8dnFsxRUCy7j38QwVLPDYvOm4fMMFxo2eFHWer67HQ9fqhu8KqISyIGzotVn9Zh8s9BNrnVUpUk",
                          "access_code": code
                           })
    access_token = response.json()['access_token']

    response = requests.post(client_url + "/api/user/me", json={
                           "access_token": access_token
                       })
    username = response.json()['username']
    url = response.json()['origin']['url']
    url = url.replace("cs3099", "")
    group_number=0
    for c in url:
        if(ord(c)>=ord('0') and ord(c)<=ord('9') and group_number==0):
            group_number= group_number*10+ int(c)
    origin = " from group "+str(group_number)
    response_object['username'] = username+origin

    return jsonify(response_object)

@oauth_bp.route('/oauth/token/', methods=['POST'])
def oauth_token():
    post_data = request.get_json()
    client_id = post_data.get('client_id')
    access_code = post_data.get('access_code')
    client_secret = post_data.get('client_secret')

    clientIdToClientSecretMap={
            "cs3099-g1": "DIiorNA4fWtGYO3NBd56EdFO6Md4xK62wvZGA3dG1eNKlmYUJma1QJu10RO6jz2c6PXGX6JeuF7DNeslGUmU5gbZmC3dWl86kFPGlUYhTywEPygA6CsDAl6f8U8hOZPDFIv2pwd6NbAX7mn5CbVZc7k2sQxSXGBYPguLpVlKInmhG9wV8zJoyAkKMTufmsHc1nd6TP58W4nazDdAmiECRgUmGHdkOvQwODOHYV3ldJmKAq0MTMrsNjHXKVxZIrmsAIZmIikZaI4Zti7k5yZLwzAyRDJ5dwVermLoFbj2XoPAVv8RI9voHPOpOLBoTuaK",
            "aces_g2": "rv7zlvkfa30dr46v6y7fnwz8zvb9uijrqq5q1w2mlknoyyx8mpvollc1g6fhwsdpsweoq69dmbqu8bpkqak1ekw8ag2gdzvmjfr3ja5xlkmal8tlgu64csddow48711pq61je8ibt7fft53l4s94ik8wq1zthbw39rod5eght70wqvbbkislurptam9imo41jpfqmjn0eujg20fayb8r783teeepvrnko848bmbf1gdkz9eogohqsp84owpy8t3x",
            "cs3099group3": "wxhsoESvXI18ezjSGTYV2V3yqKNgJWqFNvTj2G7GOgmBpx1BCwFrEu3UAQq5n6cMXuJW73Gg1aagbHmcqsby9unlhDaN1aBgtba3",
            "cs3099-g4": "2d39ab2a49b691f5cab7bbbdc46e2f01c67bb0921a816472f768f9bae3abb52b702708c8e72f54712254fd16e3b08ac30b877bf968305092d72b6b7e92397f6d1ed8d288eef8397a112d6decfbc99ed20186a62df26639e110c699e59f959aa9470147387e7807ba31af2cd01766d39d57a56aa94087246aa14d904da624401f",
            "g6": "0001001000010111110100000110001111010110100010110111000000100100110101111101110001111110101101100001010110001000101100010110111001111110110011010000111101101001011011010101110101001000110011000010010100000111010111000110001110100110010100001100011110111110",
            "aces-g7": "Ey1SNTG2bQxrfTV6bkgk2Gj6SXIxq3Q20IS10hdEelYU1Od2XuiXkWokWmZ2L609bhJKzLkHFisgT9kYSo3ZeaSIEzxbtzJzc4ymrECTmfUPTFRWZ9KJyMrrm6dQUDRGl3Xd6Qkt8qRJXclwV4xzrnAtzFyHNOa5Ld5RqmpW6qTAf3EnwWJQeI3gfpDyUkmKxMzrAS8jXudm0dS0uej7FkgNEGPMpY5NU7wMQftoB15pAXBc9Xl0kseNEWRcTAjLaZ56R7CwHYpGn2W1Gm3So2rNWQ1Xe8YXPzmGSIZqUu4f2E7gh0TXCfF9HlcNOYLm",
            "aces-eight": "5um608eo6ejt9wuiqqf7miikuqxexgtzeu5kbvv2jz8cnmtmnhpkxowzqcje1r2f",
            "aces-g9": "tSOOeUSId0ZSRVaW0Y8mbG9FZ4u6MARPtCnCeDYcq3VRiR9XJzO6qrf9T9T3jTyL22gghmBufr7JtJ6ngU9UHiHMEyzxsHRBahnTnpgX78bHQee2MSfotH34xkAVrOKIj5LUYXnOBAQUVvx1pVVaf9",
    }

    if clientIdToClientSecretMap[client_id]!=client_secret:
        abort(404)
    secret_key = b'2SKCP4P9BvPTeVYjRnsv_f6Z9NCjQYDrVyAeCsaSZLE='
    decrypted_access_code = decrypt_data(access_code, b'V33ID7OcBtYEkNVgCtzEh-MNSB8Tm-b94n4GiKTOW5o=')
    access_token = encrypt_data(decrypted_access_code , secret_key)
    return jsonify({"access_token": access_token})
