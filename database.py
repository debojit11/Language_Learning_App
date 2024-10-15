import sqlite3

db_file = "language_learning.db"

def connect_db():
    '''Connect to the SQLite database and return conn obj'''
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file}")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_tables(conn):
    """Create tables for vocabulary and progress tracking."""
    try:
        cursor = conn.cursor()
        # Create vocabulary table with language and romaji
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS vocabulary(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                romaji TEXT NOT NULL,
                translation TEXT NOT NULL,
                topic TEXT NOT NULL,
                language TEXT NOT NULL  -- Adding language column
            )
        ''')
        
        # Create progress table with an added quiz_score column
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS progress(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word_id INTEGER NOT NULL,
                learned BOOLEAN NOT NULL,
                quiz_score INTEGER DEFAULT 0,  -- Adding quiz_score column
                date TEXT DEFAULT CURRENT_TIMESTAMP,  -- Adding date column
                FOREIGN KEY (word_id) REFERENCES vocabulary(id)
            )
        ''')
        conn.commit()
        print("Tables created successfully")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

def insert_initial_vocabulary(conn):
    """Insert initial vocabulary into the database."""
    try:
        cursor = conn.cursor()  # Create a cursor for this function
        # Sample Japanese vocabulary with Romaji
        japanese_vocabulary = [
            ('こんにちは', 'Konnichiwa', 'Hello', 'Greetings', 'Japanese'),
            ('さようなら', 'Sayōnara', 'Goodbye', 'Greetings', 'Japanese'),
            ('ありがとう', 'Arigatou', 'Thank you', 'Greetings', 'Japanese'),
            ('おはよう', 'Ohayou', 'Good morning', 'Greetings', 'Japanese'),
            ('こんばんは', 'Konbanwa', 'Good evening', 'Greetings', 'Japanese'),
            ('すみません', 'Sumimasen', 'Excuse me', 'Greetings', 'Japanese'),
            ('おやすみ', 'Oyasumi', 'Good night', 'Greetings', 'Japanese'),
            ('どういたしまして', 'Douitashimashite', 'You are welcome', 'Greetings', 'Japanese'),
            ('お元気ですか', 'Ogenki desu ka', 'How are you', 'Greetings', 'Japanese'),
            ('よろしくお願いします', 'Yoroshiku onegaishimasu', 'Nice to meet you', 'Greetings', 'Japanese'),
            
            # Common Phrases
            ('はい', 'Hai', 'Yes', 'Common Phrases', 'Japanese'),
            ('いいえ', 'Iie', 'No', 'Common Phrases', 'Japanese'),
            ('わかりません', 'Wakarimasen', 'I do not understand', 'Common Phrases', 'Japanese'),
            ('いくらですか', 'Ikura desu ka', 'How much is it?', 'Common Phrases', 'Japanese'),
            ('どこですか', 'Doko desu ka', 'Where is it?', 'Common Phrases', 'Japanese'),
            ('時間は何ですか', 'Jikan wa nan desu ka', 'What time is it?', 'Common Phrases', 'Japanese'),
            ('助けてください', 'Tasukete kudasai', 'Please help me', 'Common Phrases', 'Japanese'),
            ('大丈夫ですか', 'Daijoubu desu ka', 'Are you okay?', 'Common Phrases', 'Japanese'),
            
            # Colors
            ('赤', 'Aka', 'Red', 'Colors', 'Japanese'),
            ('青', 'Ao', 'Blue', 'Colors', 'Japanese'),
            ('緑', 'Midori', 'Green', 'Colors', 'Japanese'),
            ('黄色', 'Kiiro', 'Yellow', 'Colors', 'Japanese'),
            ('黒', 'Kuro', 'Black', 'Colors', 'Japanese'),
            ('白', 'Shiro', 'White', 'Colors', 'Japanese'),
            ('オレンジ', 'Orenji', 'Orange', 'Colors', 'Japanese'),
            ('紫', 'Murasaki', 'Purple', 'Colors', 'Japanese'),
            
            # Numbers
            ('一', 'Ichi', 'One', 'Numbers', 'Japanese'),
            ('二', 'Ni', 'Two', 'Numbers', 'Japanese'),
            ('三', 'San', 'Three', 'Numbers', 'Japanese'),
            ('四', 'Shi', 'Four', 'Numbers', 'Japanese'),
            ('五', 'Go', 'Five', 'Numbers', 'Japanese'),
            ('六', 'Roku', 'Six', 'Numbers', 'Japanese'),
            ('七', 'Nana', 'Seven', 'Numbers', 'Japanese'),
            ('八', 'Hachi', 'Eight', 'Numbers', 'Japanese'),
            ('九', 'Kyuu', 'Nine', 'Numbers', 'Japanese'),
            ('十', 'Juu', 'Ten', 'Numbers', 'Japanese'),
            
            # Food
            ('ご飯', 'Gohan', 'Rice', 'Food', 'Japanese'),
            ('パン', 'Pan', 'Bread', 'Food', 'Japanese'),
            ('肉', 'Niku', 'Meat', 'Food', 'Japanese'),
            ('魚', 'Sakana', 'Fish', 'Food', 'Japanese'),
            ('野菜', 'Yasai', 'Vegetables', 'Food', 'Japanese'),
            ('果物', 'Kudamono', 'Fruits', 'Food', 'Japanese'),
            ('卵', 'Tamago', 'Egg', 'Food', 'Japanese'),
            ('チーズ', 'Chiizu', 'Cheese', 'Food', 'Japanese'),
            ('牛乳', 'Gyunyu', 'Milk', 'Food', 'Japanese'),
            
            # Animals
            ('犬', 'Inu', 'Dog', 'Animals', 'Japanese'),
            ('猫', 'Neko', 'Cat', 'Animals', 'Japanese'),
            ('鳥', 'Tori', 'Bird', 'Animals', 'Japanese'),
            ('魚', 'Sakana', 'Fish', 'Animals', 'Japanese'),
            ('馬', 'Uma', 'Horse', 'Animals', 'Japanese'),
            ('象', 'Zou', 'Elephant', 'Animals', 'Japanese'),
            ('ライオン', 'Raion', 'Lion', 'Animals', 'Japanese'),
            ('虎', 'Tora', 'Tiger', 'Animals', 'Japanese'),
            ('うさぎ', 'Usagi', 'Rabbit', 'Animals', 'Japanese'),
            
            # Directions
            ('上', 'Ue', 'Up', 'Directions', 'Japanese'),
            ('下', 'Shita', 'Down', 'Directions', 'Japanese'),
            ('左', 'Hidari', 'Left', 'Directions', 'Japanese'),
            ('右', 'Migi', 'Right', 'Directions', 'Japanese'),
            ('前', 'Mae', 'Front', 'Directions', 'Japanese'),
            ('後ろ', 'Ushiro', 'Back', 'Directions', 'Japanese'),
            
            # Miscellaneous
            ('音楽', 'Ongaku', 'Music', 'Miscellaneous', 'Japanese'),
            ('映画', 'Eiga', 'Movie', 'Miscellaneous', 'Japanese'),
            ('旅行', 'Ryokou', 'Travel', 'Miscellaneous', 'Japanese'),
            ('仕事', 'Shigoto', 'Work', 'Miscellaneous', 'Japanese'),
            ('学校', 'Gakkou', 'School', 'Miscellaneous', 'Japanese'),
            ('友達', 'Tomodachi', 'Friend', 'Miscellaneous', 'Japanese'),
            ('家族', 'Kazoku', 'Family', 'Miscellaneous', 'Japanese'),
            ('趣味', 'Shumi', 'Hobby', 'Miscellaneous', 'Japanese'),
            ('愛', 'Ai', 'Love', 'Miscellaneous', 'Japanese'),
            ('幸せ', 'Shiawase', 'Happiness', 'Miscellaneous', 'Japanese'),
            ('悲しい', 'Kanashii', 'Sad', 'Miscellaneous', 'Japanese')
        ]
        
        # Sample Chinese vocabulary
        chinese_vocabulary = [
            ('你好', 'Nǐ hǎo', 'Hello', 'Greetings', 'Chinese'),
            ('再见', 'Zàijiàn', 'Goodbye', 'Greetings', 'Chinese'),
            ('谢谢', 'Xièxiè', 'Thank you', 'Greetings', 'Chinese'),
            ('早上好', 'Zǎoshang hǎo', 'Good morning', 'Greetings', 'Chinese'),
            ('晚上好', 'Wǎnshàng hǎo', 'Good evening', 'Greetings', 'Chinese'),
            ('对不起', 'Duìbùqǐ', 'Excuse me', 'Greetings', 'Chinese'),
            ('晚安', 'Wǎn ān', 'Good night', 'Greetings', 'Chinese'),
            ('不客气', 'Bù kèqì', 'You are welcome', 'Greetings', 'Chinese'),
            ('你好吗', 'Nǐ hǎo ma', 'How are you?', 'Greetings', 'Chinese'),
            ('很高兴认识你', 'Hěn gāoxìng rènshì nǐ', 'Nice to meet you', 'Greetings', 'Chinese'),
            
            # Common Phrases
            ('是', 'Shì', 'Yes', 'Common Phrases', 'Chinese'),
            ('不是', 'Bù shì', 'No', 'Common Phrases', 'Chinese'),
            ('我不懂', 'Wǒ bù dǒng', 'I do not understand', 'Common Phrases', 'Chinese'),
            ('多少钱', 'Duōshǎo qián', 'How much is it?', 'Common Phrases', 'Chinese'),
            ('在哪里', 'Zài nǎlǐ', 'Where is it?', 'Common Phrases', 'Chinese'),
            ('现在几点', 'Xiànzài jǐ diǎn', 'What time is it?', 'Common Phrases', 'Chinese'),
            ('请帮我', 'Qǐng bāng wǒ', 'Please help me', 'Common Phrases', 'Chinese'),
            ('你还好吗', 'Nǐ hái hǎo ma', 'Are you okay?', 'Common Phrases', 'Chinese'),
            
            # Colors
            ('红', 'Hóng', 'Red', 'Colors', 'Chinese'),
            ('蓝', 'Lán', 'Blue', 'Colors', 'Chinese'),
            ('绿', 'Lǜ', 'Green', 'Colors', 'Chinese'),
            ('黄', 'Huáng', 'Yellow', 'Colors', 'Chinese'),
            ('黑', 'Hēi', 'Black', 'Colors', 'Chinese'),
            ('白', 'Bái', 'White', 'Colors', 'Chinese'),
            ('橙', 'Chéng', 'Orange', 'Colors', 'Chinese'),
            ('紫', 'Zǐ', 'Purple', 'Colors', 'Chinese'),
            
            # Numbers
            ('一', 'Yī', 'One', 'Numbers', 'Chinese'),
            ('二', 'Èr', 'Two', 'Numbers', 'Chinese'),
            ('三', 'Sān', 'Three', 'Numbers', 'Chinese'),
            ('四', 'Sì', 'Four', 'Numbers', 'Chinese'),
            ('五', 'Wǔ', 'Five', 'Numbers', 'Chinese'),
            ('六', 'Liù', 'Six', 'Numbers', 'Chinese'),
            ('七', 'Qī', 'Seven', 'Numbers', 'Chinese'),
            ('八', 'Bā', 'Eight', 'Numbers', 'Chinese'),
            ('九', 'Jiǔ', 'Nine', 'Numbers', 'Chinese'),
            ('十', 'Shí', 'Ten', 'Numbers', 'Chinese'),
            
            # Food
            ('米饭', 'Mǐfàn', 'Rice', 'Food', 'Chinese'),
            ('面包', 'Miànbāo', 'Bread', 'Food', 'Chinese'),
            ('肉', 'Ròu', 'Meat', 'Food', 'Chinese'),
            ('鱼', 'Yú', 'Fish', 'Food', 'Chinese'),
            ('蔬菜', 'Shūcài', 'Vegetables', 'Food', 'Chinese'),
            ('水果', 'Shuǐguǒ', 'Fruits', 'Food', 'Chinese'),
            ('鸡蛋', 'Jīdàn', 'Egg', 'Food', 'Chinese'),
            ('奶酪', 'Nǎilào', 'Cheese', 'Food', 'Chinese'),
            ('牛奶', 'Niúnǎi', 'Milk', 'Food', 'Chinese'),
            
            # Animals
            ('狗', 'Gǒu', 'Dog', 'Animals', 'Chinese'),
            ('猫', 'Māo', 'Cat', 'Animals', 'Chinese'),
            ('鸟', 'Niǎo', 'Bird', 'Animals', 'Chinese'),
            ('鱼', 'Yú', 'Fish', 'Animals', 'Chinese'),
            ('马', 'Mǎ', 'Horse', 'Animals', 'Chinese'),
            ('象', 'Xiàng', 'Elephant', 'Animals', 'Chinese'),
            ('狮子', 'Shīzi', 'Lion', 'Animals', 'Chinese'),
            ('老虎', 'Lǎohǔ', 'Tiger', 'Animals', 'Chinese'),
            ('兔子', 'Tùzi', 'Rabbit', 'Animals', 'Chinese'),
            
            # Directions
            ('上', 'Shàng', 'Up', 'Directions', 'Chinese'),
            ('下', 'Xià', 'Down', 'Directions', 'Chinese'),
            ('左', 'Zuǒ', 'Left', 'Directions', 'Chinese'),
            ('右', 'Yòu', 'Right', 'Directions', 'Chinese'),
            ('前', 'Qián', 'Front', 'Directions', 'Chinese'),
            ('后', 'Hòu', 'Back', 'Directions', 'Chinese'),
            
            # Miscellaneous
            ('音乐', 'Yīnyuè', 'Music', 'Miscellaneous', 'Chinese'),
            ('电影', 'Diànyǐng', 'Movie', 'Miscellaneous', 'Chinese'),
            ('旅行', 'Lǚxíng', 'Travel', 'Miscellaneous', 'Chinese'),
            ('工作', 'Gōngzuò', 'Work', 'Miscellaneous', 'Chinese'),
            ('学校', 'Xuéxiào', 'School', 'Miscellaneous', 'Chinese'),
            ('朋友', 'Péngyǒu', 'Friend', 'Miscellaneous', 'Chinese'),
            ('家庭', 'Jiātíng', 'Family', 'Miscellaneous', 'Chinese'),
            ('爱好', 'Àihào', 'Hobby', 'Miscellaneous', 'Chinese'),
            ('爱', 'Ài', 'Love', 'Miscellaneous', 'Chinese'),
            ('幸福', 'Xìngfú', 'Happiness', 'Miscellaneous', 'Chinese'),
            ('悲伤', 'Bēishāng', 'Sad', 'Miscellaneous', 'Chinese')
        ]
        
        # Insert Japanese vocabulary
        for word in japanese_vocabulary:
            cursor.execute('INSERT INTO vocabulary (word, romaji, translation, topic, language) VALUES (?, ?, ?, ?, ?)', word)
        
        # Insert Chinese vocabulary
        for word in chinese_vocabulary:
            cursor.execute('INSERT INTO vocabulary (word, romaji, translation, topic, language) VALUES (?, ?, ?, ?, ?)', word)

        conn.commit()  # Commit changes
        print("Initial vocabulary inserted successfully")
        
    except Exception as e:
        print(f"Error inserting initial vocabulary: {e}")

def setup_database():
    conn = connect_db()
    if conn:
        create_tables(conn)
        insert_initial_vocabulary(conn)
        conn.close()

if __name__ == "__main__":
    setup_database()