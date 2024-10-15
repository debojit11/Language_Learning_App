import sqlite3

class FlashcardManager:
    def __init__(self, db_connection: sqlite3.Connection):
        self.flashcards = {}  # A dictionary to hold flashcards by topic
        self.current_topic = None
        self.topics_studied = set()  # Track studied topics
        self.current_flashcard_index = 0
        self.db_connection = db_connection  # Store the database connection
        self.language = None  # Initialize language to None
        self.learned_words = {}  # Track learned words by topic

    def set_language(self, language):
        """Set the language for flashcards and reload them."""
        self.language = language
        self.load_flashcards()  # Reload flashcards with the selected language

    def load_flashcards(self):
        """Load flashcards from the database for the specified language."""
        cursor = self.db_connection.cursor()
        if self.language:
            cursor.execute('SELECT DISTINCT topic FROM vocabulary WHERE language = ?', (self.language,))
            topics = cursor.fetchall()
            
            self.flashcards.clear()  # Clear the existing flashcards
            for topic_tuple in topics:
                topic = topic_tuple[0]
                cursor.execute('SELECT id, word, translation, romaji FROM vocabulary WHERE topic = ? AND language = ?', 
                               (topic, self.language))
                flashcards = cursor.fetchall()
                self.flashcards[topic] = [{'id': word_id, 'term': word, 'definition': translation, 'romaji': romaji}
                                          for word_id, word, translation, romaji in flashcards]
                if flashcards:
                    self.topics_studied.add(topic)
        else:
            print("Language not set. Please select a language before loading flashcards.")

    def add_flashcard(self, topic, question, answer, romaji):
        """Add a new flashcard to the specified topic."""
        if topic not in self.flashcards:
            self.flashcards[topic] = []
        self.flashcards[topic].append({'term': question, 'definition': answer, 'romaji': romaji})
        self.topics_studied.add(topic)  # Add topic to studied set

    def get_current_flashcard(self):
        """Get the current flashcard based on the selected topic."""
        if self.current_topic and self.flashcards[self.current_topic]:
            return self.flashcards[self.current_topic][self.current_flashcard_index]
        return None

    def next_flashcard(self):
        """Move to the next flashcard."""
        if self.current_topic and self.flashcards[self.current_topic]:
            self.current_flashcard_index += 1

            if self.current_flashcard_index >= len(self.flashcards[self.current_topic]):
                self.current_flashcard_index = 0  # Reset index for potential revisit
                return False  # All flashcards seen
            return True  # More flashcards left
        return False

    def set_topic(self, topic):
        """Set the current topic and reset the flashcard index."""
        self.current_topic = topic
        self.current_flashcard_index = 0  # Reset index for new topic

    def get_topics(self):
        """Retrieve distinct topics based on the selected language."""
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT DISTINCT topic FROM vocabulary WHERE language = ?', (self.language,))
        topics = cursor.fetchall()
        return [topic[0] for topic in topics]  # Return a list of topic names

    def add_learned_word(self, word_id):
        """Add a word to the learned set for the current topic."""
        if self.current_topic not in self.learned_words:
            self.learned_words[self.current_topic] = set()  # Use a set to avoid duplicates
        self.learned_words[self.current_topic].add(word_id)  # Track learned words

    def get_total_words_learned(self):
        """Return the total number of words learned across all topics."""
        return sum(len(words) for words in self.learned_words.values())

    def get_topic_progress(self):
        """Return a list of tuples with topic names and counts of learned words."""
        return [(topic, len(words)) for topic, words in self.learned_words.items()]