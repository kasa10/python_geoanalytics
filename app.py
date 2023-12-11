#%%
from flask import Flask, render_template
import pandas as pd
from keplergl import KeplerGl
from flask import Flask, render_template, request, redirect, url_for, session


from flask_sqlalchemy import SQLAlchemy
import secrets
# Генерируем случайный ключ
secret_key = secrets.token_hex(32)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:11061978@localhost/geosurf'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key


db = SQLAlchemy(app)

def get_user_status():
    authenticated = False
    username = None
    if 'user' in session:
        authenticated = True
        username = session['user']['username']
    return authenticated, username

# Ваш код здесь


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(800), nullable=False)
    user_type = db.Column(db.String(255), nullable=False)  # 'existing' or 'new'
    email = db.Column(db.String(120), nullable=False)  # Добавьте поле 'email'


# db.create_all()

import pandas as pd

# Создаем тестовые данные
data = {
    'latitude': [40.7128, 34.0522, 41.8781],
    'longitude': [-74.0060, -118.2437, -87.6298],
    'name': ['New York', 'Los Angeles', 'Chicago'],
}

df = pd.DataFrame(data)


# Инициализация карты Kepler.gl
kepler_config = {
    "version": "v1",
    "config": {
        "visState": {
            "layers": [
                {
                    "id": "my_data",
                    "type": "point",
                    "config": {
                        "dataId": "my_data",
                        "label": "my_data",
                        "color": [30, 150, 190],
                        "highlightColor": [252, 242, 26, 255],
                        "isVisible": True,
                        "visConfig": {
                            "radius": 5,
                            "fixedRadius": False,
                            "opacity": 0.8,
                            "outline": False,
                            "thickness": 2,
                            "strokeColor": None,
                        },
                        "hidden": False
                    }
                }
            ],
        },
        "mapState": {
            "bearing": 0,
            "dragRotate": False,
            "latitude": 40.710394,
            "longitude": -74.000288,
            "pitch": 0,
            "zoom": 12.41,
            "isSplit": False,
        },
        "mapStyle": {
            "styleType": "dark",
            "topLayerGroups": {},
            "visibleLayerGroups": {
                "label": True,
                "road": True,
                "border": False,
                "building": True,
                "water": True,
                "land": True,
                "3d building": False,
            },
            "threeDBuildingColor": [
                9.665468314072013,
                17.18305478057247,
                31.1442867897876,
            ],
            "mapStyles": {},
        },
    },
}

kepler = KeplerGl(config=kepler_config)
kepler.add_data(data=df, name="my_data")

@app.route('/')
def index():
    kepler_html = kepler._repr_html_()
    authenticated, username = get_user_status()
    return render_template('index.html', kepler_html=kepler_html, authenticated=authenticated, username=username)

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Ищем пользователя в базе данных по имени пользователя
        user = users.query.filter_by(username=username).first()

        # Проверяем, существует ли пользователь и совпадает ли хеш пароля
        if user and check_password_hash(user.password, password):
            # Устанавливаем сессию, чтобы помнить, что пользователь авторизован
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_type'] = user.user_type

            # Определяем, куда перейти в зависимости от типа пользователя
            if user.user_type == 'existingBusinessOwner':
                return redirect(url_for('existing_business_owner_page'))
            elif user.user_type == 'newEntrepreneur':
                return redirect(url_for('new_entrepreneur_page'))

    return render_template('login.html')


from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    registration_success = False
    username = None

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']  #email из формы
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_type = request.form['user_type']

        # Проверка совпадения паролей
        if password != confirm_password:
            return 'Пароли не совпадают!'

        # Хэширование пароля
        hashed_password = generate_password_hash(password)


        # Создаем нового пользователя
        new_user = users(username=username, email=email, password=hashed_password, user_type=user_type)

        # Добавляем пользователя в базу данных
        db.session.add(new_user)
        db.session.commit()

        registration_success = True
        username = request.form['username']

    return render_template('register.html', registration_success=registration_success, username=username)



from flask import render_template

