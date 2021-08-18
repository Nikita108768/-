import sqlite3
db_name = 'quiz.sqlite'
conn = None
curor = None

def check_answer(__id,answer):
    open()
    request = ''' SELECT question.answer 
                  FROM question, quiz_content 
                  WHERE quiz_content.id == ? 
                  AND quiz_content.question_id == question.id '''

    cursor.execute(request,[__id])
    data = cursor.fetchone()
    print(answer,data[0])
    if answer == data[0]:
        return True
    else:
        return False
    close()

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()
    
def create():
    open()
    cursor.execute('''PRAGMA foreign_key = on''')
    quiz_zapros = '''   CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY,
        name VARCHAR)  '''
    do(quiz_zapros)

    quest_zapros = '''   CREATE TABLE IF NOT EXISTS question (
        id INTEGER PRIMARY KEY,
        question VARCHAR,
        answer VARCHAR,
        wrong1 VARCHAR , wrong2 VARCHAR , wrong3 VARCHAR)  '''
    do(quest_zapros)

    content_zapros = '''   CREATE TABLE IF NOT EXISTS quiz_content (
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER,
        question_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz (id),
        FOREIGN KEY (question_id) REFERENCES quiz (id) )  '''
    do(content_zapros)
    close()

def add_q():
    questions =[
        ("Что больше килограмм снега или килограмм гвоздей","Одинаково","Снега","Гвоздей","Ничего"),
        ("Сколько пядей во лбу?","7","0","-4","9"),
        ("Сколько месяцев в году имеют 28 дней?","Все","Один","Ни одного","Два"),
        ("Каким станет зеленый утес, если упадет в Красное море?", 'Мокрым', 'Красным', 'Не изменится', 'Фиолетовым'),
        ("Какой рукой лучше размешивать чай?", 'Ложкой', 'Правой', 'Левой', 'Любой'),
        ("Что не имеет длины, глубины, ширины, высоты, а можно измерить?", 'Время', 'Глупость', 'Море', 'Воздух'),
        ("Когда сетью можно вытянуть воду?", 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
        ("Что больше слона и ничего не весит?", 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако'),        
        ("Как зовут менеджера в алгоритмике Владимир?","Надежда","Екатерина","Наталья","Егор"),
        ("Сколько астрокоинов дают за домашнюю работу?","10","278","1000","999"),       
    ]
    open()
    cursor.executemany(''' INSERT INTO question (question,
                                                 answer,
                                                 wrong1,
                                                 wrong2,
                                                 wrong3) 
                                                 VALUES(?,?,?,?,?)''',questions)
    conn.commit()
    close()

def add_quiz():
    quizes = [("Шуточная",),("Алгоритмика",),("Алгоритмика",)]
    open()
    cursor.executemany(''' INSERT INTO quiz (name) VALUES (?)''',quizes)
    conn.commit()
    close()

def get_quiz_names():
    open()
    request = '''SELECT * FROM quiz ORDER BY id'''
    cursor.execute(request)
    data = cursor.fetchall()
    return data

def add_links():
    open()
    cursor.execute(''' PRAGMA foreign_key = on ''')
    request = ''' INSERT INTO quiz_content (quiz_id,question_id) VALUES (?,?)'''
    mode = int(input("Хочешь добавить связь? ДА(1) или НЕТ(0)"))
    while mode:
        question_id = int(input("Вопрос с каким id добавить?"))
        quiz_id = int(input("В викторину с каким id добавить?"))
        cursor.execute(request,[quiz_id,question_id])
        conn.commit()
        mode = int(input("Хочешь ещё добавить связь? ДА(1) или НЕТ(0)"))
    close()

def get_question_after(question_id = 0,quiz_id = 1):
    open()
    request = ''' SELECT * 
    FROM question,quiz_content 
    WHERE quiz_content.question_id == question.id 
    AND quiz_content.quiz_id == ? 
    ORDER BY quiz_content.id'''

    cursor.execute(request,[quiz_id])
    result = cursor.fetchall()
    close()
    if len(result) > question_id:
        return result [question_id]
    else:
        return None

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def main():
    clear_db()
    create()
    add_q()
    add_quiz()
    add_links()
    show_tables()
    get_question_after(1,1)

if __name__ == "__main__":
    get_quiz_names()
    main()