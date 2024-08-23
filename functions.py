import grpc
import uuid
from global_vars import server


# Генерация GUID
def generate_guid() -> str:
    return str(uuid.uuid4())


# Создание gRPC-канала для подключения к серверу
def grpc_channel():
    with grpc.insecure_channel(server) as channel:
        yield channel


# Генерация случайной строки
def generate_random_string(length):
    # Определяем необходимые наборы символов
    lower_chars = 'abcdefghijklmnopqrstuvwxyz'
    upper_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cyrillic_chars = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
    digits = '0123456789'
    special_chars = '!@#$%^&*()_+~`|}{[]:;?><,./-='

    # Добавляем как минимум один символ каждого типа
    result = random.choice(digits) + \
             random.choice(special_chars) + \
             random.choice(lower_chars) + \
             random.choice(upper_chars) + \
             random.choice(cyrillic_chars)

    # Заполняем оставшуюся часть случайными символами
    remaining_length = length - len(result)
    result += ''.join(random.choices(lower_chars + upper_chars + digits + special_chars + cyrillic_chars, k=remaining_length))
    random_string = ''.join(random.sample(result, len(result)))
    # Перемешиваем символы
    return random_string