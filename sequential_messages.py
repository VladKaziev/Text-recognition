import json
import re

with open('output_response.json', 'r') as file:
    ocr_data = json.load(file)

def parse_messages(data):
    messages = []
    height_threshold = int(data['result']['textAnnotation']['height']) * 0.1  # Топ 10% картинки игнорируем
    time_stamp_pattern = re.compile(r'^\d{2}:\d{2}$')  # Выражение для отсечения блоков со временем
    message_index = 0

    # Проходимся по каждому блоку и забираем текст
    for block in data['result']['textAnnotation']['blocks']:
        for line in block.get('lines', []):
            # Отсекаем 10% скриншота сверху
            if int(line['boundingBox']['vertices'][0]['y']) > height_threshold:
                # Убираем блок со временем и исключаем символы: '/', '//'
                if not time_stamp_pattern.match(line['text']) and len(line['text']) > 1 and '//' not in line['text']:
                    # Разделяем отправителей по координате x (левый верхний угол блока с текстом)
                    x_coord = line['boundingBox']['vertices'][0]['x']
                    sender = 'sender1' if int(x_coord) in range(0,50) else 'sender2'
                    # Добавляем в список messages кортеж, содержащий индекс сообщения, отправителя и сам текст
                    messages.append((message_index, sender, line['text']))
                    message_index += 1

    # Сортируем список по индексу
    sorted_messages = sorted(messages, key=lambda x: x[0])
    return sorted_messages


indexed_messages = parse_messages(ocr_data)

sequential_messages = [f"{msg[1]}: {msg[2]}" for msg in indexed_messages]
print(sequential_messages)