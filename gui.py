import PySimpleGUI as sg
from database import connect_db
from flashcards import FlashcardManager
from quizzes import QuizManager

def main():
    # Set up database and managers
    db_connection = connect_db()
    flashcard_manager = FlashcardManager(db_connection=db_connection)

    # Language selection layout
    layout_language = [
        [sg.Text("Choose a language:", font=("Helvetica", 20))],
        [sg.Button("Chinese", size=(15, 2)), sg.Button("Japanese", size=(15, 2))],
        [sg.Button("Exit", size=(15, 2))]
    ]
    
    # Main menu layout
    layout_main = [
        [sg.Text("Language Learning App", font=("Helvetica", 20))],
        [sg.Text("Choose a topic to begin studying:"), sg.Listbox(values=[], size=(40, 15), key='-TOPIC LIST-', enable_events=True)],
        [sg.Button("Start Flashcards", disabled=True, size=(15, 2)), sg.Button("Start Quiz", disabled=True, size=(15, 2))],
        [sg.Button("Exit", size=(15, 2))]
    ]
    
    # Flashcard study layout function
    def create_flashcard_layout():
        return [
            [sg.Text("Flashcards", font=("Helvetica", 20))],
            [sg.Text("Term:", size=(15, 1)), sg.Text("", key='-TERM-', size=(40, 1))],
            [sg.Text("Definition:", size=(15, 1)), sg.Text("", key='-DEFINITION-', size=(40, 1))],
            [sg.Text("Romaji:", size=(15, 1)), sg.Text("", key='-ROMAJI-', size=(40, 1))],
            [sg.Button("Next Flashcard", size=(15, 2)), sg.Button("Back to Main", size=(15, 2))]
        ]

    # Quiz layout function
    def create_quiz_layout():
        return [
            [sg.Text("Quiz", font=("Helvetica", 20))],
            [sg.Text("Question:", size=(15, 1)), sg.Text("", key='-QUESTION-', size=(40, 1))],
            [sg.Text("Romaji:", size=(15, 1)), sg.Text("", key='-ROMAJI-', size=(30, 1))],
            [sg.Text("Your Answer:", size=(15, 1)), sg.InputText(key='-ANSWER-', size=(30, 1))],
            [sg.Button("Submit Answer", size=(15, 2), key='-SUBMIT-'), sg.Button("Back to Main", size=(15, 2))],
            [sg.Text("", size=(40, 1), key='-FEEDBACK-', font=("Helvetica", 12))]
        ]

    # Main event loop for the language selection
    window_language = sg.Window("Language Selection", layout_language, size=(400, 300))

    while True:
        event, values = window_language.read()
        
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        elif event in ["Chinese", "Japanese"]:
            language = event
            flashcard_manager.set_language(language)
            window_language.close()
            window_main = sg.Window("Main Menu", layout_main, size=(500, 400), finalize=True)
            window_main['-TOPIC LIST-'].update(values=flashcard_manager.get_topics())
            
            # Main menu event loop
            while True:
                event, values = window_main.read()
                
                if event in (sg.WINDOW_CLOSED, "Exit"):
                    break
                elif event == '-TOPIC LIST-' and values['-TOPIC LIST-']:
                    selected_topic = values['-TOPIC LIST-'][0]
                    flashcard_manager.set_topic(selected_topic)
                    window_main['Start Flashcards'].update(disabled=False)
                    window_main['Start Quiz'].update(disabled=False)
                    
                elif event == "Start Flashcards":
                    window_flashcard = sg.Window("Flashcards", create_flashcard_layout(), size=(500, 400), finalize=True)

                    # Flashcard study loop
                    while True:
                        flashcard = flashcard_manager.get_current_flashcard()
                        if flashcard:  # If there is a flashcard to show
                            window_flashcard['-TERM-'].update(flashcard['term'])
                            window_flashcard['-DEFINITION-'].update(flashcard['definition'])
                            window_flashcard['-ROMAJI-'].update(flashcard.get('romaji', 'N/A'))
                        else:
                            sg.popup("You've completed all flashcards for this topic! You can revisit them anytime.")
                            break
                        
                        flashcard_event, flashcard_values = window_flashcard.read()
                        
                        if flashcard_event == "Back to Main" or flashcard_event == sg.WINDOW_CLOSED:
                            window_flashcard.close()
                            break
                        elif flashcard_event == "Next Flashcard":
                            # Move to the next flashcard
                            if not flashcard_manager.next_flashcard():
                                sg.popup("You've completed all flashcards for this topic! You can revisit them anytime.")
                                break

                    window_flashcard.close()  # Ensure the flashcard window is closed when done
                        
                elif event == "Start Quiz":
                    quiz_manager = QuizManager(flashcard_manager)
                    quiz_manager.create_quiz(selected_topic)

                    # Check if the quiz has questions to ask
                    if len(quiz_manager.questions) == 0:
                        sg.popup("You've completed the quiz for this topic! No questions left.")
                    else:
                        window_quiz = sg.Window("Quiz", create_quiz_layout(), size=(500, 400), finalize=True)

                        # Quiz loop
                        continue_quiz = True  # Control variable for the outer loop
                        while continue_quiz:
                            question_data = quiz_manager.get_next_question()
                            if not question_data:  # No more questions
                                total_questions, score = quiz_manager.get_quiz_results()
                                sg.popup(f"Quiz complete! Your score: {score}/{total_questions}")
                                break  # Exit the loop
                            
                            # Update the quiz window with the current question
                            window_quiz['-QUESTION-'].update(question_data['question'])
                            window_quiz['-ROMAJI-'].update(question_data.get('romaji', 'N/A'))
                            window_quiz['-ANSWER-'].update("")  # Clear answer input
                            window_quiz['-FEEDBACK-'].update("")  # Clear feedback

                            # Loop to get user input for answer
                            while True:
                                quiz_event, quiz_values = window_quiz.read()

                                # Check if the window is closed or "Back to Main" was pressed
                                if quiz_event in (sg.WINDOW_CLOSED, "Back to Main"):
                                    continue_quiz = False  # Set control variable to False to exit the outer loop
                                    window_quiz.close()
                                    break  # Exit the inner loop

                                elif quiz_event == "-SUBMIT-":
                                    answer = quiz_values['-ANSWER-']
                                    if not answer.strip():  # Check if the answer is not empty
                                        window_quiz['-FEEDBACK-'].update("Please type an answer before submitting.")
                                    else:
                                        correct = quiz_manager.check_answer(answer)
                                        if correct:
                                            window_quiz['-FEEDBACK-'].update("Correct!")
                                            break  # Move to the next question
                                        else:
                                            window_quiz['-FEEDBACK-'].update(f"Incorrect. The correct answer was: {question_data['answer']}")

                        window_quiz.close()  # Ensure the quiz window is closed when done

            window_main.close()  # Ensure the main window is closed

    window_language.close()  # Ensure the language window is closed

if __name__ == "__main__":
    main()