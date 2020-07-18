# Pass path to parent directory

def check_session_message(client, redirect_path:str, message:bytes):
    '''リダイレクト直後のみmessageが表示されるか確認
    '''
    response = client.get(redirect_path)
    assert message in response.data

    response = client.get(redirect_path)
    assert message not in response.data
