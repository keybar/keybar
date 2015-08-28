from hypothesis.utils.conventions import not_set

def accept(f):
    def test_encrypt_decrypt_cycle(salt=not_set, password=not_set, message=not_set):
        return f(salt, password, message)
    return test_encrypt_decrypt_cycle
