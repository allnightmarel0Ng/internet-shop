import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor
import json

# Загрузка и предобработка обучающего датасета
data = pd.read_csv('sales_train.csv')
data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y')
data['month'] = data['date'].dt.month
data['year'] = data['date'].dt.year

# Удаление выбросов
data = data[(data['item_price'] > 0) & (data['item_cnt_day'] > 0)]

# Агрегация данных на уровне item_id и shop_id
data_agg = data.groupby(['item_id', 'shop_id']).agg({
    'item_price': 'mean',
    'item_cnt_day': 'sum'
}).reset_index()
data_agg.rename(columns={'item_price': 'avg_item_price', 'item_cnt_day': 'total_sales'}, inplace=True)

# Создание признаков
features = ['avg_item_price']
X = data_agg[features]
y = data_agg['total_sales']  # Используем сумму продаж, а не логарифм

# Обучение модели с более низкими параметрами для лучшей точности
model = LGBMRegressor(
    n_estimators=1000,  # Увеличение числа деревьев
    learning_rate=0.01,  # Снижение скорости обучения
    lambda_l1=0.2,       # Регуляризация L1
    lambda_l2=0.2,       # Регуляризация L2
    random_state=42,
    num_leaves=31,       # Меньше деревьев для лучшего обобщения
    max_depth=8,         # Ограничение глубины деревьев
    subsample=0.8,       # Снижение переобучения с помощью подвыборки
    colsample_bytree=0.8 # Снижение переобучения с помощью случайного выбора признаков
)
model.fit(X, y)

# Функция для предсказания оптимальной цены
def predict_optimal_price(json_file):
    with open(json_file, 'r') as f:
        input_data = json.load(f)

    if 'productIDs' not in input_data or not input_data['productIDs']:
        print("JSON файл не содержит список товаров для анализа.")
        return

    product_ids = input_data['productIDs']
    
    # Предсказание оптимальной цены для каждого товара из списка
    optimal_prices = []
    
    for product_id in product_ids:
        # Извлекаем агрегационные данные для товара
        product_data = data_agg[data_agg['item_id'] == product_id]
        
        if product_data.empty:
            print(f"Данные для товара с ID {product_id} не найдены в обучающем датасете.")
            continue

        avg_price = product_data['avg_item_price'].values[0]
        
        # Моделируем несколько вариантов цен вокруг средней цены товара
        test_prices = np.linspace(avg_price * 0.8, avg_price * 1.2, num=100)  # Ограничиваем диапазон

        # Прогнозируем продажи для каждого варианта цены
        test_features = pd.DataFrame({'avg_item_price': test_prices})
        predicted_sales = model.predict(test_features)

        # Рассчитываем доход
        revenues = test_prices * predicted_sales

        # Находим цену с максимальной выручкой
        optimal_price = test_prices[np.argmax(revenues)]
        
        optimal_prices.append({
            'product_id': product_id,
            'optimal_price': optimal_price
        })
    
    # Сохранение результатов
    with open('optimal_prices.json', 'w') as f:
        json.dump(optimal_prices, f, indent=4)
    
    print("Результаты сохранены в optimal_prices.json")

# Пример вызова
predict_optimal_price('new_sales_data.json')