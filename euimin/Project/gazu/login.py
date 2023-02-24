import os
import json
import gazu

class login:
    def __init__(self):
        self._host = None
        self._user_id = None
        self._user_pw = None
        self._check_host = False
        self._check_user = False

        # json 파일의 경로를 지정
        # 지정된 경로에 join을 통한 파일 경로 지정?
        self.path = os.path.expanduser('~/.config/pizza/')
        self.user_path = os.path.join(self.path + 'pizza.json')

    @property
    def host(self):
        return self._host

    @property
    def check_host(self):
        return self._check_host

    @property
    def check_user(self):
        return self._check_user


    def setting(self):
        # json file check
        if not os.path.exists(self.path):
            try:
                os.makedirs(self.path)
            except OSError:
                raise Exception("Error")

        try:
            if not os.path.exists(self.user_path):
                self.reset_setting()
        except OSError:
            raise Exception("Error")

    def reset_setting(self):
        self._host = ''
        self._user_id = ''
        self._user_pw = ''
        self._check_host = False
        self._check_user = False

        self.save_setting()

    def save_setting(self):
        user = {
        'host' : self._host,
        'user_id' : self._user_id,
        'user_pw' : self._user_pw
        }

        with open(self.user_path, 'w') as json_file:
            json.dump(user, json_file)

    def host(self, try_host):
        pass

    def log_in(self, try_id, try_pw):
        pass

    def log_out(self):



        pass



def main():
    test = login()
    # test.setting()
    test.reset_setting()

if __name__ == "__main__":
    main()
