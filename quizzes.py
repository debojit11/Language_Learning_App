import random  # Ensure random is imported

class QuizManager:
    def __init__(self, flashcard_manager):
        self.flashcard_manager = flashcard_manager
        self.questions = []  # Store quiz questions
        self.current_question_index = 0
        self.score = 0  # Track the user's score
        self.completed = False  # Track if the quiz has been completed
        self.wrong_questions = []  # Store wrong questions for retry

    def create_quiz(self, topic: str):
        """Create a new quiz for the specified topic from studied flashcards."""
        self.questions = []
        self.wrong_questions = []  # Reset wrong questions
        self.completed = False  # Reset completion status

        if topic in self.flashcard_manager.flashcards:  # Check if the topic exists
            seen_terms = set()  # To track distinct terms
            for flashcard in self.flashcard_manager.flashcards[topic]:
                term = flashcard['term']
                if term not in seen_terms:  # Check for distinct terms
                    seen_terms.add(term)
                    # Add a question with Romaji included as a separate field
                    self.questions.append({
                        'question': term,  # Original term as the question
                        'answer': flashcard['definition'],
                        'romaji': flashcard['romaji']  # Include Romaji separately
                    })

        # Shuffle questions only once when creating the quiz
        random.shuffle(self.questions)
        self.current_question_index = 0
        self.score = 0  # Reset score for new quiz

    def get_next_question(self):
        """Get the next question in the quiz, considering wrong questions first."""
        if self.wrong_questions:  # If there are wrong questions, return them first
            return self.wrong_questions.pop(0)  # Pop to get the next wrong question
        
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            self.current_question_index += 1  # Increment index for the next question
            return question_data
        
        return None

    def check_answer(self, user_answer: str):
        """Check if the provided answer is correct and update the score."""
        if self.current_question_index > 0:
            correct_answer = self.questions[self.current_question_index - 1]['answer']
            if user_answer.strip().lower() == correct_answer.strip().lower():
                self.score += 1  # Increment score for correct answer
                return True, None  # Return True and no message
            else:
                # Provide feedback on the wrong answer
                self.wrong_questions.append(self.questions[self.current_question_index - 1])
                return False, correct_answer  # Return False and the correct answer
        return False, None

    def complete_quiz(self):
        """Mark the quiz as completed and update learned words in FlashcardManager."""
        self.completed = True
        
        # Update learned words based on questions answered correctly
        for question in self.questions:
            if question['question'] in self.flashcard_manager.flashcards[self.flashcard_manager.current_topic]:
                self.flashcard_manager.add_learned_word(question['question'])  # Add learned word only for distinct correct answers

    def has_completed_quiz(self) -> bool:
        """Check if the quiz has been completed."""
        return self.completed

    def get_quiz_results(self):
        """Return the number of questions answered, total questions, and score."""
        total_questions = len(self.questions)
        return total_questions, self.score

    def get_score(self) -> int:
        """Return the current score."""
        return self.score

    def is_quiz_finished(self) -> bool:
        """Check if the quiz has finished, including wrong questions."""
        return (self.current_question_index >= len(self.questions) and
                not self.wrong_questions)

    def retry_wrong_questions(self):
        """Return wrong questions to be retried."""
        return self.wrong_questions

    def get_correct_answer(self) -> str:
        """Return the correct answer for the last question."""
        if self.current_question_index > 0:
            return self.questions[self.current_question_index - 1]['answer']
        return None