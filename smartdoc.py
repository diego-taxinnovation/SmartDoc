from decouple import config
from src import init_app

#configuration = configEnv['development']
app = init_app(config)

if __name__ == '__main__':
    app.run()