@app.route('/new_entrepreneur_page', methods=['GET', 'POST'])
def new_entrepreneur_page():
    if 'user_id' in session and 'user_type' in session and session['user_type'] == 'newEntrepreneur':
        # Список всех категорий
        categories = [
            'Товары и услуги для детей', 'Другие услуги', 'Цветы и подарки',
            'Отдых и развлечения', 'Медицинские товары и услуги', 'Образовательные услуги',
            'Печатная продукция и канцелярия', 'Кафе и рестораны', 'Другие товары',
            'Профессиональные услуги', 'Аптеки', 'Бытовая техника и электроника',
            'Производство: другое', 'Спортивные товары и услуги', 'Ремонт и строительство',
            'Товары повседневного спроса', 'Одежда и аксессуары', 'Бытовые услуги',
            'Туристические услуги', 'Мебель', 'АЗС', 'Товары и услуги для красоты',
            'Автомобильные товары и услуги', 'Товары и услуги для животных'
        ]

        if request.method == 'POST':
            business_category = request.form.get('business_category')
            business_location = request.form.get('business_location')

            if business_category:
                # Получаем рекомендации для выбранной категории
                recommendations = get_recommendations_by_category(business_category)

                # Отображаем страницу с рекомендациями
                return render_template('recommendations.html', recommendations=recommendations)

            elif business_location:
                # Ваш код обработки указанного местоположения
                # Можете использовать этот блок для получения рекомендаций по указанному местоположению
                # coordinates = get_coordinates_by_location(business_location)
                recommendations = get_recommendations_by_location()

                # Ваш код для отображения рекомендаций
                if recommendations:
                    return render_template('recommendations.html', recommendations=recommendations)

        # Ваш код для отображения страницы нового предпринимателя
        return render_template('new_entrepreneur_page.html', categories=categories)

    else:
        return redirect(url_for('login'))




#ЗДЕСЬ ЧИТАЕМ ДАННЫЕ ПОСЛЕ ПАРСИНГА
import random
import json
# Дополнительные функции для обработки данных
def get_recommendations_by_category(business_category):
# Загружаем данные из файла JSON
    with open('parsing/geotochki.json', 'r', encoding='utf-8') as json_file: #C:/Users/kiril/OneDrive/Рабочий стол/Хакатон Гео/web3/
        data = json.load(json_file)

    # Извлекаем адреса из данных JSON
    addresses_data = data
    addresses = [item['properties']['Title'] for item in addresses_data]

    # Получаем случайные рекомендации (в будущем модель будет передавать данные, но ее реализует другая часть команды, так что получаем случайные значения)
    random_recommendations = random.sample(addresses, 3)
    return random_recommendations


def get_recommendations_by_location():
    # Используем список категорий, который уже получили до этого
    categories = [
        'Товары и услуги для детей', 'Другие услуги', 'Цветы и подарки',
        'Отдых и развлечения', 'Медицинские товары и услуги', 'Образовательные услуги',
        'Печатная продукция и канцелярия', 'Кафе и рестораны', 'Другие товары',
        'Профессиональные услуги', 'Аптеки', 'Бытовая техника и электроника',
        'Производство: другое', 'Спортивные товары и услуги', 'Ремонт и строительство',
        'Товары повседневного спроса', 'Одежда и аксессуары', 'Бытовые услуги',
        'Туристические услуги', 'Мебель', 'АЗС', 'Товары и услуги для красоты',
        'Автомобильные товары и услуги', 'Товары и услуги для животных'
    ]

    # Получаем топ категории (но их вообще будет возвращать модель)
    random_top_categories = random.sample(categories, 3)
    return random_top_categories


@app.route('/logout')
def logout():
    # Просто очистим сессию
    session.clear()
    return redirect(url_for('index'))



import pandas as pd

# Функция для получения данных об удовлетворенности клиентов
def get_customer_satisfaction_data():
    # Загружаем данные из файла submit_k.csv
    df = pd.read_csv('predict_churn_bk/submit_k.csv', delimiter=';') #C:/Users/kiril/OneDrive/Рабочий стол/Хакатон Гео/web3/

    # Вычисляем процент клиентов, которые точно останутся
    stay_percentage = (df[df['buy_post'] == 0].shape[0] / df.shape[0]) * 100

    # Выводим топ людей, которые уйдут
    churned_users_data = df[df['buy_post'] == 1]['customer_id'].head(20).tolist()

    return stay_percentage, churned_users_data

@app.route('/existing_business_owner_page')
def existing_business_owner_page():
    if 'user_id' in session and 'user_type' in session and session['user_type'] == 'existingBusinessOwner':
        # Получаем данные об удовлетворенности клиентов
        stay_percentage, churned_users_data = get_customer_satisfaction_data()

        # Возвращаем страницу с передачей данных в шаблон
        return render_template('existing_business_owner_page.html', stay_percentage=stay_percentage, churned_users_data=churned_users_data)
    else:
        return redirect(url_for('login'))








if __name__ == '__main__':
    app.run(debug=True)
